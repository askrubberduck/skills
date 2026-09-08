---
name: duck-proof
description: Make the goal, the path, and the finished work earn your trust through counterexamples and executed checks. Use when the user asks whether a solution is necessary, correct, or elegant, asks to prove a plan or finished shape, or wants work verified before review.
---

# Duck Proof

Try to falsify the claim, including the owner's preferred goal or mechanism. Agreement, an
aggressive review, and a green suite are not substitutes for a discriminating test. A supported
claim may survive unchanged; do not manufacture defects to look skeptical.

## Scope and authority

Identify the object: goal, design, plan, implementation, or completed shape. State the outcome,
constraints, and claim being tested. Separate the desired benefit from the proposed mechanism:
if the mechanism worked perfectly, would the benefit follow? Challenge unsupported premises;
never silently replace the owner's values or goal. New evidence can reopen a settled premise.

Analysis-only or report-only means no candidate edits. A request to prove work authorizes local
checks; apply repairs only when execution or fixes are authorized. Continue through those repairs
and verification without asking again. Selected finding IDs limit the work. Commit, PR, push,
merge, external dispatch and messages need their own existing authority; this skill grants none.

For code, record the base and candidate; read the full relevant diff, including staged and
uncommitted changes. Include relevant untracked files when they are part of the candidate.
`git diff <base>..<candidate>`, `git diff`, and `git diff --staged` cover different states. Read
callers and the complete affected path, not just changed lines. A goal or plan needs no invented
candidate SHA or code diff.

## 1. Find what would disprove it

Read relevant project constraints and any existing defect ledger. Do not create a ledger or
block a narrow check just because none exists; state the gap when it limits coverage.

- **Goal:** establish the pain and success measure. Compare no change, removal, or reuse when
  they could meet the same outcome. An unsupported benefit stays unproven.
- **Mechanism:** trace cause to effect. Hold a plausible competing explanation and choose an
  observation that separates them. Use `duck-why` when the cause needs investigation.
- **Plan:** name the assumption that would invalidate dependent steps. Could the planned tests
  pass while the outcome fails? Run the cheapest feasibility probe before endorsing that path.
- **Implementation:** identify a contract violation that ordinary tests might miss: duplicate,
  reordered, interrupted, stale, malformed, or concurrent input as relevant to the real system.
- **Shape:** identify a mechanism that could disappear or an ownership boundary that makes the
  next realistic change hard. Compare alternatives against the same required behavior.

A broad design decision belongs in `duck-frame`; a narrow necessity claim does not require a
whole planning pipeline. Select challenges by consequence and uncertainty, not a quota of findings.

## 2. Execute the challenge

For behavioral claims, run a credible attempt to violate the central contract against the actual
candidate and inspect the final state, not just the command's exit status. Standalone proof owns
running the necessary checks; a caller's output is reusable evidence only for the same candidate,
inputs and relevant environment. For proposals, test uncertain premises with a small experiment
when possible; this does not establish the correctness of an unbuilt implementation.

Challenge the oracle as well as the code. Where useful, show that a negative control or targeted
mutation fails for the intended reason. A surviving mutation may be equivalent, outside the
contract, or expose unnecessary code: investigate before calling the tests weak. Different
implementations may produce different permitted outputs; adjudicate differences against the
contract, including ordering and tolerance, never by vote.

`duck-break` owns destructive attack isolation and recovery mechanics. Use those mechanics for
selected attacks here; invoke a full break when requested or required by the risk/policy. Drive
relevant input classes and positions, state bounds and omissions, and do not claim exhaustive
coverage of an unbounded surface. For instruction changes, execute realistic agent tasks and
inspect their actions and outcomes; a structural Markdown validator is not behavioral proof.

Cannot execute a needed check? Record what is missing and mark that claim UNPROVEN. A plausible
code read, another model's confidence, and a receipt file cannot stand in for the observation.

## 3. Repair at the level the evidence refutes

A failure can refute a line, a shared contract, the mechanism, or the goal. Explain which before
repairing it. Would deleting the unnecessary thing end the defect? Inspect sibling callers and
classify which can reach the cause; shared code does not imply every caller is broken.

When repairs are authorized, fix the cause locally, then rerun every affected check against the
edited candidate. Earlier green results are invalidated by relevant changes. Run the relevant
project gates before declaring completion; broaden for affected seams or unresolved risks, not
ceremony. A repair that fails sends the claim back through the challenge.

If the same defect class recurs, extend an executable check over its reachable surface, using
instances as cases. Record the class in an existing ledger when appropriate. Repeated one-off
patches and increasingly long checklists are not closure of the class.

## 4. Prove the completed shape

Use `duck-shape`'s realistic change probe on the assembled result: walk one representative path
end to end, then attempt a likely next change. What rules, state owners, units and ordering facts
must the reader hold together? What can be removed without losing an outcome? Cause should be
near effect, with one authoritative home per fact.

Compare credible alternatives after correctness and operational constraints hold. Prefer fewer
independent obligations and a traceable path; line count and abstraction count are not targets.
Verify the actual guarantees of a built-in before substituting it. Preserve validation, recovery,
public contracts and necessary calibration. Shape edits return to section 3's executable checks.
Run `duck-dry` on authorized edits; a prose cleanup that changes behavior also invalidates evidence.

## 5. Conclude on evidence, not concurrence

Per material claim return **SUPPORTED WITHIN SCOPE**, **REFUTED**, or **UNPROVEN**, citing the
strongest attempted refutation, actual observation and remaining limit. Name the simpler
alternative considered and why it won or lost. Several defensible paths may have different
tradeoffs; do not promise universal optimality or correctness beyond the checks performed.

Stop when the relevant claims have evidence and no substantiated blocker remains, when a central
claim is refuted, or when required evidence is unavailable. Another pass needs a named unresolved
question and a new discriminating observation. Agreement with the owner is not evidence;
opposition without evidence is not a finding.

This is self-verification, not independent release approval. `duck-review` owns that judgment.
For an additional independent challenge, use its challenge-selection reference; identify any
missing independence honestly rather than silently upgrading a self-check into a gate.

## Evidence and handoff

For a standalone question, a concise response with commands, results and limits is sufficient.
When another stage consumes the pass, write or update the project's existing durable work record:
claim, candidate identity, relevant environment, attack, observation, repairs and final reruns.
Resolve the home from instructions, existing convention, then an owner-provided task directory;
ask only if a durable handoff is required and none is available. Do not invent a records branch.

Use `proof-rN.md` when the consumer expects it, or give the consumer the exact section in a shared
work record. Evidence and referenced artifacts must survive that handoff; scratch paths that will
vanish are not durable citations. Raw logs need not be committed. Do not advance a reviewed
candidate or its base merely to save a receipt. Local work needs no commit just to record a pass;
`duck-run` and `duck-land` handle authorized release transitions and exact target checks.
