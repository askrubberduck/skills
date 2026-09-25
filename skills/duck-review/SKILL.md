---
name: duck-review
description: Review work from multiple angles or deliver an independent judgment. Use for designs, plans, documents, code, local changes, completed work or PRs; findings-only reviews; an independent second opinion; a release gate; or to answer a review you received, saying which comments still apply to what you pushed since and drafting the replies. Findings-only review stays in-session; independent and release reviews use cross-model scrutiny and return APPROVE, REJECT, or NOTE. It does not fix, repeat, or land.
---

# Duck Review

Review the specified work at its current stage. Test a design's assumptions without demanding an
implementation; judge completed work against observable results.

Independent scrutiny precedes release approval. The builder must validate the candidate first;
a reviewer is not a substitute for the doer's own breaking attempts.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

**One invocation, one pass.** Never edit the candidate, create its prerequisite evidence, loop
until reviewers approve, or land it. The caller owns repairs, owner decisions and the next
authorized action.

## Findings or independent judgment

An explicit independent, cross-model or release-gate review uses the workflow below. Otherwise a
findings-only, analysis-only or "multiple angles" request, or an answer to a received review,
uses this in-session path. With no scope specified, `[review].default` in
`~/.askrubberduck/config.toml` decides (default `findings`); `duck-run` and `duck-land` name the
release-gate path when they call it. A findings pass never satisfies a required gate.

Resolve the target, applicable base, constraints and prior dispositions as in preparation steps 1–2;
for re-review also apply step 5. Inspect relevant risk surfaces such as behavior, failure recovery
and maintainability. Use distinct lenses rather than a fixed reviewer count; delegate only when
useful and authorized; what counts as a different family is in
[challenge selection](references/challenge.md).

Substantiate and adjudicate findings against the current target using the criteria below. Why a
value, guard or construction already in the history exists is answered by `duck-why`'s decision
trace, not a guess. Return one consolidated list with stable IDs, severity, evidence and proposed
fixes, plus coverage limits. No gate verdict is issued; a receipt is needed only when policy or a
downstream handoff requires one. Report in-session. Posting comments, submitting a GitHub review and
resolving threads each need their own existing authorization. Then return to the caller: a later
selection authorizes that caller's scoped local fixes, not another review or a new approval round.
Commit and publication remain separate actions.

## Answer a received review

When the user is the author and a review has landed, judge each thread against the current
candidate, not the revision the reviewer saw, and give it one disposition with its evidence:
still valid, already fixed, disagree, out of scope, or a challenge to the approach. A thread that
questions the mechanism rather than a line gets no patch: `duck-shape` over the problem, and a
proposed shape, come before any edit. Draft one reply per thread: at most three words when
agreeing or reporting a fix, fifteen otherwise. "Resolve all" covers resolving only, and only
threads already fixed; the rest stay open and are listed.

## Prepare the review

1. Resolve the exact target, its version and the requested judgment. For a code release use the last
   released tag through the candidate, not adjacent commits; for a PR use its own base. An
   intentionally captured dirty worktree (captured as `duck-split` describes: a ref, not a stash)
   can be reviewed, but landing later needs an authorized exact commit. For a design, plan or
   document, identify the supplied revision or snapshot; no PR, commit or invented Git base is
   needed.
   A change is reviewed with what depends on it: callers, config and tests for code; the sections
   and consumers that cite it for a document. A finding outside the change is in scope. Report
   what was read beyond it; the change alone is a coverage limit to state, never the default.
2. Use the caller's recorded outcome, constraints and acceptance baseline across review rounds.
   For a standalone review, establish that baseline and the effort bound once — by default the
   setup's budget in [challenge selection](references/challenge.md) — so steps 5–6 have a bound
   to read.
   Name the coordinating caller who owns convergence, prior findings and the remaining round
   bound; `duck-run` defines the default loop
   contract for an executing caller, including stable cause IDs, reopening and what counts as a
   blocker versus a proposal. Treat the mechanism and its benefit as claims to challenge. If new
   evidence refutes the goal or criteria, return that contradiction; do not silently rewrite
   acceptance criteria to pass or fail the candidate.
