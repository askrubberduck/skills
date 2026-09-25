---
name: duck-sweep
description: Clean out stale branches, worktrees, checkouts, scratch directories, and ignore rules; the pond stays clean. Use when the user asks for repository cleanup across one or more repos, or when stale worktrees and temporary artifacts have accumulated after merged work.
---

# Duck Sweep

Multi-repo cleanup with a hard rule: **verify merged before delete, and keep nothing "just in
case"** — unmerged work gets an explicit merge-or-delete decision, not a reprieve. One
preservation invariant covers every deletion path: an entry marked **keep** relocates to its
durable home and is verified there before its container is removed.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Sweep per repo

1. Inventory: `git fetch --prune` first so remote state is current, then `git worktree list` and
   `git branch -vv`. Use absolute paths; don't cd back and forth. An unreachable remote or an
   unreadable worktree is recorded and the sweep carries on around it. A multi-repo setup means
   every sibling repo asked for, not only the one you are in.
2. Classify: **delete only what is provably preserved elsewhere**.
   - **Preserved** — the branch's commits are reachable from `origin/<default>`
     (`git branch --merged origin/<default>` is the proof). These outlive their ref. Delete with
     `-D`: `-d` re-checks against HEAD or the upstream and refuses when either is behind.
   - **Preserved by record** — squash-merged, rebased, or cherry-picked, *and* the project's
     outcome record names the landed SHA and the candidate SHA for this branch (`duck-land` writes
     them there for exactly this reason). The record is evidence the objects cannot supply. Confirm
     the landed SHA is on `origin/<default>` **and the branch tip is still that candidate**, then
     delete. A branch that gained commits after it landed is Unproven, whatever the record says.
   - **Not preserved** — squash-merged, rebased, or cherry-picked with **no such record**: the
     default branch holds an equivalent *new* commit, never these objects, and no merge metadata
     recovers the link — PR records, `git cherry`, tree diffs, and revert greps can each produce a
     false positive, and a false positive here is destroyed work. Do not build a cleverer
     classifier; treat it as Unproven.
   - **Unproven** → the Unmerged path: open the work item and decide on its state. Merge: land
     it, then reclassify by the paths above — Preserved when ancestry shows it, Preserved by
     record when the landing was a squash — and delete under that path. Delete: record the
     decision, then `-D`.
3. Delete — **but check the worktree for untracked and ignored files first**: `git status --short
   --untracked-files=all --ignored`. Plain `git status` hides ignored files, so `git worktree
   remove` exits 0 and takes the `.env`, local config, or credentials living there with it. Drop
   entries reproducible from tracked content — build output, caches, installed dependencies —
   which the repo's own ignore rules already name as artifacts. Every other `??` or `!!` entry
   gets an explicit keep-or-delete decision before removal: it may exist nowhere else, so
   **unknown means keep, and only the owner may decide to delete one**: queue it via `duck-decide`
   and keep the file meanwhile. Then — only
   once nothing in the worktree remains marked keep — `git worktree remove <path>`,
   `git branch -D <branch>` against the classification above, and `git worktree prune` for
   leftovers.
4. Scratch dirs: hunt ad-hoc temp dirs outside the sanctioned scratchpad (e.g. `~/<repo>-tmp*`,
   `/tmp/<repo>*`, stray review-tmp dirs; the sanctioned scratchpad itself is disposable by design
   and never swept per-file). A non-git dir has no merge evidence, so inventory every entry
   including dotfiles (`ls -laR`); each entry takes step 3's keep-or-delete decision. The
   preservation invariant applies; `rm -rf` the dir only when nothing in it remains marked keep.
5. `.gitignore` audit: worktree dirs (`.worktrees/`), build output, and local-config paths present
   and ignored; `git status --ignored` sanity check.

## Report shape

Per repo: deleted (with merge evidence), kept (with the work item justifying it), decisions made.
A deletion without stated merge evidence is not done.

