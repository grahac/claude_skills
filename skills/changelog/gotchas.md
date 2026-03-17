# Changelog Gotchas

Common failure patterns. Update this file every time something goes wrong.

## 1. Guessing the remote URL for comparison links
**Problem:** Generated comparison links point to the wrong repo or use SSH format instead of HTTPS.
**Fix:** Always run `git remote get-url origin` and confirm with the user before writing links.

## 2. Raw commit messages instead of human-readable entries
**Problem:** Entries read like git log output instead of a changelog.
**Fix:** Describe the impact ("Added CSV export for reports"), not the implementation ("add csv_export method to controller").

## 3. Including merge commits as entries
**Problem:** Merge commits like "Merge branch 'feature'" appear as changelog entries.
**Fix:** Always use `--no-merges` when reading git log.

## 4. Forgetting to add a fresh [Unreleased] section after cutting a release
**Problem:** After converting [Unreleased] to a version, the file has no place for new entries.
**Fix:** Always add a new empty `## [Unreleased]` above the newly created version section.

## 5. Empty change type sections
**Problem:** Sections like `### Deprecated` appear with no entries underneath.
**Fix:** Only include change type sections that have actual entries.
