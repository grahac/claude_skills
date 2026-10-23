#!/usr/bin/env python3
"""Offline TableThis release lint; stdlib only, no auth or product calls.

This intentionally parses only this package's small YAML subset (scalar fields
and JSON flow metadata). It is not a general YAML or policy/security proof.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = (
    "SKILL.md", "README.md", "LICENSE", "SOURCE-ATTRIBUTION.md",
    "references/connection.md", "references/workflows.md",
    "scripts/validate.py", "tests/test_validate.py",
)
EXPECTED_IGNORES = {
    "evidence/", "listing/", "VALIDATION.md", "__pycache__/",
    "**/__pycache__/", "*.pyc",
}
SCOPES = {
    "tables:read", "documents:read", "records:write_proposals", "schema:write",
    "changes:apply", "changes:review", "app:write", "documents:write",
    "workspace:manage",
}


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        raise ValueError("unclosed frontmatter")
    fields = {}
    for line in head.splitlines():
        match = re.fullmatch(r"([a-z][a-zA-Z]*): (.+)", line)
        if not match:
            raise ValueError("unsupported frontmatter line: " + line)
        key, value = match.groups()
        if key in fields:
            raise ValueError("duplicate frontmatter key: " + key)
        if key not in {"name", "description", "version", "metadata"}:
            raise ValueError("unexpected frontmatter key: " + key)
        fields[key] = json.loads(value) if key == "metadata" else value
    return fields, body


def validate(root):
    root = Path(root).resolve()
    errors, checks, texts = [], [], {}

    def check(ok, name):
        (checks if ok else errors).append(name)

    for rel in PAYLOAD:
        p = root / rel
        safe = not any(x.is_symlink() for x in [p, *p.parents] if x != root.parent)
        check(safe and p.is_file(), "regular non-symlink file: " + rel)
        if not safe or not p.is_file():
            continue
        raw = p.read_bytes()
        check(len(raw) <= 65536, "file <=64KiB: " + rel)
        try:
            texts[rel] = raw.decode("utf-8")
        except UnicodeError:
            errors.append("non-UTF-8 file: " + rel)
    check(sum(len(t.encode()) for t in texts.values()) <= 262144,
          "payload <=256KiB")
    ignore = root / ".clawhubignore"
    if ignore.is_file() and not ignore.is_symlink():
        rules = {x.strip() for x in ignore.read_text().splitlines() if x.strip()}
        check(rules == EXPECTED_IGNORES, "exact release evidence/cache ignore rules")
    elif ignore.exists() or ignore.is_symlink():
        errors.append(".clawhubignore must be a regular non-symlink file")
    elif (root / "listing").exists() or (root / "VALIDATION.md").exists():
        errors.append("release source needs .clawhubignore to exclude local evidence")
    else:
        checks.append("clean install bundle: source .clawhubignore is not distributed")
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if rel.parts[0] in {"evidence", "listing", ".clawhub", ".clawdhub"} or "__pycache__" in rel.parts:
            continue
        if p.is_symlink():
            errors.append("symlink in package: " + str(rel))
        elif p.is_file() and str(rel) not in {*PAYLOAD, ".clawhubignore", "VALIDATION.md"}:
            errors.append("unexpected distributable file: " + str(rel))
    skill = texts.get("SKILL.md", "")
    try:
        fields, body = frontmatter(skill)
        check(set(fields) == {"name", "description", "version", "metadata"},
              "complete supported frontmatter")
        check(fields.get("name") == "tablethis" and root.name == "tablethis",
              "portable name matches tablethis directory")
        check(bool(re.fullmatch(r"\d+\.\d+\.\d+", fields.get("version", ""))),
              "semver release version")
        check(40 <= len(fields.get("description", "")) <= 1024,
              "bounded useful description")
        meta = fields.get("metadata", {})
        check(isinstance(meta, dict) and set(meta) == {"openclaw"},
              "supported runtime namespace")
        oc = meta.get("openclaw", {}) if isinstance(meta, dict) else {}
        check(isinstance(oc, dict) and set(oc) == {"homepage", "emoji"}
              and oc.get("homepage") == "https://www.tablethis.ai/",
              "truthful homepage-only runtime needs; no credential requirement")
    except (ValueError, TypeError, AttributeError) as exc:
        errors.append("frontmatter: " + str(exc))
        body = skill
    config_fences = re.findall(r"```json\n(.*?)\n```", body, re.S)
    try:
        definition = json.loads(config_fences[0])
        check(definition == {
            "url": "https://app.tablethis.ai/mcp", "transport": "streamable-http",
            "auth": "oauth", "oauth": {"scope": "tables:read documents:read"}},
            "read-only native OAuth config example")
    except (IndexError, ValueError):
        errors.append("missing/invalid read-only config fence")
    for marker, label in [
        ("explicit workspace", "workspace trigger"),
        ("ask which workspace before", "no implicit workspace selection"),
        ("tool_search", "real runtime discovery"),
        ("tool_describe", "describe before MCP call"),
        ("dispatch_action", "supported generic dispatch path"),
        ("EXACT_ID_FROM_SEARCH", "no guessed TableThis tool IDs"),
        ("Gateway to be stopped", "offline CLI state ownership"),
        ("Submitting a proposal is", "submission identified as external write"),
        ("explicit owner approval", "owner approval gate"),
        ("expected-old-value", "expected-value concurrency"),
        ("Never replace the expected value", "no force-overwrite retry"),
        ("Scheduled/always-on clients cannot obtain", "async permission ceiling"),
        ("role floors", "role ceiling"),
        ("not all writes require human", "accurate immediate-write boundary"),
        ("Do not request `workspace:manage`", "no default member management"),
        ("Read back the exact proposal", "external write verification"),
        ("untrusted task data", "prompt-injection data boundary"),
        ("Product changes: none", "read-only report contract"),
    ]:
        check(marker in skill, "safety/content: " + label)
    joined = "\n".join(texts.get(x, "") for x in
                       ("SKILL.md", "README.md", "references/connection.md"))
    for scope in sorted(SCOPES):
        check(scope in joined, "documented scope: " + scope)
    # Lint the authoritative budget block, not incidental numbers in examples.
    budget = skill.partition("### Investigation budgets (ordinary and scheduled work)\n")[2]
    budget = budget.partition("### Investigation steps\n")[0]
    flat_budget = " ".join(budget.split())
    for marker, label in [
        ("| Returned records | 100 total record instances |", "aggregate records"),
        ("| Record-result pages | 4 total pages, at most 25 records per page |", "aggregate record pages"),
        ("| Documents | 5 distinct documents, including search/list hits |", "aggregate documents"),
        ("| Document-result pages/calls | 10 total list/search/read responses |", "aggregate document pages"),
        ("| Passages | 20 total returned excerpts or Markdown sections; a full document counts at least once |", "aggregate passages"),
        ("| Document text | 32 KiB (32768 UTF-8 bytes) aggregate, including snippets, previews, and full text |", "aggregate document text"),
        ("task-level investigation defaults, not product API limits", "defaults not API limits"),
        ("across all tables, queries, document searches, retries, and verification reads", "task-wide accounting"),
        ("Count re-read records/text again and empty pages too", "repeat and empty response accounting"),
        ("explicit owner-approved scoped budgets", "scoped owner budgets"),
        ("Any unspecified dimension retains its default", "unmodified ceilings retained"),
        ("Set supported tool limits no larger than the remaining budgets", "remaining tool limits"),
        ("Request adequate tool limits from the operator, or stop if a bounded read cannot be established", "bounded-read prerequisite"),
        ("Reading an unbounded response and truncating it afterward is not a bounded read", "no post-read truncation bypass"),
        ("do not enforce a runtime sandbox or server cap", "no runtime enforcement claim"),
        ("Before any call that could exceed any row, page, document, passage, or text budget, stop, report partial coverage and budget usage, and request fresh owner approval", "stop report and fresh approval"),
        ("If a response unexpectedly exceeds a requested limit, stop further reads and report the overrun", "unexpected overrun stop"),
    ]:
        check(marker in flat_budget, "investigation budget: " + label)
    workflows = " ".join(texts.get("references/workflows.md", "").split())
    for marker, label in [
        ("[investigation budgets](../SKILL.md#investigation-budgets-ordinary-and-scheduled-work)", "canonical budget reference"),
        ("For ordinary investigations and each scheduled run", "ordinary and scheduled coverage"),
        ("Before exceeding any budget, stop, report partial coverage and usage, and request fresh owner approval", "reference approval gate"),
        ("The shared investigation boundary applies to each run", "scheduled budget inheritance"),
        ("used/remaining records, record pages, documents, document pages/calls, passages, and aggregate UTF-8 text bytes", "review receipt dimensions"),
    ]:
        check(marker in workflows, "investigation budget: " + label)
    check("MIT No Attribution" in texts.get("LICENSE", ""), "MIT-0 license")
    for rel, text in texts.items():
        if rel.endswith(".md"):
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                target_path = ((root / rel).parent / target.split("#", 1)[0]).resolve()
                check(target_path.is_relative_to(root) and target_path.is_file(),
                      "valid relative link: " + rel + " -> " + target)
        # Triage only; manually review wording/semantics too.
        patterns = {
            "private key material": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
            "token-shaped literal": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,})",
            "download-and-execute": r"(?:curl|wget)[^\n|]{0,250}\|\s*(?:bash|sh)\b",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                errors.append("static scan: " + label + " in " + rel)
    return {
        "ok": not errors, "root": str(root), "payload_files": list(PAYLOAD),
        "payload_bytes": sum(len(t.encode()) for t in texts.values()),
        "checks_passed": len(checks), "checks": checks, "errors": errors,
        "limitations": ["Static content lint is not a security certification",
                        "No network, OAuth, live tool schemas, or product effects tested"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
