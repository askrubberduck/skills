---
name: nuclear-land
description: Merge approved work, update project records, and clean up its branch and worktree. Use when a change has passed its review gate, the user asks to land or merge it, a gate-passed PR is ready, or merged work was never recorded in status or outcome documentation.
---

# Nuclear Land

The ship step: gate passed → merge → record → clean. A merge without a recorded outcome is work
the repo forgot; a record without a verified merge is fiction.

Use `$askrubberduck:<name>` as the canonical bundled-skill reference. Before its step starts, resolve
it with the active host's discovered invocation syntax. Preserve `askrubberduck:` when the host
exposes plugin namespaces; use `$<name>` or `<name>` when it exposes skills unqualified or for a
standalone install. If no installed form resolves, stop and name the missing skill; never retry
under another name after that step's side effects start.

## Preconditions (fail closed — any miss stops the landing)

- The gate actually passed per the repo's policy, including a proven different-family approval from
  `$askrubberduck:nuclear-review`. "Probably fine" is not a gate state.
- **The branch head equals the reviewed SHA.** Delegated builders commit on detached HEADs and
  wrong branches; confirm branch, origin, and PR head all point at what was reviewed.
- Re-verify the base: `git fetch`, compare origin/<base> to what was branched from; if it advanced,
  integrate and re-run the repo's checks before merging.
- CI green on the exact head being merged.

## Land

1. Merge per the repo's policy (squash-merge the PR, or direct push where that is the standard).
2. **Confirm the merge landed**: the new SHA is on the default branch and matches what you merged —
   read it back, don't assume.
3. Record the outcome where the repo keeps truth: shipped log / status doc / delivery board — with
   PR number, merged SHA, and what changed. One recorded outcome per landing.
4. Close or queue obligations the change touched — the doer never closes an item that needs the
   owner's sign-off; queue those (`$askrubberduck:nuclear-decide` presents them).
5. Clean up: delete the merged branch and its worktree (`$askrubberduck:nuclear-sweep` discipline —
   verify merged, then delete). End the session at this boundary; landing is a stage transition.

## Common mistakes

- Recording the outcome before step 2's read-back — squash merges mint a new SHA; record the one
  that actually landed, not the branch head.
- Landing two changes in one record — one packet, one landing, one recorded outcome.
- Leaving the worktree "for reference" — the record is the reference; the worktree is debt.
- Skipping the base re-verify because the branch is "fresh" — fresh was true when you last fetched.
