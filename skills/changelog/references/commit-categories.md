# Commit Categorization Heuristics

Map each commit to the appropriate change type using these clues:

| Commit clues | Category |
|---|---|
| `feat:`, `add`, `new`, `implement` | Added |
| `refactor`, `update`, `change`, `improve`, `rename` | Changed |
| `deprecate` | Deprecated |
| `remove`, `delete`, `drop` | Removed |
| `fix`, `bug`, `patch`, `correct` | Fixed |
| `security`, `vuln`, `CVE`, `auth` | Security |

## Writing Good Entries

Group related commits into single meaningful entries. Write entries for humans — describe the impact, not the implementation.

**Good:** `- Added CSV export for user reports`
**Bad:** `- feat: add csv_export method to UserReportController`

## Rules

- Keep entries concise — one line each, sentence case, no trailing period
- If commits are ambiguous, group them conservatively and note uncertainty
- Never invent entries that aren't supported by the git history
