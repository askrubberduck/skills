---
name: duck-plan
description: Turn a settled outcome into necessary changes and checks that can expose a wrong plan. Use for implementation planning, consequential uncertainty, or work that previously needed repeated review fixes. Reuse established design decisions and cut speculative tasks.
---

# Duck Plan

Produce a plan someone can execute and verify. Each unit must change a required outcome or resolve
an uncertainty that blocks it. Agreement among planners does not establish feasibility.

Follow the user's language; preserve commands, paths, identifiers, quoted errors and verdicts.
Planning does not authorize implementation or publication. Return to an executing caller so it can
continue within existing authority; a standalone planning request ends with the plan.

## Start from the actual decision

Reuse the outcome, constraints, affected flow and decisions established by `duck-frame`. If they
are missing or contradicted, resolve only the unsettled design before planning dependent work.
A small settled task can use the short form; no separate architecture document is required merely
to restate the request. Read relevant source, tests and project instructions before naming changes.

Use `duck-shape` in analysis mode on proposed mechanisms, reusing valid analysis already done.
Search for existing helpers and platform capabilities. Remove speculative layers, migration paths,
configuration and cleanup tasks that no required outcome needs. Do not defer structural problems
introduced by the plan to a later cleanup phase.

## Write executable units

Group work by a shared cause or independently verifiable outcome, not by file or review finding.
A small change can be one unit. For each meaningful unit, give:

- The required behavior and the concrete change, with the relevant source location.
- Dependencies and contracts it can affect; order only where a dependency requires it.
- The observation that would expose a wrong implementation, and the existing check or focused new
  check that will produce it. Name a feasibility experiment when code cannot yet be planned safely.

Use actual operations: "deduplicate retries by event ID at ingestion; check two retries produce
one charge" gives an implementer something to do and verify. "Build a robust processing layer,
add comprehensive tests, update docs" does not.

Use existing checks where they cover the contract. Add coverage for a material gap, not a test per
helper or a suite that mirrors the proposed branches. Keep necessary integration, failure recovery
and security checks; a happy-path unit test cannot stand in for them. Trivial edits need no invented
test. State the final user-visible observation, not merely that all planned steps were completed.

## Try to invalidate the plan

Ask whether its checks could pass while the outcome fails. Test the consequential assumption with
the cheapest available experiment before endorsing dependent work. Record what ran, what happened
and what remains untested. A plan for an unbuilt implementation cannot prove runtime correctness.

Choose challenge method and participants using [challenge selection](../duck-review/references/challenge.md).
A narrow plan may use a self-check with a decisive experiment; otherwise use the independent input
that reference and repository policy require. For external calls use `duck-review`'s
[dispatch mechanics](../duck-review/references/dispatch.md). Do not claim independence that did not run.

Independent authors receive the outcome, constraints and source before seeing the preferred plan.
A critic instead receives the proposed plan and seeks a concrete counterexample. Choose the method
that resolves the uncertainty; do not require both. Compare alternative decompositions only where
they change feasibility, dependencies or verification. Do not blend incompatible designs to retain
every participant's contribution.

Resolve factual disagreements with source or execution. A genuine owner tradeoff goes to
`duck-decide`; routine technical choices do not. Evidence refuting the design returns to frame.

## Cut and hand off

Remove any unit that contributes no required behavior, necessary evidence or safe transition.
Merge repeated fixes at their shared owner. Remove duplicate requirements and explanations already
in the frame. Keep a necessary migration, compatibility boundary or rollback even when it adds work.

Return READY when the units and checks are actionable with no substantiated blocker. Otherwise name
the refuted premise, missing evidence or owner decision and which work depends on it. Report actual
challenge participants and unresolved findings; a solo draft stays labeled solo.

Bound critique before dispatch: at most two critique rounds after the initial draft unless the
owner supplies another limit. Another round needs new evidence or a materially changed approach.
Stop redispatching at the bound and preserve unresolved claims; do not loop until everyone agrees.

Update one existing plan when a durable execution handoff is needed, using `duck-proof`'s evidence-home
rules. A short standalone plan can stay in the response. Record decisive checks and disagreements,
not a transcript of the planning process. This does not replace a required `duck-review` release gate.
