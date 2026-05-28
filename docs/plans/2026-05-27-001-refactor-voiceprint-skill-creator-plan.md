---
title: "refactor: Restore voiceprint plugin to skill-creator output format"
status: active
created: 2026-05-27
plan_type: refactor
target_repo: claude_skills
---

# refactor: Restore voiceprint plugin to skill-creator output format

## Summary

Restore the voiceprint plugin to the pre-`a615b5a` "special skill creator" pattern from commit `bf604e8`: `voiceprint-creator` packages an installable per-medium Claude skill (`myvoiceprint-<medium>`) rather than writing a raw rules file consumed by a runtime skill. Delete the runtime `voiceprint` skill and the separate `voiceprint-refine` skill, fold the refine flow into `voiceprint-creator` as a Step 0 mode branch, collapse the two commands into a single `/voiceprint` entry, bump the plugin to `v2.0.0`. Intentional breaking change — existing v1.x rules files at `~/Documents/voiceprints/<medium>.md` are not migrated.

## Problem Frame

The current v1.1.0 plugin (commit `a615b5a` onward) splits voice handling into three skills:

- `voiceprint-creator` writes raw rules to `~/Documents/voiceprints/<medium>.md`
- `voiceprint` runtime skill detects medium, reads the rules file, applies them
- `voiceprint-refine` surgically edits the rules file

The runtime indirection is fragile: it depends on the `voiceprint` skill firing (which requires it to be installed and matched by description) AND on the rules file being readable from `~/Documents/voiceprints/`. Cowork users in particular need the voice to apply automatically when drafting, and a description-matched runtime skill is less reliable than a self-applying skill whose own frontmatter triggers on the drafting intent.

The old format (commit `bf604e8`, May 6 2026) had a cleaner contract: the creator emitted a proper installable skill with its own frontmatter. The skill self-triggered on email-drafting intent — no runtime wrapper needed. This plan restores that pattern and generalizes from email-only to three mediums (email / LinkedIn / longform content).

## Requirements

