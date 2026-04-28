# pr-recap gotchas

## Don't drop direct commits to main

Some teams merge via "squash and merge" PRs only; others push directly to main for hotfixes. The recap must include both. Use `gh pr list --state merged` for PRs and `git log origin/main` for direct commits, then deduplicate by SHA.

## Cutoff is exclusive on the left, inclusive on the right

"Starting with PR #176" means PR 176 IS included. Off-by-one here makes the recap repeat last week's content or skip a release. Test with the boundary PR every time.

## "Do it again" means re-run, not append

When the user says "do it again" / "be more in depth", re-run the recap with the same cutoff and produce a fresh version with more detail. Don't append to the previous output — it produces tangled, hard-to-read summaries.

## What-to-test goes at the BOTTOM

The user explicitly asks for this ordering. Don't move it to the top "for prominence" — they read changes first, then think about testing. Putting test items first makes the recap feel like a QA checklist, not a product update.

## Avoid implementation language

Banned: "refactored", "optimized N+1", "extracted module", "added migration `0042_...`". Replace with user-visible behavior: "made the X page load faster", "added a Y option to the Z screen". The audience is a product collaborator, not an engineer.

## Mention deploy-affecting changes

If a PR has a database migration, env var change, or new external dependency, call it out at the bottom under "deploy notes" or inline. The product person needs to know if testing requires a fresh deploy.

## Empty result

If no PRs are merged since the cutoff, say so plainly: "Nothing merged since PR #N." Don't fabricate filler activity from open PRs or in-progress branches.
