#!/usr/bin/env python3
"""Aggregate user prompts and tool usage from recent Claude Code transcripts.

Outputs a markdown report with:
- Sessions, project counts, date range
- Global tool usage histogram
- Bash command 2-grams (recipe candidates)
- Per-project: sessions, top tools, top existing-skill matches, deduplicated user prompts

Usage: analyze_transcripts.py [--days N] [--min-prompts N] [--out PATH] [--no-skill-match]
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SKILLS_USER_DIR = Path.home() / ".claude" / "skills"
SKILLS_PLUGIN_CACHE = Path.home() / ".claude" / "plugins" / "cache"

# --- Noise filters: tags and auto-injected content that aren't real user intents ---
NOISE_TAG_RES = [
    re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL),
    re.compile(r"<system[_-]instruction>.*?</system[_-]instruction>", re.DOTALL),
    re.compile(r"<command-(name|message|args)>.*?</command-\1>", re.DOTALL),
    re.compile(r"<local-command-stdout>.*?</local-command-stdout>", re.DOTALL),
    re.compile(r"<local-command-caveat>.*?</local-command-caveat>", re.DOTALL),
    re.compile(r"<task-notification>.*?</task-notification>", re.DOTALL),
    re.compile(r"<bash-input>.*?</bash-input>", re.DOTALL),
    re.compile(r"<bash-stdout>.*?</bash-stdout>", re.DOTALL),
    re.compile(r"<bash-stderr>.*?</bash-stderr>", re.DOTALL),
    re.compile(r"\[Image:[^\]]*\]"),
]
SKILL_DUMP_PREFIX = re.compile(r"^Base directory for this skill: ", re.MULTILINE)
SESSION_RESUME_PREFIX = "This session is being continued from a previous conversation"
CONDUCTOR_RE = re.compile(r"^(/Users/[^/]+/conductor/workspaces/[^/]+)(/.+)?$")

# Common English stopwords + Claude-specific filler for skill matching.
STOPWORDS = set("""
a an the and or but if then so to of in on at for with without about into onto from by as is are was were be been
being do does did doing have has had having i you he she it we they me him her us them my your his their our its
this that these those there here what which who whom whose when where why how can could should would will shall
may might must use used using when after before during while please thanks ok yes no not none any some all most
many few one two three first second next last new old via like via etc
skill skills plugin plugins claude code use
also anything between create edit even false back asks audit body branch brainstorm browser codex deployment
design dialogs done changes content contents callers caller change check command commands commits common create
created creates creating data default detailed details document documents doing edit edits even ever every example
file files fix fixes form forms full general guide guides help include including info information install installed
issue issues item items launch let level like list lists local make makes making manage manages managing model
models name names need needs note notes only open option options output outputs page pages part parts pass pull
push read ready report reports request requests result results review reviews run running runs see send sent
session sessions set sets setting settings setup share show shows side simple single small specific start started
status stop store stored support supported supports system tab tag tags task tasks team test testing tests text
thing things time times tool tools type types update updated updates upload uploaded uploads view views way ways
work workflow working works auto automated automatic automatically begin between build building built call called
calls case cases cases central change changes click code coding command commands commit committed commits common
config configuration configure configured contain containing contains content context contexts continue continued
copy copying create created creates creating cross current data day days delete deleted deletes deleting describe
description direct directly display displayed displays does done easily easy effective effectively element elements
end ends ended ensure ensures ensured ensuring entire entries entry environment environments error errors event
events example examples execute executed executes executing existing experience extend extended extending feature
features field fields filter filtering find finding finds flag flags follow followed following follows form forms
format formats found friction generic global goal goals good great group groups handle handles handling history
hold holding holds idea ideas identify identifies identifying ignore ignored implement implementation implementing
include included includes including individual install installed installing installation interface interfaces
invocation invocations invoke invoked invokes invoking item items job jobs json keep kept key keys label labels
language large layer layers level levels limit limits link links live load loaded loading loads location locations
log logs long made main maintain maintenance major manage managed management many map mapped mapping maps mark
matches matched matter mean means meant memory message messages method methods minor mode modes module modules
move moved moves moving multi multiple namespace native need needed needs network never normal notes nothing
notify notification notifications object objects offer offered offering offers operate operated operates operating
operation operations option options order ordered ordering organize organized origin original other others output
outputs page pages parameter parameters part parts particular particularly path paths pattern patterns perform
performance period place places plain platform play please point points position post posts power preferences
prefer preferred preferring previous primary print priority private process processes processing produce produced
producing product profile profiles project projects prompt prompts properly property propose proposed proposing
provide provided provides public quickly raise raised raising range ranges rate raw recent recently record records
reduce reduces reducing reference references reflect reflected refresh refreshed regular relate related relevant
remain remained remaining remove removed removes removing render rendered rendering replace replaced replaces
replacing represent represents request requests require required requires requiring research resolve resolved
resolves resource resources respond responded respond response responses result results return returned returning
returns rule rules runs sample samples scan scanned scanning schedule scheduled scheduling scope scoped score
scores screen screens search searched searching select selected selects send sending sense separate separated
sequence sequences serve served service services session sessions short side similar similarly simple simply since
size sized small smart solution solutions solve solved solves solving someone source sources space spaces specific
specifically split standard standards start started starting starts state states stay stays step steps storage
store stored stores storing string strings structure structured structures sub submit submitted submitting subset
suit suits summary surface surfaces surfacing sync system systems table tables target targeted targets technical
template templates terminal then think thinking time times tone took tool tools touch touched touching track
tracked tracking transform transformed transforms transition turn turned turns under understand understanding
understands unique units update updated updates user users using utility valid validate validated validates
validating value values various verify verified verifies version versions visible vs walk walking want wanted
wants ways weak well wide wider window word words workflow workflows wrap wrapped wraps write written wrote
""".split())


def decode_project_path(dirname: str) -> str:
    if dirname.startswith("-"):
        return "/" + dirname[1:].replace("-", "/")
    return dirname


def collapse_project_path(path: str) -> str:
    """Roll up Conductor workspace dirs to their project root."""
    m = CONDUCTOR_RE.match(path)
    if m:
        return m.group(1)
    return path


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_result":
                    return ""
        return "\n".join(parts)
    return ""


def clean_prompt(text: str) -> str:
    for r in NOISE_TAG_RES:
        text = r.sub("", text)
    text = text.strip()
    if not text:
        return ""
    if text.startswith(SESSION_RESUME_PREFIX):
        return ""
    if SKILL_DUMP_PREFIX.match(text):
        return ""
    return text


def normalize_prompt(text: str) -> str:
    """Collapse whitespace and lowercase for dedup grouping."""
    return re.sub(r"\s+", " ", text.strip().lower())


def is_real_user_prompt(entry: dict) -> bool:
    if entry.get("type") != "user":
        return False
    msg = entry.get("message", {})
    return msg.get("role") == "user"


def parse_ts(entry: dict):
    ts = entry.get("timestamp")
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def extract_bash_command(tool_use: dict) -> str | None:
    """Pull `binary subcommand` (or just binary) from a Bash tool_use entry.

    Two-token granularity makes 2-grams meaningful as recipes:
    `fly machine` → `fly deploy` is signal; `fly` → `fly` is not.
    """
    if (tool_use.get("name") or tool_use.get("tool_name")) != "Bash":
        return None
    inp = tool_use.get("input") or {}
    cmd = inp.get("command") if isinstance(inp, dict) else None
    if not cmd or not isinstance(cmd, str):
        return None
    cmd = cmd.strip().lstrip("(").lstrip()
    tokens = []
    for tok in cmd.split():
        if "=" in tok and not tok.startswith("-"):
            continue
        if tok in {"sudo", "exec", "time"}:
            continue
        tokens.append(tok.split("/")[-1].rstrip(";").rstrip("|"))
        if len(tokens) == 2:
            break
    if not tokens:
        return None
    binary = tokens[0]
    # For multi-subcommand CLIs, keep `binary subcommand`. For one-shot tools, just binary.
    multi_sub = {"git", "gh", "fly", "mix", "npm", "npx", "yarn", "pnpm", "docker",
                 "kubectl", "brew", "pip", "pip3", "python", "python3", "cargo",
                 "go", "psql", "rails", "bundle", "rake", "make", "tsc", "node"}
    if binary in multi_sub and len(tokens) > 1 and not tokens[1].startswith("-"):
        return f"{binary} {tokens[1]}"
    return binary


def process_file(path: Path):
    """Yield ('prompt', text) | ('tool', name) | ('bash', cmd) | ('ts', datetime)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                ts = parse_ts(entry)
                if ts:
                    yield ("ts", ts)

                if is_real_user_prompt(entry):
                    raw = extract_text(entry["message"].get("content", ""))
                    cleaned = clean_prompt(raw)
                    if cleaned:
                        yield ("prompt", cleaned)
                elif entry.get("type") == "tool_use":
                    name = entry.get("name") or entry.get("tool_name")
                    if name:
                        yield ("tool", name)
                    bash = extract_bash_command(entry)
                    if bash:
                        yield ("bash", bash)
                elif entry.get("type") == "assistant":
                    msg = entry.get("message", {})
                    content = msg.get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                name = block.get("name")
                                if name:
                                    yield ("tool", name)
                                bash = extract_bash_command(block)
                                if bash:
                                    yield ("bash", bash)
    except OSError:
        return


