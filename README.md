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
- [nanobanana](#nanobanana)
- [appstore-images](#appstore-images)

### Strategy

- [indispensable-need](#indispensable-need)

### Development

- [elixir-simplifier](#elixir-simplifier)
- [prompt-cache-optimizer](#prompt-cache-optimizer)
- [changelog](#changelog)

### Productivity

- [granola-scoop](#granola-scoop)

### Writing

- [voiceprint-creator](#voiceprint-creator)
- [voiceprints](#voiceprints)

### Security

- [security-audit-skills](#security-audit-skills)

### Contracts

- [contract-manager](#contract-manager)

> **Full file map:** See [SKILLS-MAP.md](SKILLS-MAP.md) for the complete directory structure of every skill.

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

### nanobanana

Generates professional photo-realistic images using structured JSON prompts and Google's Gemini image API.

**Use when:**
- Creating product shots, lifestyle images, ad creative, or hero images
- Generating consistent brand imagery with full control over lighting, camera, and composition
- Iterating on image concepts with structured prompt refinement

**Key principles:**
- Transforms plain descriptions into structured JSON prompts (scene, camera, lighting, style)
- Camera details and specific lighting setups produce dramatically better results than vague adjectives
- Iterates on one axis at a time — never changes everything at once
- Uses `gemini-2.5-flash-image` for speed, `gemini-3-pro-image-preview` for text and maximum quality

**Invoke:** `/nanobanana`

---

### appstore-images

Generates polished App Store preview screens for iPhone, iPad, and Mac — composites screenshots onto colored backgrounds with realistic device mockups (dynamic island, side buttons, MacBook chrome) and bold headline typography.

**Use when:**
- Preparing App Store / Mac App Store listing assets
- Creating marketing screenshots with consistent device framing across a screen set
- Generating multi-device sets (iPhone + iPad + Mac) from raw simulator captures

**Key principles:**
- Bundles 7 font presets (montserrat default, oswald, bebas, anton, archivo, monasans, fredoka) and 20+ background colors plus custom hex/gradient support
- Renders realistic device frames matching Apple's required canvas sizes (1290×2796 iPhone, 2048×2732 iPad, 2880×1800 Mac)
- Vary the headline per screen to tell a story across a set; keep gradient and font consistent

**Invoke:** `/appstore-images`

---

## Strategy

### indispensable-need

Identifies a product's indispensable need — the high-stakes job-to-be-done that has no good substitute.

**Use when:**
- Stress-testing whether a product is irreplaceable or merely nice-to-have
- Mapping competitive substitutes and where they fall short
- Surfacing the functional, emotional, and social dimensions of why someone hires a product

**Key principles:**
- Multiple parallel agents probe functional, emotional, and social JTBD dimensions
- Combines competitive research with deep codebase reading to ground claims in what the product actually does
- Outputs a sharp statement of the indispensable need, not a feature list

**Invoke:** `/indispensable-need`

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

## Writing

### voiceprint-creator

Creates a voiceprint capturing your personal writing voice for a specific medium (email, LinkedIn, or longform content) and writes it as a single `.md` skill file you can install on claude.ai, Claude Code, or Cowork. Run once per medium; install the file and Claude drafts in your voice.

**Use when:**
- Setting up a voiceprint for the first time
- Adding a new medium (already have email, want LinkedIn or longform)
- Rebuilding after your writing voice has drifted

**Key principles:**
- Asks which medium up front (email / LinkedIn / content); each has its own corpus source
- **Email** — pulls from any connected email MCP (Gmail, Outlook/M365, Fastmail, ProtonMail, etc.). Supports MULTIPLE accounts in one run (e.g., personal + work under separate MCPs) and merges into one voiceprint with per-account signature guidance
- **LinkedIn** — parses your LinkedIn data export (Settings → Data privacy → Get a copy of your data)
- **Content** — scrapes longform pieces from a URL you provide (blog index, Substack archive)
- Corpus pull runs in a fresh-context subagent so large mailboxes don't overflow context
- Preserves minimalist single-line sign-offs (`--firstname`, `-C`) while stripping multi-line contact blocks
- Analyzes 8 voice dimensions; asserts a pattern only when it appears in ≥3 corpus pieces
- Distinguishes universal voice patterns from account-specific ones (sigs, CTAs, formality) in multi-account runs
- Walks through human review (WRONG / OVERSTATED / MISSING / NEEDS_NUANCE) and calibration samples (GOOD / CLOSE / OFF) before writing

**Output:** `~/Documents/voiceprints/<medium>.md` — plain Markdown rules file (e.g., `email.md`, `linkedin.md`, `content.md`). The companion `voiceprints` skill reads it automatically when you draft content. No separate install per medium.

**Invoke:** `/voiceprint-creator`

---

### voiceprints

Runtime companion to `voiceprint-creator`. Applies your personal writing voice whenever you draft email, LinkedIn posts, or longform content — reads the voice rules from `~/Documents/voiceprints/<medium>.md` and applies them automatically. Lean (~30 lines) so it doesn't bloat context when loaded.

**Use when:**
- Drafting any email, LinkedIn post, or longform content on your behalf (auto-applies)
- Already created a voiceprint via `/voiceprint-creator` and want it to apply

**Key principles:**
- Auto-detects medium from context (email / LinkedIn / longform); asks if ambiguous
- Reads `~/Documents/voiceprints/<medium>.md` at runtime — edits to the file take effect immediately, no reinstall
- If the voiceprint is missing, points you to `/voiceprint-creator` and proceeds with default Claude voice (doesn't block the draft)
- Stays small so it costs almost nothing when auto-loaded during drafting

**Invoke:** auto-loads on any drafting task (or `/voiceprints` to force-load)

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

## Contracts

### contract-manager

Multi-agent contract management — creates, reviews, and edits contracts using three specialized Claude subagents that independently analyze, cross-review, and debate disagreements.

**Use when:**
- Creating a new contract (NDA, consulting/freelance engagement, or general)
- Reviewing an existing contract for risks, clarity, and business viability
- Editing an existing contract with specific changes

**Key principles:**
- Three independent Claude agents (The Shield, The Plain Speaker, The Deal Maker) work in parallel
- Cross-review with AGREE/ELEVATE/CHALLENGE protocol for conflict resolution
- Checklist verification against required clauses by contract type
- Produces professional `.docx` output

**Invoke:** `/contract-manager`

---

## Skill Folder Structure

Every skill follows a consistent structure. See [SKILLS-MAP.md](SKILLS-MAP.md) for the full directory listing.

```
skill-name/
  SKILL.md              # When to use, core instructions, file map
  gotchas.md            # Failure patterns — update when things go wrong
  references/           # Detailed examples, checklists (read on demand)
  assets/               # Templates, starter files, reusable formats
  scripts/              # Executable scripts
```

---

## Contributing

PRs welcome! Add new skills in the `skills/` directory following the existing format.

## License

MIT
