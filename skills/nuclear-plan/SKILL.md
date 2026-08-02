---
name: nuclear-plan
description: Use when about to plan or implement packet-sized, architectural, or trust-touching work — a plan or draft exists or is about to be written — or when past review gates for similar work took many REJECT rounds.
---

# Plan Co-Authoring with the Red Team

Decorrelated rigor arrives either as *co-authorship* now or as *rejections* later. Do NOT draft a
plan same-family and send it out for adversarial review — that path produced 19-round gates; letting
the other families co-author cut it to 4 and deleted 2 of 4 work items as no-code-needed.

## Recipe

1. **Investigate the real code seams first.** Ground everything in actual source, never a summary.
2. **Ask each decorrelated CLI (codex, agy) to PRODUCE a plan, not review one**: "author the safest
   build plan, the task decomposition, and the traps you'd attack", with the design + seam map
   provided. Dispatch mechanics, CLI traps, absolute-path/background rules: same as
   askrubberduck:nuclear-review — pin the agy model, neutral cwd, outputs to scratchpad.
3. **Synthesize** the two decorrelated plans + your own analysis into ONE plan. Reconcile
   disagreements by READING SOURCE (`git show <sha>:path`), never by vote.
4. Apply a cut pass: any task the synthesis shows unnecessary dies here — cheapest build is the one
   not built.
5. Fix-pass the draft **in place**, multi-round (r1, r2, …), until both families concur on the plan.
   The draft is a working doc — no commit per round; commit the settled plan once.
6. Keep the binding decorrelated CODE gate after the build (askrubberduck:nuclear-review). Co-authored
   plans make it converge; they don't replace it.

## Red flags

- "The plan is simple, review after building is enough" — that's how 19-round gates start.
- A refuted attack is not a defended design; N red-teamed mutations are not coverage of the N+1th.
- One option enumerated is no decision made — synthesis needs real alternatives to reconcile.
