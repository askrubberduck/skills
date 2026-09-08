---
name: duck-plan
description: Find the hole in the plan before building over it; assumptions and acceptance checks must survive challenge. Use for architectural or high-risk work, planning with proof, competing decompositions, or changes that previously needed repeated review fixes.
---

# Duck Plan

A plan is an argument that the proposed work reaches the outcome. Independent agreement can
expose blind spots; it cannot establish feasibility or replace executable evidence.

## Ground and choose the challenge

Use `duck-frame` to establish or reuse the outcome, constraints and affected paths. If the plan
reaches a boundary the frame did not examine, complete that analysis first. A small settled task
may use the short form; do not restate an unchanged frame. Challenge whether the proposed goal
and mechanism deliver the intended benefit before treating them as premises.

Select participants and approach using [challenge selection](../duck-review/references/challenge.md).
A narrow plan can be self-checked with competing hypotheses and a decisive experiment. Otherwise
use an independent co-author or critic; broader work may justify two. Respect the selected setup
and repository requirements. Do not imply cross-family review when no such participant ran.
Use `duck-review`'s [dispatch mechanics](../duck-review/references/dispatch.md) for external calls.

For independent generation, provide the outcome, constraints, source and alternatives still open,
not the doer's preferred plan. Each co-author produces a decomposition before seeing the others'.
For a critical review of an existing plan, provide that plan and ask what would falsify it. These
are different methods; choose by the uncertainty, not a rule that every task must use both.

## Shape before decomposition

Apply `duck-shape` in analysis mode before dividing the work: trace the proposed end-to-end path,
assign one owner per rule and state, compare reuse/deletion with new mechanisms, and try a realistic
next change against the proposed boundaries. Reuse a frame's valid structural analysis. This is
part of planning, not a refactor or a deferred cleanup task. Carry its preserved contracts and
structural checks into the units; proof later checks the assembled result against them.

## Plan the evidence with the work

Each meaningful unit names:

- the required observable outcome and intervention that should cause it;
- the assumption or failure mode that would refute that intervention;
- the check that fails beforehand and should pass afterward, or the feasibility experiment needed
  before code exists;
- dependencies, affected invariants, and how the completed result will be observed.

Use existing tests and platform mechanisms when they fit. Do not manufacture tests for trivial
edits. A check copied from the proposed implementation can encode the same mistake: derive it
from the outcome. Run the cheapest experiment on a consequential unknown before endorsing work
that depends on it. Name checks not yet run; a ready plan is not a proven implementation.

## Compare and cut

Compare credible decompositions, including reuse or deletion where they could satisfy the same
outcome. Prefer one owner per rule or state and fewer exceptional paths. An abstraction with one
implementation needs a real contract or change-path justification; its count alone neither
condemns nor saves it. Use `duck-shape`'s lens and preserve necessary boundaries and calibration.
Consolidate repeated findings on one cause into a unit that checks and repairs the shared surface.

Resolve factual disagreements with source or an experiment. Explain internal reversible choices
using the evidence. Only a genuine owner tradeoff goes to `duck-decide`; routine disagreement
between models is not automatically an owner decision. Contrary evidence about the goal returns
to frame. Do not force a synthesis of incompatible designs just to keep something from each plan.

## Settle without an agreement loop

Synthesize once, then address substantiated challenges. Before dispatch, state the unresolved
question and round bound; default at most two critique rounds after the initial draft unless the
owner supplies another limit. Another round needs new evidence or a materially changed approach.
If no progress is being made, change the experiment or report the unresolved claim. Do not loop
until every participant concurs, discard justified dissent, or count repeated phrasing as progress.

Return READY when the outcome, decomposition and checks are settled with no substantiated blocker;
otherwise identify the refuted premise, missing evidence or owner decision. Record which checks
ran, participants' verified identities, the selected method, disagreements and their resolution.
A solo draft is labeled solo; a list of family names without what they contributed is not evidence.

Save a handoff beside the work item when execution needs it; update one plan in place. Follow
`duck-proof`'s evidence-home rules. Commit only when authorized, not as a prerequisite to local
planning. Report-only stops at the plan; an executing caller resumes the authorized work.
Planning evidence does not replace the later `duck-review` gate required for release.