# --- Skill index (existing-skill cross-check) ---

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def load_skill_index() -> list[dict]:
    """Return list of {name, description, tokens} for every installed skill, deduped by name.

    Tokens are filtered to drop terms that appear in >25% of skills — generic words
    like 'review', 'page', 'file', 'test', 'code' are noise for matching.
    """
    seen = {}
    for skill_md in list(SKILLS_USER_DIR.glob("*/SKILL.md")) + list(
        SKILLS_PLUGIN_CACHE.glob("**/SKILL.md")
    ):
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = FRONTMATTER_RE.search(text)
        if not m:
            continue
        body = m.group(1)
        name = None
        desc_lines = []
        in_desc = False
        for line in body.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("'\"")
                in_desc = False
            elif line.startswith("description:"):
                desc_lines.append(line.split(":", 1)[1].strip())
                in_desc = True
            elif in_desc and (line.startswith("  ") or line.startswith("\t")):
                desc_lines.append(line.strip())
            elif in_desc and ":" in line:
                in_desc = False
        if not name or name in seen:
            continue
        desc = " ".join(desc_lines).strip().strip("'\"")
        seen[name] = {
            "name": name,
            "description": desc,
            "tokens": tokenize(desc),
        }
    skills = list(seen.values())

    # Drop tokens that appear in too many skills — they don't discriminate.
    if skills:
        df = Counter()
        for s in skills:
            df.update(s["tokens"])
        max_df = max(1, int(len(skills) * 0.08))
        common = {tok for tok, count in df.items() if count > max_df}
        for s in skills:
            s["tokens"] = s["tokens"] - common
    return skills


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower())
    return {w for w in words if w not in STOPWORDS}


