---
name: duck-split
description: Hold a branch, PR or document to the one thing it was opened for; nothing rides along, nothing falls off. Use when the user asks what in a branch, PR, document or plan does not belong to the original task, asks to extract, split or move part of it into its own branch, PR or document, or whether it still carries only what it was meant to.
---

# Duck Split

Expect a unit of work to carry parts that belong elsewhere. Sort it against the unit's intent, part
by part, and show that the pieces sum to the original before anything leaves it.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
A question ("what doesn't belong?") gets the classification and no edits. An instruction to
extract authorizes creating the new units only; removing the moved parts from the original needs an
explicit removal instruction ("cut it from here" or any paraphrase). A unit others already hold is
not rewritten even then: report it and leave the choice to the owner. Pushing, force-pushing,
publishing a unit and every forge action each need their own authorization.

## Name the intent

Use the recorded intent: the [`duck-frame`](../duck-frame/SKILL.md) outcome, the work item, or the
unit's own title and description. With none recorded, state the intent its first parts imply as an
assumption and classify against that. A doubt about the intent itself is not a scope finding; leave
it open.

## Judge each part

Read part by part — a hunk, a section, a plan item — not commit by commit or file by file.

- **Belongs**: removing it weakens the intent. A test, fixture or migration the change needs in
  order to work belongs with it.
- **Does not belong**: the intent survives without it. Name where it would go. A good fix found
  on the way still does not belong.
- **Unsure**: it serves both, or a named fact would decide it. Unsure stays.

Answer two questions: does the unit carry only its intent, and does it carry all of it. Stop here
unless extraction was asked for.

## Extract

1. Back up the original in a copy or ref this pass never deletes; confirm it resolves before
   touching anything else.
2. Build one new unit per destination from the original's parts. A part that cannot stand without
   the rest, or collides with a sibling, depends on another new unit; say which and why.
3. Only on a removal instruction, take the moved parts out of the original. Otherwise report that
   those parts now exist in two places.
4. Prove nothing was lost: recombine every resulting unit and compare with the backup, counting
   each source part once (a copy left in the original counts as the original's). Then run each
   unit's checks alone; one that passes only beside its sibling depends on it: return it to step 2
   as a dependency, or fold the two.
5. Report what each unit carries and sits on, the backup, the comparison, the checks, whether the
   original was rewritten, and the publishing steps left unrun. Once the comparison passed and the
   units exist, say the backup has done its job so the next sweep can retire it.

## On a git branch

- Take the base from `git merge-base`, not from a base branch that has moved. Include staged,
  uncommitted and untracked work. For an open PR, compare the local branch with the pushed head
  and report what exists on one side only.
- The backup is a ref at the current tip with staged, uncommitted and untracked work committed
  onto it; a stash will not do, since the comparison reads commits. Those files stay uncommitted
  in the checkout and are the one difference the comparison may show: name each.
- Ignored files stay out of the backup, and a checkout overwrites one whose path the target tracks.
  List `git status --ignored`, and build the new branches in a separate worktree so this checkout
  never switches.
- Split a mixed commit with `git apply --cached <patch>` over a patch holding the selected hunks,
  never `git add -p`.
- Compare against the backup merged with the base the new branches sit on, or a base that moved
  since the fork reads as loss. For a stack, diff that against the top; for separate branches,
  merge them all onto a scratch branch from the base and diff that.
- With the removal instruction, push and forge authority, rebase each stacked layer with
  `git rebase --onto <new-parent> <old-fork-point> <layer>`, the fork point read from the backup
  or the reflog, never guessed from a parent that moved. Where the layers are open PRs, repoint
  each base before any force-push, or the forge marks a child whose commits its base reaches as
  merged and may delete its branch.
- The backup's commits land under new SHAs, so [`duck-sweep`](../duck-sweep/SKILL.md) will find it
  Unproven: name it in the report as the work item its Unmerged path reads, with the comparison
  result as the decision that lets it be deleted.
