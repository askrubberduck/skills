---
name: duck-shape
description: Take the mechanism apart and rebuild the simplest robust path; leave the reader less to hold in their head. Use while implementing, to verify completed structure, or for deep simplification that dismantles accidental mechanisms and rebuilds a robust path. Judge concepts and realistic changes, not line count.
---

# Duck Shape

The cost is what a reader must hold simultaneously before changing the code safely. A layer earns
its place when it answers a question and ends the read. Depth, file count and line count cannot
measure that. Removing a required invariant to shorten the code is a failed simplification.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

Apply improvements within authorized implementation scope. Report-only means inspect and recommend
without edits. Selected findings limit subsequent fixes; continue authorized local work through
verification, not through unrequested commits, PRs or pushes.

## Understand before cutting

Read the affected flow from entry to observable effect, including callers, state owners, failure
recovery and project constraints. Pick a realistic next change or the last bug. What must you open
and what facts must you hold before safely editing? A diff alone hides most of that path.

Look especially for:

- a flag set elsewhere that changes a branch's meaning;
- unenforced ordering or lifetime: initialize first, close later, valid only in some states;
- units, timezone, precision or calibration whose meaning lives elsewhere;
- shared mutable state and duplicate homes for a rule;
- forwarding layers that make the reader travel without answering a question;
- a mode or parameter that looks live but no reachable caller needs.

State the outcome lost if a mechanism disappears. No lost outcome is a deletion candidate, not
permission to ignore public contracts or callers you have not inspected. Dead code matters when
readers must carry it as a live possibility; unrelated sediment is not automatically this task.

## Compare structures against the same contract

Prefer removal, an existing helper, stdlib, or a native platform mechanism when its actual
guarantees fit. A familiar name often ends a read; a one-call dependency can add a vocabulary and
lifecycle that cost more than it saves. A wrapper helps when it names the operation or isolates
real volatility, and hurts when it hides a familiar contract behind an uninformative name.

Ask whether a reader can state what an operation does and identify where to look next without a
search. A hierarchy whose contracts answer that question may be cheaper than flattening it into
one function. Composition helps when it reduces facts held together, not because inheritance is
inherently defective. Keep required polymorphic, platform, public-version and volatile boundaries.

An abstraction with one implementation is neither automatically debt nor automatically justified
by a possible second case. Read the roadmap and current contract; ask the owner only when an
unresolved bet changes the decision. Compare the cost of the seam today with introducing it when
needed. Preserve one concise explanation of a real constraint; a name for a hypothetical future
must not immunize unnecessary machinery from challenge.

A leaky seam charges a hop while still requiring knowledge of the inside. A wrong seam splits
things that change together. Trace a realistic change or relevant history to distinguish these
from a naming problem. Re-cutting a boundary uses `duck-frame` to settle the affected contract;
relabeling a wrong boundary does not repair it.

## Reconstruction, when local cleanup cannot remove the mechanism

Use this for an explicitly requested deep simplification or a demonstrated wrong boundary, bounded
to the subsystem under discussion. Compare with a smaller in-place correction before replacing it.

1. Recover the required outcomes and contracts, including failure recovery and known next changes.
2. Separate inputs, decisions, state and side effects conceptually. This is analysis, not a demand
   for a class or file per piece.
3. Classify mechanisms as required by the problem, required by the platform, or accidental. Attack
   duplicate state, parallel paths, mode flags, translation layers and caller ordering obligations.
4. Assemble the smallest path with one owner per rule and state transition. Reuse existing
   facilities and keep security, validation, accessibility and necessary calibration intact.
5. Replace within the authorized scope, test the contracts, and remove superseded code, config and
   tests that only encode the old mechanism. Preserve tests of required outcomes. Intentional
   behavior changes need explicit checks rather than blind equivalence to the original bug.

Do not rebuild merely because the alternative looks cleaner. The replacement must remove a real
obligation or make a realistic change easier without weakening the contracts.

## Verify the completed shape

Walk the assembled path again and attempt the representative change. Name what the reader no
longer has to hold and where each remaining fact belongs. A smaller diff that spreads state or
hides ordering failed the probe; more lines with fewer independent obligations can win.

Run affected behavioral checks after restructuring. Use `duck-proof` for contract counterexamples,
final-state evidence and comparison of surviving alternatives. Shape edits invalidate relevant
prior evidence. Keep causes near effects and one authoritative home per fact. A regex, clever
comprehension or compressed branch wins only when its semantics are actually easier to read.

Comments can reveal hidden coupling, but their absence proves no clarity. Fix the structure that
made an explanation necessary; `duck-dry` owns the surviving prose and protects parsed directives,
external contracts and calibrated knobs. Do not silently change behavior during a comment sweep.

## Handoff

Apply justified changes where execution is already authorized. Take the edited diff through
[the prose bar](../duck-dry/references/bar.md) before verifying: a restructure moves the code a
comment described. A real owner decision goes to `duck-decide`; independent work can continue. A
whole-product critique belongs to `duck-roast`, not an unrequested expansion of the current
restructure.

The structural probe is evidence, not independent approval. `duck-review` judges release work under
the repository's policy. Keep unrelated restructures separate from behavior changes when commits
are authorized; shaping the code a unit already changes belongs in that unit.
