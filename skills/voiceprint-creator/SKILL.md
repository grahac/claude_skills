---
name: voiceprint-creator
description: >
  Extract the user's personal email writing voice from their last 50 sent emails and
  package it as an installable Claude skill called "myvoiceprint". Use when the user says
  "extract my voice", "build my voiceprint", "analyze my email tone", "make me sound like
  me", "create my voiceprint skill", or any variation of capturing their writing style as
  a reusable skill. Runs once; the output is a single .skill file the user installs on
  claude.ai, Claude Code, or Cowork.
---

# Voiceprint Creator

Pulls the user's last 50 sent emails, analyzes them for genuine voice patterns, walks
through a human review pass, runs calibration samples, and packages the result as an
installable skill called `myvoiceprint`. The user installs that skill once; from then on,
Claude applies their voice to every email draft.

The output is a `.skill` file — a packaged, single-file skill that works on every Claude
environment (claude.ai, Claude Code, Cowork).

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

## Step 3 — Draft the voiceprint content

Produce a draft voiceprint using this structure. Order matters — rules listed first
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

Show the draft in full. Do not package yet.

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

## Step 6 — Package as the `myvoiceprint` skill

The output is an installable `.skill` file the user can drop into claude.ai, Claude Code,
or Cowork. Use the `skill-creator` skill's scripts when available; fall back to writing a
raw `SKILL.md` file when not.

### 6a — Build the personalized SKILL.md content

Assemble the full SKILL.md text the `myvoiceprint` skill needs. Structure:

```markdown
---
name: myvoiceprint
description: >
  Apply [Name]'s personal email writing voice to every email or short-form message draft.
  Use whenever drafting any email, reply, follow-up, intro response, check-in, decline,
  or short-form outbound message on [Name]'s behalf. Enforces [Name]'s LLM-ism ban list,
  anti-performative rules, and mode-specific patterns.
---

# [Name]'s Voiceprint

When asked to draft any email or short-form written content on [Name]'s behalf:

1. Apply every rule in the voiceprint below.
2. Do not mention that you are applying a voiceprint. Just produce the draft.
3. If a mode-specific rule conflicts with a general rule, the mode-specific rule wins.

---

## Voiceprint

[Full voiceprint content from Step 3, after Step 4 review and Step 5 calibration.
Sections 1 through 5, exactly as agreed with the user.]
```

### 6b — Try skill-creator (preferred path)

Check whether `skill-creator` is installed. Common locations:
- `~/.claude/skills/skill-creator/`
- `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/`

If present, use its scripts:

```bash
# Scaffold the skill folder
<skill-creator-path>/scripts/init_skill.py myvoiceprint --path ~/Documents/

# Overwrite the generated SKILL.md with the personalized content from 6a
# (use the Write tool)

# Package the skill folder into a distributable .skill file
<skill-creator-path>/scripts/package_skill.py ~/Documents/myvoiceprint
```

The result is `~/Documents/myvoiceprint.skill`.

### 6c — Fall back to raw SKILL.md (if skill-creator missing)

If skill-creator is not installed, do this instead:

```bash
mkdir -p ~/Documents/myvoiceprint
```

Write the personalized SKILL.md content (from 6a) to `~/Documents/myvoiceprint/SKILL.md`.
No `.skill` package. Tell the user they can install skill-creator later to package it,
or manually upload the SKILL.md depending on their environment.

### 6d — Tell the user

Once the output is written, give the user concrete install instructions:

> "Done. Your voiceprint is packaged at:
>
> - `~/Documents/myvoiceprint.skill` (if skill-creator was available)
> - or `~/Documents/myvoiceprint/SKILL.md` (raw file fallback)
>
> Install:
> - **claude.ai**: upload the .skill file (or SKILL.md content) via skill settings
> - **Claude Code**: drop the folder into `~/.claude/skills/myvoiceprint/`
> - **Cowork**: drop the folder into your Cowork skills directory
>
> To update your voice later, rerun /voiceprint-creator or edit the SKILL.md directly."

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
