---
name: duck-decide
description: Walk the owner through the decisions they have been ducking, one at a time. Use when open decisions, blocked obligations, or approvals need the owner's answer, the user asks to walk through decisions or options, or several owner decisions are pending.
---

# Duck Decide

Present blocking decisions **one at a time, in full, in plain language** (for a batch, see Order).

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Per decision, present

1. **Context**: what the decision unblocks and why the owner decides it, readable at a glance.
2. **Options**: two to four real options with concrete tradeoffs, gains and risks. Include material
   cost or schedule when relevant. Sunk effort does not justify keeping a defect. A single option offers
   no decision.
3. **Recommendation**: one, with the reason in one sentence.
4. **Wait on the dependent action.** If standalone, stop until the owner answers. Inside a workflow,
   return the pending decision to the caller. The caller owns independent work with its own
   authorization; that work does not approve the blocked action. Silence never supplies an answer or
   permission.

Check the decision log first, and never present a settled decision again. After each answer, record
it and its status (executed or outstanding) where the repo keeps it: decision log, obligations
registry, or other. Then present the next decision.

## Order

Use the owner's order; otherwise, most blocking first. At the start, say how many are queued ("4
decisions queued; here is 1 of 4").

If more than five are queued, first ask the owner how to take them:

- one at a time;
- every recommendation;
- every recommendation except the policy items;
- later.

Name the policy items: money, risk, anything that changes what an operator or user can do. Keep them
out of every batch. Walk only the decisions the owner keeps. Record each batched decision as the
owner's answer, with the words that took it.
