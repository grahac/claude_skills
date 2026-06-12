---
name: voiceprint
description: >
  Create or refine a voiceprint capturing the user's personal writing voice for a
  specific medium (email, LinkedIn, or longform content), and package it as an
  installable Claude skill (one per medium: myvoiceprint-email, myvoiceprint-linkedin,
  or myvoiceprint-content). The user installs that
  skill once; from then on, Claude applies their voice when drafting in that medium.
  Use when the user says "create my voiceprint", "build my voiceprint", "refine my
  voiceprint", "update my voiceprint", "make me sound like me", "extract my voice",
  or any variation of capturing or adjusting their writing style. Asks create-or-refine
  and which medium up front.
---

# Voiceprint

Builds or refines a per-medium voiceprint and packages it as an installable Claude skill.

**Two modes:**
- **Create** — pull the user's real writing for a chosen medium, run 8-dimension analysis, a human review pass, calibration samples, and package the result as `myvoiceprint-<medium>`.
- **Refine** — surgically update an already-installed `myvoiceprint-<medium>` skill (add bans, fix tone, swap an exemplar) without re-running the full corpus pull.

The generated skill is written directly to `~/.claude/skills/myvoiceprint-<medium>/SKILL.md`, so it's installed and active the moment it lands — no copy step, no `~/Documents/` intermediate. It carries its own frontmatter and self-triggers when the user drafts content in that medium — no runtime intermediary required.

Supported media:
- **email** — last 40–50 sent emails across one or more email MCPs (Gmail, Outlook/M365, Fastmail, ProtonMail, etc.). Supports MULTIPLE accounts in one run — useful when the user has personal + work mailboxes under separate MCPs and wants a single merged voiceprint.
- **linkedin** — posts from the user's LinkedIn data export
- **content** — longform pieces fetched from URLs the user provides

---

## Step 0 — Determine intent

Don't ask cold. Infer as much as possible from the user's invocation and what's already installed, then ask only when there's genuine ambiguity.

### Step 0a — Resolve `$HOME` and probe installed voiceprints

**Resolve `$HOME` to an absolute path before any file op.** The `Read`, `Write`, and `Edit` tools do NOT expand `~`. Run a shell call once and cache `<HOME>`:

- macOS / Linux / WSL: `echo "$HOME"`
- Windows (PowerShell): `echo "$env:USERPROFILE"`

Then list existing voiceprints:

```bash
ls -d <HOME>/.claude/skills/myvoiceprint-*/ 2>/dev/null
```

Record which media already have an installed skill (any of `email`, `linkedin`, `content`).

`INSTALLED_PATH = <HOME>/.claude/skills/myvoiceprint-<medium>` — where the generated skill is written AND where refine reads from. Never pass a literal `~` to a file tool.

### Step 0b — Infer medium from the invocation

Look at the user's invocation arguments and any conversation context. Pick the first that matches:

- **content** ← any URL is supplied (http/https), or "blog", "essay", "substack", "longform", "article", "newsletter", "post" (when not "LinkedIn post")
- **email** ← "email", "sent mail", "Gmail", "Outlook", "inbox", "M365", "Microsoft 365", "Fastmail", "ProtonMail"
- **linkedin** ← "LinkedIn", "Shares.csv", "LinkedIn post", "LinkedIn export"
- **unknown** ← no signal

### Step 0c — Decide mode and route

Combine inferred medium with what's installed:

| Inferred medium | Skill exists? | What to do |
|---|---|---|
| Known (e.g., `content`) | No | **Create mode**, that medium. Proceed silently to Step 1 — don't ask. Tell the user: "Creating a new `myvoiceprint-<medium>`." |
| Known | Yes | Ask one question: "You already have a `myvoiceprint-<medium>` skill at `~/.claude/skills/myvoiceprint-<medium>/`. **Refine it**, **replace it from scratch**, or **build a different medium**?" Route by answer. |
| Unknown | One or more exist | Ask: "You have voiceprints for [list]. **Refine one of those** (which?), or **create a new one** (email / LinkedIn / content)?" Route by answer. |
| Unknown | None exist | Ask: "Which medium — email, LinkedIn, or content (longform)?" Then proceed in create mode. |

