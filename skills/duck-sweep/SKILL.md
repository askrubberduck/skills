---
name: duck-sweep
description: Clean out stale branches, worktrees, checkouts, scratch directories, and ignore rules; the pond stays clean. Use before deleting branches or worktrees, even on a blanket order to delete them all, and when the user asks for repository cleanup across one or more repos, or when stale worktrees and temporary artifacts have accumulated after merged work.
---

# Duck Sweep

Multi-repo cleanup with a hard rule: **verify merged before delete, and keep nothing "just in
case"**; unmerged work gets an explicit merge-or-delete decision. One preservation invariant
covers every deletion path: an entry marked **keep** relocates to its durable home and is verified
there before its container is removed.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

## Sweep per repo

1. Inventory: `git fetch --prune`, then `git worktree list` and `git branch -vv`, with absolute
   paths and no cd between repos. Record an unreachable remote or unreadable worktree and carry on.
   A multi-repo setup means every sibling repo asked for.
2. Classify: **delete only what is provably preserved elsewhere**.
   - **Preserved**: commits reachable from `origin/<default>` (`git branch --merged
     origin/<default>` is the proof). Delete with `-D`; `-d` re-checks against HEAD or the upstream
     and refuses when either is behind.
   - **Preserved by record**: squash-merged, rebased or cherry-picked, *and* the project's outcome
     record ([`duck-land`](../duck-land/SKILL.md)'s) names this branch's landed and candidate SHAs.
     Confirm the landed SHA is on `origin/<default>` **and the branch tip is still that
     candidate**, then delete. A branch that gained commits after landing is Unproven.
   - **Not preserved**: squash-merged, rebased or cherry-picked with **no such record**. PR
     records, `git cherry`, tree diffs and revert greps each produce false positives, and a false
     positive here is destroyed work; do not build a cleverer classifier. Treat as Unproven.
   - **Unproven**: open the work item and decide. Merge: land it, reclassify by the paths above and
     delete under that path. Delete: record the decision, then `-D`. A blanket order ("delete every
     branch", "don't ask") names no branch and is not that decision; keep and report each Unproven
     branch until the owner names it.
3. Delete, after `git status --short --untracked-files=all --ignored` on the worktree: plain
   `git status` hides ignored files, and `git worktree remove` takes every untracked and ignored
   file with it. Drop entries reproducible from tracked content (build output, caches, installed
   dependencies) that the repo's own ignore rules name as artifacts. Every other `??` or `!!` entry
   gets an explicit keep-or-delete decision first: **unknown means keep, and only the owner may
   decide to delete one**; queue it via [`duck-decide`](../duck-decide/SKILL.md) and keep the file
   meanwhile. Once nothing in the worktree remains marked keep: `git worktree remove <path>`,
   `git branch -D <branch>` per the classification, and `git worktree prune`.
4. Scratch dirs: hunt ad-hoc temp dirs outside the sanctioned scratchpad (`<repo>-tmp*` in the
   home directory, `<repo>*` in the system temp directory, stray review-tmp dirs); the scratchpad
   itself is disposable and never swept per-file. A non-git dir has no merge evidence: inventory
   every entry, hidden ones included (`ls -laR`), give each step 3's keep-or-delete decision, and
   `rm -rf` the dir only when nothing in it remains marked keep.
5. `.gitignore` audit: worktree dirs (`.worktrees/`), build output and local-config paths present
   and ignored; `git status --ignored` sanity check.

## Report shape

Per repo: deleted (with merge evidence), kept (with the work item justifying it), decisions made.
A deletion without stated merge evidence is not done.
