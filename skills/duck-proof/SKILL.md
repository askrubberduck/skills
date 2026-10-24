---
name: duck-proof
description: Make the goal, the path, and the finished work earn your trust through counterexamples and executed checks. Use when the user asks whether a solution is necessary, correct, or elegant, asks to prove a goal, a plan or a finished shape, asks whether every piece of finished work is earning its place before review, or wants work verified before review.
---

# Duck Proof

Try to falsify the claim, including the owner's preferred goal or mechanism. Agreement, an
aggressive review and a green suite are not substitutes for a discriminating test. A supported
claim may survive unchanged; do not manufacture defects to look skeptical.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

## Scope and authority

Identify the object: goal, design, plan, implementation or completed shape. State the outcome,
constraints and claim under test. Separate the desired benefit from the proposed mechanism.
Challenge unsupported premises; never silently replace the owner's values or goal. New evidence can
reopen a settled premise.

Analysis-only or report-only means no candidate edits. A request to prove work authorizes local
checks; apply repairs only when execution or fixes are authorized, then continue through repairs
and verification without asking again. Selected finding IDs limit the work; report each as applied,
skipped with its reason, or parked. Commit, PR, push, merge, external dispatch and messages need
their own existing authority; this skill grants none.

For code, record base and candidate; read the full relevant diff including staged, uncommitted and
relevant untracked content, carried into a test copy the way [`duck-split`](../duck-split/SKILL.md)
captures a dirty tree — a ref, not a stash. Read callers and the complete affected path, not just
changed lines. A goal or plan needs no invented candidate SHA or diff.

## 1. Find what would disprove it

Read relevant project constraints and the defect ledger, `defect-classes.md` at the durable records
home (section "Evidence and handoff"), when one exists; never block a narrow check because none
exists, but state the gap when it limits coverage.

- **Goal:** establish the pain and success measure. Compare no change, removal or reuse when they
  could meet the same outcome. An unsupported benefit stays unproven.
- **Mechanism:** trace cause to effect. Hold a plausible competing explanation and choose an
  observation that separates them; use [`duck-why`](../duck-why/SKILL.md) when the cause needs
  investigation.
- **Plan:** name the assumption that would invalidate dependent steps. Could the planned tests
  succeed while the outcome fails? Run the cheapest feasibility probe before endorsing that
  path.
- **Implementation:** identify a contract violation ordinary tests might miss: duplicate,
  reordered, interrupted, stale, malformed or concurrent input as relevant to the real system.
- **Shape:** identify a mechanism that could disappear or an ownership boundary that makes the
  next realistic change hard. Compare alternatives against the same required behavior.

A broad design decision belongs in [`duck-frame`](../duck-frame/SKILL.md); a narrow necessity claim
needs no planning pipeline. Select challenges by consequence and uncertainty, not a quota.

## 2. Execute the challenge

For behavioral claims, run a credible attempt to violate the central contract against the actual
candidate and inspect the final state, not just the exit status. A suite collecting zero tests or
skipping every test establishes no coverage; report that limit even at exit 0. For textual claims,
source comparison can establish a broken reference or contradiction. Standalone proof runs the
necessary checks itself; a caller's output is reusable only for the same candidate, inputs and
environment. For proposals, test uncertain premises with a small experiment when possible; this
does not prove an unbuilt implementation correct.

Challenge the oracle as well as the code. Where useful, show that a negative control or targeted
mutation fails for the intended reason; a surviving mutation may be equivalent, outside the contract
or expose unnecessary code, so investigate before calling the tests weak. Adjudicate differing
permitted outputs against the contract, including ordering and tolerance, never by vote.

[`duck-break`](../duck-break/SKILL.md) owns destructive attack isolation and recovery mechanics. Use
them for selected attacks here; invoke a full break when requested or required by risk or policy.
Drive relevant input classes and positions, state bounds and omissions, and claim no exhaustive
coverage of an unbounded surface. Instruction changes take the agent trials `duck-break` requires.

