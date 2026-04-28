---
name: pr-recap
description: Generate a short, non-technical product-person summary of what's changed since a given PR number or date. Use when the user says "give me a 2-3 sentence non-technical description of what was changed in PRs starting with N", "what's been merged since PR X", "summarize recent PRs and commits for product", or "what changed since I last looked". Pulls merged PRs and direct commits, clusters by feature, writes to a product audience, and ends with a "what to test" punch list.
---

# PR Recap

Write a casual product-person changelog covering everything merged since a given PR number (or date). Audience is the user's non-technical collaborator — they need to know what to look at and what to test, not implementation details.

## Inputs

User typically says one of:
- "starting with PR 176"
- "since PR 184"
- "the latest" (after a previous recap — figure out the last covered PR from the prior conversation turn)
- "since [date]"

If ambiguous, ask once for the cutoff.

## Workflow

1. **Determine cutoff.** From the user's prompt, extract a PR number or date. If they say "the latest", look at your prior recap output in this conversation; if there is none, ask.

2. **Fetch merged PRs since cutoff.**
   ```
   gh pr list --state merged --base main --limit 100 --json number,title,mergedAt,body,url
   ```
   Filter to PRs with number `>=` cutoff (or merged after cutoff date). Sort by merge time ascending.

3. **Fetch direct commits to main since cutoff.**
   ```
   git fetch origin main
   git log --no-merges --pretty=format:"%h|%s|%an|%ad" --date=short origin/main --since="<date of cutoff PR merge>"
   ```
   Drop commits that are part of the merged PRs (match by the PR's merge SHA range). Keep only direct-to-main commits.

4. **Cluster by feature.** Group related PRs/commits — one bullet per user-visible change. A single bullet may span multiple PRs (e.g. "Endorsement decline flow — PR #189, #191, plus follow-up commit abc123").

5. **Write the recap.** Format:

   ```
   ## Since PR #<cutoff>

   Two-to-four-sentence opening: high-level theme of this batch in plain English. What kind of work was this — a polish pass, a new feature, bug squashing? Mention the user-facing direction.

   ### What changed
   - **<feature/area>** — one sentence in product language. (PR #N, #M)
   - **<feature/area>** — …
   - …

   ### What to test
   - <concrete user action>
   - <concrete user action>
   - …
   ```

6. **Iterate.** If the user says "do it again" / "be more in depth" / "include commits in addition to PRs", re-run with the same cutoff but expanded detail. If they say "do the latest starting with N", treat N as new cutoff.

## Voice rules

- Product-person language. No "refactored the X service", no migration numbers, no module names. Say "made the invitation page faster to load" instead of "optimized N+1 query in InviteController".
- Lead with user-visible impact. Implementation detail only if it changes risk ("this required a database migration — needs deploy").
- "What to test" goes at the bottom — the user explicitly asked for this ordering.
- Keep it tight. If there are 15 PRs, the recap should still fit in one screen.
- No emojis unless the user asks.

## Common variants

- "explain to a product person who may need to test" → already the default.
- "be more in depth" → expand each bullet from one sentence to 2–3, but keep voice and structure.
- "include commits in addition to PRs" → add a line at the end of relevant bullets noting any direct-to-main commits.
- "git pull and do it again" → run `git pull` first, then re-run the recap with the same cutoff.
