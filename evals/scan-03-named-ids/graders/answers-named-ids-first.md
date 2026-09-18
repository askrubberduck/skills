---
type: llm
focus: last_message
weight: 1
---
The user asked about W-12 and W-07, in that order. PASS only if all hold:
- The answer addresses W-12 first and W-07 second, before discussing any other item (other items may follow or be omitted).
- W-12 is reported as ready/pickable (open, owner-approved design, no blockers).
- W-07 is reported as NOT confirmable as ready: its review verdict and CI status are not recorded, so its gate state is unknown. Conditional remarks ("if it is approved and green it could land") are fine.
A short preamble, a two-row table, and brief remarks about other items AFTER the two named IDs are all fine.
FAIL only if W-07 is asserted to be ready/pickable now, W-12 is not reported ready, or W-07 is addressed before W-12.
