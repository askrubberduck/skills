---
name: duck-roast
description: Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end. Use when the user asks for a roast or repeated full critique of the standing solution, wants a codebase audited for over-engineering, bloat, or what could be deleted repo-wide, or wants a milestone-level adversarial assessment rather than a change review or backlog sweep.
---

# Duck Roast

Find consequential defects and unnecessary mechanisms across the whole relevant flow. A criticism
names what fails or what can disappear without losing a required outcome; no finding is a valid
result when the claims survive inspection.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
Roast reports findings and proposed dispositions; it does not edit the candidate. One change
belongs to [`duck-review`](../duck-review/SKILL.md), a backlog sweep to
[`duck-cut`](../duck-cut/SKILL.md), and verification of your own candidate to
[`duck-proof`](../duck-proof/SKILL.md).

## Ground the critique

Read the source and product constraints; fix the requested scope, observable outcomes and operating
conditions. Challenge the benefit when the task calls for it, without inventing a market, deployment
or future requirement.

Choose the relevant questions:

- Does the mechanism deliver the required outcome? Can existing behavior or deletion satisfy it?
- Where do duplicate rules/state, unused paths, speculative options or leaking wrappers create a
  real maintenance burden? Apply [`duck-shape`](../duck-shape/SKILL.md)'s necessity checks.
- Do affected trust boundaries hold against malformed input or a compromised component in the
  actual deployment?
- Which required operation can fail, how is it noticed, and what recovery exists?
- Does an evidenced upcoming change expose misplaced ownership or coupling?

Trace callers and consequences before calling a pattern defective; co-changing files, dense comments
and old code are leads, not proof. Repeated instances may share one fix, and repetition alone does
not make that fix an owner decision.

## Substantiate and bound the pass

Choose method, participants and effort bound with [`duck-review`](../duck-review/SKILL.md)'s
[challenge selection](../duck-review/references/challenge.md); label a focused self-critique as
such. Use its [dispatch mechanics](../duck-review/references/dispatch.md) for external participants,
with the required authorization and identity checks; their ledger rows carry `stage = roast`. Give
independent critics the same constraints and complementary questions, not each other's conclusions.

For each finding, name the violated contract or concrete cost, cite its source and execute a
counterexample when feasible. Distinguish demonstrated defects, supported maintenance findings and
untested suspicions. Propose the fix at the level the evidence refutes; deletion or reuse when that
suffices. Do not rank by lines removed, file age or reviewer confidence.

Group findings by cause; keep substantiated ones, resolve previously disputed claims explicitly,
drop discarded hunches. The pass ceiling is `[bounds].roast_passes` (default 2), which `dispatch.py`
enforces on dispatched passes, unless the user supplies another. Another pass needs an unresolved
question and new evidence or a materially different approach; never repeat until the finding list is
empty or every critic agrees.

## Return the useful result

Report findings with location, consequence, evidence and proposed action, then material coverage
limits. Separate required repairs, optional improvements and owner decisions; use
[`duck-decide`](../duck-decide/SKILL.md) only for a tradeoff the owner must settle.

A standalone critique stays in the response. Update an existing review/work record when requested,
required by policy or needed for a handoff, under [`duck-proof`](../duck-proof/SKILL.md)'s
durable-home rules; a finding alone creates no packet or backlog entry.

Return to the caller for already-authorized repairs: small fixes need their relevant checks,
substantial work may need [`duck-plan`](../duck-plan/SKILL.md), and release follows the
[`duck-review`](../duck-review/SKILL.md) gate. The roast itself grants neither repair authority nor
release approval.
