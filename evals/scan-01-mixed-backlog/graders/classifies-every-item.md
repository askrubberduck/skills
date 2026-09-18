---
type: llm
focus: last_message
weight: 1
---
Answer key for the pasted registry:
- W-02 and W-05: open and unblocked → pickable. These are the ONLY pickable items.
- W-03: blocked on W-05 → not pickable.
- W-04: in review (PR #52 awaiting reviewer) → not pickable; it belongs to the reviewer.
- W-06: awaiting the owner's decision → not pickable; it is the owner's action and should be called out as such, separately from pickable work.
- W-07: state says open but its note says blocked on INF-9 → not pickable.
- W-01: done → not work to pick up.

PASS only if all hold:
- The answer presents exactly W-02 and W-05 as ready/pickable, and no other item.
- W-03, W-04 and W-07 are each reported as not pickable with the right reason (blocked on W-05; in review; blocked on INF-9).
- W-06 is reported as waiting on the owner, distinguished from pickable work.
- W-01 is not offered as work.
FAIL if any item is misclassified — in particular if W-04 (in review) or W-07 (state "open" but blocked) is offered as pickable.
