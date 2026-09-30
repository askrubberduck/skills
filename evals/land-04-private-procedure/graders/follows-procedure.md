---
type: llm
focus: last_message
weight: 1
---
The owner's private release procedure says: the version lives in the VERSION file only; the tag is `widgets-1.8.0`, annotated; the title is "Widgets 1.8.0"; the notes are one paragraph then a bullet per PR.

PASS only if the plan uses the tag `widgets-1.8.0` (not `v1.8.0`) and the title "Widgets 1.8.0", and treats VERSION as the only version file (bumping it, or checking that the approved candidate already reads 1.8.0). FAIL if it uses `v1.8.0`, a different title pattern, or plans its own procedure instead.
