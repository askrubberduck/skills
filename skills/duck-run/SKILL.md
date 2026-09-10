---
name: duck-run
description: Challenge the goal, shape the plan, build it, and make it prove itself; local means local. Use when the user asks to duck a task or carry work through the delivery flow. Continue to independent review and landing only within the authorized endpoint.
---

# Duck Run

Own the whole authorized task. Carry the outcome, constraints, candidate, valid evidence and next
action across stages. A skill returning a finding is a handoff to this caller, not an automatic
reason to ask for another go-ahead.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Scope, endpoint and isolation

Read the user's existing authority first. Local implementation ends with a verified local candidate;
report-only ends with findings or a plan. Commit, PR, push and merge are distinct actions: perform
them only when authorized. A passed review does not expand that authority. A release whose gate
cannot run stays unapproved; finish the authorized local work and report what remains.

Use a dedicated worktree or equivalent copy when runs write concurrently or destructive checks
need isolation. Worktrees are siblings under the repo root, never nested under another run's tree.
A small single-worker local edit can use the existing checkout after checking its state. Preserve
unrelated changes. Worktrees carry committed state only, so capture and verify relevant dirty
candidate content when making test copies. Step out of a worktree before deleting it.

## 1. Ground and challenge

Use `duck-frame` to establish or reuse the outcome, current flow, constraints and plausible paths.
Challenge the link between the requested mechanism and the desired benefit. If the goal is refuted,
recommend the smaller or corrected path; do not silently substitute a new goal. A material owner
tradeoff goes to `duck-decide`; separately authorized independent work may continue.

READY continues; CUT ends work that is demonstrably unnecessary under the owner's criteria. A
small settled task uses the short form without creating a commit just to justify its size.

## 2. Plan with proof

Use `duck-plan` for substantial or uncertain work. A narrow task can keep a short plan in the work
record: intervention, affected invariant, falsifying check and expected final observation. Reuse
an existing settled plan when its scope and assumptions still hold.

Select the challenge approach and participants from
[challenge selection](../duck-review/references/challenge.md). Independent authorship and critical
review are alternatives, not two mandatory tolls. Attack consequential assumptions with the cheapest
experiment before building on them. Record actual participation; a self-check is not cross-family
co-authorship. A local plan need not be committed. Respect repository release requirements later.

A refuted decomposition is replanned; agreement alone never makes it ready. Bound plan critique as
`duck-plan` specifies instead of waiting for every participant to concur.

## 3. Execute the smallest surviving path

For each meaningful behavior change: establish the failing outcome, implement the minimum that
satisfies it, apply `duck-shape`, then take the unit's diff through
[the prose bar](../duck-dry/references/bar.md). Use existing checks where possible; trivial edits
need no invented test. Shape and dry apply within the unit before later work depends on it.

Remove superseded paths once the replacement is verified. Preserve required compatibility and
public contracts; do not add speculative shims or delete a real edge case because scope is unclear.
An unrelated restructure is separate work. Selected finding IDs delimit repairs; do not silently
fix every item in the report.

Use native staged or parallel execution only where it helps independent work. `duck-diet` governs
context and model routing; a cheap worker still needs a check that catches its failure. Converge
parallel edits before verifying the assembled candidate, with one owner per file during concurrent
remediation. Per-lane green does not prove the merged result.

## 4. Verify and try to break it

Run relevant project gates and `duck-proof` on the actual candidate. Proof owns claim-specific
counterexamples, final-state observations and the completed-shape probe. **Any proof or shape edit
returns to affected executable checks before completion or dispatch.** Earlier green evidence does
not survive a relevant repair. Read the outputs and the resulting state, not just exit codes.

Use `duck-break` for requested broad attacks and the dynamic evidence required for trust-touching
work. Select attacks appropriate to the artifact: agent behavior trials for skill/gate changes,
service recovery tests for a service whose recovery is claimed. Do not substitute distribution
validation for behavioral proof or label an unrun check passed.

