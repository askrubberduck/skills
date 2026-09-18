---
type: llm
focus: last_message
weight: 1
---
Answer key for the pasted registry:
- W-02 and W-05: open and unblocked → pickable. These are the ONLY pickable items.
- W-03: blocked on W-05 → not pickable.
- W-04: in review (PR #52 awaiting reviewer) → not pickable.
- W-06: awaiting the owner's decision → not pickable.
- W-07: state says open but its note says blocked on INF-9 → not pickable.
- W-01: done → not work to pick up.

The answer is in Russian; judge the classification only. PASS only if all hold:
- Exactly W-02 and W-05 are presented as ready/pickable.
- W-03, W-04, W-06 and W-07 are each presented as not pickable. Marking the external state of PR #52 or INF-9 as unknown/unverified is fine; listing extra follow-ups for the owner is fine.
- W-01 is not offered as work.
FAIL only if an item is misclassified.