3. Select the required participants and effort bound using [challenge
   selection](references/challenge.md). Record the selected set before dispatch. A gate-semantics
   change uses the PRE-change rules, including prerequisites and participant count; the new text
   cannot authorize itself.
4. Check the caller's evidence using `duck-proof`'s durable-home rules. A release gate requires a
   proof receipt tied to the final candidate; substantial, uncertain or trust-touching work also
   needs the settled `duck-plan` record, including its actual challenge and any required independent
   input. Trust-touching work needs `duck-break` evidence appropriate to the changed surface;
   executable code arriving from `duck-run` carries its rally receipt or the reason the rally did
   not run. Instruction changes need agent behavior trials, not invented service crash tests.
5. Spot-check cited commands or artifacts; file presence alone is not evidence. A repair invalidates
   relevant earlier checks. For re-review, identify the previous reviewed revision or snapshot and
   the current target. Inspect the new delta and affected contracts or paths, reopen impacted
   findings, and reuse only evidence whose assumptions still hold. Never check only the old finding
   list. Report both revisions and which causes closed, stayed open or reopened. If the previous
   target is unavailable or changed contracts invalidate wider evidence, name the gap and broaden
   the review accordingly. Missing material evidence means the gate cannot
   approve; a standalone opinion may still report what it can establish.
6. Do not dispatch beyond the caller's recorded bound; return the unresolved status and evidence
   without approval. For a third or later review round, require the caller's recorded loop
   diagnosis. Judge progress by unresolved causes, not wording or finding counts. A local
   record needs no commit unless the repository requires one. Do not dispatch an unchanged candidate
   just to seek a friendlier verdict.

Use [dispatch mechanics](references/dispatch.md) for identity, isolation, export authority and
transport checks. Pass review material by absolute path with source access; the brief carries
requirements and receipts as claims to attack, never as a coverage map. Reviewers seek a
credible counterexample and a simpler valid path, substantiate their findings, and accept a claim
that survives. Neither owner preference nor a mandate to be negative is evidence.

## Reviewer result contract

Require each reviewer to return `APPROVE | REJECT | NOTE` and findings ranked
`BLOCKER | SHOULD | NOTE`. A reviewer's `APPROVE` claims no release-blocking defect and its
`REJECT` claims at least one; its `NOTE` is not `APPROVE-W-CONDITIONS` and not an outage. These
are inputs to the superreview, not votes. A malformed result is *unranked* or *unsupported* as
[dispatch mechanics](references/dispatch.md) defines them; only *unsupported* leaves the gate
short a reviewer, and both leave findings that are still claims to adjudicate.

## Adjudicate the claims

Treat every verdict and finding as a claim, not a fact. For each finding, inspect the current target
and classify it as a substantiated `BLOCKER`, retained `SHOULD`, retained `NOTE`, or dismissed with
a recorded reason.

**When the actor adjudicating is the actor that built the candidate, adjudication is the weak
point** — the reviewers are different families but the synthesis is not, and dismissing a true
finding looks identical to dismissing a false one. Say so in the report, dismiss only on evidence a
third party can re-check from the artifacts, and let a finding you cannot settle stand rather
than fall. Under the Broad setup, each family's findings are dispositioned by the other family
first — one findings-list dispatch each, smaller than a review, recorded with `stage =
disposition` so `remaining` never mistakes it for a capture — and the doer synthesizes where
the dispositions agree; where they disagree, the doer dismisses only on executed evidence.
A finding that stands unsubstantiated after that is a `NOTE` with the disagreement named, not a
`BLOCKER`. Record who adjudicated each finding in `adjudicated_by`; `scripts/ledger.py precision`
turns the `substantiated` column into precision per family, class and tier.
A substantiated blocker stands until resolved. An unsubstantiated suspicion is not a blocker;
if missing evidence prevents a gate decision, return `NOTE` and name the uncertainty.

