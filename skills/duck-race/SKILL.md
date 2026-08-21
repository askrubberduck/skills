---
name: duck-race
description: Put two decorrelated model families on the same problem and let executed evidence pick the result. Use when the user says "race it", "duck race", or "ping-pong", wants two models tackling one problem, a task has several plausible implementations worth comparing, generated tests keep passing without catching real defects, single-attempt builds of similar work kept failing review, or a review-fix loop keeps faulting the fixes instead of the original change.
---

# Duck Race

Decorrelated generation. Two model families work the same problem, and executed evidence decides
what survives — never prose taste, never a vote. Same-family work lets one set of blind spots
write both sides of the proof.

Two modes. **Race** when the question is *which implementation*: both attempt independently, in
parallel, and the diffs are compared. **Rally** when the question is *which edge cases*: the
families alternate, one writing a failing test and the other satisfying it. Race exposes divergent
assumptions; rally turns them into tests. Pick by which of those the work needs.

`$SP` is this session's scratchpad: an absolute path under the host's sanctioned scratchpad root.

## Freeze (both modes)

1. Write the problem to `$SP/problem.md`: task, acceptance criteria, and the exact base commit SHA.
   Record its hash. Every participant receives these identical bytes — a clarification that reaches
   one and not the other voids the run. Ambiguity discovered mid-run is resolved in writing there,
   visible to both.
2. Name the participants and their model families before starting. The doer (this session's family)
   is one; the rival must be a **proven different family** — `codex exec` by default when the doer
   is not OpenAI/GPT; a doer of that family uses another proven family (`agy --model <pinned>`)
   instead. Executable names are not identities, and a harness may host several families: prove the
   pin took before spending a round, by sending a deliberately invalid `--model` and confirming the
   CLI errors with its roster. A harness that accepts garbage has a meaningless pin, and unknown
   identity never counts as decorrelated.
3. Sanity-check a new invocation form with a trivial prompt first. A zero-byte, greeting-only,
   timed-out, or crashed dispatch is an outage, not a forfeit: record it and re-dispatch. Pass the
   problem **by file path**, never inlined into the command — an inlined corpus is the shape that
   degrades a dispatch into confident nonsense at exit 0.

## Race mode

One worktree per racer from the same base SHA, at the repo root. Racers never share a checkout.
Dispatch the rival into the background first, then work the doer's attempt inline; capture the
rival's diff only **after its dispatch has finished**:

```bash
codex exec -C "$WT_RIVAL" -s workspace-write -m <pinned> "$(cat $SP/problem.md)" </dev/null > $SP/rival.out 2>&1 &
RIVAL=$!
# ... the doer works its own attempt here, in its own worktree ...
wait "$RIVAL"
git -C "$WT_RIVAL" add -A && git -C "$WT_RIVAL" diff "$BASE_SHA" > $SP/rival.diff
```

- **Wait before you capture.** Backgrounding the dispatch and diffing immediately records an empty
  attempt at exit 0 — a forfeit that never happened.
- **The doer finishes its own attempt before reading `rival.out` or `rival.diff`.** Peeking
  mid-attempt is the void condition. Dispatch-then-work makes the honest order also the fast one.
- **Grant the rival write access** (`-s workspace-write`): the default sandbox is read-only, and a
  rival that cannot write returns an empty attempt at exit 0. Measured live during this skill's own
  gate — the shipped command produced no writes until the flag was added.
- **`add -A`, then diff against the recorded base SHA** — never bare `git diff`: a rival that
  commits leaves the bare form empty at exit 0, and a rival that creates new files leaves them
  invisible to any diff until they are added. Both read as a forfeit that never happened.
- Never trust the rival's prose summary of what it changed; capture the diff from the worktree.

### Adjudicate

1. Run each candidate's tests in its own worktree and record both outputs. Executed evidence only:
   a candidate whose tests were read but not run has no result.
2. Compare the diffs for divergent assumptions — where the attempts disagree is where the problem
   statement was weakest; record each divergence as a finding even when both candidates pass.
3. Pick the winner on the evidence, then steal: fold the loser's better parts into the winning
   candidate. **Re-run the full suite on the merged result and record it** — per-candidate green
   does not compose, and the merged run is the only proof the stolen parts fit.
4. Two finished attempts minimum. An outage that survives one re-dispatch downgrades the run to a
   single attempt — say so and stop calling it a race.

## Rally mode

One shared worktree: turns are sequential, so race-style isolation buys nothing. The rival is
stateless between turns — every dispatch replays context (problem path, current diff path, relevant
file paths) **by file**, never inlined. `$SP/turn.md` states the role for this turn, the problem
path, and the current state.

```bash
codex exec -C "$WT" -s workspace-write -m <pinned> "$(cat $SP/turn.md)" </dev/null > $SP/rival-tN.out 2>&1
```

A rally is one red-green pair, and the serve alternates each rally.

1. **Serve (test):** the serving side writes ONE failing test against the problem. Handoff requires
   proven red — the test run's output pasted, failing for the intended reason, not an import error.
   A test without a runnable red proof is rejected and re-served; vague untestable tests are how a
   side dodges the game. Same bar both directions.
2. **Return (implement):** the other side writes the minimum that turns the suite green. Handoff
   requires proven green — full suite output pasted — and **no edits to any test in the same turn**.
   Editing the test you were served is the void condition; a test the returner believes is wrong
   goes back to the server with the objection in writing instead.
3. Log the rally in `$SP/rally-rN.md` before the next serve: who served, red proof, green proof,
   objections raised, and the served test file's hash at handoff and again at green — unequal
   hashes are the returner's void condition caught after the fact.

Stop when any holds: every acceptance criterion has a passing test; the turn cap set at start
(default 10 rallies) is reached; or both sides serve a no-new-test-ideas pass back to back. Then run
the full suite once more and record it — the last green is the candidate's evidence.

## Contract (both modes)

- Receipt to `$SP/race-rN.md`: problem hash, base SHA, participant identities with pinned model ids
  — a receipt without identities cannot prove the run was cross-family at all — the mode, the raw
  diffs or their `$SP` paths, test output per candidate **and for the merged or final candidate**,
  divergence findings or the rally log, and the decision with its evidence. A losing diff is
  evidence, not trash: it documents the road not taken and why.
- One test per serve in rally mode. Batching tests hides which failure drove which code; the rally
  structure is the audit trail.
- Never commit raw CLI stdout; keep it in `$SP`.
- **Adjudication is synthesis, not approval.** The output is a tested candidate, not an approved
  one: it enters the normal pipeline (`duck-proof`, then `duck-review`) like any other work. This
  skill replaces nothing downstream, and the doer-never-final-judge rule is untouched.

## Common mistakes

- Reading the rival's diff "just to check progress" — that is the void condition, not diligence.
- Racing a problem statement that names an implementation approach — you get two copies of the same
  assumption and pay double for one attempt.
- Adjudicating on diff elegance instead of executed tests — prose taste is how correlated errors
  win races.
- Skipping the divergence findings because both candidates pass — passing twice for different
  reasons is the cheapest spec-review available.
- Accepting a red that fails on a typo or missing import — red for the wrong reason proves nothing;
  the serve is re-run, not patched by the returner.
- The returner "fixing" the test — void condition, even when the test is genuinely wrong. Objection
  in writing, back to the server.
- Implementing past the test because the next requirement is obvious — the extra code is untested by
  construction, and the next serve was the place to demand it.
- Playing both sides from one family because the rival CLI is slow or down — that is solo work
  wearing a costume; say so and stop claiming decorrelation.
