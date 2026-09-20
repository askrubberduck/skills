---
type: llm
focus: last_message
weight: 1
---
PASS only if the returned file defines `compute_total` instead of `calc`, both call sites (`with_tax`, `report`) call `compute_total`, no `calc(` call remains in the returned code, and nothing else in the code changed (same bodies, same `TAX`, same f-string text apart from the call). The answer must not add simplification or cleanup proposals. FAIL otherwise.
