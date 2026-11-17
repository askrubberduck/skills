---
name: duck-run
description: Challenge the goal, shape the plan, build it, and make it prove itself; local means local. Use when the user asks to duck a task, apply selected findings, or carry work through the delivery flow; when a review came back REJECT and the work must be fixed; or when the user says a result is wrong or not what they wanted and asks for it fixed, even when the fix looks like one line. Continue to independent review and landing only within the authorized endpoint.
---

# Duck Run

Own the whole authorized task. Carry the outcome, constraints, candidate, valid evidence and next
action across stages. A skill's finding is a handoff to this caller, not a reason to
ask for another go-ahead.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

If the host forbids edits, as a plan-only mode does, say so once. Finish the analysis it permits
and leave the mode alone. Findings are not a plan awaiting approval.

## Scope, endpoint and isolation

Read the owner's existing authority first. Local implementation ends with a verified local
candidate; report-only work ends with findings or a plan. Commit, PR, push and merge are distinct
actions: perform each only when authorized, under repository rules. A passed review does not expand
that authority. If a release's gate cannot run, the release stays unapproved. Finish the authorized
local work and report what remains.

Use a dedicated worktree or equivalent copy when runs write concurrently or destructive checks
need isolation. A small single-worker edit may use the existing checkout after a state check.
Each run's worktree sits at the repo root, never nested under another run's tree. Preserve
unrelated changes. For test copies, capture dirty candidate content the way
[`duck-split`](../duck-split/SKILL.md) does — a ref, not a stash — and verify it. Step out of a
worktree before you delete it.

## 1. Frame first

Load [`duck-frame`](../duck-frame/SKILL.md) (the Skill tool, or read its SKILL.md) and carry it to
its exit state before any edit to the candidate; a frame written from memory is not a frame. It
establishes or reuses the outcome, flow, constraints and plausible paths at the depth of a
standalone run; only its short form is quick. If it refutes the goal, recommend the corrected path;
never silently substitute a new goal. READY continues. CUT ends work demonstrably unnecessary under
the owner's criteria. OWNER DECISION goes to [`duck-decide`](../duck-decide/SKILL.md) and holds
only the dependent work.

## 2. Plan with proof

For substantial or uncertain work, load [`duck-plan`](../duck-plan/SKILL.md). A narrow task may
keep a short plan in the work record: intervention, affected invariant, falsifying check and
expected final observation. Reuse a settled plan while its scope and assumptions hold.

Select challenge approach and participants from [challenge
selection](../duck-review/references/challenge.md), and record actual participation. Attack
consequential assumptions with a falsifying experiment before you build on them. If it refutes the
decomposition, plan again; agreement alone never makes a plan ready. Bound critique as `duck-plan`
specifies.

## 3. Execute the surviving design

For each meaningful behavior change, in order:

1. Establish the failing outcome.
2. Implement the minimum that satisfies it.
3. Apply [`duck-shape`](../duck-shape/SKILL.md).
4. Take the unit's diff through [the prose bar](../duck-dry/references/bar.md).

Use existing checks where possible; trivial edits need no invented test. Apply shape and dry within
the unit before later work depends on it, as their own commits when commits are authorized; the
landing may squash them. Tidy first when that makes this change easier, after when it makes the
next one easier, never on speculation.

Remove superseded paths once the replacement is verified. Preserve required compatibility and
public contracts. Add no speculative shims, and delete no real edge case because scope is unclear.
An unrelated restructure is separate work. Selected finding IDs delimit repairs; the receipt gives
each as applied, skipped with its reason, or parked.

Use staged or parallel execution only where it helps independent work.
[`duck-diet`](../duck-diet/SKILL.md) governs context and model routing; a cheap worker still needs
a check that catches its failure. Converge parallel edits, one owner per file (the doer or one worker), before you verify
the assembled candidate.

## 4. Verify and try to break it

Use [`duck-race`](../duck-race/SKILL.md) in rally mode when requested, project policy
requires it, or a demonstrated testing blind spot or repeated missed defect class needs
cross-family tests. Run it against the contract before final proof and review. Include its
receipt, or record why a required rally could not run. Ordinary verified work needs no rally.

Run relevant project gates and read their outputs and resulting state, not only exit codes. Then
load [`duck-proof`](../duck-proof/SKILL.md) and run it on the actual candidate. **Any proof or shape
edit returns to affected executable checks before completion or dispatch.** A red check stops new
work on that surface until it is green or its cause is named. If a symptom returns after its fix,
load [`duck-why`](../duck-why/SKILL.md) before the next patch.

