---
name: security-audit-skills
description: Perform security audit of Claude Code skills, plugins, agents, and hooks. Checks for overly permissive configurations, third-party code, and potential vulnerabilities.
---

# Security Audit for Claude Code Configuration

Perform a comprehensive security review of all Claude Code skills, plugins, agents, hooks, and permission configurations.

## When to Use

- Periodically review your Claude Code setup for security issues
- After installing new plugins or skills
- When adding new permission allowlist entries
- Before sharing your configuration with others

## Audit Process

### Step 1: Load Ignore List

Read the ignore list at `~/.claude/skill-audit-ignore.md` to identify items that have been previously reviewed.

**IMPORTANT:** Ignored items are NOT silently skipped. They are fully scanned and any findings are reported in a separate "Previously Reviewed Items" section. This prevents malicious code from bypassing audits by including an ignore file — you always see what would have been flagged.

Parse the file to extract:
- Ignored skills (under "## Ignored Skills")
- Ignored plugins (under "## Ignored Plugins")
- Ignored findings (under "## Ignored Findings")

### Step 2: Scan Configuration Locations

Scan these locations for Claude Code configuration:

**Global Configuration:**
- `~/.claude/settings.json` - Global settings and enabled plugins
- `~/.claude/skills/` - User-defined skills
- `~/.claude/plugins/` - Installed plugins and marketplaces
- `~/.claude/CLAUDE.md` - Global instructions

**Project Configuration (current directory):**
- `.claude/settings.local.json` - Project permission allowlists
- `.claude/skills/` - Project-specific skills
- `.claude/agents/` - Project-specific agents
- `.claude/commands/` - Project-specific commands
- `CLAUDE.md` - Project instructions

### Step 3: Check for Security Issues

For each item found, check against this security criteria:

#### Permission Allowlist (HIGH priority)
Check `.claude/settings.local.json` for risky patterns:
- `Bash(*:*)` - Wildcard bash (CRITICAL)
- `Bash(psql:*)` without SELECT restriction
- `Bash(python:*)` or `Bash(python3:*)` without path restriction
- `Bash(rm:*)`, `Bash(sudo:*)` - Destructive commands
- `Bash(curl:*)`, `Bash(wget:*)` - Unrestricted network access

**Safe patterns:**
- `Bash(mix compile:*)`, `Bash(mix test:*)` - Bounded to mix commands
- `Bash(git status:*)` - Read-only git
- `Bash(psql -c SELECT:*)` - Read-only SQL

#### Third-Party Plugins (HIGH priority)
Check `~/.claude/plugins/known_marketplaces.json` for non-Anthropic sources:
- Official (safe): `anthropics/claude-code`, `anthropics/claude-plugins-official`
- Third-party (review needed): Any other GitHub repo

For each third-party plugin:
1. Flag for review with the source repo
2. If in ignore list, include in "Previously Reviewed Items" section instead of main findings

#### Hooks (MEDIUM priority)
Check for hooks that execute code:
- `hooks/hooks.json` files in plugins
- Shell scripts (`.sh`) or Python scripts (`.py`) in hook directories

Flag hooks that:
- Run on every tool use (PreToolUse, PostToolUse)
- Have broad file access
- Make network requests

#### Skills with External Access (MEDIUM priority)
Flag skills that:
- Use `WebFetch` to arbitrary URLs
- Have browser automation capabilities
- Write to file system outside project
- Call external APIs

#### Hardcoded Paths (LOW priority)
Flag skills with hardcoded absolute paths that could be stale or exploited.

### Step 4: Generate Report

Output a report with sections:

```
# Security Audit Report
Date: [current date]

## Summary
- Items scanned: X skills, Y plugins, Z agents
- New issues found: X high, Y medium, Z low
- Previously reviewed items: X (verify these still look acceptable)

## HIGH Severity
[List NEW issues with location and recommendation]

## MEDIUM Severity
[List NEW issues with location and recommendation]

## LOW Severity
[List NEW issues with location and recommendation]

## Previously Reviewed Items (Verify These)
[List ALL findings that matched ignore patterns - shown for transparency]
[Include full details: what was found, severity, location]
[User should glance at these to confirm they're still expected]

## Recommendations
[Actionable next steps]
```

### Step 5: Offer Fixes

For common issues, offer to fix them:
- Remove risky permission patterns
- Disable third-party plugins
- Add items to ignore list if reviewed and accepted (moves them to "Previously Reviewed" in future audits, but still shows them)

## Example Usage

**User:** "Run a security audit of my Claude setup"

**You should:**
1. Read `~/.claude/skill-audit-ignore.md`
2. Scan all configuration locations listed above
3. Check ALL items against security criteria (nothing is silently skipped)
4. Generate the report with new issues in main sections
5. Show previously-reviewed items in a separate section (user glances to verify they're still expected)
6. Offer to fix critical issues or add newly reviewed items to ignore list

## Adding to Ignore List

If the user reviews an item and wants to ignore it:

```markdown
### item-name
- **Reason:** [user's reason]
- **Reviewed:** [today's date]
- **Reviewer:** [username]
```

Add this to the appropriate section in `~/.claude/skill-audit-ignore.md`.

## Official Plugin Sources

These GitHub repositories are considered official/trusted:
- `anthropics/claude-code`
- `anthropics/claude-plugins-official`

Plugins from other sources require explicit review and should be added to the ignore list only after audit.
