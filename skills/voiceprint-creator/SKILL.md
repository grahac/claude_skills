---
name: voiceprint-creator
description: >
  Create a voiceprint capturing the user's personal writing voice for a specific
  medium (email, LinkedIn, or longform content) and write it as a single `.md` skill
  file in `~/Documents/voiceprints/`. Use when the user says "create my voiceprint",
  "build my voiceprint", "make me sound like me", "extract my voice", or any
  variation of capturing their writing style. Asks which medium up front; runs once
  per medium.
---

# Voiceprint Creator

Pulls the user's existing writing for a chosen medium, analyzes voice patterns, walks
through a human review pass, runs calibration samples, and writes the result as a
single `.md` skill file in `~/Documents/voiceprints/`. The user installs that file
once; from then on, Claude applies their voice to drafts in that medium.

Supported media:
- **email** — last 50 sent emails (any email MCP: Gmail, Outlook/Microsoft 365, Fastmail, ProtonMail, etc.). Supports MULTIPLE accounts in one run — useful when the user has personal + work mailboxes under separate MCPs and wants a single merged voiceprint.
- **linkedin** — posts from the user's LinkedIn data export
- **content** — longform pieces fetched from a URL the user provides

Output path: `~/Documents/voiceprints/<medium>.md` (e.g., `email.md`, `linkedin.md`,
`content.md`). Each voiceprint is an independent skill — duplicated LLM-ism ban list
across files is intentional, since skills don't reliably reference each other.

---

## Step 0 — Choose medium

Ask: "Which voiceprint do you want to create — email, LinkedIn, or content (longform)?"

Create `~/Documents/voiceprints/` if it doesn't exist.

If `~/Documents/voiceprints/<medium>.md` already exists, ask before overwriting. Offer
to save the new one as `<medium>_YYYY-MM-DD.md` so the previous version is preserved.

---

## Step 1 — Pull the corpus

Branch by medium.

### 1a — Email

**MCP detection (main agent).** Scan the connected tool list for ALL email MCPs —
don't assume Gmail, don't assume just one. Different accounts often live under
different MCPs (e.g., personal Gmail + work Outlook, or two Gmail MCPs namespaced
separately). Common provider signatures:

- **Gmail MCP** — `Gmail:search_threads`, `Gmail:get_thread` (also namespaced
  variants like `mcp__claude_ai_Gmail__*`, `mcp__gmail_work__*`)
- **google-mcp** — `google-mcp:gmail_search`, `google-mcp:gmail_read`
- **Microsoft 365 / Outlook** — tools containing `outlook`, `m365`, `microsoft365`,
  or `mail_*`
- **Fastmail, ProtonMail, Hey, generic IMAP MCPs** — tools matching `*mail*`,
  `*email*`, `*messages*`

List every distinct email MCP found and ask:

> "I found these email MCPs connected: [list]. Which one(s) should I pull from, and
> what's the authored email address for each? List all accounts you want included —
> the voiceprint will merge them into one."

If none are connected, tell the user to install one for their provider and stop.

**Why a subagent.** A 50-message search + per-message full-content fetch overflows
the main agent's context. Spawn a fresh-context subagent (`general-purpose`) to do
the pull, filter, and clean — the main agent only ever sees the cleaned corpus.

**Brief the subagent with:**
- A LIST of `(MCP tool names, user email address)` pairs to pull from. Example:
  `[(mcp__gmail_personal__search_threads + get_thread, user@example.com),
    (mcp__outlook_work__search + get_message, user@work.example.com)]`.
  For a single-account run, the list has one entry.
- Per-provider query syntax for "sent mail, recent" for each MCP (Gmail:
  `in:sent -in:draft -in:chats newer_than:18m` plus `from:<address>`; Outlook:
  filter on `Sent Items` folder with `from:<address>`)
- The filter-and-clean rules below
- The merge rules: combine all accounts into one corpus, tag each message with
  source account
- A demand to return prose findings only — no raw provider JSON

**Subagent rules — run the per-account loop, then merge:**

For EACH `(MCP, address)` pair in the input list:

1. Pull the user's authored sent messages using that MCP. If the provider exposes a
   messages-level API (Gmail `users.messages.list`, Outlook `/messages`), prefer it
   with a `from:<address>` filter to get user-authored messages directly. If only a
   threads API is available (e.g., the current Gmail MCP which exposes
   `search_threads` / `get_thread`), pull threads with `in:sent` then filter to
   messages where `sender` contains `<address>` — same end result.
2. Paginate until at least 40 user-authored messages from this account are collected
   (target ~50 each when there are multiple accounts; relax to fewer if the account
   is low-volume).
