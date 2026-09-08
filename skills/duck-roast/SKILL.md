---
name: duck-roast
description: Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end. Use when the user asks for a roast or repeated full critique of the standing solution, wants a codebase audited for over-engineering, bloat, or what could be deleted repo-wide, or wants a milestone-level adversarial assessment rather than a change review or backlog sweep.
---

# Duck Roast

Adversarial critique of the **whole solution** — the fourth critique altitude. Wrong tool if the
target is one change (`duck-review`), the backlog
(`duck-cut`), or your own fresh diff (`duck-proof`). Roast reads
what exists end to end and argues it should be different or dead.

## Angles (cover material claims within the requested scope)

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

Ground criticism in the actual product and deployment. When the owner asks to challenge the goal,
question the evidence for its benefit and success measures too. Do not invent market or deployment
requirements, or substitute a new goal to make the critique stronger.

## Recipe

1. Ground in the real artifacts: canonical docs + actual source, not summaries.
2. Select the method, participants and effort bound from `duck-review`'s
   [challenge selection](../duck-review/references/challenge.md); use its
   [dispatch mechanics](../duck-review/references/dispatch.md) for external participants. A focused
   self-critique is labeled as such, not cross-family review. Give independent critics complementary
   material questions and the same constraints, not each other's conclusions.
3. Merge findings; every finding carries evidence (file, doc, observed behavior). The roast does
   retains substantiated findings with their consequences; group or rank when the owner requests
   it. Keep dismissed claims with their refutation so another pass does not resurrect them.
4. **Another round needs a question.** Default at most two passes unless the owner supplies a
   different bound. Re-dispatch only for a named unresolved claim with new evidence or a materially
   different approach. Stop on supported conclusions, refuted premises, unavailable evidence or the
   effort limit; record uncertainty. Never require an endless sequence of empty finding lists or
   mistake agreement for proof.
5. Land the output in the repo's reviews doc or a packet — the substantiated finding list and dismissed claims, each with evidence and a proposed disposition: fix now / backlog / owner decision
   (present those via `duck-decide`) / rejected-with-reason.

## Common mistakes

- Roasting the latest diff — wrong altitude; the roast reads the whole standing solution.
- Silently dropping substantiated findings; prioritizing a complete list is different from hiding
  evidence or inventing severity.
- Reading "surfaces everything" as "checks nothing" — weighing is the owner's, validating is the
  roast's. A claim it could not substantiate is reported as unsubstantiated, never laundered into
  the list as a finding.
- Buying another round without a question it could settle, or keeping a later, more complex
  candidate merely because it was produced last.
- Letting the roast write fixes — output is findings + dispositions; execution goes through the
  normal pipeline (`duck-plan` / `duck-review`) like any other work.