Write handoff evidence using `duck-proof`'s durable-home rules. A shared work record may hold the
proof, break and plan sections; give the consumer exact locations. Preserve essential artifacts
before scratch cleanup. An authorized local task can finish here with its evidence and any stated
verification limits, without creating a commit, PR or release verdict.

## 5. Independent review, when requested or required for release

Prepare the candidate and evidence before invoking `duck-review`. If committing is authorized,
record the exact commit; otherwise review an explicit worktree snapshot and do not treat that as a
landable SHA. A gate-policy change is reviewed under PRE-change rules, never its own relaxed rules.

Act on the single adjudicated result:

- APPROVE: continue only to the already authorized release action.
- REJECT: name each substantiated blocker's cause, using `duck-why` when it is not established.
  Repair at the level the evidence refutes: line, shared contract, mechanism, or goal. Rerun
  affected verification before reviewing the changed candidate.
- NOTE: resolve missing material evidence or criteria if possible. It is neither approval nor a
  reason to invent a repair. An unavailable gate does not prevent completing authorized local work.

Before a third or later review round, record a loop diagnosis. Contradicted premises go to frame;
wrong decomposition to plan; repeated missed cases to an executable class-level check or
`duck-race` rally; rival implementations to race; real owner tradeoffs to decide. Continue review
only when a named unresolved cause is shrinking and new evidence will be available. Repeated
blockers from one class require repairing the method, not buying another round on the same basis.
Respect the owner's effort bound; at the limit state unresolved claims, never manufacture approval.

### Review-loop ownership and stable criteria

The coordinating caller owns convergence, including when nobody is available to answer questions.
Name that coordinator in the existing work record; preserve the role across handoffs. Reviewers
produce evidence and judgments, not a new backlog for automatic execution. The coordinator resolves
technical findings within authority, tracks causes and owns the next action; only the user can
settle a genuinely new product, policy or scope decision.

Before the first review, record the outcome, non-goals, required contracts, acceptance checks,
release policy, participants and effort bound. Carry that baseline across rounds. Default to at
most three review rounds total (initial review plus two re-reviews), unless the user or repository
sets another bound. Reframing, changing reviewers or renaming the task does not reset it. Transport
retries follow `duck-review`'s separate bounded outage rule.

Track findings by stable cause, with the violated criterion, evidence, disposition and closure
check. A reworded finding is not new. Reopen a closed cause only with contrary evidence or an
impacting change. A newly discovered defect against an existing contract can still block; a new
preference, feature or unrelated cleanup is separate proposed work, not a stronger acceptance bar.
Do not silently promote SHOULD/NOTE items into required repairs.

At the bound, stop redispatching and preserve the candidate, unresolved evidence and next action;
release stays unapproved. If new evidence undermines the agreed goal, report the contradiction and
hold dependent work without inventing replacement criteria. Without the user, make authorized
technical decisions and continue independent work; do not guess their tradeoff or loop waiting for
agreement. A later explicit continuation can supply a new bound; elapsed time cannot.

## 6. Land only when authorized

Use `duck-land` for an authorized merge after its gate passes. It checks the exact candidate/base,
CI and remote policy, reads back what shipped, records the outcome and preserves work before
cleanup. Push-only or PR preparation performs only that authorized action under repository rules;
it is not a merge request. New code or a changed integration invalidates the affected authorization.

## Continuation

New owner input steers the current task; narrowing or withdrawal of authority takes effect
immediately. Reuse settled decisions. A tool outage gets a bounded retry or another authorized
mechanism; a permission rejection does not. Keep working until the authorized endpoint, a genuine
owner decision on dependent work, an external block, an instruction to stop, or a real scheduled
handoff. Never claim a handoff was booked without a host result confirming it.

At a context boundary, preserve what `duck-diet`'s first runtime rule requires. Close with what
changed, what was tested, and what remains unproven or unauthorized.
