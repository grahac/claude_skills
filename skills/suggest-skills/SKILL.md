---
name: suggest-skills
description: Mine recent Claude Code transcripts to surface candidate skills and plugins worth building. Use when the user asks to "find skill ideas from my transcripts", "what skills should I build", "analyze my Claude history for automation opportunities", "suggest plugins from my last week", or any variant about extracting reusable workflows from past sessions. Looks for repeated tasks, recurring corrections, command sequences, and cross-project friction.
---

# Suggest Skills

Surfaces candidate skills/plugins by analyzing the user's own Claude Code transcripts.

## Workflow

### 1. Run the analyzer

```bash
python3 /Users/charliegraham/.claude/skills/suggest-skills/scripts/analyze_transcripts.py \
  --days 7 --min-prompts 3 --out /tmp/suggest_skills_report.md
```

Defaults: 7-day window, projects with ≥3 prompts. Adjust `--days` if the user specifies a different range.

What the script does:
- Scans `~/.claude/projects/*/*.jsonl`, strips system-reminders, command tags, local-command output, task-notifications, image refs, and session-resume restarts.
- Rolls up Conductor workspaces (`/conductor/workspaces/<project>/<workspace>`) to project root.
- Deduplicates prompts by normalized form, annotating repeats as `(×N)`.
- Captures per-project date ranges and workspace counts.
- Builds Bash command 2-grams at `binary subcommand` granularity (e.g. `mix compile → mix test`) — these are recipe candidates.
- Indexes installed skills (`~/.claude/skills/`, `~/.claude/plugins/cache/**/SKILL.md`), filters out generic terms (in >8% of skills), and pre-flags each project with the top 3 skills whose distinctive terms appear in its prompts.

Report is typically 200-300KB on an active week.

Flags worth knowing:
- `--no-skill-match` — skip the skill cross-check (faster, useful when iterating)
- `--bash-ngram-min N` — change the floor for Bash 2-grams (default 4)
- `--max-prompt-chars N` — truncate per-prompt snippets (default 400)

### 2. Read the report in two passes

**Pass A — global view** (cheap):
```bash
head -45 /tmp/suggest_skills_report.md   # session count, tool histogram, Bash recipes
grep -nE "^## |^_" /tmp/suggest_skills_report.md | head -60   # project ranking
```

**Pass B — sample top 5–8 projects.** Use `Read` with explicit line ranges from the grep output, or:
```bash
awk '/^## <project_path>/,/^## /' /tmp/suggest_skills_report.md
```

Don't `Read` the whole file. It blows context for marginal gain — the dedup + rollup mean section headers already tell you which projects matter.

### 3. Pattern-hunt

Three signal layers, each maps to a different suggestion type:

| Layer | What to look for | Suggestion type |
| --- | --- | --- |
| **Bash 2-grams (top of report)** | High-count `A → B` pairs, especially command families like `fly machine → fly deploy`, `gh pr → gh pr` | Skill or thin wrapper that runs the recipe; permission allowlist additions |
| **Repeat prompts (`×N` annotations)** | Same intent surfaced 3+ times across projects | Skill encoding the recipe |
| **Per-project distinctives** | Unique error strings, domain terms, mistakes the user keeps fixing | Per-domain reference doc, CLAUDE.md rule, or hook |

Also watch for:
- **Correction loops** — `<do X>` followed by `<no, do Y>` in the same project. The script doesn't auto-detect these; eyeball them.
- **Cross-project recurrence** — same intent in 3+ projects = strong skill candidate. Within-session repetition = weaker (one painful debug).
- **Possibly covered** annotations — if the per-project skill match overlaps with what you'd suggest, *don't suggest it* — the user already has a skill for it. Note in the skip list.

### 4. Deliver suggestions

Per the user's global preferences (3+ options with tradeoffs, confidence score), produce:

- **Top 5–8 candidates**, each with:
  - **Name** (lowercase-hyphenated)
  - **Trigger phrase / when** (what the user would say)
  - **Evidence** — concrete prompts (×N counts) or Bash 2-grams from the report. Quote 2–3, cite the project.
  - **Frequency** — count across projects
  - **Sketch** — 1–3 sentences on what the skill does and what scripts/refs it bundles
  - **Tradeoff vs alternatives** — skill vs CLAUDE.md rule vs hook vs allowlist
- **Cross-cutting recommendations** — global CLAUDE.md additions, permission allowlist entries, hook ideas
- **Skip list** — patterns the report flagged as "Possibly covered" plus any others you spotted that match an installed skill
- **Confidence score** (1-10) with a one-line reason

Bias toward fewer, higher-evidence suggestions. Three excellent ideas beat ten mediocre ones.

## Notes

- The skill match annotation lists the **terms that overlapped** so you can sanity-check why it matched. If the terms look like generic filler ("create", "edit", "data"), discount the match — the user might still need a skill there.
- Prompts containing `<local-command-stdout>`, image refs, "session continued from..." restarts, and `Base directory for this skill:` dumps are stripped automatically — you should not see them in the report.
- A single very long session ≠ recurring intent. Weight cross-session/cross-project repetition higher.
- If `--days 7` produces too little signal, try `--days 14` or `--days 30`.