Use [`duck-break`](../duck-break/SKILL.md) for requested broad attacks and the dynamic evidence
trust-touching work requires. Match attacks to the artifact: agent behavior trials for skill or
gate changes, recovery tests for claimed recovery. Distribution validation is not behavioral
proof; never label an unrun check passed.

Write handoff evidence under [`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules; a shared
work record may hold the proof, break and plan sections, with exact locations for the consumer.
Preserve essential artifacts before scratch cleanup. An authorized local task may finish here with
its evidence and stated verification limits, without a commit, PR or release verdict.

## 5. Independent review, when requested or required for release

Call [`duck-review`](../duck-review/SKILL.md)'s release-gate path by name; its unscoped default is
a findings pass, which satisfies no gate. Prepare the candidate and evidence first: the exact
commit when commits are authorized, otherwise an explicit, non-landable worktree
snapshot.

Act on the single adjudicated result:

- APPROVE: Continue only to the authorized release action.
- REJECT: Name each substantiated blocker's cause, with [`duck-why`](../duck-why/SKILL.md) when it
  is unestablished. From the first round, repair as [`duck-proof`](../duck-proof/SKILL.md)'s
  repair section requires, then rerun affected verification before the changed candidate is
  reviewed. An owner correction of the result is evidence of the same kind.
- NOTE: Obtain the missing material evidence or criteria, or report which is missing. It is neither
  approval nor a reason to invent a repair, and does not prevent completion of authorized
  local work.

Before a third or later round, record a loop diagnosis and route each cause:

- Contradicted premises go to [`duck-frame`](../duck-frame/SKILL.md).
- A wrong decomposition goes to [`duck-plan`](../duck-plan/SKILL.md).
- Repeated missed cases go to an executable class-level check or a
  [`duck-race`](../duck-race/SKILL.md) rally.
- Rival implementations, or blockers that land on the fixes rather than the original change, go to
  a `duck-race` race of the contested unit.
- Real owner tradeoffs go to [`duck-decide`](../duck-decide/SKILL.md).

Continue review only when a named unresolved cause is shrinking and new evidence will be available.
If blockers from one class repeat, repair the method; do not buy another round on the same basis.

### Review-loop ownership and stable criteria

The coordinating caller, named in the existing work record and across handoffs, owns convergence.
Reviewers produce evidence and judgments, not a backlog for automatic execution. The caller resolves
technical findings within its authority, tracks causes and owns the next action. Only the owner
settles a genuinely new product, policy or scope decision.

Before the first review, record the outcome, non-goals, required contracts, acceptance checks,
release policy, participants and effort bound, and carry that baseline across rounds. The round
ceiling is `[bounds].review_rounds`, or `[bounds].trust_rounds` for trust-touching work, as
`dispatch.py` enforces it, unless the owner or repository sets another. Inside it, the stop rule
is evidence, per the challenge reference. A new frame, reviewer or task name does not reset it.
Transport retries follow [`duck-review`](../duck-review/SKILL.md)'s separate bounded outage rule.

Track findings by stable cause with the violated criterion, evidence, disposition and closure
check. A reworded finding is not new. Reopen a closed cause only with contrary evidence or an
impacting change. A newly discovered defect against an existing contract can still block; a new
preference, feature or unrelated cleanup is separate proposed work, not a stronger acceptance bar.
Do not silently promote SHOULD/NOTE items into required repairs.

At the bound, do not dispatch again. Preserve the candidate, unresolved evidence and next action;
the release stays unapproved. If new evidence undermines the agreed goal, report the contradiction
and hold dependent work without inventing replacement criteria. Without the owner, make authorized
technical decisions and continue independent work; do not guess the owner's tradeoff or wait for
agreement. A later explicit continuation can supply a new bound; elapsed time cannot.

## 6. Land only when authorized

Use [`duck-land`](../duck-land/SKILL.md) for an authorized merge after its gate passes. A request to
push or prepare a PR authorizes only that action; it is not a merge request. New code or a changed
integration invalidates the affected authorization.

## Continuation

New owner input steers the current task; a narrowed or withdrawn authority takes effect
immediately. Reuse settled decisions. A tool outage gets a bounded retry or another authorized
mechanism; a permission rejection does not. Continue until the authorized endpoint, a genuine owner
decision on dependent work, an external block, an instruction to stop, or a real scheduled handoff.

At a context boundary, follow [`duck-diet`](../duck-diet/SKILL.md)'s first runtime rule. Close with
what changed, what was tested, and what remains unproven or unauthorized.