3. Fetch FULL_CONTENT (full message body) for each.
4. Clean each message body:
   a. **Strip the quoted reply chain**: lines starting with `>`, blocks starting
      with "On [date], X wrote:", Outlook-style "From: … Sent: … Subject: …"
      headers, and everything below them.
   b. **Strip the signature CONTACT BLOCK only** — multi-line trailing content
      containing `@`, phone-number digits, URLs, company/title lines, or legal
      disclaimers. Typically appears below a `--` divider or a blank line at the
      end.
   c. **PRESERVE minimalist single-line sign-offs.** These are voice signal — they
      tell the analyzer how the user closes. Rule: if the trailing line(s) after
      the blank line or `--` divider is a SINGLE line under ~25 chars and
      contains no `@`, no URL, no phone digits, KEEP it. Examples to preserve
      (generic patterns): `--<firstname>`, `--<Firstname>`, `-<initial>`,
      `<firstname>`, `thx, <initial>`, `xx`. Examples to strip (multi-line
      contact blocks): `<Full Name>\n+1-415-...`, `Best,\n<Name>\n<Title> @ <Co>\n<url>`.
5. Filter:
   - Drop messages < 30 words after stripping (relax to 20 if the clean set drops
     below 40 for this account).
   - Drop self-sends (sender equals all recipients).
   - Drop messages where the recipient list looks automated (`noreply@`,
     `notifications@`, `calendar-notification@`, `mailer-daemon@`).
   - Aim for diversity: intros, replies, follow-ups, declines, status updates.
6. Tag each kept message with `account: <address>`.

**After the per-account loop, merge across accounts:**

7. Combine into one corpus. Aim for ~50 total messages with reasonable balance
   across accounts (if account A has 80 candidates and account B has 10, sample
   account A down to ~35–40 so account B isn't drowned out — small-account
   patterns matter).
