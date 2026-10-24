---
name: duck-run
description: Challenge the goal, shape the plan, build it, and make it prove itself; local means local. Use when the user asks to duck a task, apply selected findings, or carry work through the delivery flow; when a review came back REJECT and the work must be fixed; or when the user says a result is wrong or not what they wanted and asks for it fixed, even when the fix looks like one line. Continue to independent review and landing only within the authorized endpoint.
---

# Duck Run

Own the whole authorized task. Carry the outcome, constraints, candidate, valid evidence and next
action across stages. A skill returning a finding is a handoff to this caller, not a reason to ask
for another go-ahead.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
When the host forbids edits, as a plan-only mode does, say so once, finish the analysis it permits
and leave the mode alone; findings are not a plan awaiting approval.

## Scope, endpoint and isolation

Read the user's existing authority first. Local implementation ends with a verified local candidate;
report-only ends with findings or a plan. Commit, PR, push and merge are distinct actions: perform
them only when authorized; a passed review does not expand that authority. A release whose gate
cannot run stays unapproved; finish the authorized local work and report what remains.

Use a dedicated worktree or equivalent copy when runs write concurrently or destructive checks need
isolation; a small single-worker edit can use the existing checkout after checking its state. Each
run's worktree sits at the repo root, never nested under another run's tree. Preserve unrelated
changes. Capture dirty candidate content for test copies the way
[`duck-split`](../duck-split/SKILL.md) does — a ref, not a stash — and verify it. Step out of a
worktree before deleting it.

## 1. Frame first

Load [`duck-frame`](../duck-frame/SKILL.md) (the Skill tool, or read its SKILL.md) and carry it to
its exit state before any edit to the candidate; a frame written from memory is not a frame. It
establishes or reuses the outcome, flow, constraints and plausible paths, at the depth it would have
run alone; a small settled task takes its short form. If the goal is refuted, recommend the
corrected path; never silently substitute a new goal. READY continues; CUT ends work demonstrably
unnecessary under the owner's criteria; OWNER DECISION goes to
[`duck-decide`](../duck-decide/SKILL.md) and holds only the dependent work.

## 2. Plan with proof

Load [`duck-plan`](../duck-plan/SKILL.md) for substantial or uncertain work; a narrow task can keep
a short plan in the work record: intervention, affected invariant, falsifying check and expected
final observation. Reuse a settled plan when its scope and assumptions still hold.

Select challenge approach and participants from [challenge
selection](../duck-review/references/challenge.md); record actual participation. Attack
consequential assumptions with the cheapest experiment before building on them.
A refuted decomposition is replanned; agreement alone never makes it ready. Bound critique as
`duck-plan` specifies.

## 3. Execute the surviving design

For each meaningful behavior change: establish the failing outcome, implement the minimum that
satisfies it, apply [`duck-shape`](../duck-shape/SKILL.md), then take the unit's diff through [the
prose bar](../duck-dry/references/bar.md). Use existing checks where possible; trivial edits need no
invented test. Shape and dry apply within the unit before later work depends on it, as their own
commits when committing is authorized; landing may squash them. Tidy first when it makes this
change easier, after when it makes the next one easier, never on speculation.

Remove superseded paths once the replacement is verified. Preserve required compatibility and
public contracts; add no speculative shims and delete no real edge case because scope is unclear.
An unrelated restructure is separate work. Selected finding IDs delimit repairs; the receipt gives
each as applied, skipped with its reason, or parked.

Use staged or parallel execution only where it helps independent work.
[`duck-diet`](../duck-diet/SKILL.md) governs context and model routing; a cheap worker still needs a
check that catches its failure. Converge parallel edits, one owner per file, before verifying the
assembled candidate.

## 4. Verify and try to break it

Use [`duck-race`](../duck-race/SKILL.md) in rally mode when requested, required by project policy,
or a demonstrated testing blind spot or repeated missed defect class needs cross-family tests. Run
it against the contract before final proof and review; include its receipt, or record why a
required rally could not run. Ordinary verified work does not require a rally.

Run relevant project gates and read their outputs and resulting state, not just exit codes; then
load [`duck-proof`](../duck-proof/SKILL.md) and run it on the actual candidate. **Any proof or shape
edit returns to affected executable checks before completion or dispatch.** A red check stops new
work on that surface until it is green or its cause is named. A symptom that returns after its fix:
load [`duck-why`](../duck-why/SKILL.md) before the next patch.

