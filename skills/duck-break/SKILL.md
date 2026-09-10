---
name: duck-break
description: Try to break a system's claimed behavior, then show what actually happened. Use when the user asks to break or red-team work, when a behavioral proof needs hostile inputs, or when high-risk work lacks dynamic evidence. Test the actual candidate and substantiate failures.
---

# Duck Break

An attack names the claim it could refute, executes the attempt, and observes the result. Reading
and opining is not an executed attack. Surviving the selected attacks establishes only that scope.
The breaker reports findings; the authorized caller repairs them and reruns the invalidated checks.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Bound the target and isolate destructive work

Record the candidate and relevant environment. Read its outcome, contracts and realistic operating
conditions before choosing attacks. Do not invent deployment states or require irrelevant attacks
for every task. A goal or plan with no running artifact can have premises tested, but cannot claim
runtime correctness. Instruction changes need realistic agent trials with actions and final-state
checks; a packaging validator does not establish behavior.

Attack a disposable copy for mutations or destructive tests, never the candidate checkout or live
user data. Git worktrees/clones carry committed state only: capture any staged, unstaged and
relevant untracked changes too. Verify the copied content matches the intended candidate before
attacking. Record the pre-attack state and restore that state between attacks, not an assumed clean
base. Use isolated data, ports and process groups for crash tests; verify no children survive
before restart. Preserve original uncommitted and ignored files.

## Select attacks that discriminate

- **Oracle check:** a targeted mutation or negative control should fail for the intended reason.
  If it survives, determine whether it is equivalent, irrelevant to the contract, an unnecessary
  mechanism, or missing coverage. An import failure does not demonstrate that a behavioral test
  catches the bug. Mutation testing is one tool, not the only valid check of a test.
- **Boundary and sequence abuse:** relevant malformed, empty, large, duplicate, reordered, stale
  or concurrent inputs. Derive cases from reachable paths and input classes; state limits instead
  of claiming every possible input was exhausted.
- **Invariant attack:** try to violate the required isolation, authorization, state transition or
  other contract from outside the boundary. Inspect the resulting state, not just the return code.
- **Crash/recovery:** interrupt a consequential operation, restart and inspect persisted state when
  recovery is part of the contract. Kill an isolated process group rather than leaving orphaned
  children to contaminate the result.
- **Real artifact:** exercise a critical path in the built binary or app. Test doubles and a green
  suite may omit the integration that determines the user-visible outcome.

Choose the highest-consequence plausible failures first. A focused proof can use one relevant
attack; a broad break covers the material contracts within its agreed scope. Check remaining
material claims after finding a defect unless they depend on the broken prerequisite. Respect
owner effort limits and report blocked or unattempted attacks rather than claiming they survived.

Differential results are leads, not verdicts. Resolve differences against an independent contract,
normalizing permitted ordering, nondeterminism and tolerances. One wrong result does not make both
implementations wrong; identical results can share a defect.

## Report and hand off

Capture each command/input, candidate identity, expected violation, observed output and final state.
Read exit status directly: a pipeline can report the status of a filter instead of the artifact.
Reproduce findings before calling them defects; distinguish suspected failures from substantiated
ones. Retain the complete finding list, grouped by affected claim and consequence; rank when the
owner requests it. Report no-finding attacks and limits under the same evidence standard.

Use `duck-proof`'s durable-home rules for a downstream handoff: `break-rN.md` or an explicit section
of the shared work record, with restored-state confirmation and evidence that survives scratch
cleanup. A standalone report can stay in the response. Do not advance the candidate just to save
the report. `duck-review` consumes required break evidence for release; a successful attack suite
is not independent approval.
