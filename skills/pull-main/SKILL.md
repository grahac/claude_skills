---
name: pull-main
description: Bring the current feature branch up to date with origin/main and push it. Use when the user says "pull main", "merge origin/main into this branch and push", "rebase into main and push", or any "catch this branch up with main and push" variant. Commits any uncommitted work first, fetches, merges origin/main into HEAD, then pushes the feature branch (NOT to main).
---

# Pull Main

Sync the current feature branch with `origin/main` and push it. Main itself is never written to — this updates the feature branch in place so its PR is current.

## Workflow

Run these checks before doing anything destructive. If any fail, stop and ask.

1. **Refuse to run on main.** `git rev-parse --abbrev-ref HEAD` — if it's `main` or `master`, stop and tell the user this skill is for feature branches only.

2. **Handle uncommitted changes.** `git status --porcelain`:
   - If clean → continue.
   - If dirty → show the user the diff summary (`git status` short form), ask whether to (a) commit them with a message you draft, or (b) stash. Default: commit. Never silently discard.

3. **Fetch.** `git fetch origin main`.

4. **Check whether main has moved.** `git rev-list --count HEAD..origin/main`:
   - If `0` → branch is already up to date. Skip merge, go to push.
   - If `> 0` → continue.

5. **Merge.** `git merge origin/main --no-edit`.
   - On clean merge → continue.
   - On conflict → run `git status` to list conflicted files, show the user, and stop. Do NOT attempt auto-resolution. The user resolves; they re-invoke or finish manually.

6. **Push.** `git push` (uses upstream tracking). If no upstream is set, `git push -u origin <current-branch>`.

7. **Report.** One line: `pulled N commits from main, pushed M commits. PR: <url if found via gh pr view>`.

## Rules

- Never push to `main` or `master`. Never force-push. If `git push` is rejected (e.g. someone else pushed to the feature branch), stop and report — do not `--force`.
- If the merge produces conflicts, always stop. Do not invoke other tools to "auto-resolve" — conflict resolution is the user's call.
- Skip hooks: never. If a pre-push hook fails, surface the failure; don't `--no-verify`.
- If `gh` is available, append the PR URL to the final report so the user can click through.
