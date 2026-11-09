#!/usr/bin/env python3
"""Check pwn.watch and Cloudflare Radar Zero Wire against your watchlist. Never patches anything.

  check.py              new or updated matches since the last --commit (markdown)
  check.py --all-live   also list every live pwn.watch match, ignoring seen state
  check.py --commit     record what was reported in seen.json
  check.py inventory    print installed versions on this machine + what each deployed project ships
                        (runs `git fetch` in each deployed_projects repo; nothing else is written)

Config and state live in $SECURITY_FEED_CHECK_HOME (default ~/.config/security-feed-check):
watchlist.json (copy assets/watchlist.example.json) and seen.json.
"""
import glob, json, os, platform, re, shutil, subprocess, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import date

HOME = os.path.expanduser(os.environ.get("SECURITY_FEED_CHECK_HOME", "~/.config/security-feed-check"))
WATCHLIST = os.path.join(HOME, "watchlist.json")
SEEN = os.path.join(HOME, "seen.json")
INCIDENTS_URL = "https://pwn.watch/incidents.json"
ZERO_WIRE_RSS = "https://radar.cloudflare.com/security/zero-wire/rss"
# pwn.watch rejects the default Python User-Agent with a 403.
USER_AGENT = "security-feed-check/1 (+https://github.com/grahac/claude_skills)"


