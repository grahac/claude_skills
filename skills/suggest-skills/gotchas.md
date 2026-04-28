# Gotchas

## Report is large — never `Read` the whole file
On an active week the report is 200-300KB (1500-2000 lines). Reading it whole burns context. Use `head` for the global view (sessions, tool counts, Bash 2-grams), `grep -nE "^## |^_"` for the project index, then `Read` with explicit line ranges or `awk` to pull one project's section.

## Skill match annotations: trust the terms, not the rank
Each per-project "Possibly covered by existing skills" line shows the overlapping tokens, e.g. `picky-security [dependency, endpoint, security, vulnerability]`. Always look at the bracketed terms — if they're domain-specific (security, oauth, fly, oban, ecto, changelog), trust the match. If they're generic filler that slipped past the filter ("data", "create", "edit"), discount it. The match is *evidence*, not a verdict.

## A single very long session ≠ recurring intent
Weight cross-session and cross-project repetition higher than within-session repetition. A project with `_1 sessions, 200 prompts (190 unique)_` is one long debugging session, not a recurring workflow. The unique-vs-total ratio in the section header is the tell.

## Bash 2-grams are recipes, not skills
A high-count pair like `mix compile → mix test (97)` is not "build a skill that runs both" — it's a verify loop that's already a one-liner. Look for sequences with *cross-binary* shifts (`fly machine → fly deploy`, `git diff → gh pr`) where the user keeps switching tools. Those are the workflow candidates.

## Don't suggest skills that already exist
Even with the auto-match feature, dedupe manually. Common installed-skill collisions:
- Permission allowlist mining → `fewer-permission-prompts`
- Resume-after-compaction → `gsd:resume-work`, `metaswarm:prime`
- Code review → `ce-code-review`, `phx:review`, `coderabbit:review`
- PR shepherding → `metaswarm:pr-shepherd`
- Brainstorming → `superpowers:brainstorm`, `ce-brainstorm`

If the script flags an existing skill in the per-project annotation, treat it as a hard "don't suggest this" signal.

## Compacted-session restarts are now stripped
Prompts beginning `This session is being continued from a previous conversation that ran out of context...` are auto-injected by the harness on session resume, not typed by the user. They're filtered out. **But** the *frequency* of resume points still matters as evidence — long sessions getting compacted often is itself a signal that the user might want a `/resume`-style helper. Watch for it indirectly via low unique/total ratios on long-running projects.

## Conductor workspaces collapse — but `dev/` and `conductor/` for the same logical project don't
`/Users/.../conductor/workspaces/aiqrank/*` rolls up to one section, but `/Users/.../dev/.../aiqrank` shows separately. They're the same project. When delivering suggestions, mentally combine evidence from both before scoring frequency.

## The skill index includes plugin caches with duplicates
`document-skills:foo` and `example-skills:foo` and `compound-engineering:ce-foo` and `ce:foo` may all match the same project. The script dedupes by `name`, but namespaced names (`ce-plan` vs `ce:plan`) survive as separate entries. Treat near-duplicates as the same skill in the skip list.

## Bias toward fewer, higher-evidence suggestions
A suggestion needs concrete quoted prompts (with ×N counts) or Bash 2-grams as evidence, a frequency count across projects, and a clean trigger phrase. If you can't quote 2-3 prompts, drop it.
