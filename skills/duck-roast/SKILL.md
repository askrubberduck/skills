---
name: duck-roast
description: Roast an entire product, solution, or architecture from every angle until only the defensible parts remain. Use when the user asks for a roast or repeated full critique of the standing solution, wants a codebase audited for over-engineering, bloat, or what could be deleted repo-wide, or wants a milestone-level adversarial assessment rather than a change review or backlog sweep.
---

# Duck Roast

Adversarial critique of the **whole solution** — the fourth critique altitude. Wrong tool if the
target is one change (`duck-review`), the backlog
(`duck-cut`), or your own fresh diff (`duck-proof`). Roast reads
what exists end to end and argues it should be different or dead.

## Angles (every round covers all)

1. **Containment/security posture** — boundaries enforced from outside? fail closed? what does a
   compromised component reach?
2. **Simplicity** — concepts that should die, dual paths, layers nobody needs; the biggest deletion
   available, not the tidiest nit. Cost is what a reader must hold, never lines or nesting depth,
   so hunt: layers that forward the question instead of answering it, names saying how a thing was
   built rather than what it provides, seams with one implementation whose second case nobody can
   state, hand-rolled code shadowing a name the stack already holds, branches a reader cannot tell
   are dead, and the densest comment neighbourhoods — whoever wrote them stood where the reading
   got hard. Two queries carry this angle: the same pair of files co-occurring across most commits
   is the wrong-seam signature, invisible in any single file and obvious in history; and churn per
   file, which is **evidence on a finding, never a rank** — a deep hierarchy nobody has opened in
   two years is sediment, not debt, and saying so is part of the finding. Walk three to five
   plausible next changes through the tree rather than reading files: a finding attached to a real
   walk survives argument, one attached to a grep does not. Close the angle by naming the patterns
   that repeat — one speculative seam is a finding, the same seam in nine modules is a convention,
   and that is one owner decision rather than nine edits. `duck-shape` is this lens at change
   altitude, and applies what this angle finds.
3. **Product fit and scope** — does what's built serve the stated vision? what shipped that
   shouldn't have? where is the boundary not where users need it?
4. **Extendability** — what change class is expensive that will be asked for? what's welded that
   should be a seam?
5. **Operational reality** — failure modes, recovery paths, what breaks at 3am and who notices.

Critique product and engineering substance ONLY — never market validation, user counts, or
"run the pilot first" framing.

## Recipe

1. Ground in the real artifacts: canonical docs + actual source, not summaries.
2. Dispatch independent reviewer families selected relative to the doer's verified model family,
   with the full angle list and fail-closed rules from `duck-review`. Add your own
   pass as a third perspective.
3. Merge findings; every finding carries evidence (file, doc, observed behavior). The roast does
   NOT judge severity and does not triage — every finding survives to the output; the owner weighs
   them. Refuted findings are recorded with the refutation and carried into the next round's prompt.
4. **Run and run again**: next round re-dispatches with prior findings settled. Stop only when a
   full round yields nothing new (loop-until-dry) — one pass is a review, not a roast.
5. Land the output in the repo's reviews doc or a packet — the ENTIRE finding list, unfiltered and
   unranked, each with evidence and a proposed disposition: fix now / backlog / owner decision
   (present those via `duck-decide`) / rejected-with-reason.

## Common mistakes

- Roasting the latest diff — wrong altitude; the roast reads the whole standing solution.
- Trimming the list to "the important ones" or severity-sorting it — the owner judges weight; the
  roast only surfaces. A dropped finding is a silent decision the roast had no right to make.
- Reading "surfaces everything" as "checks nothing" — weighing is the owner's, validating is the
  roast's. A claim it could not substantiate is reported as unsubstantiated, never laundered into
  the list as a finding.
- Stopping after round one because it "found plenty" — the second round against settled findings is
  where the deep ones surface.
- Letting the roast write fixes — output is findings + dispositions; execution goes through the
  normal pipeline (`duck-plan` / `duck-review`) like any other work.
