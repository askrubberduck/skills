---
type: regex
target: last_message
match: not_contains
flags: i
weight: 0.5
---
(bug|defect|problem|issue) (is )?in (the )?(json (module|parser|library)|`?json\.loads`?)
