---
name: nuclear-roast
description: Use when the user asks for a "roast", a full critique of the whole product, solution, or architecture from multiple angles, says "run and run again", or wants a milestone-level adversarial read — solution-scoped, not a change review or backlog sweep.
---

# Nuclear Roast

Adversarial critique of the **whole solution** — the fourth critique altitude. Wrong tool if the
target is one change (nuclear-review), the backlog (nuclear-cut), or your own fresh diff
(nuclear-proof). Roast reads what exists end to end and argues it should be different or dead.

## Angles (every round covers all)

1. **Containment/security posture** — boundaries enforced from outside? fail closed? what does a
   compromised component reach?
2. **Simplicity** — concepts that should die, dual paths, layers nobody needs; the biggest deletion
   available, not the tidiest nit.
3. **Product fit and scope** — does what's built serve the stated vision? what shipped that
   shouldn't have? where is the boundary not where users need it?
4. **Extendability** — what change class is expensive that will be asked for? what's welded that
   should be a seam?
5. **Operational reality** — failure modes, recovery paths, what breaks at 3am and who notices.

Critique product and engineering substance ONLY — never market validation, user counts, or
"run the pilot first" framing.

## Recipe

1. Ground in the real artifacts: canonical docs + actual source, not summaries.
2. Dispatch decorrelated families (codex + agy) with the full angle list — mechanics, traps, and
   fail-closed rules per askrubberduck nuclear-review. Add your own pass as a third perspective.
3. Merge findings; every finding carries evidence (file, doc, observed behavior) and a severity.
   Refuted findings are recorded with the refutation and carried into the next round's prompt.
4. **Run and run again**: next round re-dispatches with prior findings settled. Stop only when a
   full round yields nothing new (loop-until-dry) — one pass is a review, not a roast.
5. Land the output in the repo's reviews doc or a packet — ranked findings, each with evidence and
   a proposed disposition: fix now / backlog / owner decision (present those via askrubberduck
   nuclear-decide) / rejected-with-reason.

## Common mistakes

- Roasting the latest diff — wrong altitude; the roast reads the whole standing solution.
- Findings without evidence — a vibe is not a finding; cite the file or the behavior.
- Stopping after round one because it "found plenty" — the second round against settled findings is
  where the deep ones surface.
- Letting the roast write fixes — output is findings + dispositions; execution goes through the
  normal pipeline (nuclear-plan / nuclear-review) like any other work.
