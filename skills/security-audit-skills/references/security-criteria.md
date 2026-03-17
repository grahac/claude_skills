# Security Criteria Checklist

## Permission Allowlist (HIGH priority)
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

## Third-Party Plugins (HIGH priority)
Check `~/.claude/plugins/known_marketplaces.json` for non-Anthropic sources:
- Official (safe): `anthropics/claude-code`, `anthropics/claude-plugins-official`
- Third-party (review needed): Any other GitHub repo

For each third-party plugin:
1. Flag for review with the source repo
2. If in ignore list, include in "Previously Reviewed Items" section instead of main findings

## Hooks (MEDIUM priority)
Check for hooks that execute code:
- `hooks/hooks.json` files in plugins
- Shell scripts (`.sh`) or Python scripts (`.py`) in hook directories

Flag hooks that:
- Run on every tool use (PreToolUse, PostToolUse)
- Have broad file access
- Make network requests

## Skills with External Access (MEDIUM priority)
Flag skills that:
- Use `WebFetch` to arbitrary URLs
- Have browser automation capabilities
- Write to file system outside project
- Call external APIs

## Hardcoded Paths (LOW priority)
Flag skills with hardcoded absolute paths that could be stale or exploited.

## Official Plugin Sources
These GitHub repositories are considered official/trusted:
- `anthropics/claude-code`
- `anthropics/claude-plugins-official`

Plugins from other sources require explicit review and should be added to the ignore list only after audit.
