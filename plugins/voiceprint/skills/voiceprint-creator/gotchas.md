# Voiceprint Creator — Gotchas

## AI-contaminated corpus
If the user drafts with Claude regularly, those AI patterns will feed back into the extracted voice. Always ask up front whether any pieces are mostly Claude-drafted, and exclude those before analyzing.

## Assuming Gmail
Not every user is on Gmail. Detect the actual email MCP that's connected (Outlook, Microsoft 365, Fastmail, ProtonMail, etc.) before composing any query. Per-provider query syntax differs — Gmail's `in:sent` is not Outlook's `Sent Items` filter.

## Multiple email accounts under separate MCPs
A user with personal + work mailboxes often has them under DIFFERENT MCPs (e.g., one Gmail MCP for personal, one Outlook MCP for work). The skill supports a multi-account merged voiceprint — list all detected MCPs, ask which to include and what address per MCP, then brief the subagent with a list of (MCP, address) pairs to pull from in a loop.

## Account-specific patterns get mistaken for universal voice
With a multi-account corpus, signature contact blocks, CTA URLs, and sometimes formality differ per account. If the analyzer treats these as universal patterns, the voiceprint will instruct Claude to use the wrong sig on the wrong account. Tag account-specific findings inline; only assert as universal if they appear across all accounts.

## One account drowns out the others
If pulling 50 messages without per-account balance, a high-volume account (e.g., personal Gmail) can supply 45 of 50 messages and a low-volume work account contributes only 5 — its patterns get lost. Sample down the dominant account so smaller accounts have meaningful representation (~30/20 or 25/25 is healthier than 45/5).

## Quoted reply text bleeds in (email)
Always strip the quoted reply chain (`>` lines, "On [date], X wrote:" blocks, Outlook "From: … Sent: …" headers) before analyzing. Otherwise the user's "voice" will include text they didn't write.

## Over-aggressive signature stripping kills voice signal
Don't strip minimalist single-line sign-offs (`--<firstname>`, `--<Firstname>`, `-<initial>`, `<firstname>`, `thx, <initial>`, `xx`, etc.) — those are real voice. Only strip MULTI-LINE contact blocks (anything with phone digits, `@`, URLs, company/title lines, disclaimers). Heuristic: trailing single line under ~25 chars with no `@`/URL/phone → keep. Anything bigger or with contact info → strip.

## Thread-level `in:sent` ≠ user-authored messages
Gmail's `in:sent` (and Outlook's Sent Items filter) returns threads containing at least one sent message. Inside those threads, individual messages can be from anyone. Filter at the MESSAGE level by `sender == user_email`, never assume `thread.messages[0]` is the user's voice — for reply threads it's usually the other person's original message.

## Main-agent context overflow on email pull
A 50-thread Gmail search returns ~70k+ chars of JSON; full-content fetches multiply that. Loading either directly into the main agent will exceed context. Always delegate the pull/filter/clean to a fresh-context subagent that returns prose findings (cleaned corpus only).

## LinkedIn export file naming
LinkedIn renames the posts file across exports — sometimes `Shares.csv`, sometimes `posts.csv`, sometimes inside a `Posts/` subfolder. Glob for the actual file rather than hardcoding the name. If the export contains only reshares, ask the user to paste 20–30 original posts directly.

## Content URL is a single post, not an index
When the user passes a single post URL for the content medium, you can't build a voiceprint from one piece. Ask for more URLs until you have at least 10. Don't try to infer voice from one essay.

## Site chrome bleeds into content corpus
WebFetch returns the full rendered page. Strip nav, sidebar, comments, author bio, related-posts blocks before analyzing — otherwise the "voice" will include the site's marketing copy.

## Pattern claimed without evidence
Don't assert a pattern unless it appears in at least 3 corpus pieces. One-off usage is not voice. Always pull a real example from the corpus when claiming a pattern.

## Multilingual corpus
If the user writes in more than one language, run analysis per-language and produce per-language mode rules. A single voiceprint across languages will be inconsistent.

## Calibration step skipped
Don't write the file until at least two consecutive calibration samples come back GOOD. Skipping calibration produces a voiceprint that "looks right" on paper but generates wrong-feeling drafts.

## Overwriting an existing voiceprint
If `~/Documents/myvoiceprint-<medium>.skill` or `~/Documents/myvoiceprint-<medium>/` already exists, ask before overwriting. Offer to save the new one as `myvoiceprint-<medium>-YYYY-MM-DD` so the user keeps the previous version.

## Wrong medium for the corpus
Don't analyze LinkedIn posts and package as `myvoiceprint-email`, or vice versa — voice differs significantly across media (length, formality, formatting). The generated skill's `name:` and `description:` are medium-specific and must match the corpus source.

## Refine mode without an installed skill
Refine mode reads `~/.claude/skills/myvoiceprint-<medium>/SKILL.md` directly. If the skill isn't installed there (user generated it but never copied it into `~/.claude/skills/`, or only installed it on claude.ai), refine has no source to edit. Tell the user to install first, or rerun in create mode.

## skill-creator scripts errored mid-run
If `init_skill.py` or `package_skill.py` errors (missing deps, schema mismatch, permission issue), don't block the user — fall through to the raw `~/Documents/myvoiceprint-<medium>/SKILL.md` folder fallback. The folder is fully installable; only the single-file `.skill` package is lost.
