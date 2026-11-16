---
name: duck-review
description: Review work from multiple angles or deliver an independent judgment. Use for designs, plans, documents, code, local changes, completed work or PRs; findings-only reviews; an independent or decorrelated second opinion; a release gate; or to answer a review you received, saying which comments still apply to what you pushed since and drafting the replies. Findings-only review stays in-session; independent and release reviews use cross-model scrutiny and return APPROVE, REJECT, or NOTE. It does not fix, repeat, or land.
---

# Duck Review

Review the specified work at its current stage. Test a design's assumptions without demanding an
implementation. Judge completed work against observable results. The doer validates the candidate
first; a reviewer does not replace the doer's attempts to break it.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

**One invocation, one pass.** Never edit the candidate, create its prerequisite evidence, repeat
until reviewers approve, or land it. The caller owns repairs, owner decisions and the next
authorized action.

## Findings or independent judgment

An explicit independent, cross-model, decorrelated or release-gate review uses the workflow below
and needs a participant outside the doer's family. A findings-only, analysis-only or "multiple
angles" request, or an answer to a received review, uses this in-session path. If no scope is given,
`[review].default` in `~/.askrubberduck/config.toml` decides (default `findings`).
[`duck-run`](../duck-run/SKILL.md) and [`duck-land`](../duck-land/SKILL.md) name the release-gate
path when they call it. A findings pass never satisfies a required gate.

Resolve the target, base, constraints and prior dispositions as in preparation steps 1–2, and for a
re-review step 5. Use distinct lenses, not a fixed reviewer count. Delegate only when useful and
authorized. Inspect relevant risk surfaces such as behavior, failure recovery and maintainability. A
participant from another family runs through [dispatch](references/dispatch.md) like a gate
reviewer, with its ledger row (`--setup independent`) and its adjudicated findings in
`findings.tsv`. Its `--gate` id is the findings pass's own, such as `findings-<PR or branch>`, never
a release gate's.

Adjudicate findings against the current target with the criteria below. Answer why a value, guard or
construction in the history exists with [`duck-why`](../duck-why/SKILL.md)'s decision trace, not a
guess. Return one consolidated list with stable IDs, severity, evidence, proposed fixes and coverage
limits. Issue no gate verdict. Write a receipt only when policy or a downstream handoff requires
one. Report in-session. Posting comments, submitting a GitHub review, resolving threads, commit and
publication each need their own existing authorization. Then return to the caller; a later selection
authorizes the caller's scoped local fixes, not another review or approval round.

## Answer a received review

If the user is the author of reviewed work, judge each thread against the current candidate, not the
revision the reviewer saw. Give each thread one disposition with evidence: still valid, already
fixed, disagree, out of scope, or a challenge to the approach. A thread that questions the
mechanism, not a line, gets no patch: before any edit, apply [`duck-shape`](../duck-shape/SKILL.md)
to the problem and propose a shape. Draft one reply per thread, as short as its disposition allows,
in the reply format the user requests. "Resolve all" covers resolving only, and only threads already
fixed; list the rest, which stay open.

## Prepare the review

1. Resolve the exact target, its version and the requested judgment:
   - for a code release, the last released tag through the candidate;
   - for a PR, its own base;
   - for a design, plan or document, the supplied revision or snapshot, which needs no PR, commit or
     Git base.

   You may review a dirty worktree captured as [`duck-split`](../duck-split/SKILL.md) describes (a
   ref, not a stash); a later landing needs an authorized exact commit. Review a change with what
   depends on it: callers, config and tests for code; citing sections and consumers for a document.
   A finding outside the change is in scope; report what you read beyond it. Reading only the change
   is a coverage limit to state, never the default.
2. Use the caller's recorded outcome, constraints and acceptance baseline across rounds. For a
   standalone review, set that baseline and the effort bound once; the default bound is the setup's
   budget in [challenge selection](references/challenge.md). Name the coordinating caller who owns
   convergence, prior findings and the remaining round bound. [`duck-run`](../duck-run/SKILL.md)
   defines the default loop contract: stable cause IDs, reopening, blocker versus proposal. If new
   evidence refutes the goal or criteria, return the contradiction; never rewrite acceptance
   criteria to pass or fail the candidate.