- Judge a code change where it will run: a system that upgrades from an older state and can roll
  back, not a fresh one or an invented deployment. A new way to fail is a change to that system.
- A guard added to cover a race that appeared when another guard was removed says the removed
  one was load-bearing.
- A changed contract is incomplete until every other party to it moves in the same change or is
  named as follow-up.
- A delta nobody asked for is a finding until someone explains it.
- Check the repository's own conventions before accepting a demand for a new artifact. Existing
  evidence beats reviewer-invented ceremony.
- Ask what the code is for, and whether the mechanism delivers the stated benefit, before
  recommending a patch; challenge the goal itself only when asked. If removing the feature, flag,
  branch, or check ends the defect without losing a required outcome, recommend deletion. Sunk
  effort does not keep a mechanism that fails its outcome.
- On deletion-heavy diffs, inspect the diff prefix and post-change file before accepting a claim
  that a fact disappeared; context lines and moved facts create false blockers.
- Resolve disagreement about framework behavior by reading the dependency source, not by vote.
- Disagreement about what *should* be — a design intent, a public boundary, a policy, a cost or
  schedule tradeoff — has no source to read: route it to the owner via `duck-decide` instead of
  settling it as the doer.
- If supplied history shows the same rule drawing repeated findings, ask whether that rule should
  exist rather than proposing another patch. When two consecutive rounds' substantiated blockers
  target code introduced by remediation rather than the original candidate, **or fall in one class
  of `defect-classes.md` whatever code they land on**, say so in the report — naming the class, not
  only the instance — and recommend the caller's circuit breaker — rebuild the contested unit under
  `duck-race`'s race mode, or lock the class in under its rally mode — instead of implicitly
  inviting the next round.
- Count concepts, not lines: identify any new branch, exception, or second home for the same fact,
  any abstraction without a required contract or credible change-path justification, and any unit
  that took on a second job.
  `duck-shape` owns this lens at change time; this gate reports any miss to the caller.
- A comment that states something false about the code is a defect, ranked on what it misleads
  about. A demand for explanatory comments is not: where the code is unclear the fix is the code,
  and `duck-dry` sets what the surviving comments carry.
- Judge the change, not paperwork. A receipt or commit-message defect is a `NOTE` unless it makes
  the underlying artifact claim unverifiable.

## Synthesize one result

Return exactly one superreview result:

- `APPROVE` — a gate decision was requested, **every required reviewer returned a usable verdict**,
  and no substantiated `BLOCKER` remains. An outage on a required reviewer bars `APPROVE`: it
  produced no findings, which is not the same as finding nothing. Retry an outage once within the
  effort bound, or return `NOTE` and say which participant is missing. Never reduce the required set
  after dispatch.
- `REJECT` — at least one substantiated `BLOCKER` remains.
- `NOTE` — something material stands out, but no gate decision was requested or the available
  criteria and evidence do not support one. `NOTE` neither authorizes nor rejects the candidate.

Only a substantiated `BLOCKER` justifies `REJECT`; `SHOULD` and finding-level `NOTE` items do not.
Reviewer unanimity is neither required nor sufficient. A false `REJECT` may be dismissed with
evidence, and an `APPROVE` cannot erase a defect the superreview substantiates. A release workflow
may land only `APPROVE`; a superreview `NOTE` is a non-decision, not a hidden pass or failure.

Report the authoritative result, each reviewer's pinned model id and family, each raw verdict, every
finding's adjudicated classification and evidence, any outage or downgrade, and the exact target and
criteria reviewed. Finalize each participant's row in `~/.askrubberduck/dispatches.tsv` and append
one row per adjudicated finding to `findings.tsv`, with a stable `cause_id` shared across
participants that found the same cause; with two eligible captures (shadows excluded), report
`scripts/ledger.py remaining <gate_id>` — the estimate of defects neither found.

**Write that report where the landing gate can read it** — the same durable records home as the
receipts, never only into the caller's context or `$SP`. A verdict that exists only in a session
transcript cannot be checked later, and `duck-land` needs the authorization itself, not a
recollection that one was granted.

Then stop.
