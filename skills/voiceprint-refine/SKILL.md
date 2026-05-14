---
name: voiceprint-refine
description: >
  Surgically refine an existing voiceprint file — add or remove forbidden patterns,
  adjust tone, update voice exemplars, or fix anything that feels off after using
  the voiceprint in practice. Reads the existing file, asks what to change, applies
  edits, validates with a test draft. Use when the user says "refine my voiceprint",
  "update my voiceprint", "this doesn't sound like me", or "add X to my voiceprint".
---

# Voiceprint Refine

Iteratively improve an existing voiceprint without re-running the full creator.
Users discover gaps in practice — this workflow lets them fix them immediately.

---

## Step 0 — Identify medium and load file

Ask: "Which voiceprint do you want to refine — email, LinkedIn, or content?"

Read `~/Documents/voiceprints/<medium>.md`.

If the file doesn't exist, tell the user:
> "No voiceprint for `<medium>` yet. Run `/voiceprint-creator` to build one first."
Then stop.

If the file is present but has no `<!-- voiceprint-version: ... -->` comment at the
top, note it silently — it was built before versioning was added. Continue normally;
don't block the user.

---

## Step 1 — Ask what to refine

Do NOT summarize the voiceprint back to the user. They know it — they're here because
something specific needs fixing. Go straight to:

"What would you like to refine? Examples:
- Add phrases that felt wrong in practice
- Remove a pattern that's overclaiming (I don't actually do that)
- Adjust formality level
- Add or replace a voice exemplar with a better one
- Fix a sample transformation that felt off
- Something else — describe it"

Wait for their free-text response.

---

## Step 2 — Get specifics

Based on what they said, ask one targeted follow-up to get enough detail to act.

**Adding forbidden patterns:**
Ask: "What phrases or structures felt wrong? Paste examples from actual drafts if
you have them."

Look at the ban list in Section 1 of the voiceprint — if the pattern logically
extends an existing category, say so: "That sounds like a variant of [X] already
in your ban list — want me to add just this phrase, or expand the category?"

**Removing a pattern:**
Quote the specific text from the file and confirm: "You want this removed: [quote].
Is that right, or is the issue more nuanced?"

**Adjusting formality:**
Ask: "How would you describe the shift? More casual / less hedged / more direct?
If you have an example of the tone you want, paste it."

**Adding/replacing an exemplar:**
Ask them to paste the sample and give context (email reply, LinkedIn post, etc.).
If replacing, ask which existing exemplar it should replace or if it's an addition.

**Fixing a sample transformation:**
Ask which transformation (1, 2, or 3) and what felt wrong — generic column,
"your voice" column, or both.

**Something else:**
Ask them to describe the change in concrete terms before proceeding.

---

## Step 3 — Confirm before editing

Summarize what you're about to change in plain language:

> "Here's what I'll do:
> 1. [specific change]
> 2. [specific change if multiple]
>
> Good?"

Wait for confirmation. If they want to adjust, loop back to Step 2.

---

## Step 4 — Apply edits

Make surgical edits to `~/Documents/voiceprints/<medium>.md`. Edit rules:

1. **Add to sections, don't replace them** unless the user explicitly asked to remove something.
2. **Match the formatting** — bullet style, heading level, and wording pattern already in the file.
3. **Keep sections consistent.** If you update sentence metrics in Section 3, check
   that exemplars in Section 6 and transformations in Section 7 still reflect the
   same voice. If they don't, flag it.
4. **For new exemplars:** add to the appropriate category in Section 6 (short-form,
   medium-form, or opinionated). If the category is full (3 already), offer to
   replace the weakest one.
5. **For new forbidden patterns:** add to Section 1's ban list. If the pattern is
   medium-specific (e.g., only wrong in email), label it `[email]`.
6. **For formality adjustments:** update Section 4 (Format-specific modes) and the
   tone markers in Section 3. Also update Section 7's "Generic → your voice"
   transformations if the baseline shifted.
7. **Don't update the version comment** — leave it at whatever version the file was
   created with.

---

## Step 5 — Validate

Generate a short test draft (3–5 sentences) that specifically targets the change made.

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

If they flag an issue, loop back to Step 2 with the new feedback. Stop when they
confirm it's right or say they're satisfied.

---

## Step 6 — Wrap up

Tell the user:
> "Done. `~/Documents/voiceprints/<medium>.md` has been updated.
>
> The changes apply immediately — the `voiceprint` skill reads the file fresh
> on every draft.
>
> Run `/voiceprint-refine` again any time something else feels off."

---

## Error handling

- **File exists but looks like a stub** (under ~20 lines): warn the user that there's
  not much to refine yet, and offer to rerun `/voiceprint-creator` instead.
- **User wants multiple changes in one session:** handle them sequentially — loop
  through Steps 1–5 for each change, then do one final wrap-up.
- **Contradictions after editing:** if a new rule contradicts an existing one (e.g.,
  a newly-banned phrase appears in a voice exemplar), flag it before writing and ask
  which should win.