3. Select the required participants and the effort bound with
   [challenge selection](references/challenge.md). By default, an ordinary gate gets one verified
   cross-family reviewer. A trust-touching gate gets two reviewers from different families, and
   at least one of them is outside the doer's family. Record the selected set before
   dispatch.
4. Check the caller's evidence under [`duck-proof`](../duck-proof/SKILL.md)'s durable-home rules. A
   release gate needs a proof receipt tied to the final candidate. Packet-sized or trust-touching
   work also needs the settled [`duck-plan`](../duck-plan/SKILL.md) record with its actual challenge
   and any required independent input. Trust-touching work needs
   [`duck-break`](../duck-break/SKILL.md) evidence for the changed surface. Include a rally receipt
   when one ran. If the task or policy required a rally that did not run, record the reason and its
   effect on readiness; ordinary work needs no rally exemption. A shared work record with explicit
   proof, plan and break sections equals separate receipts when all consumers can resolve it;
   `proof-rN.md` and `break-rN.md` remain valid.
5. Spot-check cited commands or artifacts. File presence is not evidence, and a repair invalidates
   the relevant earlier checks. For a re-review:
   - name the previous reviewed revision and the current target;
   - inspect the new delta and affected contracts or paths;
   - reopen affected findings;
   - reuse only evidence whose assumptions still hold;
   - report which causes closed, stayed open or reopened.

   If the previous target is unavailable or changed contracts invalidate wider evidence, name the
   gap and broaden the review. Missing material evidence bars gate approval; a standalone opinion
   may still report what it can establish.
6. Never dispatch beyond the caller's recorded bound; the script refuses a round past it without the
   owner's recorded extension. Never dispatch an unchanged candidate just for a friendlier verdict.
   In both cases, return the unresolved status and evidence without approval. A third or later round
   requires the caller's recorded loop diagnosis. Judge progress by unresolved causes, not wording
   or finding counts. A local record needs no commit unless the repository requires one.

Use [dispatch mechanics](references/dispatch.md) for identity, isolation, export authority and
transport checks. Pass review material by absolute path with source access. The brief carries
requirements and receipts as claims to attack, never a coverage map. Reviewers seek a credible
counterexample and a simpler valid path, substantiate their findings, and accept a claim that
survives. Neither owner preference nor a mandate to be negative is evidence.

## Reviewer result contract

Each reviewer must open with the line `VERDICT: APPROVE | REJECT | NOTE` and rank findings
`BLOCKER | SHOULD | NOTE`. A reviewer's `APPROVE` claims no release-blocking defect; its `REJECT`
claims at least one. Its `NOTE` is not `APPROVE-W-CONDITIONS` nor an outage. They are inputs to the
superreview, not votes. A malformed result is *unranked* or *unsupported* as
[dispatch mechanics](references/dispatch.md) defines them. Only *unsupported* leaves the gate short
a reviewer; both leave their findings as claims to adjudicate.

## Adjudicate the claims

Before adjudication, read relevant project constraints and `defect-classes.md`. Find its home with
[`duck-proof`](../duck-proof/SKILL.md), section "Evidence and handoff". Check applicable classes
against the candidate; `defect-classes.md` supplies counterexamples, not a finding quota. An absent
`defect-classes.md` does not block a narrow review; state the coverage limit.

For each finding, inspect the current target and classify it as a substantiated `BLOCKER`, retained
`SHOULD`, retained `NOTE`, or dismissed with a recorded reason. Record each with
`$LEDGER record column=value …`, `adjudicated_by` included and in `class` the first name
`$LEDGER schema` lists that fits. `$LEDGER` means
`python3 "<absolute path of this skill's scripts/ledger.py>"`, typed out in every command.
`$LEDGER precision` measures past substantiation; it is not evidence that a current finding is
correct.

**If the adjudicator built the candidate, say so in the report.** Then dismiss only on evidence a
third party can re-check from the artifacts, and let a finding you cannot settle stand. Under the
Broad setup, the other family first gives a disposition on each family's findings. Each disposition
is one findings-list dispatch, smaller than a review, recorded with `stage = disposition` so
`remaining` never counts it as a capture. Where the dispositions agree, the doer synthesizes; where
they disagree, the doer dismisses only on executed evidence. A finding still unsubstantiated after
that is a `NOTE` naming the disagreement, not a `BLOCKER`.

