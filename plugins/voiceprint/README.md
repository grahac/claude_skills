# Voiceprint

Clone your writing voice as an installable Claude skill. Analyzes your real sent
emails, LinkedIn posts, or longform content — then packages your voice as a skill
that auto-applies whenever Claude drafts in your name.

## What it does

**Builds a voiceprint from your actual writing** — not a questionnaire, not
self-reported preferences. Pulls 50 real sent emails (or LinkedIn export / blog URLs),
runs analysis across 9 dimensions including quantified sentence metrics, selects
verbatim corpus snippets as ground-truth exemplars, and builds a ban list of AI
patterns that don't belong in your voice.

**Packages it as an installable Claude skill** — one per medium (`myvoiceprint-email`,
`myvoiceprint-linkedin`, `myvoiceprint-content`). The generated skill has its own
description that triggers whenever Claude drafts in that medium on your behalf. No
runtime intermediary, no manual invocation.

**Refines surgically over time** — when something feels off after a real draft, rerun
`/voiceprint` and pick refine mode to fix it without rebuilding from scratch.

## Command

| Command | What it does |
|---|---|
| `/voiceprint` | Build a new voiceprint OR refine an existing one — asks which up front, then which medium |

## Output

The creator writes one of:
- `~/Documents/myvoiceprint-<medium>.skill` — packaged single-file skill (when `skill-creator` is installed)
- `~/Documents/myvoiceprint-<medium>/SKILL.md` — raw skill folder (fallback)

`<medium>` is one of `email`, `linkedin`, or `content`. Each is an independent
installable skill that triggers on its own medium — install all three for a full
multi-medium voice.

The skill's body contains 7 sections: LLM-ism ban list, anti-performative rules,
core voice patterns with sentence metrics, format-specific modes, adaptation rules,
verbatim voice exemplars, and before/after sample transformations.

## Install the generated skill

After `/voiceprint` produces the output:

- **Claude Code (CLI):** copy the folder to `~/.claude/skills/myvoiceprint-<medium>/`.
  The skill auto-triggers next time you draft that medium on your behalf.
- **claude.ai (web/desktop):** upload the `.skill` file via skill settings (or the
  folder's `SKILL.md` if you got the fallback).
- **Cowork:** drop the folder into your Cowork skills directory.

## Refine an installed voiceprint

Rerun `/voiceprint`, pick **refine** at the mode prompt, and pick the medium. The
creator reads the installed skill at `~/.claude/skills/myvoiceprint-<medium>/SKILL.md`
and walks you through surgical edits (add a ban, fix a tone, swap an exemplar). No
corpus re-pull required.

## Supported sources

- **Email** — any connected email MCP (Gmail, Outlook/M365, Fastmail, ProtonMail).
  Supports multiple accounts in one run — personal + work merged into one voiceprint.
- **LinkedIn** — posts from your LinkedIn data export
- **Content** — longform pieces fetched from URLs you provide

## Install the plugin

Add the plugin directory to your Claude Code project or install from:
`https://github.com/grahac/claude_skills/tree/main/plugins/voiceprint`

## Breaking change in v2.0.0

v1.x wrote rules to `~/Documents/voiceprints/<medium>.md` and applied them via a
runtime `voiceprint` skill. v2.0.0 packages each voiceprint as its own installable
skill instead. If you used v1.x, rerun `/voiceprint` to generate a proper v2 skill —
existing v1.x files are not auto-migrated.
