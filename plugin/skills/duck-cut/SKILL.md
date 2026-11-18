---
name: duck-cut
description: Shrink a backlog the honest way; obsolete work out, duplicates merged, viable items unblocked. Use when the user asks to cut or clean a backlog, critique open or blocked backlog items, autonomously close, cut, merge, or unblock every item that does not need the owner, or when open, blocked, and deferred work keeps accumulating.
---

# Duck Cut

Challenge **every** open, blocked and deferred item with a cut bias. The goal is a smaller
backlog, not a tidier one. A "Cut this" finding weighs the same as "do this". A disposition flow
acts on IDs the owner names; this skill hunts.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

## Sweep

1. Run [`duck-scan`](../duck-scan/SKILL.md) to list every registry's items; it owns the registry
   locator. Include blocked delivery items and stale active-work directories. If it is
   missing, say so and ask once where the backlog is; never guess.
2. For each item, argue **against its existence** first (the existence check). Give one verdict:
   - **CLOSE NOW**: If satisfied, obsolete or superseded, close it with evidence (commit,
     shipped PR, doc), not a recollection.
   - **CUT**: If the need is speculative or the product moved past it, delete it; do not park it.
     Cite the lapsed requirement or the superseding decision, to the CLOSE NOW evidence bar.
   - **MERGE**: If it duplicates or is a subset of another item, fold and close it.
   - **UNBLOCK**: If the stated blocker no longer holds (verified, not assumed), make the item
     pickable. [`duck-scan`](../duck-scan/SKILL.md)'s attribution rule decides if an entry that
     lifts the blocker counts: an unattributed one does not.
   - **KEEP**: If it survives, record the one-sentence justification that saved it.

   Judge state by the landing, not the label. Give CLOSE NOW to an item labelled in progress or in
   review whose work is on the default branch (branch merged, or candidate tree matching a landed
   commit). Also give it to a closed item under an open heading.
3. Edit the registries for CLOSE/CUT/MERGE/UNBLOCK autonomously, with evidence. Local edits do
   not authorize a commit or publication. If a registry is outside version control, keep the cut
   text in the report until the owner has read it.
4. Queue items that need the owner (sign-offs, policy calls, anything the doer must not close)
   and run [`duck-decide`](../duck-decide/SKILL.md). Never close or silently drop an
   owner-gated item; continue past it.

## Report shape

Give counts first ("14 items: 4 closed, 2 cut, 1 merged, 2 unblocked, 3 kept, 2 to owner"),
then each item's verdict with evidence links.
