---
name: duck-shape
description: Make every layer earn its place; cut the machinery the problem never asked for. Use when the user asks to simplify, shorten or clean up code, calls it over-engineered, bloated, too defensive or AI slop, asks which of two designs carries less, or wants the structure of completed work checked, whether a file, a diff or a pasted snippet. Deep reconstruction is available when local cleanup cannot fix the boundary.
---

# Duck Shape

Remove a concrete maintenance burden without losing required behavior. Complexity is what makes
the code hard to change: a small edit that touches many places, facts a reader must hold before
editing safely, and behavior nobody can predict from the interface. A smaller diff or a more
impressive design is not evidence of improvement.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
Apply scoped local edits unless the request is report-only or analysis-only. Selected findings
limit repairs. Continue through verification; commits and publication need separate authorization.

## Establish the scope and behavior

Default to the current task's changed code; an explicit file or subsystem bounds a wider cleanup.
Reading goes further than the edits: a duplicate rule or a second owner of the same state
usually sits in a file the diff never touched. Read the affected path through its callers, state
owners and observable effects. Inspect shared helpers and project conventions before replacing
anything. Do not expand a cleanup into a repo audit.

Identify the outcomes that must survive, including errors, recovery and public contracts. Run the
relevant existing checks before editing. Add a focused regression check when a material contract
is uncovered, pinning what the code does today, not what it should do; do not manufacture tests for trivial edits or lock in a known bug as intended behavior.
If execution is unavailable, name the missing check and limit the claim accordingly.

## Find specific things to remove

Use these as inspection prompts (the necessity checks), not automatic deletion rules:

- Duplicate rules or state: locate the authoritative owner and the copies that can drift.
- A unit that does several unrelated jobs, or two units that always change together: the split
  should follow what changes together, and callers should pass data, not reach into shared state.
- Dead paths, exports and flags: check callers, configuration and external use before deleting.
- Pass-through wrappers and speculative options: identify the contract they actually protect.
- Reimplemented helpers or platform features: compare the existing facility's real guarantees.
- Defensive branches and fallbacks: distinguish required boundary validation and recovery from
  impossible internal states or errors silently converted into success.
- Tests that mirror implementation: preserve outcome checks; question mocks or assertions that
  can pass while the required behavior fails.

For each material candidate, choose **remove**, **simplify using an existing facility**, or **keep**.
Ground the choice in a caller, contract, failure case or demonstrated change cost. "Separation of
concerns" or a possible future use is not sufficient evidence. A single implementation may still
protect a public API, security boundary or real platform difference.

## Make the smallest justified cleanup

Start with safe deletions, then consolidate repeated rules where they belong. Keep one owner per
rule and state transition. Avoid creating a replacement abstraction merely to perform the cleanup.
Keep validation, security, accessibility, recovery and necessary calibration intact.

Keep edits focused on a cause; rerun affected checks before building on a risky change. Preserve
required behavior unless a behavior change is explicitly in scope. Comments and docstrings use
`duck-dry`'s [prose bar](../duck-dry/references/bar.md); deleting commentary does not repair the
structure or justify extracting another helper.

For an explicitly requested deep simplification or a demonstrated wrong boundary that local
cleanup cannot fix, use [reconstruction](references/reconstruction.md). If the required outcome or
boundary contract is unsettled, resolve that decision with `duck-frame` before dependent edits.
Analysis-only use compares proposed mechanisms with the same tests of necessity; it does not edit.

## Verify and finish

Run the relevant checks on the final candidate and inspect the resulting path. For structural
changes, walk a realistic next change (the realistic change probe): can a reader understand each
touched unit without its callers open, and did a duplicate rule, state owner, ordering obligation
or unnecessary hop disappear? Do not trade obvious code for dense expressions or hidden coupling.

Report the material removals or simplifications, any questionable mechanism retained and its
concrete reason, and the checks actually run with their limits. Unchanged code is a valid result
when no candidate survives inspection. Stop when the scoped findings are resolved and affected
checks pass; another pass needs an unresolved defect, not a cleanup quota.

`duck-proof` can challenge a remaining contract claim. This cleanup does not provide the independent
release approval owned by `duck-review`.