def match_project_to_skills(project_text: str, skill_index: list[dict], top_n: int = 3,
                            min_overlap: int = 4
                            ) -> list[tuple[str, list[str]]]:
    """Return top skills whose distinctive terms overlap with the project's prompts.

    Returns list of (skill_name, [overlapping_terms]) so the reader can see *why*.
    """
    if not project_text or not skill_index:
        return []
    project_tokens = tokenize(project_text)
    if not project_tokens:
        return []
    scores = []
    for skill in skill_index:
        if not skill["tokens"]:
            continue
        overlap = skill["tokens"] & project_tokens
        if len(overlap) >= min_overlap:
            scores.append((skill["name"], sorted(overlap)[:5], len(overlap)))
    scores.sort(key=lambda t: t[2], reverse=True)
    return [(name, terms) for name, terms, _ in scores[:top_n]]


# --- Main ---

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--min-prompts", type=int, default=1)
    p.add_argument("--out", default="-")
    p.add_argument("--max-prompt-chars", type=int, default=400)
    p.add_argument("--no-skill-match", action="store_true",
                   help="Skip cross-check against installed skills")
    p.add_argument("--bash-ngram-min", type=int, default=4,
                   help="Minimum count for a Bash 2-gram to surface")
    args = p.parse_args()

    if not PROJECTS_DIR.exists():
        print(f"No projects dir at {PROJECTS_DIR}", file=sys.stderr)
        sys.exit(1)

    cutoff = time.time() - args.days * 86400

    by_project_prompts = defaultdict(list)        # raw cleaned prompts (with dups)
    by_project_tools = defaultdict(Counter)
    by_project_sessions = defaultdict(set)
    by_project_workspaces = defaultdict(set)      # for Conductor rollup
    by_project_dates = defaultdict(list)
    bash_2grams = Counter()
    total_files = 0

    for proj_dir in PROJECTS_DIR.iterdir():
        if not proj_dir.is_dir():
            continue
        raw_proj = decode_project_path(proj_dir.name)
        proj_name = collapse_project_path(raw_proj)
        for jsonl in proj_dir.glob("*.jsonl"):
            try:
                if jsonl.stat().st_mtime < cutoff:
                    continue
            except OSError:
                continue
            total_files += 1
            by_project_sessions[proj_name].add(jsonl.stem)
            if proj_name != raw_proj:
                by_project_workspaces[proj_name].add(raw_proj)

            session_bash = []
            for kind, value in process_file(jsonl):
                if kind == "prompt":
                    by_project_prompts[proj_name].append(value)
                elif kind == "tool":
                    by_project_tools[proj_name][value] += 1
                elif kind == "bash":
                    session_bash.append(value)
                elif kind == "ts":
                    by_project_dates[proj_name].append(value)
            for a, b in zip(session_bash, session_bash[1:]):
                if a != b:  # skip self-repeats (retries of the same command)
                    bash_2grams[(a, b)] += 1

    skill_index = [] if args.no_skill_match else load_skill_index()

    # --- Render report ---
    lines = []
    lines.append(f"# Claude Transcript Analysis — last {args.days} days\n")
    lines.append(f"- Sessions scanned: {total_files}")
    lines.append(f"- Projects with activity: {len(by_project_sessions)}")
    if not args.no_skill_match:
        lines.append(f"- Installed skills indexed: {len(skill_index)}")
    lines.append("")

    global_tools = Counter()
    for tools in by_project_tools.values():
        global_tools.update(tools)
    if global_tools:
        lines.append("## Tool usage (all projects)\n")
        for name, count in global_tools.most_common(20):
            lines.append(f"- {name}: {count}")
        lines.append("")

    # Bash 2-grams — sequences are recipe candidates.
    common_seqs = [kv for kv in bash_2grams.most_common(30) if kv[1] >= args.bash_ngram_min]
    if common_seqs:
        lines.append(f"## Bash command sequences (2-grams, count ≥ {args.bash_ngram_min})\n")
        lines.append("_Recurring `A → B` pairs across sessions hint at workflow recipes worth automating._\n")
        for (a, b), count in common_seqs:
            lines.append(f"- `{a}` → `{b}` ({count})")
        lines.append("")

    sorted_projects = sorted(
        by_project_prompts.items(),
        key=lambda kv: len(kv[1]),
        reverse=True,
    )

    for proj, prompts in sorted_projects:
        if len(prompts) < args.min_prompts:
            continue

        # Dedup prompts by normalized form, preserve first-seen casing.
        groups: dict[str, list[str]] = {}
        order: list[str] = []
        for raw in prompts:
            key = normalize_prompt(raw)
            if key not in groups:
                groups[key] = [raw]
                order.append(key)
            else:
                groups[key].append(raw)

        unique_count = len(order)
        sessions = by_project_sessions[proj]
        workspaces = by_project_workspaces.get(proj, set())
        dates = by_project_dates.get(proj, [])
        date_range = ""
        if dates:
            d0, d1 = min(dates), max(dates)
            if d0.date() == d1.date():
                date_range = f", {d0.date()}"
            else:
                date_range = f", {d0.date()}…{d1.date()}"

        header_extra = ""
        if workspaces:
            header_extra = f", {len(workspaces)} workspaces"

        lines.append(f"## {proj}")
        lines.append(
            f"_{len(sessions)} sessions{header_extra}{date_range}, "
            f"{len(prompts)} prompts ({unique_count} unique)_\n"
        )

        tools = by_project_tools.get(proj, Counter())
        if tools:
            top = ", ".join(f"{n}({c})" for n, c in tools.most_common(8))
            lines.append(f"**Top tools:** {top}\n")

        if skill_index:
            project_text = " ".join(prompts[:200])  # cap to avoid blowup
            matches = match_project_to_skills(project_text, skill_index)
            if matches:
                pretty = "; ".join(f"{n} [{', '.join(t)}]" for n, t in matches)
                lines.append(f"**Possibly covered by existing skills:** {pretty}\n")

        lines.append("**Prompts (deduplicated, ×N = repeat count):**\n")
        # Sort dedup groups by repeat count desc, then by first-seen order.
        order_idx = {k: i for i, k in enumerate(order)}
        for key in sorted(order, key=lambda k: (-len(groups[k]), order_idx[k])):
            count = len(groups[key])
            sample = groups[key][0].replace("\n", " ").strip()
            if len(sample) > args.max_prompt_chars:
                sample = sample[: args.max_prompt_chars] + "…"
            prefix = f"(×{count}) " if count > 1 else ""
            lines.append(f"- {prefix}{sample}")
        lines.append("")

    output = "\n".join(lines)
    if args.out == "-":
        sys.stdout.write(output)
    else:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {args.out} ({len(output)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
