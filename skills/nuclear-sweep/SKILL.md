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
2. Classify each branch/worktree:
   - **Merged normally** → `git branch --merged origin/<default>`. The commits reachable from the
     branch tip are ancestors of the default branch, so **they stay reachable after the ref is gone**
     — even a later revert cannot lose them, since the objects live in the default branch's own
     history. One exception, and it is not hypothetical: a branch **reset backwards** still satisfies
     `--merged`, while the commits it was reset away from survive only in its reflog, which
     `git branch -D` destroys. If `git reflog show <branch>` holds commits above the tip, decide
     explicitly instead of deleting.
   - **Squash-merged, rebased, or cherry-picked** → `--merged` misses these: the default branch holds
     an equivalent *new* commit, so the branch's own commits go unreachable when the ref does.
     **Losing them is the intent of a squash merge — what must survive is the content, not the
     granular history.** Delete automatically only when all three hold:
     - the PR merged with **base == the default branch** (`gh pr view --json baseRefName,headRefOid`);
       merged into an unmerged parent it proves nothing about the default branch;
     - `headRefOid` **equals the branch tip** — otherwise the branch gained commits after that merge,
       or the name was reused;
     - **the content is still there**: `git diff origin/<default>..<branch>` adds nothing the default
       tree lacks. A reverted squash merge fails exactly here, which is the point — ancestry stays
       true after a revert, content does not.
     Any of the three failing → the Unmerged path below: decide explicitly and record it.
     Accepted trade, stated once: this deliberately discards intermediate commits, and a branch that
     added a file then reverted it *within its own history* diffs clean and gets deleted. That
     history is what a squash merge exists to drop.
     `git cherry` remains a **hint, never authorization** — patch-ids normalize whitespace, so
     upstream `value = "a b"` versus branch `value = "ab"` reads as contained while the trees differ.
   - **Unmerged** → open the work item it belongs to; decide merge-or-delete on its state
     (superseded/abandoned = delete; live = finish or hand off). Record the decision.
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
