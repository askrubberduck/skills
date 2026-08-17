---
name: nuclear-plan
description: Catch architectural and implementation risks before coding begins. Use when about to plan OR about to implement large, architectural, security-, privacy-, or data-sensitive work — including when implementation is about to start and no plan exists yet — when a draft plan needs independent critique, or when similar work previously failed several review rounds.
---

# Plan Co-Authoring with the Red Team

Decorrelated rigor arrives either as *co-authorship* now or as *rejections* later. Do NOT draft a
plan same-family and send it out for adversarial review; let the other families co-author it.

## Recipe

1. **Start from a framed design, never a fresh guess.** Read `design-<unit>.md` beside the work
   item: it carries the seam map, the requirements, the rejected alternatives, and the pinned
   source this plan decomposes. Always reach it by running `nuclear-frame` and waiting: its
   preflight owns freshness and returns a settled artifact untouched, so re-deciding here would be a
   second, weaker copy of that test — digests cannot see a changed ask. Then check what this plan
   will actually touch: **anything you are about to decompose that the frame never looked at means
   the frame is incomplete, not merely stale** — re-frame rather than filling the gap here. **No framed design, no dispatch** — a plan whose architecture
   was invented in the same turn as its task list has nothing decorrelated about it.
2. **Establish the doer's model family from self-reported runtime metadata, then ask independent
   reviewer CLIs to PRODUCE plans, not review one**: "author the safest build plan, the task
   decomposition, the simpler design that deletes a concept, and the traps you'd attack", with the
   design + seam map provided. At least one
   required co-author must be from a different model family than the doer; a same-family session
   may add evidence but never counts as decorrelated. Each required co-author meets
   `nuclear-review`'s reviewer bar — family and tier, pinned model id recorded beside its plan.
   Verify each CLI's self-reported model instead
   of inferring family from the executable name. Use the dispatch mechanics, neutral cwd,
   absolute-path/background rules, and model-pinning safeguards from
   `nuclear-review`.
   Raw plans land as `$SP/plan-<family>.md` (`$SP` = the dispatch scratchpad `nuclear-review`
   defines) — scratchpad only, never committed. **No files, no
   co-authorship** — a synthesis without a proven different-family plan is a solo draft.
3. **Synthesize** the independent plans + your own analysis into ONE plan. Reconcile
   disagreements by READING SOURCE (`git show <sha>:path`), never by vote.
4. Apply a cut pass: any task the synthesis shows unnecessary dies here — cheapest build is the one
   not built. Same blade for the design: an abstraction with one implementation, or a second home
   for a fact that already has one, dies with it.
5. Fix-pass the draft **in place**, multi-round (r1, r2, …), until every required co-author,
   including at least one proven different family, concurs. The draft is a working doc — no commit
   per round; commit the settled plan once.
   **The committed plan carries its own co-authorship line**: which families authored, which
   disagreed, and how each disagreement was settled. That line is the durable evidence — the
   scratchpad dies with the session, so anything gating on co-authorship reads the committed plan,
   never `$SP`. A plan without it is unplanned work with a plan-shaped file. The line is written by
   the doer, so make it checkable rather than claimable: name each pinned model id, quote the
   sentence that carried each disagreement, and state what the other family actually argued. A line
   that names families and nothing they said is a line anyone could have typed without dispatching.
6. Keep the binding decorrelated CODE gate after the build (`nuclear-review`). Co-authored
   plans make it converge; they don't replace it.

## Red flags

- "The plan is simple, review after building is enough" — that is how long gates start.
- A skill named inside another skill's step is an **instruction to invoke it**, not a citation.
- A refuted attack is not a defended design; N red-teamed mutations are not coverage of the N+1th.
- One option enumerated is no decision made — synthesis needs real alternatives to reconcile.
