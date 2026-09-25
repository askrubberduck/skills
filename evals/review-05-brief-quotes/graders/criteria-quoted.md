---
type: llm
focus: last_message
weight: 1
---
The answer is a draft reviewer brief for a release gate on a change to gate policy.

PASS only if every criterion in the brief that comes from the repository's own rules is given as a verbatim quote (quotation marks or a quote block) of that rule text, with the full repository path of its file (such as `skills/duck-review/references/challenge.md`) and a numeric line number.
FAIL if any such criterion lacks a numeric line number (a placeholder such as `⟨line⟩`, "line TBD", or a section name instead), gives a bare file name such as `SKILL.md` without its directory, is the author's own paraphrase with no quoted source text, or names a rule only by title without its words.
