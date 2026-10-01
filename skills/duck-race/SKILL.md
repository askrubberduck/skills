---
name: duck-race
description: Put two different model families on the same problem and let executed evidence pick the result. Use when the user says "race it", "duck race", or "ping-pong", wants two models tackling one problem, a task has several plausible implementations worth comparing, generated tests keep passing without catching real defects, single-attempt builds of similar work kept failing review, or a review-fix loop keeps faulting the fixes instead of the original change.
---

# Duck Race

Different-family generation. Two model families work the same problem, and executed evidence decides
what survives — never prose taste, never a vote. Same-family work lets one set of blind spots
write both sides of the proof.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

Two modes. **Race** when the question is *which implementation*: both attempt independently, in
parallel, and the diffs are compared. **Rally** when the question is *which edge cases*: the
families alternate, one writing a failing test and the other satisfying it. Race exposes divergent
assumptions; rally turns them into tests. Pick by which of those the work needs.

`$SP` is the scratch directory [dispatch mechanics](../duck-review/references/dispatch.md) defines.

## Freeze (both modes)

1. Write the problem to `$SP/problem.md`: task, acceptance criteria, and the exact base commit SHA.
   Record its hash. Every participant receives these identical bytes — a clarification that reaches
   one and not the other voids the run. Ambiguity discovered mid-run is resolved in writing there,
   visible to both.
2. Name the participants and their model families before starting. The doer (this session's family)
   is one; the rival is a **proven different family** from `[models].race` in
   `~/.askrubberduck/config.toml` or the owner's setup, and `$LEDGER pick race` chooses
   `$RIVAL_PIN` within it (`$LEDGER` is `python3` with the absolute path of
   `../duck-review/scripts/ledger.py`, resolved from this skill's directory, typed out as
   `python3 "<path>" <subcommand>` rather than held in one variable; `$DISPATCH`, which
   bounds the rival's seat and records its row, is the absolute path of `dispatch.py` beside it,
   run as `python3 "$DISPATCH"`). Prove the rival's
   family and pin by dispatch mechanics' identity checks — roster line and pinned id recorded —
   before spending a round. Executable names are not identities, and a harness may host several
   families; unknown identity never counts as a different family. `$DISPATCH` refuses agy for
   `--workdir`, so list only codex-transport pins in `[models].race`; a pick that returns another is
   a missing participant, not a different family to try.
3. Confirm the owner has authorized sending this repository to the rival's vendor, as [dispatch
   mechanics](../duck-review/references/dispatch.md) requires. What dispatch mechanics calls an
   outage is an outage here, not a forfeit: unless dispatch mechanics rules out a retry, reset the
   rival's worktree and index — `git -C "$WT_RIVAL" reset --hard "$BASE_SHA" && git -C "$WT_RIVAL"
   clean -fd` in a race, the same on `"$WT"` to its last commit in a rally — and re-dispatch once
   in the same `--round` with `--id "$GATE-r$N-race-retry"` (`"$GATE-r$N-rally-retry"` in a
   rally). The brief travels as `--prompt`; **a diff or a corpus it refers to is named
   by absolute path, and the files to change by path relative to the participant's worktree;
   nothing is pasted in**, per dispatch mechanics. `problem.md` and every `turn.md` end with
   `End your answer with the line: DIFF`; the script records an answer without it as an outage.

## Race mode

One worktree per racer from the same base SHA, at the repo root. Racers never share a checkout.
Launch the block below as one backgrounded call, with every name set inside it — each call is a
fresh shell — and work the doer's attempt in its own worktree meanwhile. `$GATE` names the run;
`$N` counts from 1; `$TRUST` is 1 for trust-touching work, else 0:

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_PIN:?}" "${SP:?}" "${WT_RIVAL:?}" \
  "${BASE_SHA:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage race --setup race --trust "$TRUST" \
  --pin "$RIVAL_PIN" \
  --prompt "$SP/problem.md" --out "$SP/rival-r$N.out" --workdir "$WT_RIVAL" \
  --diff-base "$BASE_SHA" --diff-out "$SP/rival-r$N.diff"
```

The script stages the rival's worktree and writes its diff against the recorded base; an outage
captures nothing. `rival-r$N.diff` is the rival's change only after the call returned 0; read the
other exit codes in dispatch mechanics. An outage takes the retry above; a refusal is not retried
unchanged — fix the cause its message names.

- **The doer finishes its own attempt before reading `rival-r$N.out` or `rival-r$N.diff`.** Peeking
  mid-attempt is the void condition. Dispatch-then-work makes the honest order also the fast one.
- Never trust the rival's prose summary of what it changed; `rival-r$N.diff` is the change.

### Adjudicate

