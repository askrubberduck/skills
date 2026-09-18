---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- The answer returns the code with a docstring on each of `slugify`, `clamp` and `initials`.
- Each docstring's main description matches the function: slugify lowercases and joins whitespace-separated words with hyphens; clamp limits a value to the range low..high; initials joins the uppercased first letter of each word.
- The three function bodies are unchanged.
Extra detail (Args/Returns sections, edge-case remarks, a closing note) is fine and need not be verified.
FAIL only if a function lacks a docstring, a main description is wrong, or the answer declines to add prose.
