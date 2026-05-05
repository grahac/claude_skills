---
name: email-voice
description: >
  Apply the user's personal email voice when drafting any email or short-form written
  content on their behalf. Use whenever drafting emails, follow-ups, intros, check-ins,
  nudges, declines, or any outbound message. Reads the user's voice profile from
  ~/Documents/voiceprints/email.md (falls back to ~/.claude/voiceprints/email.md for
  legacy installs) and applies every rule in it.
---

# Email Voice

When asked to draft any email or short-form written content:

1. Read the voice profile. Try `~/Documents/voiceprints/email.md` first; if not present, fall back to `~/.claude/voiceprints/email.md` (the legacy location). Use whichever exists.

2. Apply every rule in that file to the draft:
   - Section 1 (ban list): hard filter on every word and phrase listed
   - Section 2 (anti-performative): do not manufacture patterns or repeat one-off phrases
   - Section 3 (core patterns): apply sentence structure, vocabulary, and formatting rules
   - Section 4 (modes): match the draft's mode (intro reply, follow-up, decline, etc.) to the right mode rules
   - Section 5 (adaptation): run the pre-draft checklist, then the two-pass review

3. Do not mention that you are applying a voice profile. Just produce the draft.

4. If neither path has a voiceprint:
   - Tell the user: "No voice profile found. Run /voice-extractor once to build yours — takes about 15 minutes."
   - Do not attempt to draft in a generic voice as a fallback.

---

## Notes for accurate application

- Short is almost always right. When in doubt, cut.
- Answer first. Never build up to the point.
- Do not add warmth sentences that exist only to be friendly.
- Do not add a closing like "Let me know if you have questions." Only close with a genuine next-step ask or nothing at all.
- Do not reproduce any auto-signature block. Signatures are appended automatically.
- If the user's mode-specific rules conflict with a general rule, the mode-specific rule wins.