Mode-to-step mapping:
- **Create (medium)** → Step 1 (corpus pull for that medium)
- **Refine (medium)** → Refine flow, Step R1 (loads `<INSTALLED_PATH>/SKILL.md`)
- **Replace (medium)** → create mode; first back up the existing skill folder as `<INSTALLED_PATH>-YYYY-MM-DD/` so it's preserved, then proceed to Step 1

If a URL was supplied in the invocation, carry it forward to Step 1c — don't re-ask for it.

---

## Step 1 — Pull the corpus *(create mode only)*

Branch by medium.

### 1a — Email

**MCP detection (main agent).** Scan the connected tool list for ALL email MCPs — don't assume Gmail, don't assume just one. Different accounts often live under different MCPs (e.g., personal Gmail + work Outlook, or two Gmail MCPs namespaced separately). Common provider signatures:

- **Gmail MCP** — `Gmail:search_threads`, `Gmail:get_thread` (also namespaced variants like `mcp__claude_ai_Gmail__*`, `mcp__gmail_work__*`)
- **google-mcp** — `google-mcp:gmail_search`, `google-mcp:gmail_read`
- **Microsoft 365 / Outlook** — tools containing `outlook`, `m365`, `microsoft365`, or `mail_*`
- **Fastmail, ProtonMail, Hey, generic IMAP MCPs** — tools matching `*mail*`, `*email*`, `*messages*`

List every distinct email MCP found and ask:

> "I found these email MCPs connected: [list]. Which one(s) should I pull from, and what's the authored email address for each? List all accounts you want included — the voiceprint will merge them into one."

If none are connected, tell the user to install one for their provider and stop.

**Why a subagent.** A 50-message search + per-message full-content fetch overflows the main agent's context. Spawn a fresh-context subagent (`general-purpose`) to do the pull, filter, and clean — the main agent only ever sees the cleaned corpus.

**Brief the subagent with:**
- A LIST of `(MCP tool names, user email address)` pairs to pull from. Example:
  `[(mcp__gmail_personal__search_threads + get_thread, user@example.com),
    (mcp__outlook_work__search + get_message, user@work.example.com)]`.
  For a single-account run, the list has one entry.
- Per-provider query syntax for "sent mail, recent" for each MCP (Gmail: `in:sent -in:draft -in:chats newer_than:18m` plus `from:<address>`; Outlook: filter on `Sent Items` folder with `from:<address>`)
- The filter-and-clean rules below
- The merge rules: combine all accounts into one corpus, tag each message with source account
- A demand to return prose findings only — no raw provider JSON

**Subagent rules — run the per-account loop, then merge:**

For EACH `(MCP, address)` pair in the input list:

1. Pull the user's authored sent messages using that MCP. If the provider exposes a messages-level API (Gmail `users.messages.list`, Outlook `/messages`), prefer it with a `from:<address>` filter to get user-authored messages directly. If only a threads API is available (e.g., the current Gmail MCP which exposes `search_threads` / `get_thread`), pull threads with `in:sent` then filter to messages where `sender` contains `<address>` — same end result.
2. Paginate until at least 40 user-authored messages from this account are collected (target ~50 each when there are multiple accounts; relax to fewer if the account is low-volume).
3. Fetch FULL_CONTENT (full message body) for each.
4. Clean each message body:
   a. **Strip the quoted reply chain**: lines starting with `>`, blocks starting with "On [date], X wrote:", Outlook-style "From: … Sent: … Subject: …" headers, and everything below them.
   b. **Strip the signature CONTACT BLOCK only** — multi-line trailing content containing `@`, phone-number digits, URLs, company/title lines, or legal disclaimers. Typically appears below a `--` divider or a blank line at the end.
   c. **PRESERVE minimalist single-line sign-offs.** These are voice signal — they tell the analyzer how the user closes. Rule: if the trailing line(s) after the blank line or `--` divider is a SINGLE line under ~25 chars and contains no `@`, no URL, no phone digits, KEEP it. Examples to preserve (generic patterns): `--<firstname>`, `--<Firstname>`, `-<initial>`, `<firstname>`, `thx, <initial>`, `xx`. Examples to strip (multi-line contact blocks): `<Full Name>\n+1-415-...`, `Best,\n<Name>\n<Title> @ <Co>\n<url>`.
