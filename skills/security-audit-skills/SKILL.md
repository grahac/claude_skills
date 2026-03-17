---
name: security-audit-skills
description: Perform security audit of Claude Code skills, plugins, agents, and hooks. Checks for overly permissive configurations, third-party code, and potential vulnerabilities.
---

# Security Audit for Claude Code Configuration

Perform a comprehensive security review of all Claude Code skills, plugins, agents, hooks, and permission configurations.

> **Note:** This is a baseline check, not comprehensive security. It catches common misconfigurations and low-effort threats. Sophisticated attacks may evade pattern-based detection. Always review third-party code before installing.

## File Map

| File | What it contains | When to read |
|------|-----------------|--------------|
| `references/scan-locations.md` | All config paths to check (global + project) | At start of every audit |
| `references/security-criteria.md` | Detailed check criteria by severity (permissions, plugins, hooks, skills, paths) | When evaluating each finding |
| `assets/report-template.md` | The audit report output format | When generating the report |
| `assets/ignore-entry-template.md` | Format for adding items to the ignore list | When user accepts a finding |
| `gotchas.md` | Common failure patterns | When something goes wrong |

## When to Use

- Periodically review your Claude Code setup for security issues
- After installing new plugins or skills
- When adding new permission allowlist entries
- Before sharing your configuration with others

## Audit Process

### Step 1: Load Ignore List

Read `~/.claude/skill-audit-ignore.md` to identify previously reviewed items.

**IMPORTANT:** Ignored items are NOT silently skipped. They are fully scanned and any findings are reported in a separate "Previously Reviewed Items" section.

### Step 2: Scan Configuration Locations

Read `references/scan-locations.md` for the complete list of paths to check.

### Step 3: Check for Security Issues

Read `references/security-criteria.md` and evaluate each item found against the criteria. Classify findings as HIGH, MEDIUM, or LOW severity.

### Step 4: Generate Report

Use `assets/report-template.md` for the output format. Include:
- Summary counts
- New issues by severity
- Previously reviewed items (always shown for transparency)
- Actionable recommendations

### Step 5: Offer Fixes

For common issues, offer to fix them:
- Remove risky permission patterns
- Disable third-party plugins
- Add items to ignore list if reviewed and accepted (use `assets/ignore-entry-template.md` for format)

## Example Usage

**User:** "Run a security audit of my Claude setup"

**You should:**
1. Read `~/.claude/skill-audit-ignore.md`
2. Scan all configuration locations from `references/scan-locations.md`
3. Check ALL items against `references/security-criteria.md` (nothing is silently skipped)
4. Generate the report using `assets/report-template.md`
5. Show previously-reviewed items in a separate section
6. Offer to fix critical issues or add newly reviewed items to ignore list
