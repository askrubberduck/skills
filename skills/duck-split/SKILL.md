---
name: duck-split
description: Hold a branch, PR or document to the one thing it was opened for; nothing rides along, nothing falls off. Use when the user asks what in a branch, PR, document or plan does not belong to the original task, asks to extract, split or move part of it into its own branch, PR or document, or whether it still carries only what it was meant to.
---

# Duck Split

A unit of work collects what belongs elsewhere. Sort it against the unit's intent, part by part,
and show that the pieces sum to the original before anything leaves it.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
A question ("what doesn't belong?") gets the classification and no edits. An instruction to
extract authorizes creating the new units only. Taking the moved parts out of the original needs
an explicit removal instruction, "cut it from here" or any paraphrase; "extract it" alone is not
one. A unit others already hold is not rewritten even then: report it and leave the choice to the
owner. Pushing or force-pushing anything, publishing a unit and every forge action each need
their own.

## Name the intent

Use the recorded intent: the `duck-frame` outcome, the work item, or the unit's own title and
description. With none recorded, state the intent its first parts imply as an assumption and
classify against that; never sort against an intent nobody can read. A doubt about the intent
itself is not a scope finding; leave it open.

## Judge each part

Read part by part — a hunk, a section, a plan item — not commit by commit or file by file; one
commit often mixes two intents.

- **Belongs**: removing it weakens the intent. A test, fixture or migration the change needs in
  order to work belongs with it.
- **Does not belong**: the intent survives without it. Name where it would go. A good fix found
  on the way still does not belong.
- **Unsure**: it serves both, or a named fact would decide it. Unsure stays.

Answer two questions: does the unit carry only its intent, and does it carry all of it. Stop here
unless extraction was asked for.

## Extract

1. Back up the original first, in a copy or ref this pass never deletes. Confirm it resolves
   before anything else is touched.
2. Build one new unit per destination from the original's parts. A part that cannot stand
   without the rest, or collides with a sibling, depends on another new unit; say which and why.
3. Only on a removal instruction, take the moved parts out of the original.
   Otherwise the original keeps them, and the report says those parts now exist in two places.
4. Prove nothing was lost: recombine every resulting unit and compare with the backup, counting
   each source part once — when extraction left a copy in the original, the original's copy is
   the one in the comparison, not both. Then run each unit's checks alone; one that passes only
   beside its sibling depends on it: return it to step 2 as a dependency, or fold the two.
5. Report what each unit carries and sits on, the backup, the comparison, the checks, whether the
   original was rewritten, and the publishing steps left unrun. Once the comparison passed and
   the units exist, the backup has done its job: say so, so the next sweep can retire it.

## On a git branch

- Take the base from `git merge-base`, not from a base branch that has moved. Include staged,
  uncommitted and untracked work. For an open PR, compare the local branch with the pushed head
  and report what exists on one side only.
- The backup is a ref at the current tip with staged, uncommitted and untracked work committed
  onto it. A stash will not do: the comparison reads commits and cannot see one. Those files stay
  uncommitted in the checkout, so they are the one difference the comparison may show: name each.
- Ignored files stay out of the backup, and a checkout overwrites one without asking when the
  target tracks its path. List `git status --ignored`, and build the new branches in a separate
  worktree so this checkout never switches.
- Split a mixed commit by applying the selected hunks to the index: `git apply --cached <patch>`
  over a patch holding those hunks, never `git add -p`, which needs a terminal.
- Compare against the backup merged with the base the new branches sit on; a base that moved
  since the fork is otherwise reported as loss. For a stack, diff that against the top; for
  separate branches, merge them all onto a scratch branch from the base and diff that.
- With the removal instruction, push and forge authority, rebase each stacked layer with
  `git rebase --onto <new-parent> <old-fork-point> <layer>`, the fork point read from the backup or the
  reflog, never guessed from a parent that already moved. Where
  the layers are open PRs, repoint each base before any force-push: a forge that finds a child's
  commits reachable from its base marks the child merged and may delete its branch.
- The backup's commits land under new SHAs, so `duck-sweep` will find it unproven: name it in
  the report as the work item its Unmerged path reads, with the comparison result as the
  decision that lets it be deleted.
