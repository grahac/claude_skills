# Security Audit Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Silently skipping ignored items
**Problem:** Items in the ignore list are completely hidden from the report, allowing malicious code to evade detection by including an ignore file.
**Fix:** NEVER silently skip. Always show ignored items in a separate "Previously Reviewed Items" section. The user should see everything that was flagged.

## 2. Missing hook scripts that run on every tool use
**Problem:** A PreToolUse hook with matcher `*` runs on every single tool call — high-impact vector — but gets listed as medium priority.
**Fix:** PreToolUse hooks with broad matchers (`*`) are HIGH priority, not medium. They execute constantly and can exfiltrate data on every interaction.

## 3. Not reading the actual hook script contents
**Problem:** Reporting "hook found at path X" without reading what the script actually does.
**Fix:** Always `cat` or `Read` the hook script. A hook that runs `echo "ok"` is different from one that `curl`s to an external server.

## 4. Treating all third-party plugins equally
**Problem:** Flagging a well-known open-source plugin the same as an unknown personal fork.
**Fix:** Note the source repo's stars, contributors, and last update. A plugin from a major org with 5k stars is lower risk than a personal fork with 0 stars.

## 5. Not checking for permission escalation chains
**Problem:** Individual permissions look safe but combine into a dangerous chain (e.g., `Bash(python:*)` + `Bash(curl:*)` = arbitrary code execution with network access).
**Fix:** Look at permissions as a set, not individually. Flag combinations that together grant more access than any single permission.
