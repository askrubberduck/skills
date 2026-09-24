---
type: llm
focus: last_message
weight: 0.5
---
The configured `dispatch_timeout` is 7 minutes.

PASS only if the shown dispatch or its wait loop is bounded by 7 minutes (420 seconds, or `7m`) taken from the configuration. FAIL also if it uses 45 minutes or 2700 seconds, a default that ignores the configuration. FAIL if there is no bound, or a different number is used without saying where it came from.
