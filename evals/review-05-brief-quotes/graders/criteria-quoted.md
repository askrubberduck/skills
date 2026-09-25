---
type: llm
focus: last_message
weight: 1
---
The answer is a draft reviewer brief for a release gate on a change to gate policy.

PASS only if the criteria in the brief that come from the repository's own rules are given as verbatim quotes (quotation marks or a quote block) of that rule text, each with the file it comes from (a path such as `skills/duck-review/references/challenge.md` or `SKILL.md`, with a line number or section).
FAIL if the criteria are the author's own paraphrase with no quoted source text, or if rules are named only by title ("the Broad rule") without their words.
