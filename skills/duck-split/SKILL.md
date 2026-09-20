---
name: duck-split
description: Hold a branch to the one change it was opened for; whatever hitched a ride gets a branch of its own, and nothing falls off on the way. Use when the user asks what in a branch or PR does not belong to the original task, asks to extract a change into its own branch or PR, to split a branch into separate or stacked ones, or whether a branch or open PR still carries only what it was meant to.
---

# Duck Split

A branch collects work that belongs elsewhere: a fix found on the way, a refactor the reviewer
asked to separate, a migration from another line of work. Sort it against the branch's intent,
hunk by hunk, and move what does not belong without losing a line of it.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
The check is the default and changes nothing. Extraction rewrites branches, so it needs its own
authorization; pushing, opening a PR, changing a PR's base and force-pushing each need theirs.

## Name the intent

Use the recorded intent: the `duck-frame` outcome, the work item, or the PR title and body. With
none recorded, state the intent the first commits imply as an assumption and classify against
that; never sort hunks against an intent nobody can read.

## Check

Take the base from `git merge-base`, not from a base branch that has moved. Include staged,
uncommitted and untracked work. For an open PR, compare the local branch with the pushed head and
report what exists on one side only.

Classify every hunk, not every commit or file; one commit often mixes two intents.

- **Belongs**: cite the part of the intent it serves. A test, fixture or migration the change
  needs in order to work belongs with it.
- **Does not belong**: name where it would go. A good fix found on the way still does not belong.
- **Unsure**: name the fact that would decide it.

Answer two questions: does the branch carry only its intent, and does it carry all of it. Stop
here unless extraction was requested.

## Extract

1. Create a backup ref at the current tip and commit staged, uncommitted and untracked work onto
   it. A stash will not do: step 6 compares commits and cannot see one. Confirm the ref resolves
   before touching anything else. Ignored files stay out of the backup, and a checkout overwrites
   one without asking when the target tracks its path: build the new branches in a separate
   worktree so this checkout never switches, and list `git status --ignored` first.
2. Place each extracted change as told: on the head of the base, or stacked. When not told, a
   change that applies to the base and passes its checks alone goes on the base; one that needs
   the rest, or conflicts with a sibling, is stacked. Say which and why.
3. Build each branch from hunks. Cherry-pick a commit that holds one intent; split a mixed one by
   applying the selected hunks to the index. Use no interactive command.
4. Rebuild the working branch without the extracted hunks. A branch others have pulled is not
   rebuilt, and reverting there makes the extracted commit vanish when the branches meet again:
   report it and leave the choice to the owner.
5. For a stack, rebase each layer with `git rebase --onto <new-parent> <old-fork-point>`, the
   fork point read from the backup or the reflog, never guessed from a parent that already
   moved. Where the layers are open PRs, repoint each base before any force-push: a forge that finds a child's commits
   reachable from its base marks the child merged and may delete its branch.
6. Prove nothing was lost. Compare against the backup merged with the base the new branches
   sit on; a base that moved since the fork is otherwise reported as loss. Work committed onto
   the backup only for safekeeping, and still uncommitted in the checkout, is the one difference
   allowed: name each such file. For a stack, diff
   that against the top. For separate branches, merge them all onto a scratch branch from the
   base and diff that. Then run each branch's checks alone; one that passes only beside its sibling is not
   independent.
7. Report what each branch now carries, its checks and the backup ref. Never delete the backup
   in the same invocation. Its commits land under new SHAs, so `duck-sweep` will find it
   unproven and ask.

## Common mistakes

- Deleting an unrelated change instead of moving it. Removal is not extraction; the work
  is gone rather than moved.
- Narrowing a commit to the files its title names without reading what else it carried.