Prefer the check that reports a break soonest after the edit. Cannot execute a needed check? Record
what is missing and mark the claim UNPROVEN. A plausible code read, another model's confidence and
a receipt file cannot stand in for the observation.

## 3. Repair at the level the evidence refutes

A failure can refute a line, a shared contract, the mechanism or the goal; say which before
repairing. Would deleting the unnecessary thing end the defect? Inspect sibling callers and
classify which can reach the cause; shared code does not mean every caller is broken.

On a REJECT or an owner correction, first name the decision the work rests on — the goal, a frame or
plan decision, the mechanism — and ask whether it still holds against the new evidence. Patch only
when it holds; otherwise reopen it where it was made ([`duck-frame`](../duck-frame/SKILL.md),
[`duck-plan`](../duck-plan/SKILL.md), [`duck-decide`](../duck-decide/SKILL.md)) before any edit.
The repair record names the decision and its verdict: holds or reopened.

When repairs are authorized, fix the cause at the decision that produced it, then rerun every
affected check against the edited candidate and the relevant project gates before declaring
completion; broaden for affected seams or unresolved risks, not ceremony. A failed repair sends the
claim back through the challenge, at most twice per claim; at that bound the claim stays UNPROVEN
with the failed repairs named.

If the same defect class recurs, extend an executable check over its reachable surface, using
instances as cases. Two independent occurrences record the class in `defect-classes.md` at the
durable records home, creating the file on the first class;
[`duck-review`](../duck-review/SKILL.md) names that class when it recommends the caller's circuit
breaker. Repeated one-off patches and increasingly long checklists are not closure of the class.

## 4. Prove the completed shape

Run [`duck-shape`](../duck-shape/SKILL.md)'s necessity checks and realistic change probe on the
assembled result once correctness and operational constraints hold. For each mechanism, name what
removing it loses or the contract that requires it; line or abstraction counts are not targets.
Shape edits return to section 3's executable checks. Run [`duck-dry`](../duck-dry/SKILL.md) on
authorized edits; a prose cleanup that changes behavior also invalidates evidence.

## 5. Conclude on evidence, not concurrence

Per material claim return **SUPPORTED WITHIN SCOPE**, **REFUTED** or **UNPROVEN**, citing the
strongest attempted refutation, actual observation and remaining limit. Name the simpler alternative
considered and why it won or lost. Promise no optimality or correctness beyond the checks performed.

Stop when the relevant claims have evidence and no substantiated blocker remains, a central claim
is refuted, or required evidence is unavailable. Another pass needs a named unresolved question and
a new discriminating observation. Agreement with the owner is not evidence; opposition without
evidence is not a finding.

This is self-verification, not the independent release approval
[`duck-review`](../duck-review/SKILL.md) owns. For an additional independent challenge use its
challenge-selection reference, and state any missing independence rather than upgrading a
self-check into a gate.

## Evidence and handoff (durable-home rules)

A standalone question takes a concise response with commands, results and limits. When another
stage consumes the pass, write or update the project's existing durable work record: claim,
candidate identity, environment, attack, observation, repairs and final reruns. Resolve the home
from instructions — including a location outside the tree — then existing convention, then an
owner-provided task directory; ask only if a durable handoff is required and none is available. Do
not invent a records branch. The home holds `proof-rN.md`, `break-rN.md`, `race-rN.md`, review
reports, landing outcomes, `defect-classes.md` and `merge-pin-<host>.md`; dispatch measurements
live apart, in `~/.askrubberduck/`.

Use `proof-rN.md` when the consumer expects it, or give the exact section of a shared work record.
Evidence and referenced artifacts must survive the handoff; scratch paths that will vanish are not
durable citations. Raw logs and CLI stdout stay in scratch, never in a commit. Do not advance a
candidate or its base merely to save a receipt; local work needs no commit to record a pass.
[`duck-run`](../duck-run/SKILL.md) and [`duck-land`](../duck-land/SKILL.md) handle authorized
release transitions and exact target checks.
