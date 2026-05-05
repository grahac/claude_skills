---
name: voice-extractor
description: >
  Extract the user's personal email writing voice from their last 50 sent emails and
  save it as a reusable voice profile. Use when the user says "extract my voice",
  "build my voice profile", "analyze my email tone", "make me sound like me", "capture
  my writing style", or any variation of creating a personal voice profile from their
  actual sent email. Runs once; the output file is then used automatically by the
  email-voice skill on every future draft.
---

# Voice Extractor

Pulls the user's last 50 sent emails, analyzes them for genuine voice patterns, walks
through a human review pass, runs calibration samples, and saves the result to
`~/.claude/voiceprints/email.md`. The email-voice skill reads that file automatically on
every future email draft.

---

## Step 0 — Detect email connector

Probe in this order and use whichever fires first:

1. **Gmail MCP** — tools: `Gmail:search_threads` / `Gmail:get_thread`
2. **google-mcp** — tools: `google-mcp:gmail_search` / `google-mcp:gmail_read`
3. **Microsoft 365** — tools via m365 MCP connector

If more than one is connected, ask which account to use — work vs. personal voice may differ.
If none are connected, tell the user which connectors to install and stop.

If the user names a specific address, use it without asking.

---

## Step 1 — Pull 50 sent emails

Query constraints:
- Sent mail only (`in:sent` for Gmail family, `from:<address>` as backup)
- Exclude self-sends, calendar invites, automated mail, noreply addresses
- Skip messages under ~30 words on first pull; relax if clean set drops below 40
- Aim for a mix of lengths and recipient types: intros, replies, follow-ups, declines, status updates

Pull 75 raw, filter to a clean 50. For each kept message, strip the quoted reply chain
and signature block. Keep only the text the user actually composed.

Ask upfront: "Are any of your sent emails mostly Claude-drafted? If so, flag them — I'll
exclude those so AI patterns don't feed back into your voice."

---

## Step 2 — Automated analysis (8 dimensions)

Analyze the full corpus across these dimensions. For every pattern claimed, pull a real
example from the corpus. Classify each as VOICE, EMAIL_CONVENTION, or BORDERLINE.

1. **Sentence patterns** — length, variance, fragments, parenthetical asides, inline lists
2. **Opening patterns** — greeting form, first-sentence structure, what they never say
3. **Vocabulary fingerprint** — recurring words, hedges, intensifiers, filler words, slang
4. **Structural patterns** — answer-first vs context-first, bullet usage, paragraph length
5. **Tone markers** — formality shifts by recipient, warmth, directness, humor, how they decline
6. **Formatting habits** — punctuation quirks, emoji, bold/italic, link style, exclamation use
7. **Closing patterns** — sign-off phrases, name inclusion, P.S. usage
8. **LLM-ism check** — flag patterns that look AI-generated (triadic lists, em-dash
   clarifications, "I hope this finds you well", delve, leverage, etc.). Exclude those
   emails from the voice signal.

---

## Step 3 — Draft the voice profile

Produce a draft `email.md` (the voiceprint) using this structure. Order matters — rules listed first
carry more weight.

```markdown
# [Name]'s Email Voice

## 1. LLM-ism ban list (HARD)
[Never-use words and phrases. Start from the standard ban list below, add any found
in the corpus, add absences — words they never use that Claude reaches for by default.]

Standard ban list seed (always include):
- "I hope this email finds you well" / "I hope you're doing well"
- "I wanted to reach out" / "I am writing to"
- "Please don't hesitate to contact me" / "Should you have any questions"
- "As per my previous email" / "Thank you for your time"
- "Best regards" / "Sincerely" / "Kind regards" / "Warmly"
- "Moving forward" / "Going forward" / "Circle back" / "Touch base"
- "In terms of" / "It's worth noting that" / "At the end of the day"
- delve, leverage (metaphorical), navigate (metaphorical), endeavor, utilize
- seamlessly, holistically, robust, impactful, actionable
- Triadic lists for rhetorical effect
- Semicolons
- Em dashes (—) for elaboration or clarification
- Ellipses (…)

## 2. Anti-performative rules
[Prevent Claude from caricaturing the user: don't repeat a phrase just because it
appeared once, don't manufacture catchphrases, don't perform the user's casual tone.]

## 3. Core voice patterns
[Sentence structure, vocabulary, formatting. Prescriptive with right/wrong examples
from the actual corpus.]

## 4. Format-specific modes
[Opening pattern and length norm for each mode: intro reply, post-meeting follow-up,
check-in/nudge, casual/family, quick informational answer, logistics, networking/biz dev,
decline.]

## 5. Adaptation rules
[Pre-draft checklist: who is this to, what's the desired next action, reply vs new thread.
Two-pass review: LLM-ism pass then length pass. Default: write less.]
```

Show the draft in full. Do not save yet.

---

## Step 4 — Human review (Pass 2)

Ask the user to tag each section:
- **WRONG** — not my pattern, remove it
- **OVERSTATED** — occasional, not constant, soften it
- **MISSING** — I always do X and it's not here
- **NEEDS_NUANCE** — right in some contexts, wrong in others

For MISSING items, ask for a concrete example sentence.
Apply all feedback and show changed sections with labels noted.

---

## Step 5 — Calibration samples (Pass 3)

Generate 4–6 drafts covering the key modes. Use realistic scenarios, not generic ones.
At minimum: intro reply, post-meeting follow-up, nudge/check-in, decline.

Ask the user to tag each as GOOD / CLOSE / OFF.
For CLOSE or OFF, ask them to name the issue:
- TOO_FORMAL / TOO_CASUAL → update Section 4
- WRONG_WORD / LLM_ISM → update Section 1
- NOT_ME → update Section 3

Apply fixes. Generate another round if needed. Stop when two consecutive samples come
back GOOD.

---

## Step 6 — Save

**The output is a plain markdown file, not a skill.** Write the voiceprint content directly
to `~/.claude/voiceprints/email.md` using the Write tool. Do NOT package the output as a
Claude Code skill, Cowork skill, plugin, or any folder/wrapper structure. No frontmatter,
no `SKILL.md` name, no surrounding directory like `voice-name/`. The voiceprint is plain
markdown read by the existing `email-voice` skill — wrapping it in a skill shell breaks
that contract.

Save the final profile to `~/.claude/voiceprints/email.md`.

If `~/.claude/voiceprints/` does not exist, create it (`mkdir -p ~/.claude/voiceprints`).
If `email.md` already exists, ask the user before overwriting: "A voiceprint already exists.
Overwrite it, or save as `email_[date].md`?"

After saving, tell the user:

> "Saved to ~/.claude/voiceprints/email.md. The email-voice skill will apply it automatically
> on every email draft. To update it, edit the file directly or run /voice-extractor again."

---

## Accuracy notes

- Don't assert a pattern unless it appears in at least 3 of the 50 emails. One-off usage
  is not voice — flag it as low-confidence.
- Don't over-extract. If a pattern appears in 5 of 50 emails, the rule is "occasionally
  does X", not "signature move is X".
- Watch for AI contamination. If the corpus has Claude-drafted emails in it, those patterns
  will feed back in. Ask up front and exclude flagged emails.
- If the corpus has emails in more than one language, run the analysis per-language and
  produce per-language mode rules.
