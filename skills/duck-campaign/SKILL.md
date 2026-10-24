---
name: duck-campaign
description: Carve a grand vision into independent workstreams that ship without waiting on each other. Use when the user asks to start a campaign, execute all plannable work, turn a vision, a backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
---

# Duck Campaign

Turn the requested outcomes into a manageable set of workstreams and carry each to its authorized
endpoint. Split work when separate execution, ownership or release helps; two separately shippable
small changes are not by themselves two packets.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
Carry existing authority through the campaign. Local work ends with verified local changes;
commits, PRs, pushes and merges require their own authorization. A planning-only request ends with
the plan. Keep unresolved decisions attached to their dependent work.

## Establish the work that is needed

Use [`duck-scan`](../duck-scan/SKILL.md) to locate current work and read relevant product
constraints and source. Reuse existing records and decisions. Delegate bounded read-only
investigation only when it helps.

Apply [`duck-cut`](../duck-cut/SKILL.md)'s existence check to the candidates: what required outcome
is missing, what already satisfies it, and which findings share a cause? Remove speculative or
superseded work. Recheck a candidate that grows; do not quietly expand the user's goal.

Use [`duck-frame`](../duck-frame/SKILL.md) to settle shared contracts and consequential unknowns
before dependent plans, reusing valid design decisions rather than framing each packet afresh. Keep
the campaign's shared contracts in its existing work record, creating one only when no adequate home
exists. An owner decision blocks only the work that depends on it; continue other settled,
authorized work even before the roster is divided into packets.

## Group by execution needs

Keep related changes together when they share a rule, verification path or small delivery surface;
repeated findings at one boundary get one repair with several cases. Separate work with different
owners, release timing, material risks or genuinely independent execution. Avoid overlapping
ownership of files edited concurrently.

Each packet names its outcome, affected scope, dependencies and completion check, and has an
independently verifiable finish, not merely a named code area. Use the existing work-item
convention; a small campaign may need only one record with several units, not one directory,
branch, design and plan per checklist item.

Plan substantial or uncertain packets with [`duck-plan`](../duck-plan/SKILL.md); a small settled
unit can keep its steps and checks in the campaign record as [`duck-run`](../duck-run/SKILL.md)
permits. Preserve independent input required by repository policy and record actual participation;
solo work is not an independent challenge.

## Execute and keep the roster current

Use [`duck-run`](../duck-run/SKILL.md) for execution and verification, passing the outcome, valid
shared decisions and remaining authority. Parallelize only independent work that benefits from it;
isolate concurrent writers or destructive checks as that skill requires. Apply
[`duck-diet`](../duck-diet/SKILL.md) to keep dispatch overhead proportionate. Send every packet
review through [`duck-review`](../duck-review/SKILL.md), never a reviewer CLI run by hand: its
ledger, round bound, loop diagnosis and outage parking exist only there.

Maintain one roster in the durable work record: packet, state, dependencies, evidence and next
action, plus branch/worktree when used. Finish a ready unit and continue to the next without another
go-ahead. Do not open a new packet while another waits on review or integration this run could
finish first. Reconcile concurrent changes and verify the combined result before completion.

Before a turn ends with work still running, say in one line what runs, what each item waits on, and
which event brings the next update and roughly when; on each completion, one roster line. Shut a
worker down once its packet lands or hands back, and flag one idle with uncommitted changes.

Count each worker message once: a status notice older than your last instruction to that worker is
a repeat, and a cut-off report counts only after its tail arrives. Brief each worker so a
replacement can start from the brief alone — worktree, base, candidate identity, findings with
evidence paths, gates and rules — and ask for reports that lead with gates and unsettled items.

When blocked, record the actual blocker and a concrete next action, and continue independent work;
do not invent consent, rescope away a required outcome or retry an unchanged failure indefinitely.
Contrary execution evidence, or the owner correcting a result, reopens the affected shared design
before dependent work continues. Stop when the authorized work is complete or all remaining work is
blocked, and state which. A "complete" on a broad request lists what it left out and why.

At a context boundary, preserve the roster, candidate identities and valid evidence. A scheduled
continuation needs a supported authorized mechanism and confirmed booking; a written next step is
not one. Use [`duck-sweep`](../duck-sweep/SKILL.md) for already-authorized cleanup: inventory
untracked and ignored files before removal, preserve unknown files, and verify kept work at its
durable home. Do not delete work just to empty the roster.
