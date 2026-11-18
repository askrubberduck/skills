---
name: duck-proof
description: Make the goal, the path, and the finished work earn your trust through counterexamples and executed checks. Use when the user asks whether a solution is necessary, correct, or elegant, asks to prove a goal, a plan or a finished shape, asks whether every piece of finished work is earning its place before review, or wants work verified before review.
---

# Duck Proof

Try to falsify the claim, including the owner's preferred goal or mechanism. Agreement, an
aggressive review and a green suite do not replace a discriminating test. A supported claim may
survive unchanged. Do not manufacture defects to look skeptical.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

## Scope and authority

Identify the object: goal, design, plan, implementation or completed shape. State the outcome,
constraints and claim under test. Separate the desired benefit from the proposed mechanism.
Challenge unsupported premises. Never silently replace the owner's values or goal. New evidence can
reopen a settled premise.

Analysis-only or report-only work permits no candidate edits. A request to prove work
authorizes local checks. Apply repairs only when execution or fixes are authorized. Then repair
and verify without asking again. Selected finding IDs limit the work. Report
each as applied, skipped with its reason, or parked. Commit, PR, push, merge, external dispatch and
messages need their own existing authority. This skill grants none.

For code, record base and candidate. Read the full relevant diff, including staged, uncommitted and
relevant untracked content. Carry it into a test copy the way
[`duck-split`](../duck-split/SKILL.md) captures a dirty tree: a ref, not a stash. Read callers and
the complete affected path, not only changed lines. A goal or plan needs no invented candidate SHA
or diff.

## 1. Find what would disprove it

Read relevant project constraints and, if one exists, the defect ledger: `defect-classes.md` at the
durable records home (section "Evidence and handoff"). If none exists, do not block a narrow check;
state the gap when it limits coverage.

- **Goal:** Establish the pain and success measure. If the option of no change, removal or reuse
  can meet the same outcome, compare it. An unsupported benefit stays unproven.
- **Mechanism:** Trace cause to effect. Hold a plausible competing explanation, and choose an
  observation that separates them. If the cause needs investigation, use
  [`duck-why`](../duck-why/SKILL.md).
- **Plan:** Name the assumption that would invalidate dependent steps. Ask whether the planned
  tests can pass while the outcome fails. Before you endorse that path, run a feasibility probe
  that can fail.
- **Implementation:** Identify a contract violation that ordinary tests can miss. Consider
  duplicate, reordered, interrupted, stale, malformed or concurrent input, as relevant to the real
  system.
- **Shape:** Identify a mechanism that can disappear, or an ownership boundary that makes the next
  realistic change hard. Compare alternatives against the same required behavior.

A broad design decision belongs in [`duck-frame`](../duck-frame/SKILL.md). A narrow necessity claim
needs no planning pipeline. Choose challenges by consequence and uncertainty, not quota.

## 2. Execute the challenge

For a behavioral claim, run a credible attempt to violate the central contract against the actual
candidate. Inspect the final state, not only the exit status. A suite that collects zero tests or
skips every test establishes no coverage. Report that limit, even at exit 0. For a textual claim,
source comparison can establish a broken reference or contradiction. A standalone proof runs the
necessary checks itself. A caller's output is reusable only for the same candidate, inputs and
environment. For a proposal, test uncertain premises with a small experiment when possible. It does
not prove an unbuilt implementation correct.

Challenge the oracle as well as the code. Where useful, show that a negative control or targeted
mutation fails for the intended reason. A surviving mutation can be equivalent, outside the
contract, or a sign of unnecessary code. Investigate it before you call the tests weak. Adjudicate
different permitted outputs against the contract, including order and tolerance, never by vote.

[`duck-break`](../duck-break/SKILL.md) owns destructive attack isolation and recovery mechanics.
Use them for selected attacks. Invoke a full break on request, or when risk or policy requires
one. Drive relevant input classes and positions. State bounds and omissions. Claim no exhaustive
coverage of an unbounded surface. Instruction changes take the agent trials `duck-break`
requires.

Prefer the check that reports a break soonest after the edit. If a needed check cannot run, record
what is missing and mark the claim UNPROVEN. A plausible code read, another model's confidence and
a receipt file cannot replace the observation.

