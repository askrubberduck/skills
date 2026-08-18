---
name: nuclear-pingpong
description: Alternate test-writing and implementation between two decorrelated model families, one failing test per rally. Use when the user says "ping-pong" or "nuclear pingpong", wants TDD across two models, a spec is clear but its edge cases are not, or generated tests keep passing without catching real defects.
---

# Nuclear Pingpong

TDD across model families. One paddle writes a failing test; the other implements the minimum that
turns it green; roles swap each rally. The decorrelation is the point: a test written by one family
and satisfied by another is evidence neither could have manufactured alone — same-family TDD lets
one set of blind spots write both sides of the proof.

`$SP` is this session's scratchpad: an absolute path under the host's sanctioned scratchpad root.

## Setup

1. Freeze the spec to `$SP/spec.md`: task, acceptance criteria, base commit SHA. Both paddles play
   from these bytes; discovered ambiguity is resolved in writing there, visible to both.
2. One shared worktree — turns are sequential, so race-style isolation buys nothing.
3. Paddles: the doer (this session's family) and a **proven different family** — `codex exec` by
   default when the doer is not OpenAI/GPT; a doer of that family plays a different proven family
   instead — model pinned. The rival is stateless between turns: every dispatch replays context —
   spec path, current diff path, relevant file paths — by file, never inlined.

## The rally

A rally is one red-green pair. Serve alternates each rally.

1. **Serve (test):** the serving paddle writes ONE failing test against the spec. Handoff requires
   proven red — the test run's output pasted, failing for the intended reason, not an import error.
   A test without a runnable red proof is rejected and re-served; vague untestable tests are how a
   paddle dodges the game. Same bar both directions.
2. **Return (implement):** the other paddle writes the minimum that turns the suite green. Handoff
   requires proven green — full suite output pasted — and **no edits to any test in the same
   turn**. Editing the test you were served is the void condition; a test the returner believes is
   wrong goes back to the server with the objection in writing instead.
3. Log the rally in `$SP/pingpong-rN.md` before the next serve: who served, red proof, green proof,
   objections raised.

Rival dispatch per turn:

```bash
codex exec -C "$WT" -s workspace-write -m <pinned> "$(cat $SP/turn.md)" </dev/null > $SP/rival-tN.out 2>&1
```

`turn.md` states the role for this turn (serve or return), the spec path, and the current state.
The write sandbox is load-bearing: the default is read-only, and a paddle that cannot write
returns an empty turn at exit 0. Sanity-check a new invocation form first; a zero-byte or crashed
dispatch is an outage — record it and re-dispatch, never play both sides of a rally to keep the
game moving.

## Stop

Stop when any holds: the spec's criteria all have passing tests; the turn cap set at start
(default 10 rallies) is reached; or both paddles serve a no-new-test-ideas pass back to back. Then
run the full suite once more and record it — the last green is the candidate's evidence.

The output is a tested candidate, not an approved one: it enters the normal pipeline
(`nuclear-proof`, then `nuclear-review`) like any other work. Pingpong replaces nothing downstream.

## Contract

- Rally log `$SP/pingpong-rN.md` is the receipt. Header: both paddles' pinned model ids — a log
  without identities cannot prove the game was cross-family at all. Per rally — server, red
  proof, green proof, objections, and the served test file's hash at handoff and again at green:
  unequal hashes are the returner's void condition caught after the fact. Plus the final
  full-suite run. A rally without both proofs did not happen.
- One test per serve. Batching tests hides which failure drove which code — the rally structure is
  the audit trail.
- Never commit raw CLI stdout; keep it in `$SP`.

## Common mistakes

- Accepting a red that fails on a typo or missing import — red for the wrong reason proves nothing;
  the serve is re-run, not patched by the returner.
- The returner "fixing" the test — void condition, even when the test is genuinely wrong. Objection
  in writing, back to the server.
- Playing both paddles from one family because the rival CLI is slow or down — that is solo TDD
  wearing a costume; say so and stop claiming decorrelation.
- Implementing past the test because the next requirement is obvious — the extra code is untested
  by construction, and the next serve was the place to demand it.
