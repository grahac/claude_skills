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

### Product & Marketing

- [hyperslide](#hyperslide)
- [website-extractor](#website-extractor)
- [marketing-copywriter](#marketing-copywriter)
- [innovate](#innovate)

### Development

- [elixir-simplifier](#elixir-simplifier)
- [prompt-cache-optimizer](#prompt-cache-optimizer)
- [changelog](#changelog)

### Productivity

- [granola-scoop](#granola-scoop)

### Security

- [security-audit-skills](#security-audit-skills)

---

## Product & Marketing

### hyperslide

Generates polished, self-contained HTML slide deck presentations — no PowerPoint, no external tools.

**Use when:**
- Creating a presentation from a description, code, or problem statement
- Building pitch decks, architecture overviews, research presentations
- Turning any content into a visual slide deck

**Key principles:**
- Asks about content and visual style (URL or mood), then derives the palette and fonts
- Produces a single `.html` file with scroll-snap navigation, keyboard controls, and a slide counter
- Uses only inline CSS/JS — no external dependencies
- Reviews the output in a browser and fixes visual issues before delivering

**Invoke:** `/hyperslide`

---

### website-extractor

Extracts all content and design information from a website to enable a complete rewrite.

**Use when:**
- Rewriting or redesigning an existing website
- Creating a new version of a site based on the original
- Auditing a site's copy, structure, and brand identity before rebuilding

**Key principles:**
- Captures page content, brand identity (colors, fonts, tone), navigation, section-by-section copy, and CTAs
- Extracts colors from code (Tailwind classes, CSS variables), not screenshots
- Saves a structured `site-extraction.md` document ready to pass to a rewrite agent

**Invoke:** `/website-extractor`

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

### innovate

Identifies the single most innovative, high-leverage addition to any plan or proposal.

**Use when:**
- Asking "what am I missing?" or "what would you add?"
- Wanting one unexpected but compelling improvement to a plan, spec, or strategy
- Looking for the boldest move before committing to an approach

**Key principles:**
- Picks **one** thing — not a list
- Must be non-obvious, concrete, and accretive (not just incrementally better)
- Presents the idea with a clear argument for why it's the highest-leverage move available

**Invoke:** `/innovate`

---

## Development

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

## Productivity

### granola-scoop

Extracts meeting notes from [Granola's](https://granola.ai) local cache — no API needed.

**Use when:**
- Extracting recent meeting notes ("extract my granola meetings")
- Reviewing what meetings you had ("what meetings did I have this week?")
- Searching meeting content for people or topics

**Output:** Markdown files saved to `~/.granola-scoop/output/` with meeting metadata, your notes, and AI summaries.

**Invoke:** `/granola-scoop`

---

## Security

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
