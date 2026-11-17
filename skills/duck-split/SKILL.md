---
name: duck-split
description: Hold a branch, PR or document to the one thing it was opened for; nothing rides along, nothing falls off. Use when the user asks what in a branch, PR, document or plan does not belong to the original task, asks to extract, split or move part of it into its own branch, PR or document, or whether it still carries only what it was meant to.
---

# Duck Split

Expect a unit of work to carry parts that belong elsewhere. Sort the unit part by part against its
intent. Before any part leaves, show the pieces sum to the original.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

A question ("what doesn't belong?") gets the classification and no edits. An instruction to
extract authorizes only the new units. Removal of the moved parts from the original needs an
explicit removal instruction ("cut it from here" or any paraphrase). Even then, do not rewrite a
unit that others hold: report it and leave the choice to the owner. A push, a force-push, the
publication of a unit and every forge action each need their own authorization.

## Name the intent

Use the recorded intent: the [`duck-frame`](../duck-frame/SKILL.md) outcome, the work item, or the
unit's title and description. If none is recorded, state the intent its first parts imply as an
assumption and classify against it. A doubt about the intent itself is not a scope finding; leave
it open.

## Judge each part

Read part by part (a hunk, a section, a plan item), not commit by commit or file by file.

- **Belongs**: its removal weakens the intent. A test, fixture or migration the change needs to
  work belongs with it.
- **Does not belong**: the intent survives without it. Name where it goes. A good fix found on the
  way still does not belong.
- **Unsure**: it serves both, or a named fact decides it. Unsure stays.

Answer two questions. Does the unit carry only its intent? Does it carry all of it? Stop here
unless the request asked for extraction.

## Extract

1. Back up the original in a copy or ref this pass never deletes. Confirm the backup resolves
   before anything else.
2. Build one new unit per destination from the original's parts. If a part cannot stand without
   the rest, or collides with a sibling, it depends on another new unit. Say which and why.
3. Only on a removal instruction, take the moved parts out of the original. Otherwise, report that
   those parts now exist in two places.
4. Prove nothing was lost. Recombine every resulting unit and compare with the backup. Count each
   source part once (a copy left in the original counts as the original's). Then run each unit's
   checks alone. A unit that passes only beside its sibling depends on it: return it to step 2 as
   a dependency, or fold the two.
5. Report:
   - what each unit carries and sits on;
   - the backup and the comparison;
   - the checks;
   - whether the original was rewritten;
   - the publishing steps left unrun.

   When the comparison passed and the units exist, say the backup has done its job, so the next
   sweep can retire it.

## On a git branch

- Take the base from `git merge-base`, not a base branch that moved. Include staged,
  uncommitted and untracked work. For an open PR, compare the local branch with the pushed head
  and report what exists on one side only.
- The backup is a ref at the current tip with staged, uncommitted and untracked work committed
  onto it. A stash will not do, because the comparison reads commits. Those files stay uncommitted
  in the checkout and are the only difference the comparison can show: name each.
- Ignored files stay out of the backup. A checkout overwrites an ignored file whose path the
  checked-out branch tracks. List `git status --ignored`. Build the new branches in a separate
  worktree so this checkout never switches.
- Split a mixed commit with `git apply --cached <patch>` over a patch of the selected hunks, never
  `git add -p`.
- Compare against the backup merged with the base the new branches sit on. Otherwise, a base that
  moved since the fork reads as loss. For a stack, diff that merge against the top. For separate
  branches, merge them onto a scratch branch from the base and diff that.
- With the removal instruction and push and forge authority, rebase each stacked layer with
  `git rebase --onto <new-parent> <old-fork-point> <layer>`. Read the fork point from the backup or
  the reflog, never guess it from a parent that moved. If the layers are open PRs, repoint each
  base before any force-push. Otherwise, the forge marks a child merged when its base reaches the
  child's commits, and can delete the child's branch.
- The backup's commits land under new SHAs, so [`duck-sweep`](../duck-sweep/SKILL.md) finds the
  backup Unverified. In the report, name it as the work item its Unverified path reads, with the
  comparison result as the decision that permits its deletion.
