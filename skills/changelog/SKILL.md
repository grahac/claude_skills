---
name: changelog
description: Create and manage a CHANGELOG.md file following the Keep a Changelog 1.1.0 spec (https://keepachangelog.com/en/1.1.0/). Use when the user asks to update the changelog, log recent changes, create a changelog, add an entry to CHANGELOG.md, or prepare a release. Reads git history to extract what changed and organizes entries under Added, Changed, Deprecated, Removed, Fixed, or Security.
---

# Changelog Manager

Maintain `CHANGELOG.md` following [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## File Map

| File | What it contains | When to read |
|------|-----------------|--------------|
| `references/format-example.md` | Full markdown template + comparison link format | When creating a new changelog or cutting a release |
| `references/commit-categories.md` | Heuristics table for mapping commits to change types | When categorizing commits |
| `assets/changelog-template.md` | Starter CHANGELOG.md for new projects | When no CHANGELOG.md exists |
| `gotchas.md` | Common failure patterns | When something goes wrong |

## Rules

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

If no CHANGELOG.md exists, create one using `assets/changelog-template.md`.

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

Read `references/commit-categories.md` for the heuristics table. Group related commits into single meaningful entries.

### Step 4 — Update the file

- New entries go under `[Unreleased]` unless the user is cutting a release
- If cutting a release, convert `[Unreleased]` to the new version with today's date and add a fresh empty `[Unreleased]` above it

### Step 5 — Release mode (if requested)

When the user says "release X.Y.Z" or "cut version X.Y.Z":

1. Rename `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` (today's date)
2. Add a new empty `## [Unreleased]` above it
3. Update version comparison links — see `references/format-example.md` for the format
4. Ask the user to confirm the version number and remote URL if unknown

## Notes

- Ask before guessing the remote URL for version links — get it from `git remote get-url origin`
- If commits are ambiguous, group them conservatively and note uncertainty
- Never invent entries that aren't supported by the git history
- Keep entries concise — one line each, sentence case, no trailing period