- Judge a code change where it will run: a system that upgrades from an older state and can roll
  back, not a fresh one or an invented deployment. A new way to fail is a change to that system.
- If a change adds a guard for a race that appeared after another guard's removal, flag the removal:
  the removed guard was load-bearing.
- A changed contract is incomplete until all other parties move in the same change, or compatibility
  keeps the old contract working until a named follow-up.
- A delta nobody asked for is a finding until someone explains it.
- Check the repository's own conventions before you accept a demand for a new artifact.
- Before you recommend a patch, ask whether the mechanism delivers the stated benefit. Challenge the
  goal itself only when asked. If a blocker follows from a recorded design or plan decision, name
  that decision; the doer reopens it instead of a patch around it. If removing the feature, flag,
  branch or check ends the defect without losing a required outcome, recommend deletion.
- On a mostly-deletion diff, inspect the diff prefix and post-change file before you accept that a
  fact disappeared. Context lines and moved facts create false blockers.
- Settle framework-behavior disagreements from the dependency source, not by vote. A disagreement
  about what *should* be (design intent, a public boundary, a policy, a cost or schedule tradeoff)
  goes to the owner through [`duck-decide`](../duck-decide/SKILL.md) at every risk level.
- If supplied history shows repeated findings from the same rule, ask whether that rule needs to
  exist. Check the substantiated blockers of two consecutive rounds. If they target remediation
  code, not the original candidate, **or fall in one `defect-classes.md` class whatever code they
  land on**, say so in the report and name the class. Then recommend the caller's circuit breaker
  ([`duck-run`](../duck-run/SKILL.md)'s loop diagnosis) instead of the next round.
- Count concepts, not lines: a new branch, exception or second home for a fact, an abstraction
  without a required contract or credible change path, or a unit with a second job.
  [`duck-shape`](../duck-shape/SKILL.md) owns this lens at change time; this gate reports a miss to
  the caller.
- A false comment about the code is a defect, ranked by what it misleads about. A demand for
  explanatory comments is not: if the code is unclear, the fix is the code.
  [`duck-dry`](../duck-dry/SKILL.md) sets what the surviving comments carry.
- Judge the change, not the paperwork. A receipt or commit-message defect is a `NOTE` unless it
  makes the underlying artifact claim unverifiable.

## Synthesize one result

Return exactly one superreview result:

- `APPROVE` — a gate decision was requested, **every required reviewer returned a usable verdict**,
  and no substantiated `BLOCKER` remains. An outage on a required reviewer bars `APPROVE`: retry it
  once within the effort bound, or return `NOTE` and name the missing participant.
- `REJECT` — at least one substantiated `BLOCKER` remains.
- `NOTE` — something material stands out, but no gate decision was requested, or the available
  criteria and evidence do not support one. `NOTE` neither authorizes nor rejects the candidate.

Only a substantiated `BLOCKER` justifies `REJECT`; `SHOULD` and finding-level `NOTE` items do not.
Reviewer unanimity is neither required nor
sufficient. You may dismiss a false `REJECT` with evidence. An `APPROVE` cannot erase a defect the
superreview substantiates. A release workflow may land only `APPROVE`; a superreview `NOTE` is a
non-decision, not a hidden pass or failure.

Report:

- the authoritative result, and the exact target and criteria reviewed;
- each reviewer's pinned model id, family and raw verdict;
- every finding's adjudicated classification and evidence;
- any outage or downgrade.

The dispatch script finalizes each participant's row in `dispatches.tsv`. Record one row per
adjudicated finding with `$LEDGER record`; participants that found the same cause share one stable
`cause_id`. If measurement is requested, report `$LEDGER remaining <gate_id>` as an advisory
estimate, never a gate or continuation criterion.

**Write that report where the landing gate can read it**: the same durable records home as the
receipts, never only the caller's context or `$SP`, and never a commit on the candidate branch.

Then stop.
