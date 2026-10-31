---
name: duck-plan
description: Find the hole in the plan before building over it; assumptions and acceptance checks must survive challenge. Use for implementation planning, consequential uncertainty, or work that previously needed repeated review fixes. Reuse established design decisions and cut speculative tasks.
---

# Duck Plan

Produce a plan someone can execute and verify. Each unit must change a required outcome or resolve
an uncertainty that blocks it. Agreement among planners does not establish feasibility.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
Planning does not authorize implementation or publication. Return to an executing caller so it can
continue within existing authority; a standalone planning request ends with the plan.

## Start from the actual decision

Reuse the outcome, constraints, affected flow and decisions established by
[`duck-frame`](../duck-frame/SKILL.md). If they are missing or contradicted, load `duck-frame` for
the unsettled design before planning dependent work. A short-form frame can take a short plan.
Read relevant source, tests and project instructions before naming changes.

Use [`duck-shape`](../duck-shape/SKILL.md) in analysis mode on proposed mechanisms, reusing valid
analysis. Search for existing helpers and platform capabilities. Remove speculative layers,
migration paths, configuration and cleanup tasks no required outcome needs; do not defer structural
problems the plan introduces to a later cleanup.

## Write executable units

Group work by shared cause or independently verifiable outcome, not by file or review finding. A
small change can be one unit. For each meaningful unit give:

- The required behavior and concrete change, with source location.
- Dependencies and contracts it can affect; order only where a dependency requires it.
- The observation that would expose a wrong implementation, and the existing or focused new check
  that produces it. Name a feasibility experiment when code cannot yet be planned safely.

Use existing checks where they cover the contract; add coverage for a material gap, not one check
per piece. Keep necessary integration, failure recovery and security checks; a happy-path check
cannot stand in for them. State the final user-visible observation, not that all steps completed.

## Try to invalidate the plan

Ask whether its checks could pass while the outcome fails. Test the consequential assumption with
an experiment that could prove it wrong before endorsing dependent work. Record what ran, what
happened and what remains untested. A plan for an unbuilt implementation cannot prove runtime
correctness.

Choose method and participants with [challenge selection](../duck-review/references/challenge.md).
A narrow plan may use a self-check with a decisive experiment; otherwise use the independent input
that reference and repository policy require, dispatched through
[`duck-review`](../duck-review/SKILL.md)'s [dispatch
mechanics](../duck-review/references/dispatch.md) with the critic's pin from `[models].plan`. Do
not claim independence that did not run.

Independent authors receive the outcome, constraints and source before seeing the preferred plan; a
critic receives the plan and seeks a concrete counterexample. Use the method that resolves the
uncertainty; neither requires the other. Compare alternative decompositions only where they change
feasibility, dependencies or verification; do not blend incompatible designs to keep every
contribution.

An independent participant opens with `PLAN: CONCUR` or `PLAN: OBJECT`, then numbered objections,
each naming a `path:line`, an unexecuted assumption or a missing check; a result without that line
is malformed, never a silent CONCUR.

Resolve factual disagreements with source or execution. A genuine owner tradeoff goes to
[`duck-decide`](../duck-decide/SKILL.md); routine technical choices do not. Evidence refuting the
design returns to frame.

## Cut and hand off

Remove any unit that contributes no required behavior, necessary evidence or safe transition. Merge
repeated fixes at their shared owner. Drop requirements and explanations already in the frame. Keep
a necessary migration, compatibility boundary or rollback even when it adds work.

Return READY when units and checks are actionable with no substantiated blocker. Otherwise name the
refuted premise, missing evidence or owner decision and the work depending on it. Report actual
challenge participants and unresolved findings; a solo draft stays labeled solo.

Bound critique before dispatch: `[bounds].plan_rounds` (default 2), which `dispatch.py` enforces on
dispatched rounds, unless the owner sets another limit. Another round needs new evidence or a
materially changed approach. At the bound stop redispatching and preserve unresolved claims.

Update one existing plan when a durable execution handoff is needed, under
[`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules; a short standalone plan can stay in the
response. Record decisive checks and disagreements, not a transcript. This does not replace a
required [`duck-review`](../duck-review/SKILL.md) release gate.