- R1. `voiceprint-creator` outputs a per-medium installable skill named `myvoiceprint-<medium>` (one of `email`, `linkedin`, `content`).
- R2. The generated skill has its own YAML frontmatter (`name:`, `description:`) such that it auto-triggers when the user drafts content in that medium — no runtime intermediary.
- R3. The creator uses `skill-creator`'s `init_skill.py` + `package_skill.py` scripts when available, producing `~/Documents/myvoiceprint-<medium>.skill`; falls back to writing a raw `~/Documents/myvoiceprint-<medium>/SKILL.md` directory when skill-creator isn't installed.
- R4. The creator has a Step 0 mode branch: "create new" (full corpus → analyze → review → calibrate → package flow) or "refine existing" (surgical edit of an installed `~/.claude/skills/myvoiceprint-<medium>/SKILL.md` using the tagged WRONG / OVERSTATED / MISSING / NEEDS_NUANCE pass).
- R5. The runtime `voiceprint` skill is deleted entirely.
- R6. The standalone `voiceprint-refine` skill is deleted (folded into creator's refine mode).
- R7. The plugin exposes a single `/voiceprint` command (no `/voiceprint create` / `/voiceprint refine` split).
- R8. Plugin version bumps to `2.0.0` with description reflecting the skill-output model.
- R9. README documents the new install flow: run `/voiceprint`, install the generated skill folder to `~/.claude/skills/myvoiceprint-<medium>/`.
- R10. Existing 3-medium corpus-pull logic (subagent-based email scrape, LinkedIn `Shares.csv` parsing, longform URL fetch) is preserved verbatim — only Step 6 (packaging) changes and the Step 0 mode branch is added.
- R11. No automatic migration of v1.x rules files. Users with `~/Documents/voiceprints/<medium>.md` rerun the creator to get a proper skill.

## Scope Boundaries

**In scope:** the seven file operations listed under Implementation Units below in `plugins/voiceprint/`.

**Out of scope:**
- Updating top-level `claude_skills/README.md`, `CHANGELOG.md`, or `SKILLS-MAP.md` to reflect the new voiceprint shape (would be follow-up — explicitly noted by user that they only want plugin-internal changes).
- Migration tooling for existing v1.x rules files (intentional breaking change).
- Changes to other plugins or skills that may reference `voiceprint` (no known consumers — spot-checked).
- Touch-ups to the corpus-pull logic for any medium.
- Updating gotchas.md files except where their guidance contradicts the new flow.

### Deferred to Follow-Up Work

- Updating top-level repo docs (`claude_skills/README.md`, `SKILLS-MAP.md`, `CHANGELOG.md`) to reflect v2.0.0.
- A `voiceprint-creator` gotcha for the `~/.claude/skills/` install path on Windows.

## Key Technical Decisions

### KTD1. Use `skill-creator`'s scripts for packaging when available, fall back to raw SKILL.md

The old format (`bf604e8`) did this and the user explicitly named skill-creator as the packaging path. Both outputs (the `.skill` package and the raw folder) are installable to `~/.claude/skills/`, so the fallback is functionally equivalent for Claude Code CLI users; the `.skill` package is only meaningfully different for claude.ai / Cowork single-file uploads.

### KTD2. Generated skill naming: `myvoiceprint-<medium>`

User confirmed `myvoiceprint` prefix to match the old format. Suffix is the medium (`-email`, `-linkedin`, `-content`) so all three can coexist as separate skills, each with its own description triggering on its medium.

### KTD3. Fold refine into voiceprint-creator's Step 0 mode branch

User-preferred over keeping a separate `voiceprint-refine` skill. One entry point ("work on my voiceprint"), one SKILL.md, one `/voiceprint` command. Refine mode skips corpus pull and analysis entirely and jumps to surgical editing of an already-installed `~/.claude/skills/myvoiceprint-<medium>/SKILL.md`.

### KTD4. Single `/voiceprint` command replaces `/voiceprint create` + `/voiceprint refine`

The mode branch lives inside the skill, not at the command level. Simpler surface, matches the old plugin shape.

### KTD5. v2.0.0 breaking change with no migration

User explicitly said don't auto-migrate. v1.x users rerun the creator to get a proper skill. Major version bump signals the break.

## Output Structure

After changes, the plugin tree should look like:

```
plugins/voiceprint/
├── .claude-plugin/
│   └── plugin.json          (updated: version 2.0.0, new description)
├── commands/
│   └── voiceprint.md        (renamed from create.md; covers create + refine)
├── skills/
│   └── voiceprint-creator/
│       ├── SKILL.md         (rewritten: Step 0 mode branch + Step 6 packaging)
│       └── gotchas.md       (unchanged unless contradicting new flow)
└── README.md                (updated: new install model)
```

Deleted: `skills/voiceprint/`, `skills/voiceprint-refine/`, `commands/refine.md`.

## Implementation Units

### U1. Rewrite `voiceprint-creator/SKILL.md` with mode branch and skill-creator packaging

**Goal:** Replace the rules-file output flow with the skill-creator packaging flow, and add a Step 0 mode branch (create vs. refine).

**Requirements:** R1, R2, R3, R4, R10.

**Dependencies:** None.

**Files:**
- Modify: `plugins/voiceprint/skills/voiceprint-creator/SKILL.md`

**Approach:**

- Read the current `SKILL.md` (Steps 0 through 6) and the old `bf604e8` version (`git show bf604e8:skills/voiceprint-creator/SKILL.md`).
- Preserve verbatim: Step 1 (corpus pull, all three media branches 1a/1b/1c), Step 2 (8-dimension analysis + sentence metrics + exemplar selection), Step 3 (voiceprint draft structure with Sections 1–7), Step 4 (human review), Step 5 (calibration samples).
- Replace Step 0 with a mode-branch version:
  - Step 0a: Ask "Are you creating a new voiceprint or refining an existing one?"
  - **Create path:** ask which medium (email / LinkedIn / content), then continue to Step 1.
  - **Refine path:** ask which medium, resolve `~/.claude/skills/myvoiceprint-<medium>/SKILL.md`, read it, then jump to a new Step 5b (Refine) that runs the existing voiceprint-refine surgical pass (load current file → ask user to tag sections WRONG / OVERSTATED / MISSING / NEEDS_NUANCE with specific examples → apply edits → write back to the same path). Skip Steps 1–5.
- Replace Step 6 (current: write raw rules to `~/Documents/voiceprints/<medium>.md`) with the old `bf604e8` Step 6 packaging logic, adapted for per-medium naming:
  - Step 6a: Build the personalized SKILL.md content for the generated skill. Frontmatter:
    ```yaml
    name: myvoiceprint-<medium>
    description: >
      Apply [Name]'s personal <medium> writing voice when drafting any
      <medium> on their behalf. Use whenever drafting [medium-specific list].
    ```
    Body: the voiceprint Sections 1–7 (LLM-ism ban list, anti-performative rules, core voice patterns + sentence metrics, format-specific modes, adaptation rules, voice exemplars, sample transformations) — exactly the content produced by Steps 3–5 after review and calibration.
  - Step 6b: Try `skill-creator`'s scripts. Common install locations:
    - `~/.claude/skills/skill-creator/`
    - `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/`
    - Anywhere `init_skill.py` is found on `$PATH`-adjacent skill dirs.
    
    If found, scaffold via `init_skill.py myvoiceprint-<medium> --path ~/Documents/`, overwrite the generated SKILL.md with the personalized content from 6a, then package via `package_skill.py ~/Documents/myvoiceprint-<medium>`. Output: `~/Documents/myvoiceprint-<medium>.skill`.
  - Step 6c (fallback): If skill-creator isn't installed, `mkdir -p ~/Documents/myvoiceprint-<medium>` and Write the SKILL.md content directly to `~/Documents/myvoiceprint-<medium>/SKILL.md`. No `.skill` package.
  - Step 6d: Tell the user where the output landed and how to install:
    > "Install to `~/.claude/skills/myvoiceprint-<medium>/` (Claude Code), upload the `.skill` file via skill settings (claude.ai), or drop the folder into your Cowork skills directory. To refine later, rerun `/voiceprint` and pick refine mode."

- Update the skill's top frontmatter `description:` to cover both create and refine intents and to mention all three media.

**Patterns to follow:**
- Old format reference: `git show bf604e8:skills/voiceprint-creator/SKILL.md` for Step 6 packaging logic.
- Existing `plugins/voiceprint/skills/voiceprint-refine/SKILL.md` for the surgical-edit pass (folded into new Step 5b).
- Existing Steps 1–5 in `plugins/voiceprint/skills/voiceprint-creator/SKILL.md` for the 3-medium corpus + analysis logic.

**Test scenarios:**
- The rewritten SKILL.md frontmatter `description:` mentions create, refine, and all three media (email, LinkedIn, content) so the skill triggers on either intent.
- Step 0 contains an explicit mode branch ("create" vs "refine") that routes to disjoint flows.
- Refine flow does NOT pull corpus, does NOT run 8-dimension analysis, does NOT run calibration.
- Step 6 writes to `~/Documents/myvoiceprint-<medium>.skill` (preferred) or `~/Documents/myvoiceprint-<medium>/SKILL.md` (fallback) — never `~/Documents/voiceprints/<medium>.md`.
- The generated skill content embedded in Step 6a includes the medium-specific `name:` and `description:` so it self-triggers post-install.
- Install instructions in Step 6d name the `~/.claude/skills/myvoiceprint-<medium>/` target path.

**Verification:** Re-read the new SKILL.md end-to-end. Confirm: mode branch present at Step 0, all three media still supported in Step 1, Step 6 produces a packaged skill (not a rules file), no references remain to `~/Documents/voiceprints/` or to the runtime `voiceprint` skill.

### U2. Delete the runtime `voiceprint` skill

**Goal:** Remove the runtime voiceprint skill entirely.

**Requirements:** R5.

**Dependencies:** U1 (the new creator must be in place before the runtime is removed, so any in-flight user has a path forward).

**Files:**
- Delete: `plugins/voiceprint/skills/voiceprint/SKILL.md`
- Delete: `plugins/voiceprint/skills/voiceprint/gotchas.md`
- Delete: `plugins/voiceprint/skills/voiceprint/` (directory itself)

**Approach:** `rm -rf plugins/voiceprint/skills/voiceprint/`.

**Test scenarios:**
- `plugins/voiceprint/skills/voiceprint/` does not exist after deletion.
- `grep -r "voiceprint:voiceprint\b"` in the plugin returns no matches (no broken references).

**Verification:** `ls plugins/voiceprint/skills/` shows only `voiceprint-creator/`.

### U3. Delete the standalone `voiceprint-refine` skill

**Goal:** Remove the standalone refine skill (folded into U1's creator).

**Requirements:** R6.

**Dependencies:** U1.

**Files:**
- Delete: `plugins/voiceprint/skills/voiceprint-refine/SKILL.md`
- Delete: `plugins/voiceprint/skills/voiceprint-refine/gotchas.md`
- Delete: `plugins/voiceprint/skills/voiceprint-refine/` (directory itself)

**Approach:** `rm -rf plugins/voiceprint/skills/voiceprint-refine/`.

**Test scenarios:**
- `plugins/voiceprint/skills/voiceprint-refine/` does not exist after deletion.
- `grep -r "voiceprint-refine"` in the plugin returns no matches except inside U1's rewritten SKILL.md, where the refine flow is now inline.

**Verification:** `ls plugins/voiceprint/skills/` shows only `voiceprint-creator/`.

### U4. Collapse commands to a single `/voiceprint`

**Goal:** Replace `/voiceprint create` + `/voiceprint refine` with a single `/voiceprint` command.

**Requirements:** R7.

**Dependencies:** U1 (the skill the command loads must reflect both modes).

**Files:**
- Rename: `plugins/voiceprint/commands/create.md` → `plugins/voiceprint/commands/voiceprint.md`
- Delete: `plugins/voiceprint/commands/refine.md`
- Modify: the renamed file's body and frontmatter description

**Approach:**

- `git mv plugins/voiceprint/commands/create.md plugins/voiceprint/commands/voiceprint.md`.
- Rewrite the renamed file:
  ```markdown
  ---
  description: Build or refine a voiceprint — packages your voice as an installable skill per medium (email, LinkedIn, content)
  ---
  
  # /voiceprint
  
  Load skill `voiceprint:voiceprint-creator` using the Skill tool and follow the
  full workflow defined there, starting at Step 0 (Mode: create or refine).
  ```
- `rm plugins/voiceprint/commands/refine.md`.

**Test scenarios:**
- `plugins/voiceprint/commands/` contains exactly one file: `voiceprint.md`.
- The new `voiceprint.md` description mentions both create and refine.
- The new `voiceprint.md` body instructs loading `voiceprint:voiceprint-creator` and starting at Step 0 mode branch.

**Verification:** `ls plugins/voiceprint/commands/` shows only `voiceprint.md`. The file contents reference the creator skill and the Step 0 mode branch.

### U5. Update plugin manifest to v2.0.0

**Goal:** Bump version and update description to reflect skill-output model.

**Requirements:** R8.

**Dependencies:** U1–U4.

**Files:**
- Modify: `plugins/voiceprint/.claude-plugin/plugin.json`

**Approach:** Update `version` from `"1.1.0"` to `"2.0.0"`. Update `description` to reflect that the plugin builds an installable skill per medium rather than a rules file consumed at draft time. Example new description: `"Build your personal writing voiceprint as an installable Claude skill — one per medium (email, LinkedIn, longform content). Generated skills auto-apply when drafting in your name."`

**Test scenarios:**
- `plugins/voiceprint/.claude-plugin/plugin.json` parses as valid JSON.
- `version` is `"2.0.0"`.
- `description` no longer mentions "applies it automatically whenever Claude drafts" (the old runtime-skill phrasing).

**Verification:** `cat plugins/voiceprint/.claude-plugin/plugin.json | jq .` confirms valid JSON, version 2.0.0, new description.

### U6. Update plugin README

**Goal:** Reflect the new single-command, per-medium-skill, install-to-`~/.claude/skills/` model.

**Requirements:** R9.

**Dependencies:** U1–U5.

**Files:**
- Modify: `plugins/voiceprint/README.md`

**Approach:**

- Update the "What it does" prose to reflect that the plugin generates an installable skill per medium rather than a rules file plus runtime applier.
- Replace the Commands table (currently two rows: `/voiceprint create`, `/voiceprint refine`) with a single row for `/voiceprint`, noting that the skill asks create vs. refine at Step 0.
- Remove the line "The `voiceprint` skill auto-applies whenever Claude drafts content in your voice." (the runtime skill is gone).
- Update the Output section: outputs are now `~/Documents/myvoiceprint-<medium>.skill` (or fallback `~/Documents/myvoiceprint-<medium>/SKILL.md`), one per medium. Each is an installable skill.
- Add a brief Install section: drop the generated folder into `~/.claude/skills/myvoiceprint-<medium>/` for Claude Code, upload the `.skill` to claude.ai, drop folder into Cowork skills dir.
- Bump install link if it currently references v1.x release line (it doesn't appear to — leave the GitHub URL as is).
- Keep the "Supported sources" section as-is (email / LinkedIn / content unchanged).

**Test scenarios:**
- README no longer references "runtime voiceprint skill" or the `~/Documents/voiceprints/<medium>.md` path.
- README documents `myvoiceprint-<medium>` as the output skill name and `~/.claude/skills/myvoiceprint-<medium>/` as the install path.
- The commands table has exactly one row: `/voiceprint`.

**Verification:** Read the rendered README. The reader can answer: "What does this plugin do? What command do I run? Where does the output go? How do I install the output?" without confusion.

## Risks & Dependencies

- **Breaking change for v1.x users.** Anyone with `~/Documents/voiceprints/<medium>.md` from v1.x loses auto-apply (no runtime skill to read it). Mitigation: v2.0.0 major bump signals the break; users rerun `/voiceprint` to get a proper skill. User explicitly accepted this.
- **`skill-creator` script path discovery.** The creator probes a small set of known locations. If skill-creator is installed under an unusual path, the creator falls back to raw SKILL.md output, which is still installable — just not a single-file `.skill` package. Acceptable degradation.
- **Generated skill description quality.** The generated `myvoiceprint-<medium>` skill must have a description that reliably triggers on drafting intent. The old format used a strong description; U1's Step 6a copies that pattern, adapted per medium. If a generated skill fails to trigger in practice, refine the description template in a follow-up.

## Verification Strategy

After all units land:

```
ls plugins/voiceprint/
ls plugins/voiceprint/skills/
ls plugins/voiceprint/commands/
cat plugins/voiceprint/.claude-plugin/plugin.json
```

Expected:
- `plugins/voiceprint/`: `.claude-plugin/`, `commands/`, `skills/`, `README.md`
- `plugins/voiceprint/skills/`: only `voiceprint-creator/`
- `plugins/voiceprint/commands/`: only `voiceprint.md`
- `plugin.json`: version `"2.0.0"`, new description
- `git grep -i "voiceprint:voiceprint\b\|voiceprint-refine\|~/Documents/voiceprints/"` returns no live references (occurrences only inside historical context or removed files).

No code to compile or test — this is all markdown and one JSON manifest.

## Sources & Research

- Current plugin: `plugins/voiceprint/` in this repo (`claude_skills`).
- Old format reference: commit `bf604e8` (May 6 2026), specifically `skills/voiceprint-creator/SKILL.md` — fetch with `git show bf604e8:skills/voiceprint-creator/SKILL.md`.
- Conversion commit (`a615b5a`, May 14 2026): the commit that moved away from the format being restored — useful for understanding what was changed and why.
- User-confirmed decisions captured before plan-write: naming (`myvoiceprint-<medium>`), single command (`/voiceprint`), fold refine into creator, install path (`~/.claude/skills/`), no auto-migration.
