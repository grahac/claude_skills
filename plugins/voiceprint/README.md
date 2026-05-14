# Voiceprint

Clone your writing voice. Analyzes your real sent emails, LinkedIn posts, or longform
content — then applies it automatically whenever Claude drafts in your name.

## What it does

**Creates a voiceprint from your actual writing** — not a questionnaire, not
self-reported preferences. Pulls 50 real sent emails (or LinkedIn export / blog URLs),
runs analysis across 9 dimensions including quantified sentence metrics, selects
verbatim corpus snippets as ground-truth exemplars, and builds a ban list of AI
patterns that don't belong in your voice.

**Applies it automatically** — the `voiceprint` skill reads your voiceprint file and
applies every rule whenever Claude drafts email, posts, or content on your behalf. No
manual invocation needed.

**Lets you refine it over time** — when something feels off after a real draft, run
`/voiceprint refine` to surgically fix it without rebuilding from scratch.

## Commands

| Command | What it does |
|---|---|
| `/voiceprint create` | Build a new voiceprint (email, LinkedIn, or longform) |
| `/voiceprint refine` | Surgically update an existing voiceprint |

The `voiceprint` skill auto-applies whenever Claude drafts content in your voice.

## Output

Each voiceprint is saved to `~/Documents/voiceprints/<medium>.md`:
- `email.md` — sent email voice
- `linkedin.md` — LinkedIn post voice
- `content.md` — longform/blog voice

The file contains 7 sections: LLM-ism ban list, anti-performative rules, core voice
patterns with sentence metrics, format-specific modes, adaptation rules, verbatim voice
exemplars, and before/after sample transformations.

## Supported sources

- **Email** — any connected email MCP (Gmail, Outlook/M365, Fastmail, ProtonMail).
  Supports multiple accounts in one run — personal + work merged into one voiceprint.
- **LinkedIn** — posts from your LinkedIn data export
- **Content** — longform pieces fetched from URLs you provide

## Install

Add the plugin directory to your Claude Code project or install from:
`https://github.com/grahac/claude_skills/tree/main/plugins/voiceprint`
