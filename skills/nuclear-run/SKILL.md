---
name: nuclear-run
description: Full-rigor delivery loop — detailed plan, adversarial critique/red-team of the plan, execute on green via Workflow with per-stage model routing, ponytail simplification lens, verify before claiming done. Use when the user says "nuclear", "wear ponytail + nuclear soul", "plan, critique, red team, execute on green", "nuclear simplification", or invokes /nuclear-run <task>.
---

# Nuclear Run

The bundled directive stack the user otherwise types as a preamble. Argument: the task.

## Stages

1. **Ground.** Read the project's quality bar first: `SOUL.md`, `CLAUDE.md`/`AGENTS.md` if present.
   Trace the real flow end to end before planning — laziness shortens the solution, never the reading.
2. **Plan.** Detailed decomposition: units of work, gates per unit, acceptance evidence.
   Steel-man at least one alternative decomposition before committing; first idea is a candidate, not a decision.
3. **Critique (adversarial, pre-code).** Red-team the plan: wrong decomposition, missing edge cases,
   simpler design that deletes a concept. Default the critic toward refute. Run as a Workflow judge
   stage on the strongest tier (`model:` inherit). Fold findings; loop until the plan survives.
4. **Execute on green.** Run the build as a Workflow. Per-stage `model:` routing is mandatory:
   - mechanical stages (investigate, scripted edits, rebases, clerical verify, record commits) → `model: 'sonnet'`
   - adversarial review, synthesis, trust-critical code → inherit (strongest tier)
   TDD for code units: failing test first, minimal pass, then simplify.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; smallest
   diff after full understanding. Simplify touched code before building on it; clear superseded paths
   as the last step of each unit. No migrations, no back-compat shims unless the repo demands them.
6. **Verify.** Run the project's gates (tests/build/vet or doc gates). Evidence over assertion —
   a failed or unrun check means not done; say so with output.
7. **Independent review.** Never self-approve. Use the project's review policy (in waddleloop-genesis:
   the `redteam-review` skill / two-family decorrelated gate). Fix-pass until the reviewer passes.

## Rules

- Continue stages without pausing for approval unless a decision is genuinely the owner's.
- Ambiguous scope → cut it; don't add complexity for hypothetical edge cases.
- Record deferrals and owner decisions in the project's registry (never silently drop).
