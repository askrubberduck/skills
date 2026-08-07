---
name: nuclear-run
description: Plan, implement, test, and independently review a high-risk change. Use when the user requests end-to-end delivery with adversarial plan critique, says "nuclear" or "plan, critique, red team, execute on green", asks for a nuclear run or nuclear simplification, says "wear ponytail + nuclear soul", or invokes nuclear-run with a task.
---

# Nuclear Run

The bundled directive stack the user otherwise types as a preamble. Argument: the task.

## Stages

1. **Ground.** Read the project's quality bar first: `SOUL.md`, `CLAUDE.md`/`AGENTS.md` if present.
   Trace the real flow end to end before planning — laziness shortens the solution, never the reading.
2. **Plan.** Detailed decomposition: units of work, gates per unit, acceptance evidence.
   Steel-man at least one alternative decomposition before committing; first idea is a candidate, not a decision.
   Packet-sized or trust-touching: co-author the plan via `nuclear-plan` instead of
   drafting solo, and **do not enter stage 4 until the committed plan carries its co-authorship
   line** — an uncoauthored plan is the 19-round gate arriving later instead of now.
3. **Critique (adversarial, pre-code).** Red-team the plan: wrong decomposition, missing edge cases,
   simpler design that deletes a concept. Default the critic toward refute. Use an isolated judge
   stage or reviewer session on the strongest available tier. Fold findings; loop until the plan survives.
4. **Execute on green.** Use the host's native staged or multi-agent orchestration when available;
   otherwise execute the settled stages sequentially. Route mechanical stages (investigation,
   scripted edits, rebases, clerical verification, recording) to a cheaper capable worker only when
   the host exposes trustworthy per-stage routing. Keep adversarial review, synthesis, and
   trust-critical work on the strongest available tier; otherwise inherit the current model.
   TDD for code units: failing test first, minimal pass, then simplify.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; smallest
   diff after full understanding. Simplify touched code before building on it; clear superseded paths
   as the last step of each unit. No migrations, no back-compat shims unless the repo demands them.
6. **Verify.** Run the project's gates (tests/build/vet or doc gates), then invoke
   `nuclear-proof`
   on your own diff — it leaves `proof-<unit>.md`, or `$SP/proof-r1.md` when stage 7's review is
   next, which is where the gate looks; no file, no proof pass happened. Trust-touching
   work additionally gets the `nuclear-break` attacks executed before the gate. Evidence over
   assertion — a failed or unrun check means not done; say so with output.
7. **Independent review.** Never self-approve. Use the project's review policy — default: the
   `nuclear-review` / proven different-family gate. Fix-pass until the reviewer passes.

## Rules

- **Turn-end test.** A turn may end for exactly four reasons: (a) a decision genuinely the owner's —
  one where no defensible default exists; (b) an external block (spend limit, missing credential,
  denied permission, a reviewer still running); (c) the work is complete and recorded; (d) a context
  handoff whose next step is already dispatched or scheduled and named. Anything else: keep going.
- **"Say the word and I'll…" is a bug, not politeness.** If you can name the next step and it needs
  no owner input, run it. Handing an already-made plan back for a "go" is how an autonomous run
  becomes a manual one — it cost ~60 stalled turns in one week of campaign work.
- Ambiguous scope → cut it; don't add complexity for hypothetical edge cases.
- Record deferrals and owner decisions in the project's registry (never silently drop).
