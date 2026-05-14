---
name: voiceprints
description: >
  Apply the user's personal writing voice when drafting any email, LinkedIn post,
  or longform content on their behalf. Reads voice rules from
  ~/Documents/voiceprints/<medium>.md (email.md / linkedin.md / content.md) and
  applies them. Use whenever drafting any reply, post, essay, or short-form
  message on the user's behalf — applying voice is automatic, not something the
  user has to ask for.
---

# Voiceprints

When drafting any user-authored content (email, LinkedIn post, longform piece, short
reply, etc.), apply the user's voiceprint for that medium.

## How to apply

1. **Detect the medium** from context:
   - Email reply, intro, outreach, follow-up, scheduling, decline → `email.md`
   - LinkedIn post or comment → `linkedin.md`
   - Blog post, essay, longform article, op-ed → `content.md`
   - Short message (Slack, iMessage, DM) → use `email.md` as the closest match
   - If the medium is genuinely ambiguous, ask the user before drafting.

2. **Read** `~/Documents/voiceprints/<medium>.md`.

3. **Apply every rule** in that file to the draft. Mode-specific rules win over
   general rules. The file contains the user's full voice spec (ban list, voice
   patterns, format-specific modes, adaptation rules).

4. **Don't mention the voiceprint** — just produce the draft in the user's voice.

## If the voiceprint file is missing

Tell the user once per session, then proceed with default Claude voice (don't block
the draft):

> "No voiceprint for `<medium>` yet. Run `/voiceprint-creator` if installed, or
> install it from `github.com/grahac/claude_skills`. Drafting in default voice
> for now."

## If the file is empty or near-empty (under ~20 lines)

Warn the user it looks like a stub, then proceed with whatever rules are present
(or default voice if effectively none):

> "Your `<medium>` voiceprint looks like a stub. Rerun /voiceprint-creator to fill
> it out properly. Drafting with what's there for now."

## Updating a voiceprint

Tell the user they can edit `~/Documents/voiceprints/<medium>.md` directly, or
rerun `/voiceprint-creator` to regenerate.
