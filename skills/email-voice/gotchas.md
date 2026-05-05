# Email Voice — Gotchas

## No profile yet
If neither `~/Documents/voiceprints/email.md` (primary) nor `~/.claude/voiceprints/email.md` (legacy) exists, do NOT fall back to a generic voice. Tell the user to run `/voice-extractor` once and stop. A generic-voice fallback is worse than nothing — it teaches the user to ignore the skill.

## Reproducing the signature block
The voice profile may include the user's typical sign-off, but most mail clients append an auto-signature. Never reproduce a signature block in the draft body — produces double signatures.

## Over-applying one-off patterns
Section 2 (anti-performative rules) exists because Claude tends to caricature the user. If the profile says "occasionally opens with X", do not open every draft with X. Read Section 2 carefully and apply it.

## Mode mismatch
The draft's mode (intro reply vs. decline vs. nudge) determines which Section 4 rules apply. If the user's request is ambiguous, ask which mode before drafting — applying the wrong mode produces fluent but wrong-feeling email.

## Mode rule conflicts with general rule
If a Section 4 mode rule contradicts a Section 3 core pattern, the mode rule wins. Section 3 is the default; Section 4 is the override.

## Mentioning the voice profile
Never tell the user "I'm applying your voice profile" or reference the file in the draft. Just produce the draft. The skill is invisible by design.

## Stale profile
If a draft consistently feels off, suggest the user re-run `/voice-extractor` — voice drifts over months, and the profile may be stale.
