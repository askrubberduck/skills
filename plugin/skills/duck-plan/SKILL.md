---
name: duck-plan
description: Find the hole in the plan before building over it; assumptions and acceptance checks must survive challenge. Use for implementation planning, consequential uncertainty, or work that previously needed repeated review fixes. Reuse established design decisions and cut speculative tasks.
---

# Duck Plan

Produce a plan that someone can execute and verify. Each unit must change a required outcome or
resolve an uncertainty that blocks one. Agreement among planners does not establish feasibility.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.
A plan does not authorize implementation or publication. Return to an executing caller, which
continues within existing authority. A standalone planning request ends with the plan.

## Start from the actual decision

Reuse the outcome, constraints, affected flow and decisions that
[`duck-frame`](../duck-frame/SKILL.md) established. If they are missing or contradicted, load
`duck-frame` for the unsettled design before you plan dependent work. A short-form frame can take a
short plan. Read relevant source, tests and project instructions before you name changes.

Use [`duck-shape`](../duck-shape/SKILL.md) in analysis mode on proposed mechanisms, and reuse valid
analysis. Search for existing helpers and platform capabilities. Remove speculative layers,
migration paths, configuration and cleanup tasks that no required outcome needs. Do not defer
structural problems that the plan introduces to a later cleanup.

## Write executable units

Group work by shared cause or independently verifiable outcome, not by file or review finding. A
small change can be one unit. For each meaningful unit, give:

- The required behavior and concrete change, with source location.
- The dependencies and contracts it can affect. Order only where a dependency requires it.
- The observation that would expose a wrong implementation, and the existing or focused new check
  that produces it. If code cannot yet be planned safely, name a feasibility experiment.

Use existing checks where they cover the contract. Add coverage for a material gap, not one check
per piece. Keep necessary integration, failure recovery and security checks; a happy-path check
cannot replace them. State the final user-visible observation, not that all steps completed.

## Try to invalidate the plan

Ask whether its checks can pass while the outcome fails. Before you endorse dependent work, test the
consequential assumption with an experiment that can prove it wrong. Record what ran, what happened
and what remains untested. A plan for an unbuilt implementation cannot prove runtime correctness.

Choose method and participants with
[challenge selection](../duck-review/references/challenge.md). A narrow plan may use a self-check
with a decisive experiment. Otherwise, use the independent input the reference and repository
policy require, dispatched through [`duck-review`](../duck-review/SKILL.md)'s [dispatch
mechanics](../duck-review/references/dispatch.md) with the critic's pin from `[models].plan`. Do
not claim independence that did not run.

Independent authors receive the outcome, constraints and source before they see the preferred plan.
A critic receives the plan and seeks a concrete counterexample. Use the method that resolves the
uncertainty; neither requires the other. Compare alternative decompositions only where they change
feasibility, dependencies or verification. Do not blend incompatible designs to keep every
contribution.

An independent participant opens with `PLAN: CONCUR` or `PLAN: OBJECT`, then numbered objections.
Each objection names a `path:line`, an unexecuted assumption or a missing check. A result without
that line is malformed, never a silent CONCUR.

Resolve factual disagreements with source or execution. Send a genuine owner tradeoff to
[`duck-decide`](../duck-decide/SKILL.md), but not routine technical choices. Evidence that refutes
the design returns to frame.

## Cut and hand off

Remove any unit that contributes no required behavior, necessary evidence or safe transition. Merge
repeated fixes at the code that owns their shared rule. Drop requirements and explanations the
frame holds. Keep a necessary migration, compatibility boundary or rollback, even when it adds work.

Return READY when units and checks are actionable with no substantiated blocker. Otherwise, name the
refuted premise, missing evidence or owner decision and the dependent work. Report actual
challenge participants and unresolved findings. Label a solo draft as solo.

Bound critique before dispatch: `[bounds].plan_rounds` (default 2), which `dispatch.py` enforces on
dispatched rounds, unless the owner sets another limit. Another round needs new evidence or a
materially changed approach. At the bound, stop redispatch and preserve unresolved claims.

For a durable execution handoff, update one existing plan under
[`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules. A short standalone plan can stay in
the response. Record decisive checks and disagreements, not a transcript. This plan does not
replace a required [`duck-review`](../duck-review/SKILL.md) release gate.
