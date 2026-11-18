---
name: duck-roast
description: Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end. Use when the user asks for a roast or repeated full critique of the standing solution, wants a codebase audited for over-engineering, bloat, or what could be deleted repo-wide, or wants a milestone-level adversarial assessment rather than a change review or backlog sweep.
---

# Duck Roast

Find consequential defects and unnecessary mechanisms across the whole relevant flow. A criticism
names what fails, or what can disappear without loss of a required outcome. If the claims survive
inspection, no finding is a valid result.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

The roast reports findings and proposed dispositions; it does not edit the candidate. One change
belongs to [`duck-review`](../duck-review/SKILL.md), a backlog sweep to
[`duck-cut`](../duck-cut/SKILL.md), and verification of your own candidate to
[`duck-proof`](../duck-proof/SKILL.md).

## Ground the critique

Read the source and product constraints. Fix the requested scope, observable outcomes and
operating conditions. Challenge the benefit when the task calls for it, but invent no
market, deployment or future requirement.

Choose relevant questions:

- Does the mechanism deliver the required outcome? Can existing behavior or deletion satisfy it?
- Where do duplicate rules/state, unused paths, speculative options or leaking wrappers cause a
  real maintenance burden? Apply [`duck-shape`](../duck-shape/SKILL.md)'s necessity checks.
- Do affected trust boundaries hold against malformed input or a compromised component in the
  actual deployment?
- Which required operation can fail, how is it noticed, and what recovery exists?
- Does an evidenced upcoming change show misplaced ownership or coupling?

Trace callers and consequences before you call a pattern defective. Co-changing files, dense
comments and old code are leads, not proof. Repeated instances can share one fix; repetition
alone does not make it an owner decision.

## Substantiate and bound the pass

Choose method, participants and effort bound with [`duck-review`](../duck-review/SKILL.md)'s
[challenge selection](../duck-review/references/challenge.md). Label a focused self-critique as
such. For external participants, use its [dispatch mechanics](../duck-review/references/dispatch.md)
with the required authorization and identity checks; their ledger rows carry `stage = roast`. Give
independent critics the same constraints and complementary questions, not each other's
conclusions.

Name each finding's violated contract or concrete cost and cite its source. When feasible,
execute a counterexample. Separate demonstrated defects, supported maintenance findings and untested
suspicions. Propose the fix at the level the evidence refutes, deletion or reuse when that
suffices. Do not rank by lines removed, file age or reviewer confidence.

Group findings by cause. Keep substantiated ones, resolve previously disputed claims
explicitly, and drop discarded hunches. The pass ceiling is `[bounds].roast_passes` (default 2),
which `dispatch.py` enforces on dispatched passes, unless the user supplies another. Another pass
needs an unresolved question and new evidence or a materially different approach. Never repeat
until the finding list is empty or every critic agrees.

## Return the useful result

Report findings with location, consequence, evidence and proposed action, then material
coverage limits. Separate required repairs, optional improvements and owner decisions. Use
[`duck-decide`](../duck-decide/SKILL.md) only for a tradeoff the owner must settle.

A standalone critique stays in the response. Update an existing review or work record when
requested, required by policy or needed for handoff, under
[`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules. A finding alone creates no packet or
backlog entry.

Return to the caller for authorized repairs. Small fixes need relevant checks; substantial
work can need [`duck-plan`](../duck-plan/SKILL.md); release follows the
[`duck-review`](../duck-review/SKILL.md) gate. The roast grants no repair authority and no release
approval.
