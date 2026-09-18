---
name: duck-roast
description: Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end. Use when the user asks for a roast or repeated full critique of the standing solution, wants a codebase audited for over-engineering, bloat, or what could be deleted repo-wide, or wants a milestone-level adversarial assessment rather than a change review or backlog sweep.
---

# Duck Roast

Find consequential defects and unnecessary mechanisms in the requested solution. Inspect the
whole relevant flow; a convincing criticism names what fails or what can disappear without losing
a required outcome. No finding is a valid result when the claims survive inspection.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
Roast reports findings and proposed dispositions; it does not edit the candidate. One change belongs
to `duck-review`, a backlog sweep to `duck-cut`, and verification of your own candidate to `duck-proof`.

## Ground the critique

Read the actual source and product constraints. Establish the requested scope, observable outcomes
and operating conditions. Challenge the benefit when the task calls for it, but do not invent a
market, deployment or future requirement to make a criticism sound important.

Choose relevant questions rather than filling every category:

- Does the mechanism deliver the required outcome? Can existing behavior or deletion satisfy it?
- Where do duplicate rules/state, unused paths, speculative options or leaking wrappers create a
  real maintenance burden? Apply `duck-shape`'s necessity checks.
- Do affected trust boundaries enforce their contract? What can malformed input or a compromised
  component reach in the actual deployment?
- Which required operation can fail, how is it noticed, and what recovery is available?
- Does an evidenced upcoming change expose misplaced ownership or coupling?

Trace callers and consequences before calling a pattern defective. Co-changing files, dense
comments and old code are investigation leads, not proof of a wrong boundary or harmless debt.
Repeated instances may have one shared fix; repetition alone does not make that fix an owner decision.

## Substantiate and bound the pass

Choose method, participants and effort bound with `duck-review`'s
[challenge selection](../duck-review/references/challenge.md). A focused self-critique stays labeled
as such. Use its [dispatch mechanics](../duck-review/references/dispatch.md) for external participants;
required authorization and identity checks still apply. Give independent critics the same
constraints and complementary questions, not each other's conclusions.

For each proposed finding, identify the violated contract or concrete cost, cite its source and
execute a relevant counterexample when feasible. Distinguish demonstrated defects, supported
maintenance findings and untested suspicions. Prefer the smallest fix, including deletion or reuse.
Do not rank by lines removed, file age or the confidence of the reviewer.

Group findings by cause; retain substantiated ones and explicitly resolve previously disputed claims.
Do not publish every discarded hunch. Default to at most two passes unless the user supplies another
bound. Another pass needs an unresolved question and new evidence or a materially different approach;
never repeat until the finding list is empty or every critic agrees.

## Return the useful result

Report findings with location, consequence, evidence and proposed action, then material coverage
limits. Separate required repairs from optional improvements and genuine owner decisions. Use
`duck-decide` only for a tradeoff the owner actually needs to settle.

A standalone critique stays in the response. Update an existing review/work record when requested,
required by policy or needed for a downstream handoff, using `duck-proof`'s durable-home rules.
Do not create a packet or backlog entry merely because a finding exists.

Return to the caller for already-authorized repairs. Small local fixes need their relevant checks;
substantial work may need `duck-plan`, and release follows the required `duck-review` gate. The roast
itself grants neither repair authority nor release approval.
