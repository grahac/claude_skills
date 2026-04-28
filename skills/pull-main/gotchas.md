# pull-main gotchas

## Don't auto-resolve merge conflicts

When `git merge origin/main` produces conflicts, stop and surface the conflicted files. Do not invoke other tools to "auto-resolve" — the user resolves conflicts manually. Re-running the skill after a partial resolution is the correct flow, not auto-fix.

## Don't `--force` on a rejected push

If `git push` is rejected (someone else pushed to the feature branch, or the local history diverged), stop and report. Do NOT add `--force` or `--force-with-lease`. The user decides whether their local history should win.

## Refuse to run on main/master

Always check `git rev-parse --abbrev-ref HEAD` first. If on `main`, `master`, `trunk`, or any default branch, stop immediately. This skill is for keeping a feature branch fresh, not pushing to main.

## Dirty working tree

If `git status --porcelain` shows uncommitted changes, never silently discard them. Show the diff summary, ask the user whether to commit (default) or stash, and act on their answer. Stashing without telling them is just as bad as discarding.

## Hooks failing

If a pre-push hook fails, surface the failure verbatim. Never `--no-verify`. The hook is there for a reason; bypassing it on the user's behalf is a footgun.

## No upstream tracking

If `git push` errors with "no upstream branch", run `git push -u origin <current-branch>` once to set tracking, then proceed. Don't try fancier alternatives.

## Empty merge

If `git rev-list --count HEAD..origin/main` is `0`, branch is already current. Skip the merge step and go straight to push (which may also be a no-op). Report this clearly so the user knows nothing was merged in.
