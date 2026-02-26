# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `hyperslide` skill — generate polished single-file HTML presentations with scroll-snap navigation, keyboard controls, and a slide counter
- `innovate` skill — identify the single most high-leverage addition to any plan or proposal
- `website-extractor` skill — extract content, copy, and brand identity from any website into a structured document ready for rewriting
- `prompt-cache-optimizer` skill — audit Claude Code hooks and AI/LLM calls for cache-breaking patterns and produce concrete fixes
- `changelog` skill — create and maintain CHANGELOG.md following Keep a Changelog 1.1.0

### Changed
- `hyperslide` upgraded with two-font pairing (display + body), slide entry animations with staggered children, gradient mesh backgrounds, 15px minimum body text, and WCAG AA contrast guidance
- README reorganized into four categories: Product & Marketing, Development, Productivity, Security
- `marketing-copywriter` updated with explicit AI-pattern avoidance guidance
- `granola-scoop` renamed from `granola` for clarity

### Removed
- Compiled `.skill` binary files from version control (skills are now directory-based only)

## [0.1.0] - 2026-01-09

### Added
- `elixir-simplifier` skill — simplify and refactor Elixir/Phoenix/LiveView code with a focus on removing duplication
- `granola-scoop` skill — extract meeting notes from Granola's local cache without an API
- `marketing-copywriter` skill — create landing page copy, emails, and ad copy
- `security-audit-skills` skill — audit Claude Code configuration for security issues in skills, plugins, and hooks

[Unreleased]: https://github.com/grahac/claude_skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/grahac/claude_skills/commits/v0.1.0
