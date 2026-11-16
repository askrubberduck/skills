---
name: duck-shape
description: Make every layer earn its place; cut the machinery the problem never asked for. Use when the user asks to simplify, shorten or clean up code or tests, calls it over-engineered, bloated, too defensive, duplicated or AI slop, asks to cut a repeated check, inline a supposedly pointless wrapper or drop an unused mode or flag, asks which of two designs carries less, or asks if finished work has its simplest structure, even in a small file or pasted snippet that already looks plain. A request to cut is enough to check what the cut would lose. Not for explaining code, renaming, or comments alone.
---

# Duck Shape

Remove a concrete maintenance burden without loss of required behavior. Change behavior only if
it is explicitly in scope. Complexity is what makes code hard to change. A smaller diff or more
impressive design is not evidence of improvement.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

Apply scoped local edits unless the request is report-only or analysis-only. Selected findings limit
repairs. Report each finding as applied, skipped with its reason, or parked. Continue through
verification. Commits and publication need separate authorization.

## Establish the scope and behavior

By default, shape the current task's changed code. An explicit file or subsystem bounds a wider
cleanup, never a repo audit. Read the affected path through its callers, state owners and
observable effects. Inspect shared helpers and project conventions before any replacement.

Identify outcomes that must survive, including errors, recovery and public contracts. Run
relevant existing checks first. For an uncovered material contract, add a focused regression
check that pins current behavior, not desired behavior. Do not add tests for trivial
edits or lock in a known bug as intended behavior.
If execution is unavailable, name the missing check and limit the claim.

## Find specific things to remove

These are inspection prompts (the necessity checks), not automatic deletion rules:

- Duplicate rules or state: find the authoritative owner and copies that can drift.
- A unit with several unrelated jobs, or two units that always change together: split along what
  changes together. Callers pass data and do not reach into shared state.
- Dead paths, exports and flags: check callers, configuration and external use before deletion.
- Pass-through wrappers and speculative options: name the contract they protect.
- Special-case branches: can a different representation (empty instead of absent, zero-length
  instead of a flag) let the normal path cover the edge case?
- Reimplemented helpers or platform features: compare the existing facility's real guarantees.
- Defensive branches and fallbacks: separate required boundary validation and recovery from
  impossible internal states and errors silently converted into success.
- Tests that mirror implementation: keep outcome checks. Question mocks or assertions that can pass
  while the required behavior fails.

For each material item, choose **remove**, **simplify using an existing facility**, or **keep**.
Base the choice on a caller, contract, failure case or demonstrated change cost. "Separation of
concerns" or a possible future use is not evidence. A single implementation can still protect a
public API, security boundary or real platform difference. If nothing states why a mechanism
in the history exists, trace it with [`duck-why`](../duck-why/SKILL.md) before you choose
remove.

## Make the smallest justified cleanup

Start with safe deletions. Then consolidate repeated rules where they belong: one owner per rule
and state transition. Do not create a replacement abstraction only for the cleanup. Keep
validation, security, accessibility, recovery and necessary calibration intact.

Focus each edit on one cause. Rerun affected checks before you build on a risky change.
Comments and docstrings use [`duck-dry`](../duck-dry/SKILL.md)'s [prose
bar](../duck-dry/references/bar.md).
Deleted commentary neither repairs structure nor justifies another helper.

For an explicitly requested deep simplification, or a demonstrated wrong boundary beyond local
cleanup, use [reconstruction](references/reconstruction.md). Resolve an unsettled outcome or
boundary contract with [`duck-frame`](../duck-frame/SKILL.md) before dependent edits. In analysis
mode, apply the necessity checks to proposed mechanisms without edits.

## Verify and finish

Run relevant checks on the final candidate and inspect the resulting path. For structural
changes, walk a realistic next change (the realistic change probe). Can a reader understand each
touched unit without its callers open? Did a duplicate rule, state owner, order obligation or
unnecessary hop disappear? Do not trade obvious code for dense expressions or hidden coupling.

Report material removals or simplifications, each questionable mechanism kept with its concrete
reason, and the checks run with their limits. If no item survives inspection, unchanged code is a
valid result. Stop when the scoped findings are resolved and affected checks pass. Another pass
needs an unresolved defect, not a cleanup quota.

[`duck-proof`](../duck-proof/SKILL.md) can challenge a remaining contract claim. This cleanup is not
the independent release approval that [`duck-review`](../duck-review/SKILL.md) owns.
