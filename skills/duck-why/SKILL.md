---
name: duck-why
description: Name the cause of a failure before anyone writes a fix, because the symptom is not the defect. Use when a test fails, a bug is reported, a build or CI goes red, a traceback or error is pasted, something passes in one place and fails in another, a fix keeps not sticking, a review rejects a change, or the user asks why something fails, even when the code is pasted inline and the cause looks obvious. Also when the user asks who added a constant, timeout, flag or guard and why, or whether that reason still holds, even though nothing is failing. Not for explaining how something works.
---

# Duck Why

Find the demonstrated cause of the failure and the paths it affects. Stop when the explanation
accounts for the evidence; a typo need not become an architectural diagnosis.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
This skill diagnoses without editing the candidate. Return the cause and repair location to the
caller, which continues any already-authorized fix and verification. Do not request the same local
repair permission again or imply that diagnosis satisfies a release gate.

## Reproduce and trace

Reproduce and inspect output and relevant state. If the environment is unavailable or the fault
intermittent, use logs, traces and history, state the reproduction limit, and distinguish
observations from provisional explanations.

Trace the failing path to the first point where behavior diverges from the required contract. Read
what depends on the failing part (callers and configuration for code; citing sections and decisions
otherwise) and classify which can reach the failure and which enforce preconditions that prevent
it. State search limits when external or dynamic callers cannot be enumerated. Shared code does not
imply every caller is broken.

Identify the cause at the level needed to explain those paths: a shared rule may need one repair at
its owner rather than a guard in each caller; a wrong comparison may need only that comparison
fixed. A fix that would work around a recorded design or policy decision makes that decision a
cause candidate.

## Separate plausible causes

When more than one explanation fits, run the cheapest observation that distinguishes them. With
decisive direct evidence, verify that explanation without inventing a rival. A passing general
suite does not refute a reproducer it never exercises.

Cite inspected source as source evidence, executed behavior as observation, deductions as
reasoning; never describe an unexecuted prediction as observed output. Investigate additional
errors that could affect the causal chain; record why a consequential competing cause was ruled out.

## Trace an existing decision

A question about when or why something was introduced has no failure to reproduce. Trace the
artifact's own history: for code, `git log -S` or `-G` on the symbol and blame at the current line;
for a document or plan, its revisions. Find where the reason was stated (description, linked ticket,
review thread); keep the recorded reason apart from your inference and check it against today's
callers and later changes. Return the introducing change, its record, the reason, and whether it
holds, lapsed (name the change that removed the reason) or is unknown. A lapsed reason is a
finding, not a deletion; removal belongs to [`duck-shape`](../duck-shape/SKILL.md).

## Return an actionable diagnosis

For a failure, lead with the cause or the unresolved question, then:

- The reproducer or available trace, actual result and expected contract.
- Source and observations connecting the failure to the cause, including affected sibling paths.
- The shared repair location and the check that would show the failure is gone.
- Material uncertainty and the next discriminator, if the cause remains unresolved.

A repair restores the contract; deleting the failing file, directory or check removes the evidence,
not the cause, and is not offered as the fix.

For a cause in code landed from a reviewed candidate, append a row to
`~/.askrubberduck/findings.tsv` with `dispatch_id = -`, `tier = production`, `substantiated = 1`, a
new `cause_id`, and in `candidate` the SHA the gate reviewed ([`duck-land`](../duck-land/SKILL.md)'s
outcome record maps the landed commit back to it). `$LEDGER missed` (`python3` with the absolute
path of `../duck-review/scripts/ledger.py`, resolved from this skill's directory, typed out as
`python3 "<path>" <subcommand>` rather than held in one variable) joins that SHA to every dispatch
that returned `APPROVE` on it.

Keep ruled-out hypotheses only when their evidence prevents repeating a consequential dead end. Do
not create a design or work item to explain a local defect: an unsettled architectural contract
belongs to [`duck-frame`](../duck-frame/SKILL.md), an owner policy choice to
[`duck-decide`](../duck-decide/SKILL.md). [`duck-proof`](../duck-proof/SKILL.md) verifies the
eventual repair.
