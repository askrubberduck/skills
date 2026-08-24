---
name: duck-review
description: Run one independent cross-model superreview and deliver an evidence-backed APPROVE, REJECT, or NOTE; no participation trophies. Use when a PR or diff is ready to review, a security-, privacy-, or data-sensitive change reaches its release gate, the user says "gate it" or asks for a red-team or independent second opinion. It reviews and judges; it does not fix, repeat, or land.
---

# Decorrelated Superreview

The doer is never the final judge. Use a **different model family**, never a same-family second
pass. If no decorrelated family is available, fail closed. *Final* carries the weight: this gate
takes the doer's authority to approve, never the doer's duty to validate and question the candidate
first — an unscrutinized candidate wastes the round.

**One invocation, one judgment.** A superreview may consult several independent reviewers, but it
does not loop until they approve and it is not a vote. Inspect their claims, adjudicate the evidence,
and return one authoritative result. Never edit the candidate, produce its prerequisite artifacts,
repeat the review after fixes, or land it; the calling agent or workflow owns that execution.

## Prepare the review

`$SP` is this review's scratchpad: an absolute path under the host's sanctioned scratchpad root
(for example, `<scratchpad-root>/<topic>-review`), created before step 1. Keep every dispatch
artifact there. `rN` numbers review invocations, not an internal approval loop.

**Trust-touching** means security-, privacy-, or data-sensitive work, or a change to any gate's
semantics.

**Establish that the export is authorized before spending a round.** This gate works by sending the
candidate's contents to model vendors outside the machine it runs on; that is what decorrelation
buys and it is not a transport detail. Confirm the owner has authorized sending *this repository* to
the named external families, and record where that authorization lives, in the durable records home
beside the receipts. A host that refuses the dispatch on those grounds has asked the owner's
question, not thrown an error — measured: `Rejected("… can transmit private repository contents to
an untrusted third-party destination; the user authorized the roast workflow but did not
specifically authorize exporting this repository data")`. Route it to `duck-decide`, never to a
re-dispatch: an authorization question answered by retrying is the failure this precondition exists
to prevent. No authorization, no dispatch — which is this gate failing closed as designed, and the
exit is stated to the caller rather than left to be discovered.

1. Resolve the exact review target: `gh pr diff <N>`, packet draft, committed object, or an
   intentionally captured worktree diff. A release candidate spans the last released tag to the
   exact candidate commit, with both full SHAs stated in the prompt; a PR keeps its own base. Never
   guess a range from adjacent commits or review a different checkout.
2. Take acceptance criteria from the work item, PR, or user's request; never invent them at
   dispatch. Freeze them for this invocation.
3. Check, but do not produce, the candidate's evidence, in the project's durable records home —
   never the scratchpad, which the session that wrote it has usually already ended:
   - `proof-rN.md` from `duck-proof` for every review;
   - the committed `duck-plan` co-authorship line for packet-sized or trust-touching work;
   - `break-rN.md` from `duck-break` for trust-touching work.

   For a third or later round on the same work (N≥3 in `rN`), the dispatch also carries the
   caller's committed loop diagnosis (`loop-diagnosis: …`): which breaker exit was weighed —
   `duck-frame` re-frame, `duck-plan` replan, `duck-race` in either mode, `duck-decide` —
   and why another review round is the right spend. No diagnosis, no dispatch: the gate does
   not sell round N+1 to a caller that has not judged its own loop.

   **No receipt, no dispatch — and presence is not verification**: spot-check each receipt by
   re-running or inspecting at least one claim's cited command or artifact; a claim that does not
   check out is a finding against the receipt. Measured: three receipts in one build overclaimed
   and every one passed a presence check. A change to this gate's own semantics is reviewed under
   the PRE-change rules; the new rules bind the next candidate.
4. Record the doer's self-reported model family. Name two required reviewers from two different
   model families, with at least one proven different from the doer. Each runs the **strongest tier
   of its family the host lists and you can pin**: decorrelation buys independence; tier buys rigor.
   Record the pinned model id plus the listing command and output that ranked it. Executable names
   are not identities: one harness routinely hosts several families — `agy` serves Gemini, Claude,
   and GPT-OSS from the same binary — while nested `codex` remains OpenAI/GPT when the doer is
   OpenAI/GPT. Unknown identity never counts as decorrelated.

   **The harness's roster is the family of record.** A model asked what it is answers from its
   prompt, and that claim is unfalsifiable. Print the harness's roster, find the pinned id in it,
   and take the family the roster attributes to that id; if it matches the doer's, the reviewer is
   not decorrelated whatever the binary is called. Record that roster line beside the pinned id.
   A harness that prints no roster establishes no family — measured, `codex` warns "Defaulting to
   fallback metadata" and proceeds — and an absent roster is the unknown identity this step already
   refuses to count, never a passed check. Sending a deliberately invalid `--model` to see whether
   the harness rejects it is discipline this gate names and does not enforce; the soul says which
   controls are checked and which are not.

   Give each reviewer **its own scratchpad directory**. Reviewers that share one can read — and
   overwrite — each other's output before synthesis reads it, which buys correlation in the one
   place the gate is paying for independence.
5. Write one prompt to `$SP` containing the target, frozen criteria, and receipts as claims to
   attack, never as a coverage map. Require the result contract below. Missing receipt evidence is
   itself a finding. Reviewer default: refute, not bless.

## Run the reviewers

Run from a neutral scratch directory, never the target checkout. Close stdin, use absolute paths,
and run in the background because reviews can take 10–45 minutes. Minimum shapes:

```bash
codex exec -m <strongest-listed> --skip-git-repo-check "$(cat $SP/prompt.md)" </dev/null > $SP/codex-rN.out 2>&1
agy --model <verified-non-doer> --add-dir "$SP" --print-timeout 45m -p "..." </dev/null > $SP/agy-rN.out 2>&1
```

**The prompt is an argument; the material under review is a path inside it.** Hand the reviewer
your instructions on the command line, and have those instructions name the diff, corpus, or files
by absolute path for the reviewer to open — never paste that material into the command. Delivery is
not a performance detail, it is a verdict-integrity control. Measured: the same pinned model, same
target, same instructions, disagreed on 28 of 41 verdicts between a run with the corpus pasted into
the prompt and one where the prompt named it on disk — every flip toward the finding standing. The
pasted run quoted the corpus fluently and was wrong. Pasting also forces a no-tools constraint,
which is the prompt shape that provokes the permission-denied outage.

Sanity-check a new invocation form with `-p "Reply with exactly: OK"`. These traps yield plausible
reviews at exit 0:

- An unpinned invocation can silently use the wrong model family. Always pin `--model`, and prove
  the pin per step 4.
- The prompt must be an **argument**. `--print "<text>"` can drop it, and a prompt redirected on
  **stdin** is discarded entirely — the reviewer answers with a greeting at exit 0.
- Large inlined inputs time out, and short ones degrade the verdict. Pass them by path.

A zero-byte, greeting-only, timed-out, or crashed dispatch is an outage: a dispatch attempted that
produced no verdict. **A degraded dispatch is the harder case — full length, well formed, and
wrong.** Nothing in the exit status distinguishes it, so before trusting any result, read three of
its justifications and confirm each quote actually supports its verdict; one that cites the claim
under attack as proof of that claim is a malformed result, recorded as such and not counted.
**A REJECT is never an outage**, and a same-family pass never substitutes for a required reviewer.

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
A tie goes to the reviewer.

- Check the repository's own conventions before accepting a demand for a new artifact. Existing
  evidence beats reviewer-invented ceremony.
- Ask what the code is for before recommending a patch. If removing the feature, flag, branch, or
  check ends the defect without losing a required outcome, recommend deletion.
- On deletion-heavy diffs, inspect the diff prefix and post-change file before accepting a claim
  that a fact disappeared; context lines and moved facts create false blockers.
- Resolve disagreement about framework behavior by reading the dependency source, not by vote.
- Disagreement about what *should* be — a design intent, a public boundary, a policy — has no
  source to read: route it to the owner via `duck-decide` instead of settling it as the doer.
  Measured: three such disagreements in one build, each settled by the party the gate exists to
  check.
- If supplied history shows the same rule drawing repeated findings, apply the growth ratchet: ask
  whether that rule should exist rather than proposing another patch. When two consecutive rounds'
  substantiated blockers target code introduced by remediation rather than the original candidate,
  say so in the report and recommend the caller's circuit breaker — rebuild the contested unit
  under `duck-race`'s race mode, or lock findings in as failing tests under its rally mode —
  instead of implicitly inviting the next round.
- Count concepts, not lines: identify any new branch, exception, or second home for the same fact,
  any abstraction with a single implementation, and any unit that took on a second job.
- A comment that states something false about the code is a defect, ranked on what it misleads
  about. A demand for explanatory comments is not: where the code is unclear the fix is the code,
  and `duck-dry` sets what the surviving comments carry.
- Judge the change, not paperwork. A receipt or commit-message defect is a `NOTE` unless it makes
  the underlying artifact claim unverifiable.

## Synthesize one result

Return exactly one superreview result:

- `APPROVE` — a gate decision was requested, **both required reviewers returned a verdict**, and no
  substantiated `BLOCKER` remains. An outage on a required reviewer bars `APPROVE`: it produced no
  findings, which is not the same as finding nothing. Re-dispatch it, or return `NOTE` and say which
  family is missing. Measured: a v1.0.0 release gate approved on a single family because the other
  outaged for the third time that gate and nothing barred the verdict.
- `REJECT` — at least one substantiated `BLOCKER` remains.
- `NOTE` — something material stands out, but no gate decision was requested or the available
  criteria and evidence do not support one. `NOTE` neither authorizes nor rejects the candidate.

Only a substantiated `BLOCKER` justifies `REJECT`; `SHOULD` and finding-level `NOTE` items do not.
Reviewer unanimity is neither required nor sufficient. A false `REJECT` may be dismissed with
evidence, and an `APPROVE` cannot erase a defect the superreview substantiates. A release workflow
may land only `APPROVE`; a superreview `NOTE` is a non-decision, not a hidden pass or failure.

Report the authoritative result, each reviewer's pinned model id and family, each raw verdict, every
finding's adjudicated classification and evidence, any outage or downgrade, and the exact target and
criteria reviewed. Never commit raw CLI stdout; keep it in `$SP`.

**Write that report where the landing gate can read it** — the same durable records home as the
receipts, never only into the caller's context or `$SP`, and never as a commit on the candidate
branch, which would advance the head past the SHA this report authorizes. A verdict that exists
only in a session transcript cannot be checked later, and `duck-land` needs the authorization
itself, not a recollection that one was granted.

Then stop. Persisting the result, executing a fix or deletion, resolving an owner decision,
reviewing a materially changed candidate, and landing belong to the calling agent or workflow.

## Optional lens: product fit

When the user requests product-fit review, use the same single invocation and judgment with this
lens: does the change fit the product's scope, what should be cut, and is the boundary where users
need it? Weigh functionality, extendability, and security; never weigh sunk implementation effort.
