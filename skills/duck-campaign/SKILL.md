---
name: duck-campaign
description: Carve a grand vision into independent workstreams that ship without waiting on each other. Use when the user asks to start a campaign, execute all plannable work, turn a vision, a backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
---

# Duck Campaign

Turn the requested outcomes into a manageable set of workstreams and carry each to its authorized
endpoint. Split work when separate execution, ownership or release helps; the ability to ship two
small changes separately is not by itself a reason to create two packets.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
Carry existing authority through the campaign. Local work ends with verified local changes;
commits, PRs, pushes and merges require their own authorization. A planning-only request ends with
the plan. Keep unresolved decisions attached to their dependent work.

## Establish the work that is needed

Use `duck-scan` to locate current work and read relevant product constraints and source. Reuse
existing records and decisions. Delegate bounded read-only investigation only when it helps;
a campaign does not need a scout fleet merely to begin.

Apply `duck-cut`'s necessity check to the candidates: what required outcome is missing, what already
satisfies it, and which findings share a cause? Remove speculative or superseded work. Recheck a
candidate that grows; do not quietly expand the user's goal.

Use `duck-frame` to settle shared contracts and consequential unknowns before dependent plans.
Reuse valid design decisions instead of framing each packet afresh. Keep the campaign's shared
contracts in its existing work record, creating a record only when no adequate home exists.
CUT ends unnecessary work. An owner decision blocks the work that depends on it; continue other
settled, authorized work when available, even if the roster has not yet been divided into packets.

## Group by execution needs

Keep related changes together when they share a rule, verification path or small delivery surface.
Repeated findings at one boundary usually need one repair with several cases, not one packet per
finding. Conversely, separate work with different owners, release timing, material risks or genuinely
independent execution. Avoid overlapping ownership of files that will be edited concurrently.

Each packet names its outcome, affected scope, dependencies and completion check. Use the existing
work-item convention; a small campaign may need only one record with several units. Do not create
one directory, branch, design and plan per checklist item. A packet must have an independently
verifiable finish, not merely be a named code area.

Plan substantial or uncertain packets with `duck-plan`; a small settled unit can keep its concrete
steps and checks in the campaign record as `duck-run` permits. Preserve independent input required
by repository policy. Record actual participation; solo work is not an independent challenge.

## Execute and keep the roster current

Use `duck-run` for execution and verification, passing the outcome, valid shared decisions and
remaining authority. Parallelize only independent work that benefits from it; otherwise execute
sequentially. Isolate concurrent writers or destructive checks as that skill requires. Apply
`duck-diet` to preserve useful context and keep dispatch overhead proportionate.

Maintain one roster in the durable work record: packet, state, dependencies, evidence and next
action; include branch/worktree only when used. Finish a ready unit and continue to the next without
another go-ahead. Reconcile concurrent changes and verify the combined result before completion.

When blocked, record the actual blocker and a concrete next action. Continue independent work;
do not invent consent, rescope away a required outcome or retry an unchanged failure indefinitely.
Contrary execution evidence reopens the affected shared design before dependent work continues.
Stop when the authorized work is complete or all remaining work is blocked, and state which.

At a context boundary, preserve the roster, candidate identities and valid evidence using
`duck-diet`. Schedule a continuation only through a supported, authorized host mechanism and verify
it was booked. Do not claim that a written next step schedules anything. Use `duck-sweep` for
already-authorized cleanup when needed; do not delete work just to make the roster appear empty.
