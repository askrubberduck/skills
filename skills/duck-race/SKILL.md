---
name: duck-race
description: Put two different model families on the same problem and let executed evidence pick the result. Use when the user says "race it", "duck race", or "ping-pong", wants two models tackling one problem, a task has several plausible implementations worth comparing, generated tests keep passing without catching real defects, single-attempt builds of similar work kept failing review, or a review-fix loop keeps faulting the fixes instead of the original change.
---

# Duck Race

Two model families work the same problem; executed evidence decides what survives, never prose
taste or a vote.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

**Race** answers *which implementation*: both attempt independently, in parallel, and the diffs
are compared. **Rally** answers *which edge cases*: the families alternate, one writing a failing
test and the other satisfying it.

`$SP` is the scratch directory [dispatch mechanics](../duck-review/references/dispatch.md) defines.

## Freeze (both modes)

1. Write the problem to `$SP/problem.md`: task, acceptance criteria, exact base commit SHA. Record
   its hash. Every participant receives these identical bytes; a clarification that reaches one
   and not the other voids the run. Resolve mid-run ambiguity in writing there.
2. Name the participants and families before starting. The doer (this session's family) is one;
   the rival is a **proven different family** from `[models].race` in
   `~/.askrubberduck/config.toml` or the owner's setup, and `$LEDGER pick race` chooses
   `$RIVAL_MODEL` within it (`$LEDGER` means
   `python3 "<absolute path of ../duck-review/scripts/ledger.py>"`, resolved from this skill's
   directory and typed out in every command; `$DISPATCH` is the absolute
   path of `dispatch.py` beside it, run as `python3 "$DISPATCH"`). Prove the rival's family and pin
   by dispatch mechanics' identity checks (roster line and pinned id recorded) before spending a
   round; executable names are not identities, and unknown identity is not a different family.
   `$DISPATCH` refuses agy for `--workdir`, so list only codex-transport pins in `[models].race`; a
   pick that returns another is a missing participant.
3. Confirm the owner has authorized sending this repository to the rival's vendor, as dispatch
   mechanics requires. An outage (dispatch mechanics' definition) is not a forfeit: unless dispatch
   mechanics rules out a retry, reset the rival's worktree and index (`git -C "$WT_RIVAL" reset
   --hard "$BASE_SHA" && git -C "$WT_RIVAL" clean -fd` in a race; the same on `"$WT"` to its last
   commit in a rally) and re-dispatch once in the same `--round` with `--id
   "$GATE-r$N-race-retry"` (`"$GATE-r$N-rally-retry"` in a rally). The brief travels as
   `--prompt`; **a diff or corpus it refers to is named by absolute path, the files to change by
   path relative to the participant's worktree; nothing is pasted in.** `problem.md` and every
   `turn.md` end with `End your answer with the line: VERDICT: DIFF`; an answer without it is
   recorded as an outage.

## Race mode

One worktree per racer at the repo root, from the same base SHA, never shared. Launch the block
below as one backgrounded call with every name set inside it (each call is a fresh shell) and work
the doer's attempt meanwhile. `$GATE` names the run; `$N` counts from 1; `$TRUST` is 1 for
trust-touching work, else 0:

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_MODEL:?}" "${SP:?}" "${WT_RIVAL:?}" \
  "${BASE_SHA:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage race --setup race --trust "$TRUST" \
  --pin "$RIVAL_MODEL" \
  --prompt "$SP/problem.md" --out "$SP/rival-r$N.out" --workdir "$WT_RIVAL" \
  --diff-base "$BASE_SHA" --diff-out "$SP/rival-r$N.diff"
```

`rival-r$N.diff` is the rival's change only after the call returned 0; read the other exit codes in
dispatch mechanics. An outage takes the retry above; a refusal is not retried unchanged: fix the
cause its message names. **The doer finishes its own attempt before reading `rival-r$N.out` or
`rival-r$N.diff`**; peeking is the void condition. The rival's prose summary is not the change;
`rival-r$N.diff` is.

### Adjudicate

1. Run the same outcome checks against both candidates in their own worktrees, plus each
   candidate's relevant tests. Derive the shared oracle from the frozen requirements, independently
   of the implementations where possible; each passing its own tests proves nothing comparative.
   Record inputs, outputs and environment; tests read but not executed have no result.
2. Compare the diffs for divergent assumptions; record relevant divergences even when both pass.
   Different permitted outputs are not defects.
3. Pick the winner on the evidence. Retain it whole unless combining parts improves the required
   behavior or shape; if you combine, **rerun the common outcome checks and relevant suites on the
   assembled result**. Resolve divergences against permitted behavior, including ordering and
   tolerances, never by vote.
4. Two finished attempts minimum.

## Rally mode

One shared worktree; turns are sequential. The rival is stateless between turns: every dispatch
replays context (problem path, current diff path, relevant file paths) **by file**, never inlined.
`$SP/turn.md` states this turn's role, the problem path, and the current state.

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_MODEL:?}" "${SP:?}" "${WT:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage rally --setup rally --trust "$TRUST" \
  --pin "$RIVAL_MODEL" \
  --prompt "$SP/turn.md" --out "$SP/rival-t$N.out" --workdir "$WT"
```

`$N` is the turn number; read the turn's output only after the script exits.

A rally is one red-green pair; the serve alternates each rally.

1. **Serve (test):** write ONE failing test against the frozen outcome contract, not merely the
   existing implementation. Handoff requires proven red: the test run's output saved under `$SP`
   and named by path, failing for the intended reason, not an import error. A serve without a
   runnable red proof is rejected and re-served, and still counts against the turn cap. Same bar
   both directions.
2. **Return (implement):** write the minimum that turns the suite green. Handoff requires proven
   green (full suite output saved under `$SP`, named by path) and **no edits to any test in the
   same turn**; editing the served test is the void condition. A test the returner believes is
   wrong goes back to the server with the objection in writing. Commit each red serve and each
   green return in `$WT`, so a retry resets to a commit and keeps the served test.
3. Hash the suite's test files at handoff and again at green; unequal hashes are the returner's
   void condition caught after the fact. Red proof, green proof and objections go straight into
   the receipt below; nothing else reads a per-rally log.

A void (a peek, an edited test, a clarification one side did not receive) ends the run: what stands
is the last green before it, and a re-run starts a new turn count.

Stop when any holds: every acceptance criterion has a passing test; the turn ceiling
`[bounds].rally_turns`, which `dispatch.py` enforces, is reached, counting every
serve, return, rejected serve and objection as one turn; or both sides serve a no-new-test-ideas
pass back to back. Then run the full suite once more and record it; the last green is the
candidate's evidence.

**Rally at class level.** When the serves would be instances of one defect class, serve the table:
one test driving every position of the surface with the class's catalogue, on every
implementation; the return closes the class.

## Contract (both modes)

- An outage that survives one re-dispatch leaves one family playing: say so and stop calling the
  work different-family.
- Receipt to `race-rN.md` in the durable records home as [`duck-proof`](../duck-proof/SKILL.md)
  resolves it, never the scratchpad or a commit on the candidate branch: problem hash, base SHA,
  participant identities with pinned model ids, mode, the diffs themselves (the losing diff too,
  inside the receipt, not as a `$SP` path), test output per candidate **and for the merged or
  final candidate**, divergence findings or the rally's red and green proofs, and the decision
  with its evidence.
- Never commit raw CLI stdout; keep it in `$SP`.
- **Adjudication is synthesis, not approval.** The tested candidate enters the normal pipeline
  ([`duck-proof`](../duck-proof/SKILL.md), then [`duck-review`](../duck-review/SKILL.md)) like any
  other work.

## Common mistakes

- Racing a problem statement that names an implementation approach: two copies of one assumption.
- Implementing past the test because the next requirement is obvious: the extra code is untested,
  and the next serve was the place to demand it.
