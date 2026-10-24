---
name: duck-decide
description: Walk the owner through the decisions they have been ducking, one at a time. Use when open decisions, blocked obligations, or approvals need the owner's answer, the user asks to walk through decisions or options, or several owner decisions are pending.
---

# Duck Decide

Blocking decisions are presented **one at a time, in full, in plain language**, unless the owner
chooses a batch once more than five are queued (see Order).

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Per decision, present

1. **Context**: what the decision unblocks and why it's the owner's call, readable at a glance.
2. **Options**: two to four real options with concrete tradeoffs, gains and risks, including
   material cost or schedule when relevant; sunk effort does not justify keeping a defect. One
   option is no decision offered.
3. **Recommendation**: one, with the reason in one sentence.
4. **Wait on the dependent action.** Standalone, stop until the owner answers. Embedded in an
   executing workflow, return the pending decision to the caller; continuing separately authorized
   independent work is the caller's responsibility, not approval of the blocked action. Silence
   never supplies an answer or permission.

Check the decision log first; never re-present a settled decision. After the answer, record it, and
whether it is executed or still outstanding, in the owning registry/doc (decision log, obligations
registry, whatever the repo uses) before presenting the next decision.

## Order

Owner-specified order first; otherwise most-blocking first. Say how many are queued up front ("4
decisions queued; here is 1 of 4").

Past five queued, ask first how to take them: one at a time; every recommendation; every
recommendation except the policy items; later. Name the policy items (money, risk, anything that
changes what an operator or user can do) and keep them out of any batch. Walk only the ones the
owner keeps; record each batched decision as the owner's answer with the words that took it.
