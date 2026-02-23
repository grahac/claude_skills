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

## Skills

- [changelog](#changelog)
- [elixir-simplifier](#elixir-simplifier)
- [granola-scoop](#granola-scoop)
- [marketing-copywriter](#marketing-copywriter)
- [prompt-cache-optimizer](#prompt-cache-optimizer)
- [security-audit-skills](#security-audit-skills)

---

### changelog

Creates and manages `CHANGELOG.md` following the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) spec.

**Use when:**
- Adding recent changes to the changelog
- Preparing a release and versioning the changelog
- Creating a CHANGELOG.md from scratch

**Key principles:**
- Reads git history to extract what changed — never invents entries
- Organizes changes into Added, Changed, Deprecated, Removed, Fixed, Security
- Supports `[Unreleased]` workflow and cutting versioned releases with comparison links

**Invoke:** `/changelog`

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

---

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

### prompt-cache-optimizer

Audits hooks and AI/LLM API calls for prompt caching anti-patterns, then produces concrete fixes to maximize cache hit rate and reduce API costs.

**Use when:**
- Reviewing Claude Code hooks for cache-breaking patterns
- Auditing project AI/LLM calls for suboptimal prompt structure
- Reducing AI API costs through better caching
- Diagnosing low prompt cache hit rates

**Key principles:**
- Scans `~/.claude/settings.json` and project settings for hooks
- Classifies injected data as globally static / project static / session static / frequently dynamic
- Makes guesses about dynamic vs static data, then confirms with you before generating fixes
- Produces before/after code examples for every issue found
- Never changes tools mid-session; never silently assumes

**Invoke:** `/prompt-cache-optimizer`

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

## Contributing

PRs welcome! Add new skills in the `skills/` directory following the existing format.

## License

MIT
