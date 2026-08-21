---
name: duck-why
description: Name the cause of a failure before anyone writes a fix, because the symptom is not the defect. Use when a test fails, a bug is reported, a build breaks, something behaves differently than expected, a fix keeps not sticking, or the user asks why something is broken.
---

# Duck Why

Explain the failure out loud, in order, to something that believes none of it. Most bugs die in
that sentence — the step you skip while explaining is the step you skipped while writing.

**This skill names a cause. It does not fix one.** Doer and judge stay separate here for the same
reason they do in `duck-break`: the pass that finds a cause and the pass that repairs it reward
opposite instincts, and running them together turns "I understand this" into "I changed something
and it stopped". The output is a named, evidenced cause; the fix travels the normal pipeline like
any other change. Separation bars the fix, never the thinking.

## Reproduce before you reason

A failure you cannot reproduce on demand is a report, not a defect. Get to one command that fails
and record it — that command is the only thing that will later prove the cause was real.

Cannot reproduce? That is the finding. Say what you ran, what happened instead, and what would
distinguish a flake from a fix that already landed. **Never reason about a failure you have not
seen**; a plausible explanation of an unobserved bug is fiction with a stack trace.

## Symptom, then cause

The report names where it hurt, not where it broke. Walk outward from the failing assertion to the
first point where reality diverged from intent — the last place the state was still correct is the
edge of the defect.

Ask why until the answer stops being about the code and starts being about a decision: a contract
nobody wrote down, an assumption that used to hold, a boundary two components disagreed about.
Stopping at the first line that could be edited to make the red go away is how a symptom gets
patched and the cause ships.

**Grep every caller before you name it.** A cause in a shared function that only one caller trips
is still a cause in the shared function, and the sibling callers are already broken.

## Competing hypotheses, cheap discriminators

One hypothesis pursued is a guess defended. Hold at least two, and for each write down the cheapest
observation that would **rule it out** — then run that, not the one that would confirm your
favourite. A hypothesis with no discriminating test is not a hypothesis, it is a preference.

Evidence is what a command printed. Reasoning about what the code must do is a hypothesis, however
confident; label it as one. When history is the evidence, bisect it and name the commit rather than
reading diffs for something that looks guilty.

Errors dismissed along the way as unrelated are hypotheses too. Say why each is unrelated, or it
stays on the list.

## What comes back

- The **reproducing command** and its output.
- The **cause**, in one sentence, at the level of the decision that produced it.
- The **evidence chain**: each step citing `file:line`, a command and its output, or a named commit.
  A link asserted rather than observed is marked as an assumption.
- **Every caller or path that shares the cause**, not just the reported one.
- Hypotheses ruled out, each with what ruled it out. A short list of dead ends is worth more than a
  confident single answer, because it is what stops the next person re-running them.
- Where the fix belongs, named but **not made**: a unit for `duck-run`, a re-frame via `duck-frame`
  when the cause is the architecture, an owner call via `duck-decide` when the cause is a policy
  nobody has set. `duck-proof` is what later shows the fix actually took.

## Common mistakes

- Fixing it because the cause was obvious once found — that is the boundary this skill exists to
  hold, and "it was a one-liner" is how an unreviewed change lands in a gate file.
- Explaining the failure instead of reproducing it. The explanation is the method, not the evidence.
- Stopping at the line that makes the test green rather than the decision that made the line wrong.
- One hypothesis, pursued until it fits. Ruling nothing out is not investigating.
- Treating a passing suite as proof the cause is gone — nothing was fixed yet, and if the suite
  passed while the bug existed, the suite is a second finding.