Use [`duck-break`](../duck-break/SKILL.md) for requested broad attacks and the dynamic evidence
trust-touching work requires. Match attacks to the artifact: agent behavior trials for skill or
gate changes, recovery tests for claimed recovery. Distribution validation is not behavioral proof;
never label an unrun check passed.

Write handoff evidence under [`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules; a shared
work record may hold the proof, break and plan sections, with exact locations for the consumer.
Preserve essential artifacts before scratch cleanup. An authorized local task can finish here with
its evidence and stated verification limits, without a commit, PR or release verdict.

## 5. Independent review, when requested or required for release

Call [`duck-review`](../duck-review/SKILL.md)'s release-gate path by name; its unscoped default is a
findings pass, which satisfies no gate. Prepare the candidate and evidence first: the exact commit
when committing is authorized, otherwise an explicit worktree snapshot that is not a landable SHA.

Act on the single adjudicated result:

- APPROVE: continue only to the already authorized release action.
- REJECT: name each substantiated blocker's cause, using [`duck-why`](../duck-why/SKILL.md) when it
  is not established. From the first round, repair as [`duck-proof`](../duck-proof/SKILL.md)'s
  repair section requires, then rerun affected verification before reviewing the changed
  candidate. An owner correction of the result is evidence of the same kind.
- NOTE: obtain the missing material evidence or criteria, or report which is missing. It is
  neither approval nor a reason to invent a repair, and does not prevent completing authorized
  local work.

Before a third or later round, record a loop diagnosis. Contradicted premises go to
[`duck-frame`](../duck-frame/SKILL.md); wrong decomposition to [`duck-plan`](../duck-plan/SKILL.md);
repeated missed cases to an executable class-level check or a [`duck-race`](../duck-race/SKILL.md)
rally; rival implementations, or blockers landing on the fixes rather than the original change, to
a `duck-race` race of the contested unit; real owner tradeoffs to
[`duck-decide`](../duck-decide/SKILL.md). Continue review only when a named unresolved cause is
shrinking and new evidence will be available. Repeated blockers from one class require repairing
the method, not buying another round on the same basis.

### Review-loop ownership and stable criteria

The coordinating caller owns convergence: named in the existing work record, preserved across
handoffs. Reviewers produce evidence and judgments, not a backlog for automatic execution. The
coordinator resolves technical findings within authority, tracks causes and owns the next action;
only the user settles a genuinely new product, policy or scope decision.

Before the first review, record the outcome, non-goals, required contracts, acceptance checks,
release policy, participants and effort bound; carry that baseline across rounds. The round ceiling
is `[bounds].review_rounds` in `~/.askrubberduck/config.toml` (default 3: initial review plus two
re-reviews; `[bounds].trust_rounds` (default 2) for trust-touching work) unless the user or
repository sets another; the stop rule inside it is evidence, per the challenge reference.
Reframing, changing reviewers or renaming the task does not reset it. Transport retries follow
[`duck-review`](../duck-review/SKILL.md)'s separate bounded outage rule.

Track findings by stable cause with the violated criterion, evidence, disposition and closure
check. A reworded finding is not new; reopen a closed cause only with contrary evidence or an
impacting change. A newly discovered defect against an existing contract can still block; a new
preference, feature or unrelated cleanup is separate proposed work, not a stronger acceptance bar.
Do not silently promote SHOULD/NOTE items into required repairs.

At the bound, stop redispatching and preserve the candidate, unresolved evidence and next action;
release stays unapproved. If new evidence undermines the agreed goal, report the contradiction and
hold dependent work without inventing replacement criteria. Without the user, make authorized
technical decisions and continue independent work; do not guess their tradeoff or wait for
agreement. A later explicit continuation can supply a new bound; elapsed time cannot.

## 6. Land only when authorized

Use [`duck-land`](../duck-land/SKILL.md) for an authorized merge after its gate passes. Push-only or
PR preparation performs only that action under repository rules; it is not a merge request. New
code or a changed integration invalidates the affected authorization.

## Continuation

New owner input steers the current task; narrowing or withdrawal of authority takes effect
immediately. Reuse settled decisions. A tool outage gets a bounded retry or another authorized
mechanism; a permission rejection does not. Keep working until the authorized endpoint, a genuine
owner decision on dependent work, an external block, an instruction to stop, or a real scheduled
handoff.

At a context boundary, preserve state and follow [`duck-diet`](../duck-diet/SKILL.md)'s first
runtime rule. Close with what changed, what was tested, and what
remains unproven or unauthorized.
