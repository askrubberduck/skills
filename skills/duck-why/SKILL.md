---
name: duck-why
description: Name the cause of a failure before anyone writes a fix, because the symptom is not the defect. Use when a test fails, a bug is reported, a build breaks, something behaves differently than expected, a fix keeps not sticking, or the user asks why something is broken.
---

# Duck Why

Find the demonstrated cause of the failure and the paths it affects. Stop when that explanation
accounts for the evidence; a typo need not become an architectural or organizational diagnosis.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
This skill diagnoses without editing the candidate. Return the cause and repair location to the
caller, which continues any already-authorized fix and verification. Do not request the same local
repair permission again or imply that diagnosis satisfies a release gate.

## Reproduce and trace

Obtain a reproducing command and inspect its output and relevant state. If the environment is
unavailable or the fault intermittent, use logs, traces and history, state the reproduction limit,
and distinguish observations from provisional explanations.

Trace the failing path to the first point where behavior diverges from the required contract.
Read the function's callers and relevant configuration; classify which can reach the failure and
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

## Return an actionable diagnosis

Lead with the cause or the unresolved question, then provide:

- The reproducer or available trace, actual result and expected contract.
- Source and observations connecting the failure to the cause, including affected sibling paths.
- The shared repair location and the check that would show the failure is gone.
- Material uncertainty and the next discriminator, if the cause remains unresolved.

Keep ruled-out hypotheses only when their evidence prevents repeating a consequential dead end.
Do not create a design or work item merely to explain a local defect. An unsettled architectural
contract belongs to `duck-frame`; an actual owner policy choice belongs to `duck-decide`.
The executing caller may use `duck-run`; `duck-proof` verifies the eventual repair.
