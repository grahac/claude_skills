---
name: changelog
description: Create and manage a CHANGELOG.md file following the Keep a Changelog 1.1.0 spec (https://keepachangelog.com/en/1.1.0/). Use when the user asks to update the changelog, log recent changes, create a changelog, add an entry to CHANGELOG.md, or prepare a release. Reads git history to extract what changed and organizes entries under Added, Changed, Deprecated, Removed, Fixed, or Security.
---

# Changelog Manager

Maintain `CHANGELOG.md` following [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

## [1.2.0] - 2026-02-22

### Fixed
- Bug description

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
```

**Rules:**
- `[Unreleased]` section always at the top
- Versions in descending order (`## [X.Y.Z] - YYYY-MM-DD`)
- Six change types: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
- Only include sections that have entries — omit empty ones
- Each entry is a human-readable bullet, not a raw commit message
- Version links at the bottom of the file

## Workflow

### Step 1 — Check existing changelog

```bash
cat CHANGELOG.md 2>/dev/null || echo "NO_CHANGELOG"
```

If no CHANGELOG.md exists, create one with the header and an empty `[Unreleased]` section.

### Step 2 — Get recent commits

Determine the range to inspect. If CHANGELOG.md exists, find the last logged version tag:

```bash
# Get last tagged version
git tag --sort=-version:refname | head -1

# Get commits since last tag (or all commits if no tags)
git log v1.2.0..HEAD --oneline --no-merges
# or
git log --oneline --no-merges -30
```

### Step 3 — Categorize commits

Map each commit to the appropriate change type. Use these heuristics:

| Commit clues | Category |
|---|---|
| `feat:`, `add`, `new`, `implement` | Added |
| `refactor`, `update`, `change`, `improve`, `rename` | Changed |
| `deprecate` | Deprecated |
| `remove`, `delete`, `drop` | Removed |
| `fix`, `bug`, `patch`, `correct` | Fixed |
| `security`, `vuln`, `CVE`, `auth` | Security |

Group related commits into single meaningful entries. Write entries for humans — describe the impact, not the implementation.

**Good:** `- Added CSV export for user reports`
**Bad:** `- feat: add csv_export method to UserReportController`

### Step 4 — Update the file

- New entries go under `[Unreleased]` unless the user is cutting a release
- If cutting a release, convert `[Unreleased]` to the new version with today's date and add a fresh empty `[Unreleased]` above it

### Step 5 — Release mode (if requested)

When the user says "release X.Y.Z" or "cut version X.Y.Z":

1. Rename `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` (today's date)
2. Add a new empty `## [Unreleased]` above it
3. Update the version comparison links at the bottom:
   ```markdown
   [Unreleased]: https://github.com/owner/repo/compare/vX.Y.Z...HEAD
   [X.Y.Z]: https://github.com/owner/repo/compare/vY.Y.Y...vX.Y.Z
   ```
4. Ask the user to confirm the version number and remote URL if unknown

## Notes

- Ask before guessing the remote URL for version links — get it from `git remote get-url origin`
- If commits are ambiguous, group them conservatively and note uncertainty
- Never invent entries that aren't supported by the git history
- Keep entries concise — one line each, sentence case, no trailing period