def fetch_raw(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def load_watchlist():
    if not os.path.exists(WATCHLIST):
        sys.exit(f"No watchlist at {WATCHLIST}. Copy assets/watchlist.example.json there and edit it.")
    return json.load(open(WATCHLIST))


def matches(inc, watch):
    tags = {t.lower() for t in inc.get("tags", [])}
    if tags & watch["tags"]:
        return True
    hay = (inc.get("product", "") + " " + inc.get("title", "")).lower()
    return any(re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", hay) for k in watch["keywords"])


def fmt(inc):
    cves = ", ".join(inc.get("cveIds") or []) or "no CVE"
    fixed = ", ".join(inc.get("fixedVersions") or []) or "none yet"
    affected = ", ".join(inc.get("affectedVersions") or []) or "unspecified"
    return (
        f"- **[{inc['severity']}/{inc['patchStatus']}/{inc['status']}]** {inc['title']}\n"
        f"  {inc['url']}\n"
        f"  product: {inc.get('product','?')}\n"
        f"  affected: {affected}\n"
        f"  fixed in: {fixed}\n"
        f"  CVEs: {cves} · updated {inc['updatedAt'][:10]} · brief: {inc['json']}"
    )


def zero_wire():
    """('Needs attention' items, total items parsed). A short curated feed, so no watchlist filtering."""
    all_items = list(ET.fromstring(fetch_raw(ZERO_WIRE_RSS)).iter("item"))
    items = []
    for it in all_items:
        cats = [c.text for c in it.findall("category")]
        if "Needs attention" not in cats:
            continue
        guid = it.findtext("guid")  # slug@last-update-date, so it changes when the item is updated
        items.append({"slug": "zerowire:" + guid.split("@")[0], "guid": guid, "title": it.findtext("title"),
                      "link": it.findtext("link"), "tags": [c for c in cats if c != "Needs attention"],
                      "action": it.findtext("description")})
    return items, len(all_items)


def check(all_live, commit):
    wl = load_watchlist()
    watch = {"tags": {t.lower() for t in wl["tags"]}, "keywords": [k.lower() for k in wl["keywords"]]}
    seen = json.load(open(SEEN)) if os.path.exists(SEEN) else {}
    data = json.loads(fetch_raw(INCIDENTS_URL))
    incidents = [i for i in data["incidents"] if not i.get("isExample")]
    if not incidents:
        sys.exit("COVERAGE LOST: pwn.watch returned 0 incidents. Do not treat this run as clean.")
    matched = [i for i in incidents if matches(i, watch)]
    live = [i for i in matched if i["status"] == "live"]
    new = [i for i in matched if seen.get(i["slug"]) != i["updatedAt"]]

    print(f"# Security feed check {date.today().isoformat()}")
    print(f"pwn.watch feed updated {data['updatedAt'][:16]}Z · {len(incidents)} incidents · "
          f"{len(matched)} match watchlist · {len(live)} live · {len(new)} new/updated since last run\n")
    print("## pwn.watch: new or updated matches" + (" (first run: everything counts as new)" if not seen else ""))
    print("\n".join(fmt(i) for i in new) if new else "- none")
    if all_live:
        print("\n## pwn.watch: all live matches")
        print("\n".join(fmt(i) for i in live) if live else "- none")

    zw, total = zero_wire()
    if not total:
        sys.exit("COVERAGE LOST: Zero Wire feed parsed 0 items. Do not treat this run as clean.")
    print(f"\n## Cloudflare Zero Wire: needs attention ({len(zw)} of {total} items; "
          "not watchlist-filtered, check each for applicability)")
    for z in zw:
        print(f"- {'🆕 ' if seen.get(z['slug']) != z['guid'] else ''}**{z['title']}** ({z['guid']})\n"
              f"  {z['link']}\n  tags: {', '.join(z['tags'])}\n  action: {z['action']}")
    if not zw:
        print("- none")

    if commit:
        state = {i["slug"]: i["updatedAt"] for i in matched} | {z["slug"]: z["guid"] for z in zw}
        with open(SEEN + ".tmp", "w") as f:  # write-then-rename so an interrupted run cannot corrupt seen.json
            json.dump(state, f, indent=1)
        os.replace(SEEN + ".tmp", SEEN)
        print(f"\n_seen.json updated ({len(state)} slugs)_")


def sh(cmd):
    """Fixed shell pipelines only; never interpolate config values here (use run())."""
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as e:  # inventory is best-effort; a failed probe is printed, not fatal
        return f"error: {e}"


def run(argv):
    """Run a probe without a shell. Returns stdout, or a line starting with UNKNOWN on any failure."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=120,
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except FileNotFoundError:
        return f"UNKNOWN (not on PATH: {argv[0]})"
    except subprocess.TimeoutExpired:
        return f"UNKNOWN (timed out: {' '.join(argv)})"
    if r.returncode != 0:
        return f"UNKNOWN (exit {r.returncode}: {r.stderr.strip()[:200]})"
    return r.stdout.strip()


def lock_versions(text):
    """Compact 'name version;' list from a mix.lock or package-lock.json body (top-level npm packages only)."""
    if text.lstrip().startswith("{"):
        pkgs = json.loads(text).get("packages", {})
        return ";".join(f"{k[13:]} {v.get('version','?')}" for k, v in sorted(pkgs.items())
                        if k.startswith("node_modules/") and "/node_modules/" not in k[13:])
    return ";".join(f"{n} {v}" for n, v in re.findall(r'^  "([a-z_0-9]+)": \{:hex, :[a-z_0-9]+, "([0-9][^"]*)"', text, re.M))


def inventory():
    wl = load_watchlist()
    print("## This machine")
    print("os:", platform.platform())
    print("runtimes: node", sh("node -v 2>/dev/null"), "| python3", sh("python3 --version 2>/dev/null"),
          "| ruby", sh("ruby -v 2>/dev/null"), "| elixir", sh("elixir --short-version 2>/dev/null"),
          "| erlang/otp", sh("erl -noshell -eval 'io:format(\"~s\", [erlang:system_info(otp_release)]), halt().' 2>/dev/null"),
          "| docker", sh("docker --version 2>/dev/null"), "| git", sh("git --version 2>/dev/null"))
    if sys.platform == "darwin":
        print("apps:", sh("for a in /Applications/*.app \"$HOME\"/Applications/*.app; do [ -e \"$a\" ] || continue; "
                          "v=$(defaults read \"$a/Contents/Info.plist\" CFBundleShortVersionString 2>/dev/null); "
                          "echo \"$a $v\"; done | tr '\\n' ';'"))
    print("brew:", ";".join(run(["brew", "list", "--versions"]).splitlines()))
    print("npm -g:", sh("npm ls -g --depth=0 2>/dev/null | tail -n +2 | tr '\\n' ';'"))

    for pattern in wl.get("local_lockfile_globs", []):
        for path in sorted(glob.glob(os.path.expanduser(pattern))):
            print(f"\n### {path}\n{lock_versions(open(path).read())}")

    projects = wl.get("deployed_projects", {})
    if projects:
        print("\n## Deployed projects (read from each repo's origin default branch, assumed to be what is deployed)")
    for name, repo in projects.items():
        repo = os.path.expanduser(repo)
        fetch = run(["git", "-C", repo, "fetch", "-q", "origin"])
        ref = run(["git", "-C", repo, "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD"])
        print(f"\n### {name} ({repo} @ {ref})")
        if fetch:
            print("fetch:", fetch)
        if ref.startswith("UNKNOWN"):
            continue
        dockerfile = run(["git", "-C", repo, "show", f"{ref}:Dockerfile"])
        print("image:", "no Dockerfile" if dockerfile.startswith("UNKNOWN") else
              ";".join(l for l in dockerfile.splitlines() if re.match(r"(ARG [A-Z_]*VERSION|FROM)", l)))
        for lock in ("mix.lock", "package-lock.json", "assets/package-lock.json"):
            body = run(["git", "-C", repo, "show", f"{ref}:{lock}"])
            if not body.startswith("UNKNOWN"):
                print(f"{lock}:", lock_versions(body))

    for app in wl.get("fly_postgres_apps", []):
        out = run(["fly", "machines", "list", "-a", app, "--json"])
        images = out if out.startswith("UNKNOWN") else sorted({m["config"]["image"].split("@")[0] for m in json.loads(out)})
        print(f"\nfly postgres {app}:", images)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "inventory" in args:
        inventory()
    else:
        check("--all-live" in args, "--commit" in args)
