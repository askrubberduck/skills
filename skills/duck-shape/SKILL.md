---
name: duck-shape
description: Make every layer earn its place; cut the machinery the problem never asked for. Use when the user asks to simplify, shorten or clean up code or tests, calls it over-engineered, bloated, too defensive, duplicated or AI slop, asks to cut a repeated check, inline a supposedly pointless wrapper or drop an unused mode or flag, asks which of two designs carries less, or asks if finished work has its simplest structure, even in a small file or pasted snippet that already looks plain. A request to cut is enough to check what the cut would lose. Not for explaining code, renaming, or comments alone.
---

# Duck Shape

Remove a concrete maintenance burden without losing required behavior, unless a behavior change is
explicitly in scope. Complexity is what makes code hard to change; a smaller diff or a more
impressive design is not evidence of improvement.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
Apply scoped local edits unless the request is report-only or analysis-only. Selected findings
limit repairs; report each one applied, skipped with its reason, or parked. Continue through
verification; commits and publication need separate authorization.

## Establish the scope and behavior

Default to the current task's changed code; an explicit file or subsystem bounds a wider cleanup,
never a repo audit. Read the affected path through its callers, state owners and observable
effects; inspect shared helpers and project conventions before replacing anything.

Identify the outcomes that must survive, including errors, recovery and public contracts. Run the
relevant existing checks before editing. Add a focused regression check when a material contract is
uncovered, pinning what the code does today, not what it should do; no tests for trivial edits,
and no known bug locked in as intended behavior.
If execution is unavailable, name the missing check and limit the claim.

## Find specific things to remove

Inspection prompts (the necessity checks), not automatic deletion rules:

- Duplicate rules or state: find the authoritative owner and the copies that can drift.
- A unit doing several unrelated jobs, or two units that always change together: split along what
  changes together; callers pass data rather than reach into shared state.
- Dead paths, exports and flags: check callers, configuration and external use before deleting.
- Pass-through wrappers and speculative options: name the contract they actually protect.
- Special-case branches: can a different representation (empty instead of absent, zero-length
  instead of a flag) let the normal path cover the edge case?
- Reimplemented helpers or platform features: compare the existing facility's real guarantees.
- Defensive branches and fallbacks: separate required boundary validation and recovery from
  impossible internal states and errors silently converted into success.
- Tests that mirror implementation: keep outcome checks; question mocks or assertions that can
  pass while the required behavior fails.

For each material candidate choose **remove**, **simplify using an existing facility**, or **keep**,
grounded in a caller, contract, failure case or demonstrated change cost. "Separation of concerns"
or a possible future use is not evidence; a single implementation may still protect a public API,
security boundary or real platform difference. When nothing states why a mechanism already in the
history exists, trace it with [`duck-why`](../duck-why/SKILL.md) before choosing remove.

## Make the smallest justified cleanup

Start with safe deletions, then consolidate repeated rules where they belong: one owner per rule
and state transition, no replacement abstraction created just to perform the cleanup. Keep
validation, security, accessibility, recovery and necessary calibration intact.

Keep edits focused on a cause; rerun affected checks before building on a risky change. Comments
and docstrings use [`duck-dry`](../duck-dry/SKILL.md)'s [prose bar](../duck-dry/references/bar.md);
deleting commentary neither repairs structure nor justifies another helper.

For an explicitly requested deep simplification or a demonstrated wrong boundary local cleanup
cannot fix, use [reconstruction](references/reconstruction.md). Resolve an unsettled outcome or
boundary contract with [`duck-frame`](../duck-frame/SKILL.md) before dependent edits. Analysis mode
applies the necessity checks to proposed mechanisms without editing.

## Verify and finish

Run the relevant checks on the final candidate and inspect the resulting path. For structural
changes, walk a realistic next change (the realistic change probe): can a reader understand each
touched unit without its callers open, and did a duplicate rule, state owner, ordering obligation
or unnecessary hop disappear? Do not trade obvious code for dense expressions or hidden coupling.

Report the material removals or simplifications, any questionable mechanism retained with its
concrete reason, and the checks run with their limits. Unchanged code is a valid result when no
candidate survives inspection. Stop when the scoped findings are resolved and affected checks
pass; another pass needs an unresolved defect, not a cleanup quota.

[`duck-proof`](../duck-proof/SKILL.md) can challenge a remaining contract claim. This cleanup is not
the independent release approval owned by [`duck-review`](../duck-review/SKILL.md).
