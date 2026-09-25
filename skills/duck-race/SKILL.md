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
   `~/.askrubberduck/config.toml` (default `[families].reviewers`) or the owner's setup, and
   `scripts/ledger.py pick race` chooses within it. Prove the rival's family and pin by dispatch
   mechanics' identity checks — roster line and pinned id recorded — before spending a round.
   Executable names are not identities, and a harness may host several families; unknown identity
   never counts as a different family. The blocks below show the `codex` transport; another CLI
   takes its shape from dispatch mechanics.
3. Confirm the owner has authorized sending this repository to the rival's vendor, as [dispatch
   mechanics](../duck-review/references/dispatch.md) requires — a rival dispatch ships the same
   material a review does. Sanity-check a new invocation form and classify a failed one by dispatch
   mechanics; what it calls an outage is an outage here, not a forfeit: record it, and re-dispatch
   unless dispatch mechanics rules out a retry. The problem statement travels as the command's
   argument, but **a diff or a corpus it refers to is named by absolute path, and the files to
   change by path relative to the participant's worktree; nothing is pasted in.** Pasted material
   degrades a dispatch into confident nonsense at exit 0.

## Race mode

One worktree per racer from the same base SHA, at the repo root. Racers never share a checkout.
Dispatch the rival into the background first, then work the doer's attempt inline; capture the
rival's diff only **after its dispatch has finished**:

```bash
set -um   # -u: an unbound name fails here, not as a 0-byte diff; -m: the rival gets its own process group
: "${RIVAL_MODEL:?pinned id, proven per dispatch.md}" "${WT_RIVAL:?rival worktree}" "${BASE_SHA:?from problem.md}"
DEADLINE=$((SECONDS + ${DISPATCH_SECONDS:?[bounds].dispatch_timeout in seconds}))   # past it the rival is an outage, not a forfeit
codex exec -C "$WT_RIVAL" -s workspace-write -m "$RIVAL_MODEL" "$(cat "$SP/problem.md")" </dev/null > "$SP/rival.out" 2>&1 &
RIVAL=$!
# run this block as one backgrounded shell call; the doer works its own attempt meanwhile, in its own worktree
while kill -0 -- "-$RIVAL" 2>/dev/null && [ "$SECONDS" -lt "$DEADLINE" ]; do sleep 30; done   # the group, not the leader
if kill -0 -- "-$RIVAL" 2>/dev/null; then kill -KILL -- "-$RIVAL"; wait "$RIVAL"; STATUS=deadline   # KILL: TERM can be ignored
else wait "$RIVAL"; STATUS=$?; fi
kill -KILL -- "-$RIVAL" 2>/dev/null; while kill -0 -- "-$RIVAL" 2>/dev/null; do sleep 1; done   # stragglers gone before capture
if [ "$STATUS" = 0 ]; then git -C "$WT_RIVAL" add -A && git -C "$WT_RIVAL" diff "$BASE_SHA" > "$SP/rival.diff"
else echo "rival outage: $STATUS" >> "$SP/rival.out"; fi   # an outage captures nothing: re-dispatch, never diff
```

- **Wait before you capture.** Backgrounding the dispatch and diffing immediately records an empty
  attempt at exit 0 — a forfeit that never happened.
- **The doer finishes its own attempt before reading `rival.out` or `rival.diff`.** Peeking
  mid-attempt is the void condition. Dispatch-then-work makes the honest order also the fast one.
- **Grant the rival write access** (`-s workspace-write`): the default sandbox is read-only, and a
  rival that cannot write returns an empty attempt at exit 0.
- **`add -A`, then diff against the recorded base SHA** — never bare `git diff`: a rival that
  commits leaves the bare form empty at exit 0, and a rival that creates new files leaves them
  invisible to any diff until they are added. Both read as a forfeit that never happened.
- Never trust the rival's prose summary of what it changed; capture the diff from the worktree.

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
codex exec -C "$WT" -s workspace-write -m "$RIVAL_MODEL" "$(cat "$SP/turn.md")" </dev/null > "$SP/rival-tN.out" 2>&1
```

Bound each turn with the race block's deadline, kill and wait before reading its output.

A rally is one red-green pair, and the serve alternates each rally.

1. **Serve (test):** the serving side writes ONE failing test against the frozen outcome contract,
   not merely the existing implementation. Handoff requires proven red — the test run's output saved
   under `$SP` and named by path, failing for the intended reason, not an import error. A test
   without a runnable red proof is rejected and re-served, and the rejected serve still counts
   against the turn cap; vague untestable tests are how a side dodges the game. Same bar both
   directions.
2. **Return (implement):** the other side writes the minimum that turns the suite green. Handoff
   requires proven green — full suite output saved under `$SP` and named by path — and **no edits to
   any test in the same turn**. Editing the test you were served is the void condition; a test the
   returner believes is wrong goes back to the server with the objection in writing instead.
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
implementation, and the return closes the class. One instance per serve is how a class outlives
the turn cap — and how a review loop outlives its budget.

## Contract (both modes)

- An outage that survives one re-dispatch leaves one family playing: say so and stop calling the
  work different-family. Each dispatch gets its row in `~/.askrubberduck/dispatches.tsv`:
  verdict `DIFF`, or `-` with `outage = 1`.
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
