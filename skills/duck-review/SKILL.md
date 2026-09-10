---
name: duck-review
description: Run one independent cross-model superreview and deliver an evidence-backed APPROVE, REJECT, or NOTE; no participation trophies. Use when a PR or diff is ready to review, a security-, privacy-, or data-sensitive change reaches its release gate, the user says "gate it" or asks for an independent second opinion. It reviews and judges; it does not fix, repeat, or land.
---

# Duck Review

Independent scrutiny precedes release approval. The builder must validate the candidate first;
a reviewer is not a substitute for the doer's own breaking attempts. If the builder adjudicates
the independent findings, identify that limited independence rather than claiming the final
judgment was wholly external.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

**One invocation, one judgment.** Never edit the candidate, create its prerequisite evidence, loop
until reviewers approve, or land it. The caller owns repairs and the next authorized action.
Analysis-only returns findings without implying release approval.

## Prepare the review

1. Resolve the exact base, candidate and requested judgment. For a release use the last released
   tag through the candidate, not adjacent commits; for a PR use its own base. An intentionally
   captured dirty worktree can be reviewed, but landing later needs an authorized exact commit.
2. Use the caller's recorded outcome, constraints and acceptance baseline across review rounds.
   For a standalone review, establish that baseline once. Name the coordinating caller who owns
   convergence, prior findings and the remaining round bound; `duck-run` defines the default loop
   contract for an executing caller. Treat the mechanism and its benefit as
   claims to challenge. If new evidence refutes the goal or criteria, return that contradiction;
   do not silently rewrite acceptance criteria to pass or fail the candidate. Each blocker names
   the existing criterion, required contract or binding policy it violates and the supporting
   evidence. A newly discovered real defect may block even when earlier reviewers missed it.
   New preferences, features and unrelated cleanup are proposals outside the gate's acceptance bar.
   Retain stable cause IDs and prior dispositions; reopening needs new contrary evidence or an
   impacting change, not another reviewer's wording.
3. Select the required participants and effort bound using
   [challenge selection](references/challenge.md). Ordinary gates default to one verified
   cross-family reviewer; trust-touching gates default to two as that reference specifies.
   Record the selected set before dispatch. A gate-semantics change uses the PRE-change rules,
   including prerequisites and participant count; the new text cannot authorize itself.
4. Check the caller's evidence using `duck-proof`'s durable-home rules. A release gate requires a
   proof receipt tied to the final candidate; packet-sized or trust-touching work also needs the
   settled `duck-plan` record, including its actual challenge and any required independent input.
   Trust-touching work needs `duck-break` evidence appropriate to the changed surface. Instruction
   changes need agent behavior trials, not invented service crash tests. A shared work record with
   explicit proof/plan/break sections is equivalent to separate named receipts when all consumers
   can resolve it. Existing `proof-rN.md` and `break-rN.md` conventions remain valid.
5. Spot-check cited commands or artifacts; file presence alone is not evidence. A repair invalidates
   relevant earlier checks. For re-review, inspect the new delta and affected paths, reopen impacted
   findings, and reuse only evidence whose assumptions still hold. Never check only the old finding
   list. Missing material evidence means the gate cannot approve; a standalone opinion may still
   report what it can establish.
6. Do not dispatch beyond the caller's recorded bound; return the unresolved status and evidence
   without approval. For a third or later review round, require the caller's recorded loop
   diagnosis: why another round will add evidence, or which reframe/replan/race/rally/owner-decision
   exit it selected. Judge progress by unresolved causes, not wording or finding counts. A local
   record needs no commit unless the repository requires one. Do not dispatch an unchanged candidate
   just to seek a friendlier verdict.

Use [dispatch mechanics](references/dispatch.md) for identity, isolation, export authority and
transport checks. Pass review material by absolute path with source access; the brief carries
requirements and receipts as claims to attack, never as a coverage map. Reviewers should seek a
credible counterexample and a simpler valid path, substantiate their findings, and accept a claim
that survives. Neither owner preference nor a mandate to be negative is evidence.

## Reviewer result contract

Require each reviewer to return `APPROVE | REJECT | NOTE` and findings ranked
`BLOCKER | SHOULD | NOTE`:

- `APPROVE` claims no release-blocking defect was found.
- `REJECT` claims at least one finding is release-blocking.
- `NOTE` says something material stands out without making a gate decision. It neither authorizes
  nor rejects, is not `APPROVE-W-CONDITIONS`, and is not an outage.

These are inputs to the superreview, not votes. A reviewer that does not rank its findings has not
finished; use whatever evidence is present, but record the malformed result.

## Adjudicate the claims

Treat every verdict and finding as a claim, not a fact. For each finding, inspect the current target
and classify it as a substantiated `BLOCKER`, retained `SHOULD`, retained `NOTE`, or dismissed with
a recorded reason.

**When the actor adjudicating is the actor that built the candidate, adjudication is the weak
point** — the reviewers are decorrelated but the synthesis is not, and dismissing a true finding
looks identical to dismissing a false one. Say so in the report, dismiss only on evidence a third
party can re-check from the artifacts, and let a finding you cannot settle stand rather than fall.
A substantiated blocker stands until resolved. An unsubstantiated suspicion is not a blocker;
if missing evidence prevents a gate decision, return NOTE and name the uncertainty.

- Check the repository's own conventions before accepting a demand for a new artifact. Existing
  evidence beats reviewer-invented ceremony.
- Ask what the code is for before recommending a patch. If removing the feature, flag, branch, or
  check ends the defect without losing a required outcome, recommend deletion.
- On deletion-heavy diffs, inspect the diff prefix and post-change file before accepting a claim
  that a fact disappeared; context lines and moved facts create false blockers.
- Resolve disagreement about framework behavior by reading the dependency source, not by vote.
- Disagreement about what *should* be — a design intent, a public boundary, a policy — has no
  source to read: route it to the owner via `duck-decide` instead of settling it as the doer.
- If supplied history shows the same rule drawing repeated findings, apply the growth ratchet: ask
  whether that rule should exist rather than proposing another patch. When two consecutive rounds'
  substantiated blockers target code introduced by remediation rather than the original candidate,
  **or fall in one ledger class whatever code they land on**, say so in the report — naming the
  class, not only the instance — and recommend the caller's circuit breaker — rebuild the
  contested unit under `duck-race`'s race mode, or lock the class in under its rally mode —
  instead of implicitly inviting the next round.
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
criteria reviewed. Keep raw CLI stdout in scratch; preserve the decisive evidence before scratch
cleanup.

**Write that report where the landing gate can read it** — the same durable records home as the
receipts, never only into the caller's context or `$SP`, and never as a commit on the candidate
branch. A verdict that exists only in a session transcript cannot be checked later, and
`duck-land` needs the authorization itself, not a recollection that one was granted.

Then stop. Acting on the result, executing a fix or deletion, resolving an owner decision,
reviewing a materially changed candidate, and landing belong to the calling agent or workflow.

## Goal and product fit

Challenge whether the requested mechanism delivers the stated benefit. When the user asks to
challenge the goal itself, assess its evidence and alternatives too. Ground objections in the real
product constraints; do not invent deployment states or substitute another goal. Present genuine
value, cost or schedule tradeoffs to the owner. Sunk implementation effort does not justify keeping
a mechanism that fails its outcome.