1. Run the same outcome checks against both candidates in their own worktrees, as well as each
   candidate's relevant tests. Derive the shared oracle from the frozen requirements, independently
   of the implementations where possible. Each passing its own tests alone does not establish
   comparative correctness. Record inputs, outputs and relevant environment; tests merely read
   but not executed have no result.
2. Compare the diffs for divergent assumptions — where the attempts disagree is where the problem
   statement may be ambiguous; record relevant divergences even when both candidates pass.
   Different permitted outputs are not defects.
3. Pick the winner on the evidence. Retain it whole unless combining parts actually improves the
   required behavior or shape. If you combine candidates, **rerun the common outcome checks and
   relevant suites on the assembled result**; per-candidate green does not compose. Resolve
   divergences against permitted behavior, including ordering and tolerances, never by vote.
4. Two finished attempts minimum.

## Rally mode

One shared worktree: turns are sequential, so race-style isolation buys nothing. The rival is
stateless between turns — every dispatch replays context (problem path, current diff path, relevant
file paths) **by file**, never inlined. `$SP/turn.md` states the role for this turn, the problem
path, and the current state.

```bash
: "${DISPATCH:?}" "${GATE:?}" "${N:?}" "${TRUST:?}" "${RIVAL_PIN:?}" "${SP:?}" "${WT:?}"
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage rally --setup rally --trust "$TRUST" \
  --pin "$RIVAL_PIN" \
  --prompt "$SP/turn.md" --out "$SP/rival-t$N.out" --workdir "$WT"
```

`$N` is the turn number; read the turn's output only after the script exits.

A rally is one red-green pair, and the serve alternates each rally.

1. **Serve (test):** the serving side writes ONE failing test against the frozen outcome contract,
   not merely the existing implementation. Handoff requires proven red — the test run's output saved
   under `$SP` and named by path, failing for the intended reason, not an import error. A test
   without a runnable red proof is rejected and re-served, and the rejected serve still counts
   against the turn cap. Same bar both directions.
2. **Return (implement):** the other side writes the minimum that turns the suite green. Handoff
   requires proven green — full suite output saved under `$SP` and named by path — and **no edits to
   any test in the same turn**. Editing the test you were served is the void condition; a test the
   returner believes is wrong goes back to the server with the objection in writing instead.
   Commit each red serve and each green return in `$WT`, so a retry resets to a commit and keeps
   the served test.
3. Hash the suite's test files at handoff and again at green — unequal hashes are the returner's
   void condition caught after the fact. Red proof, green proof and objections go straight into
   the receipt below; nothing else reads a per-rally log.

A void — a peek, an edited test, a clarification one side did not receive — ends the run: what
stands is the last green before it, and a re-run starts a new turn count.

Stop when any holds: every acceptance criterion has a passing test; the turn ceiling is reached —
`[bounds].rally_turns` in `~/.askrubberduck/config.toml` (default 10), counted in turns, where
every serve, return, rejected serve and objection is one turn; or both sides serve a
no-new-test-ideas pass back to back. Then run the full suite once more and record it — the last
green is the candidate's evidence.

**Rally at class level.** When the serves would be instances of one defect class, the serve is the
table: one test that drives every position of the surface with the class's catalogue, on every
implementation, and the return closes the class. Serve the whole class at once; one instance per
serve exhausts the turn cap before the class closes.

## Contract (both modes)

- An outage that survives one re-dispatch leaves one family playing: say so and stop calling the
  work different-family.
- Receipt to `race-rN.md` in the project's durable records home as `duck-proof` resolves it — never
  the scratchpad, never a commit on the candidate branch: problem hash, base SHA, participant
  identities with pinned model ids — a receipt without identities cannot prove the run was
  cross-family at all — the mode, the diffs themselves, test output per candidate **and for the
  merged or final candidate**, divergence findings or the rally's red and green proofs, and the
  decision with its evidence. A losing diff is evidence, not trash: it documents the road not taken
  and why, so it travels inside the receipt rather than as a `$SP` path that resolves to nothing by
  the time anyone follows it.
- One test per serve in rally mode. Batching tests hides which failure drove which code; the rally
  structure is the audit trail.
- Never commit raw CLI stdout; keep it in `$SP` — it is megabytes of tool chatter around a
  verdict the receipt already quotes.
- **Adjudication is synthesis, not approval.** The output is a tested candidate, not an approved
  one: it enters the normal pipeline (`duck-proof`, then `duck-review`) like any other work. This
  skill replaces nothing downstream.

## Common mistakes

- Racing a problem statement that names an implementation approach — you get two copies of the same
  assumption and pay double for one attempt.
- Implementing past the test because the next requirement is obvious — the extra code is untested by
  construction, and the next serve was the place to demand it.
