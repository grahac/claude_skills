# Voiceprint Creator — Gotchas

## AI-contaminated corpus
If the user drafts emails with Claude regularly, those AI patterns will feed back into the extracted voice. Always ask up front whether any sent emails are mostly Claude-drafted, and exclude those before analyzing.

## Multiple connectors connected
If both Gmail and Microsoft 365 (or work + personal Gmail) are connected, ask which account to use before pulling. Work and personal voice often differ — mixing them produces a muddled voiceprint.

## Quoted reply text bleeds in
Always strip the quoted reply chain (`>` lines, "On [date], X wrote:" blocks) and any signature block before analyzing. Otherwise the user's "voice" will include text they didn't write.

## Pattern claimed without evidence
Don't assert a pattern unless it appears in at least 3 of the 50 emails. One-off usage is not voice. Always pull a real example from the corpus when claiming a pattern.

## Multilingual corpus
If the user emails in more than one language, run analysis per-language and produce per-language mode rules. A single voiceprint across languages will be inconsistent.

## Calibration step skipped
Don't package the skill until at least two consecutive calibration samples come back GOOD. Skipping calibration produces a voiceprint that "looks right" on paper but generates wrong-feeling drafts.

## skill-creator not installed
The packaging step (6b) depends on skill-creator's `init_skill.py` and `package_skill.py`. Check both common install paths first; if neither exists, fall back to writing a raw `~/Documents/myvoiceprint/SKILL.md` (Step 6c) and tell the user how to install skill-creator if they want the `.skill` package.

## Overwriting an existing myvoiceprint
If `~/Documents/myvoiceprint/` or `~/Documents/myvoiceprint.skill` already exists, ask before overwriting. Offer to save the new one as `myvoiceprint_[date].skill` so the user keeps the previous version.

## Forgetting to embed the voiceprint
The personalized SKILL.md MUST contain the full voiceprint content inline (Section 1 through 5). The skill is single-file; if you only put the application logic and reference an external file, the skill won't work on claude.ai.
