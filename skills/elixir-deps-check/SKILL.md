---
name: elixir-deps-check
description: Audit Elixir dependencies in mix.exs and mix.lock against the latest versions on hex.pm, summarize what changed between the locked and latest versions in plain language, and recommend whether each dep needs a mix.exs constraint bump or just a mix.lock refresh. Use when the user asks "what deps are outdated", "should I update <package>", "audit my mix deps", "what changed in <package> since I locked it", or any variant about Elixir dependency freshness, upgrade planning, or deciding mix.exs vs mix.lock updates.
---

# Elixir Deps Check

Audit Elixir deps and produce a per-package recommendation: leave alone, refresh mix.lock, or bump mix.exs constraint. Includes a plain-language summary of what changed in each upgradeable package.

## Workflow

### 1. Confirm we're in an Elixir project

Check `mix.exs` and `mix.lock` exist at the working directory or one level up. If not, ask the user where the project root is. Do not run mix commands outside the project root.

### 2. Snapshot current state

```bash
mix hex.outdated --all
```

This is the source of truth. It prints a table of all hex deps (including transitive) with columns:

- **Dependency** — package name
- **Current** — the version locked in `mix.lock`
- **Latest** — newest published version on hex.pm
- **Status** — `Up-to-date`, `Update possible`, `Update not possible`
- **Requirement** — the constraint from `mix.exs` (only for top-level deps)

Read the output carefully:
- `Update possible` = latest version satisfies the current constraint → `mix deps.update <pkg>` will pick it up; no `mix.exs` change needed.
- `Update not possible` = latest version is outside the constraint → must bump the constraint in `mix.exs` to upgrade.
- Transitive deps (rows with no Requirement column value) can usually only be updated by bumping the parent that brings them in.

If `mix hex.outdated` errors (e.g. no `_build`, missing deps), run `mix deps.get` first.

### 3. Classify each upgradeable dep by bump magnitude

For each row where `Current != Latest`, classify by semver:

- **Patch** (`1.2.3 → 1.2.4`) — bug fixes; almost always safe.
- **Minor** (`1.2.x → 1.3.0`) — new features, no breaking changes (per semver). Usually safe.
- **Major** (`1.x → 2.0`) — breaking changes; read the release notes before upgrading.
- **Pre-1.0** (`0.x → 0.y`) — Elixir convention treats `0.x.0 → 0.(x+1).0` as potentially breaking. Treat any non-patch bump on a `0.x` as major.

### 4. Fetch what changed (only for non-trivial bumps)

Skip changelog lookup for patch bumps unless the user asked for full detail. For minor and major bumps:

1. **Find the source repo.** Hit the hex API:
   ```
   curl -s https://hex.pm/api/packages/<name> | jq '.meta.links'
   ```
   Look for `GitHub`, `Source`, or similar. If absent, fall back to `https://hex.pm/packages/<name>` and read the page metadata.

2. **Fetch the changelog.** Try in this order, stopping at the first that works:
   - `https://github.com/<owner>/<repo>/blob/main/CHANGELOG.md` (WebFetch)
   - `https://github.com/<owner>/<repo>/releases` (WebFetch — covers tagged releases)
   - HexDocs: `https://hexdocs.pm/<name>/changelog.html`

3. **Extract the relevant range.** Only summarize entries between Current+1 and Latest (inclusive). Skip everything older than Current.

4. **Summarize in plain language.** Two-to-four sentences per package. Lead with user-visible impact ("adds support for X", "fixes a bug where Y"). Mention breaking changes prominently. Avoid module names and internal refactors unless they affect callers.

### 5. Build the recommendation per dep

For each outdated dep, decide:

| Situation | Recommendation |
|---|---|
| Patch bump, status `Update possible` | `mix deps.update <name>` — refreshes `mix.lock` only. Low risk. |
| Minor bump, status `Update possible` | `mix deps.update <name>` — `mix.lock` only. Read changelog first if it's a load-bearing dep (Phoenix, Ecto, your auth library). |
| Minor or major bump, status `Update not possible` | Bump constraint in `mix.exs` first (e.g. `~> 1.2` → `~> 1.3`), then `mix deps.update <name>`. Both files change. |
| Major bump | Always read the upgrade guide. May require code changes. Surface migration steps explicitly in the report. |
| Pre-1.0 bump | Treat as major regardless of which segment moved. |
| Transitive dep is outdated | Note it but the fix is upstream — usually means bumping the parent package. Don't recommend direct action. |

### 6. Produce the report

Format:

```
## Mix Deps Audit

**Up to date:** N packages — no action.

**Patch bumps (safe):**
- `pkg_a` 1.2.3 → 1.2.4 — <one-line summary>. Run: `mix deps.update pkg_a`
- ...

**Minor bumps:**
- `pkg_b` 1.2.0 → 1.3.0 — <2-3 sentence plain-language summary of what's new>.
  - Recommendation: `mix deps.update pkg_b` (mix.lock only)
  - Risk: Low / Medium — <one-line why>
- ...

**Major bumps (need attention):**
- `pkg_c` 1.x → 2.0 — <2-4 sentence summary including breaking changes>.
  - Recommendation: bump `mix.exs` constraint to `~> 2.0`, then `mix deps.update pkg_c`. Likely code changes: <list>.
  - Risk: High — <one-line why>
- ...

**Transitive deps out of date:** N — listed for awareness; fix by bumping parents above.
```

End with a short overall risk summary (Low / Medium / High) and which dep dominates the risk.

## Rules

- **Don't run `mix deps.update` automatically.** Audit only. The user decides what to update; this skill produces the recommendation.
- **Don't edit `mix.exs` automatically.** If they ask you to apply the recommendations, do so as a separate, explicit step after they confirm.
- **Patch bumps:** still call them out, but don't spend tokens fetching changelogs unless asked.
- **No fallbacks on errors.** If `mix hex.outdated` fails, surface the error and stop — don't silently skip and produce a partial audit. (Per the user's Elixir-no-fallbacks rule.)
- **Always note what version of Elixir the project requires** (`elixir:` line in `mix.exs`). If the user is on an older Elixir, some latest packages may require a newer one — call this out when relevant.

## Common follow-ups

- "Apply the patch bumps" → run `mix deps.update <name>` for each, then `mix compile && mix test` to verify.
- "Bump <pkg> to latest" → if `Update not possible`, edit the `mix.exs` constraint, then `mix deps.update <pkg>`. Show the diff.
- "Why is X locked at Y" → use `mix deps.tree` to find what brings it in.
