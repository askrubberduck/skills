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
2. Classify by one invariant: **delete only what is provably preserved elsewhere**.
   - **Preserved** — the branch's commits are reachable from `origin/<default>`
     (`git branch --merged origin/<default>`, then `-d`, never `-D`; `-d` alone checks
     HEAD-or-upstream, a narrower promise than its name). These outlive their ref. Delete.
   - **Not preserved** — squash-merged, rebased, or cherry-picked: the default branch holds an
     equivalent *new* commit, never these objects, and no merge metadata proves otherwise — PR
     records, `git cherry`, tree diffs, and revert greps have all produced false positives that end
     in destroyed work. Do not build a cleverer classifier; route to a decision instead.
   - **Unproven** → the Unmerged path: open the work item, decide merge-or-delete on its state,
     record the decision, then `-D`.
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

- Cleaning only the repo you're in when the setup is multi-repo — sweep all sibling repos asked for.
