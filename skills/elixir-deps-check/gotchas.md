# elixir-deps-check gotchas

## Run from the project root

`mix hex.outdated` only works from a directory containing `mix.exs`. If the user invokes the skill from a subdirectory, `cd` to the project root first or surface the error. Don't try to grep `mix.lock` directly to fake the comparison — `mix hex.outdated` knows about `:override`, umbrella projects, and dep types in ways manual parsing won't.

## Don't auto-update

This skill is an audit, not a workflow. Never run `mix deps.update` or edit `mix.exs` automatically. Produce the report; let the user decide what to apply. If they then say "apply the patch bumps", that's a separate, explicit action.

## "Update possible" vs "Update not possible" matters

- `Update possible` → latest fits current constraint → only `mix.lock` changes.
- `Update not possible` → constraint blocks the upgrade → `mix.exs` must change too.

Don't conflate them in the report. The user needs to know which file changes.

## Pre-1.0 minor bumps are major-shaped

Elixir/Erlang convention treats `0.x.0 → 0.(x+1).0` as a potentially breaking change. Phoenix LiveView, Oban Pro, etc. all use this. Always treat any non-patch bump on a `0.x` package as a major bump in the recommendation table.

## Skip changelog fetch for patch bumps

Fetching changelogs is the most token-expensive step. Patch bumps are bug fixes; the diff is not interesting to a human in a recap. Save the fetch for minor and major bumps only — unless the user explicitly asks for full detail.

## Transitive deps need parent context

If a transitive dep is outdated, the fix isn't `mix deps.update <transitive>` — it's bumping whichever top-level dep brings it in. Use `mix deps.tree` to identify the parent, and recommend bumping the parent (not the transitive) in the report.

## Changelog fallback chain

Try in this order: GitHub `CHANGELOG.md` → GitHub `/releases` → HexDocs `/changelog.html`. Stop at the first that works. If none yield a clear summary between the two versions, say so honestly — point the user at the GitHub compare URL (`https://github.com/<owner>/<repo>/compare/v<old>...v<new>`) rather than fabricating release notes.

## Elixir version constraint matters

Some packages bump their `elixir:` requirement in their mix.exs (e.g. requiring Elixir 1.16+). If the user is on an older Elixir, the latest version of a dep may simply not be reachable. Note the project's Elixir requirement and flag any deps whose latest version requires a newer one.

## Don't confuse `~>` semantics

- `~> 1.2` allows `>= 1.2.0 and < 2.0.0` (any 1.x ≥ 1.2)
- `~> 1.2.3` allows `>= 1.2.3 and < 1.3.0` (only 1.2.x ≥ 1.2.3)

The two-segment vs three-segment form changes the bump scope. When recommending a constraint update, match the user's existing style (don't switch from `~> 1.2` to `~> 1.3.0` — keep it as `~> 1.3`).
