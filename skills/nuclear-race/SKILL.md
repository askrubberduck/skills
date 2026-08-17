---
name: nuclear-race
description: Race two decorrelated model families independently against the same frozen problem, then adjudicate on executed evidence. Use when the user says "race it" or "nuclear race", wants two models tackling the same problem at once, a task has several plausible implementations worth comparing, or single-attempt builds of similar work kept failing review.
---

# Nuclear Race

Decorrelated generation. Two model families attempt the same problem independently; neither sees
the other's work until both attempts land. The value is the divergence: two honest attempts expose
assumptions a single attempt ships silently. Cross-talk before the finish line correlates the
attempts and destroys exactly what the race exists to buy.

`$SP` is this race's scratchpad: an absolute path under the host's sanctioned scratchpad root.

## Freeze

1. Write the problem statement once to `$SP/problem.md`: task, acceptance criteria, and the exact
   base commit SHA. Record its hash. Every racer receives these identical bytes — a clarification
   that reaches one racer and not the other voids the race.
2. Create one worktree per racer from the same base SHA. Racers never share a checkout.
3. Name the racers and their model families before starting. The doer (this session's family) is
   one racer; the rival must be a **proven different family**, `codex exec` by default, a third via
   `agy --model <pinned>` optional. Executable names are not identities — unknown identity never
   counts as decorrelated.

## Run the race

Dispatch the rival first, in the background, working in its own worktree; then run the doer's
attempt inline in the doer's worktree:

```bash
codex exec -C "$WT_RIVAL" -m <strongest-listed> "$(cat $SP/problem.md)" </dev/null > $SP/rival.out 2>&1
git -C "$WT_RIVAL" diff > $SP/rival.diff
```

- Sanity-check a new invocation form with a trivial prompt first. A zero-byte, greeting-only,
  timed-out, or crashed dispatch is an outage, not a forfeit: record it and re-dispatch; a race
  with one runner is not a race.
- **The doer finishes its own attempt before reading `rival.out` or `rival.diff`.** Peeking
  mid-attempt is the void condition. Dispatch-then-work makes the honest order also the fast one.
- Pass the problem by file, pin the model, capture the diff from the worktree — never trust the
  rival's prose summary of what it changed.

## Adjudicate

1. Run each candidate's tests in its own worktree and record both outputs. Executed evidence only:
   a candidate whose tests were read but not run has no result.
2. Compare the diffs for divergent assumptions — where the attempts disagree is where the problem
   statement was weakest; record each divergence as a finding even when both candidates pass.
3. Pick the winner on the evidence, then steal: fold the loser's better parts into the winning
   candidate where tests prove they fit. The merged candidate is the race's output.
4. Adjudication is synthesis, not approval. The merged candidate enters the normal pipeline
   (`nuclear-proof`, then `nuclear-review`) like any other work — the race replaces nothing
   downstream, and the doer-never-final-judge rule is untouched.

## Contract

- Receipt to `$SP/race-rN.md`: problem hash, base SHA, racer identities with pinned models, both
  raw diffs (or their `$SP` paths), test output per candidate, divergence findings, and the merge
  decision with its evidence. A losing diff is evidence, not trash — it documents the road not
  taken and why.
- Never commit raw CLI stdout; keep it in `$SP`.
- Two finished attempts minimum. An outage that survives one re-dispatch downgrades the run to a
  single attempt — say so and stop calling it a race.

## Common mistakes

- Reading the rival's diff "just to check progress" — that is the void condition, not diligence.
- Racing a problem statement that names an implementation approach — you get two copies of the
  same assumption and pay double for one attempt.
- Adjudicating on diff elegance instead of executed tests — prose taste is how correlated errors
  win races.
- Skipping the divergence findings because both candidates pass — passing twice for different
  reasons is the cheapest spec-review the collection offers.
