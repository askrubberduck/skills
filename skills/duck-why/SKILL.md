---
name: duck-why
description: Name the cause of a failure before anyone writes a fix, because the symptom is not the defect. Use when a test fails, a bug is reported, a build breaks, a traceback or error is pasted, something passes in one environment and fails in another, behavior differs from what was expected, a fix keeps not sticking, or the user asks why something is broken, including when the code is pasted inline and the cause looks obvious. Also when the user asks who added a value, flag, guard or behavior and why, or whether that reason still holds; not for a plain explanation of how something works.
---

# Duck Why

Find the demonstrated cause of the failure and the paths it affects. Stop when that explanation
accounts for the evidence; a typo need not become an architectural or organizational diagnosis.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
This skill diagnoses without editing the candidate. Return the cause and repair location to the
caller, which continues any already-authorized fix and verification. Do not request the same local
repair permission again or imply that diagnosis satisfies a release gate.

## Reproduce and trace

Obtain a reproduction and inspect its output and relevant state. If the environment is
unavailable or the fault intermittent, use logs, traces and history, state the reproduction limit,
and distinguish observations from provisional explanations.

Trace the failing path to the first point where behavior diverges from the required contract.
Read what depends on the failing part, callers and configuration for code, the sections and
decisions that cite it otherwise; classify which can reach the failure and
which enforce preconditions that prevent it. State search limits when external or dynamic callers
cannot be enumerated. Shared code does not imply every caller is broken.

Identify the cause at the level needed to explain those paths. A shared rule may need one repair
at its owner rather than a guard in each caller. An incorrect comparison may need only that
comparison corrected. Investigate a deeper design or policy decision only when evidence points to it.

## Separate plausible causes

When more than one explanation fits, choose the cheapest observation that distinguishes them and
run it. With decisive direct evidence, verify that explanation without inventing a rival hypothesis.
A passing general suite does not refute a reproducer it never exercises.

Cite inspected source as source evidence, executed behavior as an observation, and deductions as
reasoning. Do not describe an unexecuted prediction as observed output. Investigate additional
errors that could affect the causal chain; record why a consequential competing cause was ruled out.

## Trace an existing decision

A question about when or why something was introduced has no failure to reproduce. Trace it
through the artifact's own history: for code, `git log -S` or `-G` on the symbol and blame at the
current line; for a document or plan, its revisions. Then find where the reason was stated:
description, linked ticket, review thread. Keep the recorded reason apart from your inference.
Check it against today's callers and later changes. Return the introducing change, its record,
the reason, and whether it holds, lapsed (name the change that removed the reason) or is
unknown. A lapsed reason is a finding, not a deletion; removal belongs to `duck-shape`.

## Return an actionable diagnosis

For a failure, lead with the cause or the unresolved question, then provide:

- The reproducer or available trace, actual result and expected contract.
- Source and observations connecting the failure to the cause, including affected sibling paths.
- The shared repair location and the check that would show the failure is gone.
- Material uncertainty and the next discriminator, if the cause remains unresolved.

A cause located in code that a reviewed candidate landed is the ground truth every gate lacks:
append a row to `~/.askrubberduck/findings.tsv` with `dispatch_id = -`, `tier = production`,
`substantiated = 1`, and in `candidate` the SHA the gate reviewed — `duck-land`'s outcome record
maps the landed commit back to it, since a squash gives the same tree a new identity;
`scripts/ledger.py missed` joins that SHA to every dispatch that returned `APPROVE` on it.

Keep ruled-out hypotheses only when their evidence prevents repeating a consequential dead end.
Do not create a design or work item merely to explain a local defect. An unsettled architectural
contract belongs to `duck-frame`; an actual owner policy choice belongs to `duck-decide`.
`duck-proof` verifies the eventual repair.
