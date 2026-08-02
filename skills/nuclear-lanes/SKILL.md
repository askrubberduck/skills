---
name: nuclear-lanes
description: Use when one review gate returns findings spanning several files/modules and a single fix-pass agent would serialize them — or when parallel fix teammates start crossing reports, drifting budgets, or flooding the coordinator with idle pings.
---

# Multi-Lane Fix-Pass

Fan one gate's findings across N parallel lanes by **file/module ownership**. One lane owns a file;
no two lanes edit the same file. The gate stays singular — lanes fix, the coordinator re-dispatches
the review.

## Recipe

1. **Partition findings by owned file set**, not by finding type. A finding touching two lanes' files
   goes to exactly one lane, named in both lanes' briefs.
2. **Brief each lane with only its findings** plus the shared invariants (perimeter/LOC budget, test
   suite, naming). Full finding list to every lane = N× the tokens for zero extra coverage.
3. **Re-pin the shared budget every round**: coordinator states the current total and each lane's
   delta ("LOC 30418, +13 all yours") so drift is caught at the round boundary, not at the gate.
4. **Reconcile crossed reports**: a lane claiming "already fixed" or "still broken" about another
   lane's file may be reading pre-fix code — settle by reading the current tree at the merge base,
   never by lane vote.
5. **Batch lane traffic**: coordinator polls lanes at round boundaries; an idle ping carrying no new
   state gets no reply. Each relayed no-op message re-bills the whole coordinator context.
6. Round ends when every lane reports landed + green; then ONE re-dispatch of the decorrelated gate
   (askrubberduck:nuclear-review). Loop.

## Common mistakes

- Lanes partitioned by finding severity — two lanes end up editing one file and conflict.
- Coordinator relaying every lane message into its own context verbatim — summarize per round.
- Letting a lane self-approve its fix as "gate-passed" — lanes never talk to the gate; the
  coordinator owns dispatch.
- Skipping the budget re-pin "because lanes are trusted" — drift is additive and invisible per lane.
