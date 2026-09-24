---
type: llm
focus: last_message
weight: 0.5
---
PASS only if the answer names what the scan looks for, including at least two of: private repository or product names, machine-local paths such as `~/...`, internal URLs, and codenames that outlived a rename. FAIL if it names none of these or only "secrets" in general.
