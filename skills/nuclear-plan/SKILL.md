---
name: nuclear-plan
description: Catch architectural and implementation risks before coding begins. Use when about to plan OR about to implement large, architectural, security-, privacy-, or data-sensitive work — including when implementation is about to start and no plan exists yet — when a draft plan needs independent critique, or when similar work previously failed several review rounds.
---

# Plan Co-Authoring with the Red Team

Decorrelated rigor arrives either as *co-authorship* now or as *rejections* later. Do NOT draft a
plan same-family and send it out for adversarial review — that path produced 19-round gates; letting
the other families co-author cut it to 4 and deleted 2 of 4 work items as no-code-needed.

## Recipe

1. **Investigate the real code seams first.** Ground everything in actual source, never a summary.
2. **Establish the doer's model family from self-reported runtime metadata, then ask independent
   reviewer CLIs to PRODUCE plans, not review one**: "author the safest build plan, the task
   decomposition, and the traps you'd attack", with the design + seam map provided. At least one
   required co-author must be from a different model family than the doer; a same-family session
   may add evidence but never counts as decorrelated. Each required co-author runs the strongest
   available tier of its family (`nuclear-review`'s reviewer rule — family buys independence, tier
   buys rigor). Verify each CLI's self-reported model instead
   of inferring family from the executable name. Use the dispatch mechanics, neutral cwd,
   absolute-path/background rules, and model-pinning safeguards from
   `nuclear-review`.
   Raw plans land as `$SP/plan-<family>.md` (`$SP` = the dispatch scratchpad `nuclear-review`
   defines) — scratchpad only, never committed. **No files, no
   co-authorship** — a synthesis without a proven different-family plan is a solo draft wearing the
   word "synthesized".
3. **Synthesize** the independent plans + your own analysis into ONE plan. Reconcile
   disagreements by READING SOURCE (`git show <sha>:path`), never by vote.
4. Apply a cut pass: any task the synthesis shows unnecessary dies here — cheapest build is the one
   not built.
5. Fix-pass the draft **in place**, multi-round (r1, r2, …), until every required co-author,
   including at least one proven different family, concurs. The draft is a working doc — no commit
   per round; commit the settled plan once.
   **The committed plan carries its own co-authorship line**: which families authored, which
   disagreed, and how each disagreement was settled. That line is the durable evidence — the
   scratchpad dies with the session, so anything gating on co-authorship reads the committed plan,
   never `$SP`. A plan without it is unplanned work with a plan-shaped file.
6. Keep the binding decorrelated CODE gate after the build (`nuclear-review`). Co-authored
   plans make it converge; they don't replace it.

## Red flags

- "The plan is simple, review after building is enough" — that's how 19-round gates start.
- A skill named inside another skill's step is an **instruction to invoke it**, not a citation. A week
  of packet-sized campaign work with zero `nuclear-plan` invocations is what that
  failure looks like.
- A refuted attack is not a defended design; N red-teamed mutations are not coverage of the N+1th.
- One option enumerated is no decision made — synthesis needs real alternatives to reconcile.
