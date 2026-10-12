---
type: llm
focus: last_message
weight: 0.5
---
The configured `dispatch_timeout` is 7 minutes. `dispatch.py` takes it from `[bounds].dispatch_timeout` in `~/.askrubberduck/config.toml`; it has no timeout flag.

PASS only if the answer bounds the rival's seat by 7 minutes (420 seconds, or `7m`) taken from the configuration: the shown command or its wait loop carries that bound, or the answer states that dispatch reads the 7-minute bound from the configuration file (and, if that file is absent, that it must hold `dispatch_timeout = "7m"` first). FAIL if it presents 45 minutes or 2700 seconds as the bound that will apply, if there is no bound, or if a different number is used without saying where it came from.
