# Voiceprints — Gotchas

## Wrong medium auto-detected
If the user's prompt is ambiguous ("draft a quick message to..."), don't guess. Ask which medium they want — email, LinkedIn, or longform — before reading the file. A LinkedIn voiceprint applied to a customer email will read wrong.

## Voiceprint file is stale or empty
If `~/Documents/voiceprints/<medium>.md` exists but is empty or under ~20 lines, warn the user it looks like a stub and recommend rerunning `/voiceprint-creator`. Don't apply a partial voiceprint as if it were complete.

## Cross-platform file path
`~/Documents/voiceprints/` resolves to `$HOME/Documents/voiceprints/` on macOS/Linux and to `%USERPROFILE%\Documents\voiceprints\` on Windows. Use the home-directory abstraction available in whatever environment the agent runs in — don't hardcode `/Users/...`.

## Old installable myvoiceprint skill still present
A user who set up voiceprints before this design split may have a `~/.claude/skills/myvoiceprint_<medium>/` folder from the previous workflow. If both that folder AND `~/Documents/voiceprints/<medium>.md` exist, prefer the Documents version (single source of truth). Mention to the user that the old skill folder can be deleted.

## Multiple voiceprint files exist
If `~/Documents/voiceprints/` contains files beyond the canonical three (e.g., `email_old.md`, `email_2026-05-12.md`, archives), read only `email.md`, `linkedin.md`, `content.md`. Don't guess which dated variant is active.

## Reads the file every draft
This is intentional, not a bug. Reading at runtime means edits to the voiceprint file take effect immediately. Don't cache or memoize.

## Don't auto-run voiceprint-creator
When the voiceprint is missing, point the user to `/voiceprint-creator` but never invoke it transparently. Voiceprint creation is a 15–30 min interactive flow; surprising the user with it mid-draft is bad UX.

## Length pass after applying
The voiceprint typically tells Claude to "write less" / "default to fewer words". Run a final length pass on the draft. AI drafts trend long; voiceprints tend to want them shorter.
