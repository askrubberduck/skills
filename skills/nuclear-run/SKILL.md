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
3. **Critique (adversarial, pre-code) — for solo-drafted plans only.** When `nuclear-plan` ran in
   stage 2, its multi-round concurrence loop already **is** this stage; a second gate on a
   co-authored plan is redundancy, not rigor. Otherwise: red-team the plan — wrong decomposition,
   missing edge cases, simpler design that deletes a concept. Default the critic toward refute, use
   the strongest available tier, fold findings, loop until the plan survives.
4. **Execute on green.** Use the host's native staged or multi-agent orchestration when available;
   otherwise execute the settled stages sequentially. Route mechanical stages (investigation,
   scripted edits, rebases, clerical verification, recording) to a cheaper capable worker only when
   the host exposes trustworthy per-stage routing — trustworthy means the worker's model is
   pinnable, its self-report verifiable, and its output lands in a gated verification stage; fail
   any of the three and the stage runs on the inherited model. Keep adversarial review, synthesis, and
   trust-critical work on the strongest available tier; otherwise inherit the current model.
   TDD for code units: failing test first, minimal pass, then simplify.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; smallest
   diff after full understanding. Simplify touched code before building on it; clear superseded paths
   as the last step of each unit. No migrations, no back-compat shims unless the repo demands them.
   **Write for a senior reader.** Code explains itself; comments supplement it. A comment earns its
   place only for a decision the code cannot show — a non-obvious tradeoff, a constraint on inputs or
   schema, a trap. Never narrate what the next line does, and never leave the war story of the bug
   that caused it: that belongs in the commit, and in the code it is dead weight the next edit
   silently falsifies.
6. **Verify.** Run the project's gates (tests/build/vet or doc gates), then invoke
   `nuclear-proof`
   on your own diff — it leaves `proof-<unit>.md`, or `$SP/proof-r1.md` when stage 7's review is
   next (`$SP`: `nuclear-review`'s dispatch scratchpad), which is where the gate looks; no file, no
   proof pass happened. Trust-touching
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
- **A finding is not a work order.** Under review pressure the fastest way to look responsive is to
  add code, so every fix pass starts with "would deleting this end the finding?" and every unit asks
  what outcome dies if the code is not written. The most reliable code is the code never written;
  that is the spirit, not a tiebreaker for close calls.
- **Judge the shape, not the diffstat.** Fewer lines is a smell, not a goal. What compounds is how
  many concepts a reader holds, whether one path traces without jumping, whether cause sits near
  effect, and whether each fact has one home. A short knot costs more than a long straight path, and
  the line metric scores the knot as the win — which is exactly why it cannot be the target.
- Record deferrals and owner decisions in the project's registry (never silently drop).
