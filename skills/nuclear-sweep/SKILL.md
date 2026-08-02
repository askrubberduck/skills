---
name: nuclear-sweep
description: Use when the user asks to clean up branches, worktrees, stale checkouts, temp/scratch dirs, or .gitignore across one or more repos, or when stale worktrees accumulate after merged work.
---

# Worktree and Branch Hygiene Sweep

Multi-repo cleanup with a hard rule: **verify merged before delete, and keep nothing "just in
case"** — unmerged work gets an explicit merge-or-delete decision, not a reprieve.

## Sweep per repo

1. Inventory: `git worktree list`, `git branch -vv`, `git fetch --prune` first so remote state is
   current. Use absolute paths; don't cd back and forth.
2. Classify each branch/worktree:
   - **Merged normally** → `git branch --merged origin/<default>` catches it → delete.
   - **Squash-merged** → `--merged` MISSES these. Check `gh pr list --state merged --search
     "head:<branch>"` or `git cherry origin/<default> <branch>` (all `-` = contained) before
     declaring unmerged.
   - **Unmerged** → open the work item it belongs to; decide merge-or-delete on its state
     (superseded/abandoned = delete; live = finish or hand off). Record the decision.
3. Delete: `git worktree remove <path>` then `git branch -D <branch>`; `git worktree prune` for
   leftovers.
4. Scratch dirs: hunt ad-hoc temp dirs outside the sanctioned scratchpad (e.g. `~/<repo>-tmp*`,
   `/tmp/<repo>*`, review-tmp dirs) and remove them with the same verify-then-delete discipline.
5. `.gitignore` audit: worktree dirs (`.worktrees/`), build output, and local-config paths present
   and ignored; `git status --ignored` sanity check.

## Report shape

Per repo: deleted (with merge evidence), kept (with the work item justifying it), decisions made.
A deletion without stated merge evidence is not done.

## Common mistakes

- Trusting `git branch --merged` on a squash-merge workflow — its misses are the #1 wrong-delete.
- Deleting a worktree with uncommitted changes — `git status` inside it first; stash nothing, decide.
- Cleaning only the repo you're in when the setup is multi-repo — sweep all sibling repos asked for.
