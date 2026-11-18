---
name: duck-break
description: Try to break a system's claimed behavior, then show what actually happened. Use when the user asks to break or red-team work, when a behavioral proof needs hostile inputs, or when high-risk work lacks dynamic evidence. Test the actual candidate and substantiate failures.
---

# Duck Break

An attack names the claim it can refute, executes the attempt, and observes the result. Reading and
opinion are not an attack. Survival of the selected attacks establishes only that scope. The doer
reports findings. The authorized caller repairs them and reruns the invalidated checks.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

## Bound the attacks and isolate destructive work

Record the candidate and environment. Read its outcome, contracts and realistic operating
conditions first. Do not invent deployment states or require irrelevant
attacks. A goal or plan with no running artifact can have premises tested but cannot claim
runtime correctness. Instruction changes need realistic agent trials with actions and final-state
checks; a packaging validator does not establish behavior. Run each arm with only its own text
loaded, since an installed copy of the skill otherwise answers for the candidate. In Claude
Code, `claude -p --setting-sources project --plugin-dir <arm>` drops the user's skills,
hooks and instructions that `--plugin-dir` alone leaves in. A prompt that names no skill measures
whether the description fires. One that names it measures only the body.

Attack a disposable copy for mutations or destructive tests, never the candidate checkout or live
user data. Worktrees and clones carry only committed state. Capture staged, unstaged and relevant
untracked changes as [`duck-split`](../duck-split/SKILL.md) does: as a ref, not a stash. Verify the
copy matches the candidate before you attack. Record the pre-attack state, and restore it between
attacks. Use isolated data, ports and process groups for crash tests. Verify no children survive
before a restart. Point every database, queue, external API and cloud account the copy
reaches at a disposable or stubbed endpoint, and remove live credentials. If you cannot, leave that
attack unattempted and say so. Preserve original uncommitted and ignored files.

## Select attacks that discriminate

- **Oracle check:** expect a targeted mutation or negative control to fail for the intended reason. If
  it survives, decide if it is equivalent, irrelevant to the contract, an unnecessary mechanism, or
  missing coverage. An import failure does not show a behavioral test catches the bug.
  Mutation testing is one tool, not the only valid check.
- **Boundary and sequence abuse:** malformed, empty, large, duplicate, reordered, stale or
  concurrent inputs, derived from reachable paths and input classes. State limits; do not claim
  every input was exhausted.
- **Invariant attack:** violate the required isolation, authorization, state transition or other
  contract from outside the boundary. Inspect the resulting state, not only the return code.
- **Crash/recovery:** if recovery is part of the contract, interrupt a consequential operation,
  restart and inspect persisted state. Kill an isolated process group; leave no orphaned children.
- **Real artifact:** exercise a critical path in the built binary or app. Test doubles and a green
  suite can omit the integration that decides the user-visible outcome.

Choose the highest-consequence plausible failures first. A focused proof can use one attack. A broad
break covers material contracts in its agreed scope. After a defect, keep checking remaining
material claims unless they depend on the broken prerequisite. Respect owner effort limits. Report
blocked or unattempted attacks; do not claim they survived.

Differential results are leads, not verdicts. Resolve differences against an independent contract,
with permitted order, nondeterminism and tolerances normalized. One wrong result does not make
both implementations wrong. Identical results can share a defect.

## Report and hand off

Capture for each attack:

- the command or input;
- the candidate identity;
- the expected violation;
- the observed output;
- the final state.

Read exit status directly: a pipeline can report a filter's status instead of the artifact's. A
defect is a contract violation observed directly. A captured invariant breach counts once, even if
a race will not trigger twice. Reproduce when the capture is inconclusive. Record repeatability
apart from strength. Distinguish suspected failures from substantiated ones. Keep the complete
finding list, grouped by affected claim and consequence. Rank it when the owner asks. Report
no-finding attacks and limits under the same evidence standard.

Use [`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules for a downstream handoff:
`break-rN.md` or an explicit section of the shared work record, with restored-state confirmation
and evidence that survives scratch cleanup. A standalone report can stay in the response. Do not
advance the candidate only to save the report. [`duck-review`](../duck-review/SKILL.md) consumes
required break evidence for release; a successful attack suite is not independent approval.
