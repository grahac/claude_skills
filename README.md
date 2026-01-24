# Claude Code Skills

Personal productivity skills for [Claude Code](https://claude.ai/claude-code) — tools for development, meetings, writing, and security.

## Installation

To use these skills globally across all your Claude Code projects:

```bash
# Clone into your .claude/skills directory
git clone https://github.com/grahac/claude_skills.git ~/.claude/skills/claude_skills

# Or copy individual skills
cp -r skills/elixir-simplifier ~/.claude/skills/
```

## Available Skills

### granola-scoop

Extracts meeting notes from [Granola's](https://granola.ai) local cache — no API needed.

**Use when:**
- Extracting recent meeting notes ("extract my granola meetings")
- Reviewing what meetings you had ("what meetings did I have this week?")
- Searching meeting content for people or topics

**Output:** Markdown files saved to `~/.granola-scoop/output/` with meeting metadata, your notes, and AI summaries.

**Invoke:** `/granola-scoop`

---

### marketing-copywriter

Creates compelling marketing copy for landing pages, emails, ads, and product messaging.

**Use when:**
- Writing landing page copy
- Crafting email campaigns
- Creating ad copy
- Developing product messaging and value propositions
- Improving existing marketing copy

**Key principles:**
- Clarity over cleverness
- Audience-first messaging
- Specific outcomes over vague promises
- Avoids AI-sounding patterns (no "elevate", "seamless", "unlock your potential")

**Invoke:** `/marketing-copywriter`

---

### security-audit-skills

Performs security audits of your Claude Code configuration — skills, plugins, hooks, and permission allowlists.

**Use when:**
- Periodically reviewing your Claude setup for security issues
- After installing new plugins or skills
- Before sharing your configuration with others

**Key principles:**
- Nothing is silently skipped — ignored items are shown in a "Previously Reviewed" section
- Flags risky permission patterns (wildcard bash, unrestricted network access)
- Identifies third-party plugins that need review
- Checks for hooks with broad access

**Invoke:** `/security-audit-skills`

---

### elixir-simplifier

Simplifies and refines Elixir/Phoenix/LiveView code with a focus on **removing duplicate code**.

**Use when:**
- Finding and removing duplicate code across modules
- Extracting repeated patterns into shared components
- Reviewing recently written Elixir/Phoenix/LiveView code
- Refactoring existing code for clarity
- Checking if code follows Phoenix patterns

**Key principles:**
- DRY - Remove duplicate code (primary focus)
- KISS - Keep it simple
- LiveView over JavaScript
- Phoenix context patterns (no Repo in `_web` modules)
- HEEx `{}` syntax over `<%= %>`
- No hardcoded color hex codes
- No defensive fallbacks - let it crash

**Invoke:** `/elixir-simplifier`

## Contributing

PRs welcome! Add new skills in the `skills/` directory following the existing format.

## License

MIT
