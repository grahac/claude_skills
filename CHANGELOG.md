# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses date-based releases.

## [Unreleased]

### Added
- `voice-extractor` skill — one-time extraction of personal email writing voice from the last 50 sent emails (Gmail / google-mcp / Microsoft 365), with human review and calibration passes before saving the voiceprint to `~/Documents/voiceprints/email.md`
- `email-voice` skill — applies the saved voiceprint to every email draft, enforcing the LLM-ism ban list, anti-performative rules, and mode-specific patterns; prompts to run `/voice-extractor` if no voiceprint exists. Reads from `~/Documents/voiceprints/email.md` with a fallback to `~/.claude/voiceprints/email.md` for legacy installs.
- New `Writing` skills category in README and SKILLS-MAP

### Changed
- Voiceprint storage canonical location is `~/Documents/voiceprints/email.md` (was `~/.claude/voiceprints/`). `~/Documents` is writable by sandboxed agents like Cowork, while `~/.claude/` is not. `email-voice` retains a fallback read of the legacy `~/.claude/voiceprints/email.md` path.
- `voice-extractor` Step 6 hardened with explicit anti-pattern guard — output must be a plain markdown file at `~/Documents/voiceprints/email.md`, never packaged as a Cowork/Claude Code skill folder. Prevents agents from generating `voice-name/SKILL.md` wrappers instead of the expected file.
- `hyperslide` upgraded with two-font pairing (display + body), slide entry animations with staggered children, gradient mesh backgrounds, 15px minimum body text, and WCAG AA contrast guidance
- `hyperslide` example updated to demonstrate all new design patterns

## [2026-02-25]

### Added
- `hyperslide` skill — generate polished single-file HTML presentations with scroll-snap navigation, keyboard controls, and a slide counter
- `innovate` skill — identify the single most high-leverage addition to any plan or proposal
- `website-extractor` skill — extract content, copy, and brand identity from any website into a structured document ready for rewriting
- `prompt-cache-optimizer` skill — audit Claude Code hooks and AI/LLM calls for cache-breaking patterns and produce concrete fixes
- `changelog` skill — create and maintain CHANGELOG.md following Keep a Changelog 1.1.0
- `security-audit-skills` skill — audit Claude Code configuration for security issues in skills, plugins, and hooks
- `granola-scoop` skill — extract meeting notes from Granola's local cache without an API
- `marketing-copywriter` skill — create landing page copy, emails, and ad copy
- `elixir-simplifier` skill — simplify and refactor Elixir/Phoenix/LiveView code with a focus on removing duplication

### Changed
- README reorganized into four categories: Product & Marketing, Development, Productivity, Security
- `marketing-copywriter` updated with explicit AI-pattern avoidance guidance
- `granola-scoop` renamed from `granola` for clarity

### Removed
- Compiled `.skill` binary files from version control (skills are now directory-based only)

[Unreleased]: https://github.com/grahac/claude_skills/compare/2026-02-25...HEAD
[2026-02-25]: https://github.com/grahac/claude_skills/commits/main
