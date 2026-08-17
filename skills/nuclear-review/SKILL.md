---
name: nuclear-review
description: Run one independent cross-model superreview and synthesize an evidence-backed APPROVE, REJECT, or NOTE. Use when a PR or diff is ready to review, a security-, privacy-, or data-sensitive change reaches its release gate, the user says "gate it" or asks for a red-team or independent second opinion. It reviews and judges; it does not fix, repeat, or land.
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

1. Resolve the exact review target: `gh pr diff <N>`, packet draft, committed object, or an
   intentionally captured worktree diff. A release candidate spans the last released tag to the
   exact candidate commit, with both full SHAs stated in the prompt; a PR keeps its own base. Never
   guess a range from adjacent commits or review a different checkout.
2. Take acceptance criteria from the work item, PR, or user's request; never invent them at
   dispatch. Freeze them for this invocation.
3. Check, but do not produce, the candidate's evidence:
   - `$SP/proof-rN.md` from `nuclear-proof` for every review;
   - the committed `nuclear-plan` co-authorship line for packet-sized or trust-touching work;
   - `$SP/break-rN.md` from `nuclear-break` for trust-touching work.

   **No receipt, no dispatch — and presence is not verification**: spot-check each receipt by
   re-running or inspecting at least one claim's cited command or artifact; a claim that does not
   check out is a finding against the receipt. Measured: three receipts in one build overclaimed
   and every one passed a presence check. A change to this gate's own semantics is reviewed under
   the PRE-change rules; the new rules bind the next candidate.
4. Record the doer's self-reported model family. Name two required reviewers from two different
   model families, with at least one proven different from the doer. Each runs the **strongest tier
   of its family the host lists and you can pin**: decorrelation buys independence; tier buys rigor.
   Record the pinned model id plus the listing command and output that ranked it. Executable names
   are not identities: `agy` can host Claude, Gemini, or another family, while nested `codex`
   remains OpenAI/GPT when the doer is OpenAI/GPT. Unknown identity never counts as decorrelated.
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

Sanity-check a new invocation form with `-p "What is 2+2?"`. These traps can yield plausible empty
reviews at exit 0:

- An unpinned `agy` invocation can silently use the wrong model family. Always pin `--model`.
- `--print "<text>"` can drop the prompt; use `-p`.
- Large inlined diffs can time out; pass them by absolute file path.

A zero-byte, greeting-only, timed-out, or crashed dispatch is an outage: a dispatch attempted that
produced no verdict. Record its evidence. **A REJECT is never an outage**, and a same-family pass
never substitutes for a required reviewer.

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
  source to read: route it to the owner via `nuclear-decide` instead of settling it as the doer.
  Measured: three such disagreements in one build, each settled by the party the gate exists to
  check.
- If supplied history shows the same rule drawing repeated findings, apply the growth ratchet: ask
  whether that rule should exist rather than proposing another patch.
- Count concepts, not lines: identify any new branch, exception, or second home for the same fact,
  any abstraction with a single implementation, and any unit that took on a second job.
- A comment that states something false about the code is a defect, ranked on what it misleads
  about. A demand for explanatory comments is not: where the code is unclear the fix is the code,
  and `nuclear-dry` sets what the surviving comments carry.
- Judge the change, not paperwork. A receipt or commit-message defect is a `NOTE` unless it makes
  the underlying artifact claim unverifiable.

## Synthesize one result

Return exactly one superreview result:

- `APPROVE` — a gate decision was requested and no substantiated `BLOCKER` remains.
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

**Write that report where the landing gate can read it** — beside the work, in the repo's own
convention for review records, never only into the caller's context or `$SP`. A verdict that exists
only in a session transcript cannot be checked later, and `nuclear-land` needs the authorization
itself, not a recollection that one was granted.

Then stop. Persisting the result, executing a fix or deletion, resolving an owner decision,
reviewing a materially changed candidate, and landing belong to the calling agent or workflow.

## Optional lens: product fit

When the user requests product-fit review, use the same single invocation and judgment with this
lens: does the change fit the product's scope, what should be cut, and is the boundary where users
need it? Weigh functionality, extendability, and security; never weigh sunk implementation effort.