## 3. Repair at the level the evidence refutes

A failure can refute a line, a shared contract, the mechanism or the goal. Say which before you
repair. Ask whether deletion of the unnecessary thing would end the defect. Classify which
sibling callers can reach the cause. Shared code does not mean every caller is broken.

On a REJECT or an owner correction, first name the decision under the work: the goal, a frame or
plan decision, or the mechanism. Ask whether it still holds against the new evidence. Patch only if
it holds. Otherwise, reopen it where it was made ([`duck-frame`](../duck-frame/SKILL.md),
[`duck-plan`](../duck-plan/SKILL.md), [`duck-decide`](../duck-decide/SKILL.md)) before any edit.
The repair record names the decision and its verdict: holds or reopened.

If repairs are authorized, fix the cause at the decision that produced it. Before you declare
completion, rerun every affected check and the relevant project gates on the edited candidate.
Broaden for affected seams or unresolved risks, not ceremony. A failed repair sends the claim back
through the challenge, at most twice per claim. At that bound, the claim stays UNPROVEN with the
failed repairs named.

If the same defect class recurs, extend an executable check over its reachable surface. Use
instances as cases. After two independent occurrences, record the class in `defect-classes.md`.
Create the file for the first class.
[`duck-review`](../duck-review/SKILL.md) names that class when it recommends the caller's circuit
breaker. Repeated one-off patches and ever longer checklists do not close the class.

## 4. Prove the completed shape

Once correctness and operational constraints hold, run [`duck-shape`](../duck-shape/SKILL.md)'s
necessity checks and realistic change probe on the assembled result. For each mechanism, name what
its removal loses, or the contract that requires it. Line or abstraction counts are not goals.
Shape edits return to section 3's executable checks. Run [`duck-dry`](../duck-dry/SKILL.md) on
authorized edits. A prose cleanup that changes behavior also invalidates evidence.

## 5. Conclude on evidence, not concurrence

For each material claim, return **SUPPORTED WITHIN SCOPE**, **REFUTED** or **UNPROVEN**. Cite the
strongest attempted refutation, actual observation and remaining limit. Name the simpler
alternative considered and why it won or lost. Promise no optimality or correctness beyond the
executed checks.

Stop when one of these is true:

- The relevant claims have evidence, and no substantiated blocker remains.
- A central claim is refuted.
- Required evidence is unavailable.

Another pass needs a named unresolved question and a new discriminating observation. Agreement with
the owner is not evidence. Opposition without evidence is not a finding.

This skill is self-verification, not the independent release approval that
[`duck-review`](../duck-review/SKILL.md) owns. For more independent challenge, use its
challenge-selection reference. State any missing independence. Do not upgrade a self-check into a
gate.

## Evidence and handoff (durable-home rules)

A standalone question gets a concise answer: commands, results and limits. If another stage
consumes the pass, write or update the project's existing durable work record. The record holds the
claim, candidate identity, environment, attack, observation, repairs and final reruns. Resolve the
records home in this order:

1. Instructions, including a location outside the tree.
2. Existing convention.
3. An owner-provided task directory.

Ask only if a durable handoff is required and none is available. Do not invent a records
branch.

Every handoff, from any skill, carries:

- the outcome, in that skill's own status words;
- the candidate identity;
- the evidence, by paths that survive scratch cleanup;
- the unresolved claims and coverage limits;
- the next authorized action and who owns it.

The records home holds `proof-rN.md`, `break-rN.md`, `race-rN.md`, review reports, landing
outcomes, `defect-classes.md` and `merge-pin-<host>.md`. Dispatch measurements live in
`~/.askrubberduck/`.

Use `proof-rN.md` when the consumer expects it. Otherwise, give the exact section of a shared work
record. Evidence and referenced artifacts must survive the handoff. Raw logs and CLI stdout stay in
scratch, never in a commit. Do not advance a candidate or its base only to save a receipt. Local
work needs no commit to record a pass. [`duck-run`](../duck-run/SKILL.md) and
[`duck-land`](../duck-land/SKILL.md) handle authorized release transitions and exact candidate
checks.
