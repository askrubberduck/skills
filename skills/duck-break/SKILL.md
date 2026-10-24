---
name: duck-break
description: Try to break a system's claimed behavior, then show what actually happened. Use when the user asks to break or red-team work, when a behavioral proof needs hostile inputs, or when high-risk work lacks dynamic evidence. Test the actual candidate and substantiate failures.
---

# Duck Break

An attack names the claim it could refute, executes the attempt, and observes the result; reading
and opining is not an attack. Surviving the selected attacks establishes only that scope. The
breaker reports findings; the authorized caller repairs them and reruns the invalidated checks.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

## Bound the target and isolate destructive work

Record the candidate and environment. Read its outcome, contracts and realistic operating
conditions before choosing attacks; do not invent deployment states or require irrelevant attacks.
A goal or plan with no running artifact can have premises tested but cannot claim runtime
correctness. Instruction changes need realistic agent trials with actions and final-state checks; a
packaging validator does not establish behavior. Run each arm with only its own text loaded, since
an installed copy of the same skill answers in the candidate's place: in Claude Code,
`claude -p --setting-sources project --plugin-dir <arm>`, which drops the user's skills, hooks and
instructions that `--plugin-dir` alone leaves in. A prompt that names no skill measures whether the
description fires; one that names it measures only the body.

Attack a disposable copy for mutations or destructive tests, never the candidate checkout or live
user data. Worktrees and clones carry committed state only: capture staged, unstaged and relevant
untracked changes as [`duck-split`](../duck-split/SKILL.md) does, as a ref, not a stash, and verify
the copy matches the candidate before attacking. Record the pre-attack state and restore it between
attacks. Use isolated data, ports and process groups for crash tests; verify no children survive
before restart. Point every database, queue, external API and cloud account the copy reaches at a
disposable or stubbed target and strip live credentials first, or leave that attack unattempted and
say so. Preserve original uncommitted and ignored files.

## Select attacks that discriminate

- **Oracle check:** a targeted mutation or negative control should fail for the intended reason.
  If it survives, decide whether it is equivalent, irrelevant to the contract, an unnecessary
  mechanism, or missing coverage. An import failure does not show a behavioral test catches the
  bug. Mutation testing is one tool, not the only valid check.
- **Boundary and sequence abuse:** malformed, empty, large, duplicate, reordered, stale or
  concurrent inputs, derived from reachable paths and input classes; state limits instead of
  claiming every input was exhausted.
- **Invariant attack:** violate the required isolation, authorization, state transition or other
  contract from outside the boundary; inspect the resulting state, not just the return code.
- **Crash/recovery:** interrupt a consequential operation, restart and inspect persisted state when
  recovery is part of the contract. Kill an isolated process group; leave no orphaned children.
- **Real artifact:** exercise a critical path in the built binary or app; test doubles and a green
  suite may omit the integration that decides the user-visible outcome.

Choose the highest-consequence plausible failures first. A focused proof can use one attack; a
broad break covers the material contracts within its agreed scope. Keep checking remaining material
claims after a defect unless they depend on the broken prerequisite. Respect owner effort limits
and report blocked or unattempted attacks rather than claiming they survived.

Differential results are leads, not verdicts: resolve differences against an independent contract,
normalizing permitted ordering, nondeterminism and tolerances. One wrong result does not make both
implementations wrong; identical results can share a defect.

## Report and hand off

Capture each command/input, candidate identity, expected violation, observed output and final state.
Read exit status directly: a pipeline can report a filter's status instead of the artifact's. A
defect is a contract violation observed directly; a captured invariant breach counts once even when
a race will not trigger twice. Reproduce when the capture is inconclusive; record repeatability
apart from strength. Distinguish suspected failures from substantiated ones. Retain the complete
finding list, grouped by affected claim and consequence; rank when the owner asks. Report
no-finding attacks and limits under the same evidence standard.

Use [`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules for a downstream handoff:
`break-rN.md` or an explicit section of the shared work record, with restored-state confirmation
and evidence that survives scratch cleanup. A standalone report can stay in the response. Do not
advance the candidate just to save the report. [`duck-review`](../duck-review/SKILL.md) consumes
required break evidence for release; a successful attack suite is not independent approval.