8. Deduplicate exact-duplicate messages (e.g., user self-CC'd between accounts).
   Keep one copy and note both accounts in the `account` field.
9. Stop when ~50 clean, merged messages are assembled.

**Subagent returns** a structured list — one entry per kept message:
- Subject
- Primary recipient (plus count if multi-recipient)
- Date
- **Account** (which user email address sent it — required when multi-account)
- Stripped body (the text the user actually composed, INCLUDING any minimalist
  single-line sign-off — those are voice signal)
- Word count

Plus a brief per-account summary header: how many messages came from each account
in the final 50, so the analyzer can spot account-specific patterns.

**After the subagent returns**, show the user the subject list and ask: "Are any of
these mostly Claude-drafted? Tell me which subjects to exclude so AI patterns don't
feed back." Drop those entries.

### 1b — LinkedIn

LinkedIn has no MCP for own-post access, so the user must export their data. Tell them:

> "I need your LinkedIn data export. Go to LinkedIn → Settings → Data privacy → Get a
> copy of your data → request the full archive (or just 'Posts'). It arrives by email
> in ~10 minutes. Once you unzip it, send me the path to the folder or the
> `Shares.csv` inside it."

Parse `Shares.csv` (or whichever posts file is present — LinkedIn has renamed it
across exports). Keep only the user's authored posts, not reshares of others' content.
Filter to posts ≥ ~20 words. Aim for the most recent 30–50 posts. Strip URLs and
`@mentions` before analysis.

If the export lacks posts entirely, ask the user to paste 20–30 of their posts directly.

### 1c — Content (longform)

Ask: "What's the URL? Give me your blog index, Substack archive, or any page that
lists your longform posts."

Use WebFetch to pull the page.
- If it's an index, extract post URLs and fetch each (aim for 10–20 pieces).
- If it's a single post, ask for more URLs until you have at least 10.

Strip site chrome, navigation, comments, and author bios — keep only the body text
the user wrote.

---

## Step 2 — Automated analysis (8 dimensions)

For every pattern claimed, pull a real example from the corpus. Classify each as
VOICE, MEDIUM_CONVENTION, or BORDERLINE.

1. **Sentence patterns** — length, variance, fragments, parenthetical asides, inline lists
2. **Opening patterns** — hooks, first-line structure, what they never say
3. **Vocabulary fingerprint** — recurring words, hedges, intensifiers, filler, slang
4. **Structural patterns** — answer-first vs context-first, bullet usage, paragraph length
5. **Tone markers** — formality shifts by recipient/topic, warmth, directness, humor, how they decline or disagree
6. **Formatting habits** — punctuation quirks, emoji, bold/italic, link style, exclamation use
7. **Closing patterns** — sign-offs / CTAs / outro shape, name inclusion, P.S. usage
8. **LLM-ism check** — flag patterns that look AI-generated (triadic lists, em-dash
   clarifications, "I hope this finds you well", delve, leverage). Exclude those
   pieces from the voice signal.

Medium-specific lenses to add on top:
- **email** — greeting/sign-off forms, decline patterns, reply vs. new thread cues
- **linkedin** — hook strength, line-break rhythm, hashtag usage, single-sentence paragraphs, CTA style
- **content** — header/section structure, transition phrases, narrative arc, intro/outro shape

**Multi-account email lens.** When the corpus came from more than one account, run
an extra pass: which patterns are UNIVERSAL (appear regardless of account — these
are real voice) vs. ACCOUNT-SPECIFIC (only show up under one account — these are
context, not voice). Common account-specific patterns: signature contact blocks,
CTA links (scheduling URLs may differ per account), formality level (work account
slightly more formal than personal). Tag account-specific findings inline in the
voiceprint draft instead of asserting them as universal rules.

---

## Step 3 — Draft the voiceprint

Produce a draft using the structure below. Order matters — rules listed first carry
more weight. Show the draft in full; don't write the file yet.

The output is RULES TEXT ONLY — no SKILL.md frontmatter, no application logic
header. The `voiceprints` runtime skill provides the application logic and reads
this file as raw rules.

```markdown
# [Name]'s <Medium> Voiceprint

## 1. LLM-ism ban list (HARD)

Standard ban list seed (always include):
- "I hope this email finds you well" / "I hope you're doing well"  [email]
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

[Add corpus-found additions, and absences — words the user never uses that Claude
reaches for by default.]

## 2. Anti-performative rules
[Don't repeat a phrase just because it appeared once. Don't manufacture catchphrases.
Don't caricature casual tone.]

## 3. Core voice patterns
[Sentence structure, vocabulary, formatting — prescriptive, with right/wrong examples
from the actual corpus.]

## 4. Format-specific modes
[Per-mode patterns. Email: intro reply / follow-up / nudge / decline / quick answer.
LinkedIn: hook post / story post / comment / DM. Content: essay / how-to / opinion piece.]

[Multi-account note (email only): if the corpus has more than one account, include
a "Per-account differences" sub-section listing what changes by account — typically
signature contact blocks and CTA links, sometimes formality. Don't try to merge
account-specific details into universal rules.]

## 5. Adaptation rules
[Pre-draft checklist: audience, desired next action. Two-pass review: LLM-ism pass,
then length pass. Default: write less.]
```

---

## Step 4 — Human review (Pass 2)

Ask the user to tag each section:
- **WRONG** — not my pattern, remove it
- **OVERSTATED** — occasional, not constant, soften it
- **MISSING** — I always do X and it's not here
- **NEEDS_NUANCE** — right in some contexts, wrong in others

For MISSING items, ask for a concrete example. Apply all feedback; show changed
sections with labels noted.

---

## Step 5 — Calibration samples (Pass 3)

Generate 4–6 drafts covering the key modes for the chosen medium. Use realistic
scenarios, not generic ones.

- **email** — intro reply, post-meeting follow-up, nudge/check-in, decline
- **linkedin** — short hook post, story post, comment reply, DM
- **content** — essay opening, how-to outline, opinion take, intro paragraph

Ask the user to tag each GOOD / CLOSE / OFF. For CLOSE or OFF, ask the issue:
- TOO_FORMAL / TOO_CASUAL → update Section 4
- WRONG_WORD / LLM_ISM → update Section 1
- NOT_ME → update Section 3

Apply fixes. Generate another round if needed. Stop when two consecutive samples come
back GOOD.

---

## Step 6 — Write the voiceprint file

Write the final voiceprint to `~/Documents/voiceprints/<medium>.md`. The file
contains ONLY the voice rules (Sections 1–5 plus the title header) — no
frontmatter, no application-instructions block. The runtime `voiceprints` skill
reads this file when the user drafts content and applies the rules.

Tell the user:

> "Done. Your voiceprint is at `~/Documents/voiceprints/<medium>.md`.
>
> The `voiceprints` skill picks it up automatically next time you draft <medium>.
> If you don't have `voiceprints` installed yet, install it from
> `github.com/grahac/claude_skills` (it's the runtime companion to this creator).
>
> To update, rerun /voiceprint-creator for this medium, or edit the file directly.
> To add another voice (email / LinkedIn / content), rerun and pick a different
> medium."

---

## Accuracy notes

- Don't assert a pattern unless it appears in at least 3 corpus pieces. One-off usage
  is not voice — flag it as low-confidence.
- Don't over-extract. If a pattern appears in 5 of 50 pieces, the rule is "occasionally
  does X", not "signature move is X".
- Watch for AI contamination. Ask up front and exclude flagged pieces.
- Multilingual corpus → run analysis per-language and produce per-language mode rules.
