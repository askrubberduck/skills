---
name: nuclear-sweep
description: Clean stale branches, worktrees, checkouts, scratch directories, and ignore rules. Use when the user asks for repository cleanup across one or more repos, or when stale worktrees and temporary artifacts have accumulated after merged work.
---

# Worktree and Branch Hygiene Sweep

Multi-repo cleanup with a hard rule: **verify merged before delete, and keep nothing "just in
case"** — unmerged work gets an explicit merge-or-delete decision, not a reprieve.

## Sweep per repo

1. Inventory: `git worktree list`, `git branch -vv`, `git fetch --prune` first so remote state is
   current. Use absolute paths; don't cd back and forth.
2. Classify with `git branch --merged origin/<default>`, delete with **`git branch -d`**, never `-D`.
   **Both halves are load-bearing.** `-d` alone tests merged-into-**HEAD-or-upstream**, not into the
   default branch: standing on a feature branch that happens to contain the work, `-d` deletes a
   branch that never reached the default branch at all (reproduced — `git branch -d feature` succeeds
   from an `integration` branch while `main` has none of it). `--merged origin/<default>` pins the
   reference; `-d` is the safe delete that refuses anything that reference misses.
   - **Listed and `-d` succeeds** → the commits are ancestors of the default branch and outlive the
     ref. Done.
   - **Not listed, or `-d` refuses** → squash-merged, rebased, cherry-picked, or genuinely unmerged.
     Open the work item, decide merge-or-delete on its state, record the decision, then `-D`.

   Do not build a cleverer classifier. Six were tried and each had a demonstrated counter-example:
   name-matched PRs, `git cherry` (patch-ids normalize whitespace), empty tree diffs, PRs merged into
   an unmerged parent, reverted squash merges, and revert-message greps. The built-in pair decides the
   one thing that is decidable and routes the rest to a human — which is the answer, not a fallback.
3. Delete — **but check the worktree for untracked and ignored files first**:
   `git status --short --untracked-files=all --ignored`. Plain `git status` hides ignored files, so
   `git worktree remove` exits 0 and takes the `.env`, local config, or credentials living there with
   it. Any `??` or `!!` entry gets an explicit keep-or-delete decision before removal — those files
   exist in exactly one place by definition. Then `git worktree remove <path>`, `git branch -D
   <branch>`, and `git worktree prune` for leftovers.
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
