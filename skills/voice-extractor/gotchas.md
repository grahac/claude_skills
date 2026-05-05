# Voice Extractor — Gotchas

## AI-contaminated corpus
If the user drafts emails with Claude regularly, those AI patterns will feed back into the extracted voice. Always ask up front whether any sent emails are mostly Claude-drafted, and exclude those before analyzing.

## Multiple connectors connected
If both Gmail and Microsoft 365 (or work + personal Gmail) are connected, ask which account to use before pulling. Work and personal voice often differ — mixing them produces a muddled profile.

## Quoted reply text bleeds in
Always strip the quoted reply chain (`>` lines, "On [date], X wrote:" blocks) and any signature block before analyzing. Otherwise the user's "voice" will include text they didn't write.

## Pattern claimed without evidence
Don't assert a pattern unless it appears in at least 3 of the 50 emails. One-off usage is not voice. Always pull a real example from the corpus when claiming a pattern.

## Multilingual corpus
If the user emails in more than one language, run analysis per-language and produce per-language mode rules. A single profile across languages will be inconsistent.

## Overwriting existing profile silently
If `~/Documents/voiceprints/email.md` already exists, ask before overwriting. Offer to save as `email_[date].md` instead so the user keeps the previous version.

## Calibration step skipped
Don't save the profile until at least two consecutive calibration samples come back GOOD. Skipping calibration produces a profile that "looks right" on paper but generates wrong-feeling drafts.