5. Filter:
   - Drop messages < 30 words after stripping (relax to 20 if the clean set drops below 40 for this account).
   - Drop self-sends (sender equals all recipients).
   - Drop messages where the recipient list looks automated (`noreply@`, `notifications@`, `calendar-notification@`, `mailer-daemon@`).
   - Aim for diversity: intros, replies, follow-ups, declines, status updates.
6. Tag each kept message with `account: <address>`.

**After the per-account loop, merge across accounts:**

7. Combine into one corpus. Aim for ~50 total messages with reasonable balance across accounts (if account A has 80 candidates and account B has 10, sample account A down to ~35–40 so account B isn't drowned out — small-account patterns matter).
8. Deduplicate exact-duplicate messages (e.g., user self-CC'd between accounts). Keep one copy and note both accounts in the `account` field.
9. Stop when ~50 clean, merged messages are assembled.

**Subagent returns** a structured list — one entry per kept message:
- Subject
- Primary recipient (plus count if multi-recipient)
- Date
- **Account** (which user email address sent it — required when multi-account)
- Stripped body (the text the user actually composed, INCLUDING any minimalist single-line sign-off — those are voice signal)
- Word count

Plus a brief per-account summary header: how many messages came from each account in the final 50, so the analyzer can spot account-specific patterns.

**After the subagent returns**, show the user the subject list and ask: "Are any of these mostly Claude-drafted? Tell me which subjects to exclude so AI patterns don't feed back." Drop those entries.

### 1b — LinkedIn

LinkedIn has no MCP for own-post access, so the user must export their data. Tell them:

> "I need your LinkedIn data export. Go to LinkedIn → Settings → Data privacy → Get a copy of your data → request the full archive (or just 'Posts'). It arrives by email in ~10 minutes. Once you unzip it, send me the path to the folder or the `Shares.csv` inside it."

Parse `Shares.csv` (or whichever posts file is present — LinkedIn has renamed it across exports). Keep only the user's authored posts, not reshares of others' content. Filter to posts ≥ ~20 words. Aim for the most recent 30–50 posts. Strip URLs and `@mentions` before analysis.

If the export lacks posts entirely, ask the user to paste 20–30 of their posts directly.

### 1c — Content (longform)

Ask: "What's the URL? Give me your blog index, Substack archive, or any page that lists your longform posts."

Use WebFetch to pull the page.
- If it's an index, extract post URLs and fetch each (aim for 10–20 pieces).
- If it's a single post, ask for more URLs until you have at least 10.

Strip site chrome, navigation, comments, and author bios — keep only the body text the user wrote.

---

## Step 2 — Automated analysis (8 dimensions) *(create mode only)*

For every pattern claimed, pull a real example from the corpus. Classify each as VOICE, MEDIUM_CONVENTION, or BORDERLINE.

1. **Sentence patterns** — length, variance, fragments, parenthetical asides, inline lists
2. **Opening patterns** — hooks, first-line structure, what they never say
3. **Vocabulary fingerprint** — recurring words, hedges, intensifiers, filler, slang
4. **Structural patterns** — answer-first vs context-first, bullet usage, paragraph length
5. **Tone markers** — formality shifts by recipient/topic, warmth, directness, humor, how they decline or disagree
6. **Formatting habits** — punctuation quirks, emoji, bold/italic, link style, exclamation use
7. **Closing patterns** — sign-offs / CTAs / outro shape, name inclusion, P.S. usage
8. **LLM-ism check** — flag patterns that look AI-generated (triadic lists, em-dash clarifications, "I hope this finds you well", delve, leverage). Exclude those pieces from the voice signal.
9. **Sentence metrics** — calculate from the full corpus:
   - Average sentence length (words per sentence across all pieces)
   - Sentence length variance (standard deviation of sentence lengths)
   - Burstiness score: variance ÷ mean (>1.0 = highly varied rhythm; <0.5 = uniform)
   - Typical range: 10th–90th percentile sentence length
   - Average paragraph length (sentences per paragraph)
   These are quantitative targets for Claude to hit when drafting, not qualitative descriptions.

**Seed-ban audit.** Check every item on the Section 1 seed ban list (see Step 3) against the corpus. Any item appearing in 3+ pieces is the user's real voice, not an LLM-ism — exclude it from the generated ban list and, if distinctive, record it as a positive pattern in Section 3. The seed list is a default, not a mandate; never ban something the user demonstrably does.

**Exemplar selection.** After analysis, choose 12–15 corpus pieces to embed verbatim in the output file as voice exemplars (scale down only if the corpus is small, e.g. a 10-piece content corpus). Tag every exemplar with scenario and register so the generated skill can pick the closest matches at draft time. Categorize them:
- **Short-form** (5–6 samples, under ~75 words each): natural rhythm across different scenarios and registers
- **Medium-form** (4–5 samples): explanation or narrative showing depth
- **Opinionated** (2–3 samples): the pieces with the strongest, most distinct voice

If a piece is over 100 words, extract the most distinctive passage — enough context to stand alone. Use raw text verbatim; do not clean up grammar or phrasing. Authenticity matters more than polish.

Medium-specific lenses to add on top:
- **email** — greeting/sign-off forms, decline patterns, reply vs. new thread cues
- **linkedin** — hook strength, line-break rhythm, hashtag usage, single-sentence paragraphs, CTA style
- **content** — header/section structure, transition phrases, narrative arc, intro/outro shape

**Multi-account email lens.** When the corpus came from more than one account, run an extra pass: which patterns are UNIVERSAL (appear regardless of account — these are real voice) vs. ACCOUNT-SPECIFIC (only show up under one account — these are context, not voice). Common account-specific patterns: signature contact blocks, CTA links (scheduling URLs may differ per account), formality level (work account slightly more formal than personal). Tag account-specific findings inline in the voiceprint draft instead of asserting them as universal rules.

---

## Step 3 — Draft the voiceprint content *(create mode only)*

Produce a draft using the structure below. Order matters — rules listed first carry more weight. Show the draft in full; don't package yet.

This is the BODY of the generated `myvoiceprint-<medium>` skill (everything after the frontmatter). Step 6 prepends the frontmatter and writes the full file.

```markdown
# [Name]'s <Medium> Voiceprint

## 1. LLM-ism ban list (HARD)

[Seed list below — include each item ONLY if it passed the Step 2 seed-ban audit
(i.e., the corpus does NOT use it). Items the user actually uses in 3+ pieces are
voice, not LLM-isms: leave them off this list.]

Standard ban list seed:
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

Enforcement: a ban line alone does not stick — character-level items (em dash,
semicolon, ellipsis) leak back in. Every draft gets a mandatory literal-text scan
against this list before delivery (see the drafting instructions at the top of this
skill). When a scan hit forces a rewrite, replace an em dash with a period, comma,
or parentheses — whichever the Section 6 exemplars support.

## 2. Anti-performative rules
[Don't repeat a phrase just because it appeared once. Don't manufacture catchphrases.
Don't caricature casual tone.]

## 3. Core voice patterns

[Sentence structure, vocabulary, formatting — prescriptive, with right/wrong examples
from the actual corpus.]

### Sentence metrics
- Average sentence length: X words
- Burstiness score: X.X (>1.0 = varied rhythm; <0.5 = uniform)
- Typical range: X–X words per sentence
- Average paragraph: X sentences

[Use these as calibration targets when drafting. If a draft consistently falls outside
the typical range, revise before delivering.]

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

## 6. Voice exemplars (verbatim)

These are actual pieces from the corpus. They ARE the voice. Before drafting, find
the 2–3 exemplars whose scenario and register tags are closest to the current task
and pattern-match against those specifically — not against the set as a whole.

### Short-form
[5–6 verbatim samples under ~75 words each. Tag each with scenario and register in
parens: (decline, casual, peer), (intro reply, formal, new contact), (nudge, brief),
(LinkedIn comment), etc.]

### Medium-form
[4–5 verbatim samples showing explanation or narrative depth. Tag scenario and register.]

### Opinionated
[2–3 verbatim samples with the strongest, most distinct voice. Tag scenario and register.]

## 7. Sample transformations

The gap between generic AI writing and this voice. Use these as a final calibration
check before delivering any draft — if your draft reads more like "Generic" than
"Your voice", revise it.

### 1. Generic opener → your voice
**Generic:** "[A typical AI opener for this medium — hollow, formal, hedged]"
**Your voice:** "[The same opening rewritten using corpus patterns]"

### 2. Formal explanation → your voice
**Generic:** "[A formal, structured AI explanation with hedges and connector words]"
**Your voice:** "[Rewritten — same content, actual voice]"

### 3. Short-form / social → your voice
**Generic:** "[A generic AI social post or short reply — polished, lifeless]"
**Your voice:** "[Rewritten — rhythm, vocabulary, and conviction from the corpus]"
```

---

## Step 4 — Human review (Pass 2) *(create mode only)*

Ask the user to tag each section:
- **WRONG** — not my pattern, remove it
- **OVERSTATED** — occasional, not constant, soften it
- **MISSING** — I always do X and it's not here
- **NEEDS_NUANCE** — right in some contexts, wrong in others

For MISSING items, ask for a concrete example. Apply all feedback; show changed sections with labels noted.

---

## Step 5 — Calibration samples (Pass 3) *(create mode only)*

Generate 4–6 drafts covering the key modes for the chosen medium. Use realistic scenarios, not generic ones.

- **email** — intro reply, post-meeting follow-up, nudge/check-in, decline
- **linkedin** — short hook post, story post, comment reply, DM
- **content** — essay opening, how-to outline, opinion take, intro paragraph

Ask the user to tag each GOOD / CLOSE / OFF. For CLOSE or OFF, ask the issue:
- TOO_FORMAL / TOO_CASUAL → update Section 4
- WRONG_WORD / LLM_ISM → update Section 1
- NOT_ME → update Section 3

Apply fixes. Generate another round if needed. Stop when two consecutive samples come back GOOD.

---

## Step 6 — Package as the `myvoiceprint-<medium>` skill

Write the generated skill directly to its install location: `<INSTALLED_PATH>/SKILL.md`. The skill is active the moment the file lands — no copy step, no portable artifact intermediate. If the user later wants to share the skill with claude.ai or Cowork, they can read it from `<INSTALLED_PATH>` and upload/copy from there.

### 6a — Build the personalized SKILL.md content

Assemble the full SKILL.md text the generated skill needs. Structure (example shown for `content`; substitute the actual medium and the user's name):

**CRITICAL — no angle brackets anywhere in the file.** The skill validator rejects any `description:` containing `<...>` (it reads as an XML tag). Substitute every placeholder with concrete text before writing: real medium (`email`/`linkedin`/`content`), the user's actual name, the real list of intents. Never leave a literal `<medium>`, `<Medium>`, or `<...>` token in the output — not in the frontmatter, not in the body.

```markdown
---
name: myvoiceprint-content
description: >
  Apply [Name]'s personal longform writing voice when drafting any blog post, essay,
  op-ed, or substantial written piece on [Name]'s behalf. Enforces [Name]'s LLM-ism
  ban list, anti-performative rules, mode-specific patterns, and voice exemplars. Use
  whenever drafting longform content as [Name].
---

# [Name]'s Content Voiceprint

When asked to draft any longform content on [Name]'s behalf:

1. Apply every rule in the voiceprint below.
2. Mode-specific rules win over general rules.
3. Before writing, find the 2–3 exemplars in Section 6 whose scenario and register tags are closest to the current task. Pattern-match the draft's opener, rhythm, and closer against those specifically — they are the ground truth.
4. Use Section 3 sentence metrics as quantitative targets. After drafting, scan rhythm; revise if the draft consistently falls outside the typical range.
5. Compare your draft against Section 7 "Your voice" examples — if it reads more like the "Generic" column, revise.
6. MANDATORY final pass before delivering: scan the literal draft text for every Section 1 ban entry, including character-level items (em dash, semicolon, ellipsis). If any appear, rewrite that sentence — for an em dash, use a period, comma, or parentheses instead. Never deliver a draft that fails this scan.
7. Do not mention that you are applying a voiceprint. Just produce the draft.

---

[Sections 1–7 from Step 3, after Step 4 review and Step 5 calibration. Exactly the content agreed with the user.]
```

**Medium-specific description templates** (use these for the `description:` field):

- **email**: "Apply [Name]'s personal email writing voice when drafting any email, reply, intro, follow-up, decline, scheduling message, or short outbound on [Name]'s behalf. Use whenever drafting email-style content as [Name]."
- **linkedin**: "Apply [Name]'s personal LinkedIn voice when drafting any LinkedIn post, comment, or DM on [Name]'s behalf. Use whenever drafting LinkedIn content as [Name]."
- **content**: "Apply [Name]'s personal longform writing voice when drafting any blog post, essay, op-ed, longform article, or substantial written piece on [Name]'s behalf. Use whenever drafting longform content as [Name]."

### 6b — Install the skill (environment-aware)

How the skill gets installed depends on the runtime. Detect which environment you're in and use the matching path. Do NOT fall back to handing the user a raw Terminal `cp` from a temp session path — that's the worst-case UX and is never correct.

**Determine the environment.** Claude Code CLI can read/write the user's real home directory; Claude Desktop and Cowork run the agent sandboxed and cannot reach `<HOME>/.claude/skills/`. Probe once:

```bash
test -d "<HOME>/.claude/skills" && test -w "<HOME>/.claude/skills" && echo "CLI_WRITABLE" || echo "SANDBOXED"
```

**Path A — Claude Code CLI (`CLI_WRITABLE`):** write directly to the install path.

```bash
mkdir -p "<INSTALLED_PATH>"
```

Use the Write tool to write the SKILL.md content (from 6a) to `<INSTALLED_PATH>/SKILL.md`. Installed and active. Then confirm:

> "Done. Your voiceprint is installed at `~/.claude/skills/myvoiceprint-<medium>/SKILL.md` and auto-activates next time you draft that medium. Run `/reload-plugins` to use it in this session, or it's live in your next one."

**Path B — Claude Desktop / Cowork (`SANDBOXED`):** the agent CANNOT write to the user's `~/.claude/skills/`. Instead, hand the finished skill to the platform's native **"add as a skill"** flow:

1. Write the SKILL.md content (from 6a) to the session workspace/outputs so it exists as a real file (e.g. `myvoiceprint-<medium>/SKILL.md` in the outputs dir).
2. Present the complete SKILL.md content to the user.
3. Tell the user — and offer to do it — in these words:

   > "Your `myvoiceprint-<medium>` skill is ready. Just say **'add this as a skill'** and I'll register it — then it auto-activates whenever you draft <medium> on your behalf. No file copying needed."

4. When the user confirms, use the environment's add-as-a-skill capability to register it. Do NOT instruct the user to run shell commands or copy files into a path the sandbox can't see.

### 6c — Closing note (both paths)

Wrap up:

> "To refine it later (add banned phrases, fix a tone issue, swap an exemplar), just say 'refine my voiceprint'. To build voiceprints for other media (email / LinkedIn / content), rerun and pick a different medium."

---

## Refine flow (Steps R1–R6) *(refine mode only)*

Used when Step 0c routes to Refine. Skips corpus pull, analysis, and calibration — operates on an already-installed `myvoiceprint-<medium>` skill.

### Step R1 — Load the installed skill

**Claude Code CLI:** read `<INSTALLED_PATH>/SKILL.md` (i.e., `<HOME>/.claude/skills/myvoiceprint-<medium>/SKILL.md`). If the file doesn't exist, tell the user:
> "No `myvoiceprint-<medium>` skill installed at `~/.claude/skills/myvoiceprint-<medium>/`. Run `/voiceprint` in create mode first."
Then stop. If the file is under ~20 lines, warn it looks like a stub and offer create mode instead.

**Claude Desktop / Cowork (sandboxed):** you can't read `<HOME>/.claude/skills/`. If the `myvoiceprint-<medium>` skill is already loaded in this session, work from its loaded content. If it isn't loaded (or you can't access its text), ask the user:
> "I can't read installed skills directly in this environment. Paste your current `myvoiceprint-<medium>` SKILL.md (or say 'create' to rebuild it from scratch), and I'll apply the refine edits, then re-register it with 'add as a skill'."

After editing in sandboxed mode, re-install via the Path B "add as a skill" flow from Step 6b rather than writing to the filesystem.

### Step R2 — Ask what to refine

Do NOT summarize the voiceprint back. The user knows it — they're here because something specific needs fixing. Ask:

> "What would you like to refine?
> - Add phrases that felt wrong in practice
> - Remove a pattern that's overclaiming (I don't actually do that)
> - Adjust formality level
> - Add or replace a voice exemplar with a better one
> - Fix a sample transformation that felt off
> - Something else — describe it"

Wait for their free-text response.

### Step R3 — Get specifics

Based on what they said, ask one targeted follow-up:

**Adding forbidden patterns:** "What phrases or structures felt wrong? Paste examples from actual drafts if you have them." Look at Section 1's ban list — if the pattern logically extends an existing category, say so: "That sounds like a variant of [X] already in your ban list — want me to add just this phrase, or expand the category?"

**Removing a pattern:** Quote the specific text from the file and confirm: "You want this removed: [quote]. Is that right, or is the issue more nuanced?"

**Adjusting formality:** "How would you describe the shift? More casual / less hedged / more direct? If you have an example of the tone you want, paste it."

**Adding/replacing an exemplar:** Ask them to paste the sample and give context (email reply, LinkedIn post, etc.). If replacing, ask which existing exemplar it should replace or if it's an addition.

**Fixing a sample transformation:** Ask which transformation (1, 2, or 3) and what felt wrong — generic column, "your voice" column, or both.

**Something else:** Ask them to describe the change in concrete terms before proceeding.

### Step R4 — Confirm before editing

Summarize what you're about to change in plain language:

> "Here's what I'll do:
> 1. [specific change]
> 2. [specific change if multiple]
>
> Good?"

Wait for confirmation. If they want to adjust, loop back to R3.

### Step R5 — Apply edits

**Claude Code CLI:** edit `<INSTALLED_PATH>/SKILL.md` in place. **Claude Desktop / Cowork:** edit the loaded/pasted content in memory, then re-register via the Path B "add as a skill" flow (Step 6b) — never write to `<HOME>/.claude/skills/` directly. Either way, apply these rules:

1. **Add to sections, don't replace them** unless the user explicitly asked to remove something.
2. **Match the formatting** — bullet style, heading level, and wording pattern already in the file.
3. **Keep sections consistent.** If you update sentence metrics in Section 3, check that exemplars in Section 6 and transformations in Section 7 still reflect the same voice. If they don't, flag it.
4. **For new exemplars:** add to the appropriate category in Section 6 (short-form, medium-form, or opinionated). If the category is full (3 already), offer to replace the weakest one.
5. **For new forbidden patterns:** add to Section 1's ban list. If the pattern is medium-specific, label it `[email]` / `[linkedin]` / `[content]`.
6. **For formality adjustments:** update Section 4 (Format-specific modes) and the tone markers in Section 3. Also update Section 7's "Generic → your voice" transformations if the baseline shifted.
7. **Do not touch the frontmatter `name:` or `description:` fields** — those drive skill activation.

### Step R6 — Validate and wrap up

Generate a short test draft (3–5 sentences) that specifically targets the change.

- Forbidden pattern added → write about a topic that would naturally tempt that pattern; verify it doesn't appear
- Formality adjusted → write in the new register; explicitly target the shift
- Exemplar added → write in the same context as the new exemplar
- Transformation fixed → show the new "Your voice" version

Present it:
> "Here's a test draft targeting the change:
>
> [draft]
>
> Does this feel right? If something's still off, tell me and I'll adjust."

If they flag an issue, loop back to R3 with the new feedback. Stop when they confirm.

Final wrap-up:
> "Done. `~/.claude/skills/myvoiceprint-<medium>/SKILL.md` has been updated. The change applies immediately — the skill reads the file fresh on every draft.
>
> Rerun `/voiceprint` (refine mode) any time something else feels off."

---

## Accuracy notes (create mode)

- Don't assert a pattern unless it appears in at least 3 corpus pieces. One-off usage is not voice — flag it as low-confidence.
- Don't over-extract. If a pattern appears in 5 of 50 pieces, the rule is "occasionally does X", not "signature move is X".
- Watch for AI contamination. Ask up front and exclude flagged pieces.
- Multilingual corpus → run analysis per-language and produce per-language mode rules.

## Refine notes

- **File exists but looks like a stub** (under ~20 lines): warn the user there's not much to refine; offer create mode instead.
- **Multiple changes in one session:** handle sequentially — loop R2–R6 per change, then one final wrap-up.
- **Contradictions after editing:** if a new rule contradicts an existing one (e.g., a newly-banned phrase appears in a voice exemplar), flag it before writing and ask which should win.
