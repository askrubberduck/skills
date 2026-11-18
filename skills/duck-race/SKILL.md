---
name: duck-race
description: Put two different model families on the same problem and let executed evidence pick the result. Use when the user says "race it", "duck race", or "ping-pong", wants two models tackling one problem, a task has several plausible implementations worth comparing, generated tests keep passing without catching real defects, single-attempt builds of similar work kept failing review, or a review-fix loop keeps faulting the fixes instead of the original change.
---

# Duck Race

Two model families work the same problem. Executed evidence decides what survives, never prose
taste or a vote.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

**Race** answers *which implementation*: both families attempt it independently, in parallel;
the doer compares the diffs. **Rally** answers *which edge cases*: the families alternate. One
writes a failing test, and the other satisfies it.

`$SP` is the scratch directory that [dispatch mechanics](../duck-review/references/dispatch.md)
defines.

## Freeze (both modes)

1. Write the problem to `$SP/problem.md`: task, acceptance criteria and exact base commit SHA.
   Record its hash. Every participant receives the same bytes. A clarification that
   reaches only one participant voids the run. Resolve mid-run ambiguity in writing in that file.
2. Name the participants and families first. The doer (this session's family) is one. The
   rival must be a **proven different family** from `[models].race` in
   `~/.askrubberduck/config.toml` or the owner's setup. `$RIVAL_MODEL` is the first pin in that
   list outside the doer's family. `$DISPATCH` is the absolute path of
   `../duck-review/scripts/dispatch.py`, resolved from this skill's directory and typed out in every
   command, run as `python3 "$DISPATCH"`. Before you spend a round, prove the rival's family and
   pin with dispatch mechanics' identity checks. Record the roster line and pinned id.
   Executable names are not identities, and an unknown identity is not a different family.
   `$DISPATCH` refuses agy and Claude pins for `--workdir`, so list only codex-transport pins in
   `[models].race`.
   A list with no such pin is a missing participant.
3. As dispatch mechanics requires, confirm that the owner authorized the transfer of this
   repository to the rival's vendor. An outage (dispatch mechanics defines it) is not a forfeit.
   Unless dispatch mechanics rules out a retry:
   1. Reset the rival's worktree and index. In a race, run
      `git -C "$WT_RIVAL" reset --hard "$BASE_SHA" && git -C "$WT_RIVAL" clean -fd`. In a rally,
      run the same on `"$WT"` to its last commit.
   2. Re-dispatch once in the same `--round` with `--id "$GATE-r$N-race-retry"`
      (`"$GATE-r$N-rally-retry"` in a rally).

   The brief travels as `--prompt`. **A diff or corpus that the brief refers to is named
   by absolute path. The files to change are named by path relative to the participant's
   worktree. Nothing is pasted in.** `problem.md` and every `turn.md` end with
   `End your answer with the line: VERDICT: DIFF`. An answer without that line is an outage.

## Race mode

Give each racer its own worktree at the repo root, from the same base SHA.
Launch the block below as one background call with every name set inside it, because each call is
a fresh shell. Work on the doer's attempt meanwhile. `$GATE` names the run.
`$N` counts from 1. `$TRUST` is 1 for trust-touching work, else 0:

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_MODEL:?}" "${SP:?}" "${WT_RIVAL:?}" \
  "${BASE_SHA:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage race --setup race --trust "$TRUST" \
  --pin "$RIVAL_MODEL" \
  --prompt "$SP/problem.md" --out "$SP/rival-r$N.out" --workdir "$WT_RIVAL" \
  --diff-base "$BASE_SHA" --diff-out "$SP/rival-r$N.diff"
```

`rival-r$N.diff` is the rival's change only after the call returned 0. Dispatch mechanics gives
the other exit codes. An outage takes the retry above. Do not retry a refusal unchanged: fix the
cause that its message names. **The doer finishes its own attempt before it reads
`rival-r$N.out` or `rival-r$N.diff`**; a peek is the void condition. The rival's prose summary is
not the change; `rival-r$N.diff` is.

### Adjudicate

1. In each candidate's own worktree, run the shared outcome checks and that candidate's relevant
   tests. Where possible, derive the shared oracle from the frozen requirements,
   independent of the implementations. A pass on its own tests proves nothing comparative. Record
   inputs, outputs and environment. An unexecuted test has no result.
2. Compare the diffs, and record relevant divergent assumptions even when both pass. Different
   permitted outputs are not defects.
3. Pick the winner on the evidence. Keep it whole unless combined parts improve the required
   behavior or shape. If you combine, **rerun the common outcome checks and relevant suites on the
   assembled result**. Resolve divergences against permitted behavior, including order and
   tolerances, never by vote.
4. The race needs at least two finished attempts.

## Rally mode

Use one shared worktree and sequential turns. The rival keeps no state between turns: every
dispatch replays the context (problem path, current diff path, relevant file paths) **by file**.
`$SP/turn.md` states this turn's role, the problem path and the current state.

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_MODEL:?}" "${SP:?}" "${WT:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage rally --setup rally --trust "$TRUST" \
  --pin "$RIVAL_MODEL" \
  --prompt "$SP/turn.md" --out "$SP/rival-t$N.out" --workdir "$WT"
```

`$N` is the turn number. Read the turn's output only after the script exits.

A rally is one red-green pair. The serve alternates each rally.

1. **Serve (test):** Write ONE failing test against the frozen outcome contract, not only the
   existing implementation. The handoff requires proven red: the test run's output, saved under
   `$SP` and named by path. The test must fail for the intended reason, not an import error.
   Reject and re-serve a serve without a runnable red proof; it still counts against the turn cap.
   The same bar applies in both directions.
2. **Return (implement):** Write the minimum that turns the suite green. The handoff requires
   proven green: the full suite output, saved under `$SP` and named by path. **Do not edit any
   test in the same turn**; an edit to the served test is the void condition. A test that the
   returner believes wrong goes back to the server with a written objection. Commit each
   red serve and each green return in `$WT`, so that a retry resets to a commit and keeps the
   served test.
3. Hash the suite's test files at handoff and again at green. Unequal hashes are the returner's
   void condition, caught after the fact. Put red proof, green proof and objections into
   the receipt below; nothing else reads a per-rally log.

A void ends the run. The last green before it stands. A re-run starts a new turn count.

Stop when any of these holds:

- Every acceptance criterion has a passing test.
- The turn ceiling `[bounds].rally_turns`, which `dispatch.py` enforces, is reached. Every serve,
  return, rejected serve and objection counts as one turn.
- Both sides serve a no-new-test-ideas pass back to back.

Then run and record the full suite once more. The last green is the candidate's evidence.

**Rally at class level.** If the serves would be instances of one defect class, serve the table:
one test that drives every surface position with the class's catalogue, on every implementation.
The return closes the class.

## Contract (both modes)

- If an outage survives one re-dispatch, only one family remains. Say so; the work is no longer
  different-family.
- Write the receipt to `race-rN.md` in the durable records home that
  [`duck-proof`](../duck-proof/SKILL.md) resolves, never to the scratchpad or a commit on the
  candidate branch. The receipt holds the problem hash, base SHA, participant identities with
  pinned model ids, mode, and both diffs inside the receipt, not as a `$SP` path. It also holds
  test output per candidate **and for the merged or final candidate**, the divergence findings or
  the rally's red and green proofs, and the decision with its evidence.

- Never commit raw CLI stdout. Keep it in `$SP`.
- **Adjudication is synthesis, not approval.** The tested candidate enters the normal pipeline
  ([`duck-proof`](../duck-proof/SKILL.md), then [`duck-review`](../duck-review/SKILL.md)).

## Common mistakes

- A race on a problem statement that names an implementation approach: it compares two copies of one
  assumption.
- The returner implements past the served test because the next requirement is obvious. The extra
  code is untested; the next serve is the place to demand it.
