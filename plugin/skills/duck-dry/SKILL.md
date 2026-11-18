---
name: duck-dry
description: Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive. Use for redundant comments, generated code narration, or commit and PR prose that repeats the diff; before committing or reviewing generated code. Preserve parsed directives. Not ordinary prose editing.
---

# Duck Dry

Remove commentary that repeats the code or tells an obsolete story. Keep the facts a maintainer
cannot recover from the code: constraints, external contracts, traps and calibration.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
By default, dry the current task's diff with staged changes. Sweep committed files or a tree only
if named. Report-only means no edits. Local cleanup does not
authorize commits or publication.

## Read before deleting

Read the code each comment describes, and apply [the prose bar](references/bar.md). Check if tools
consume the text: directives, licenses, doctests and published docstrings are not disposable. Fix
generated prose at its source, or leave it if the generator is outside scope.

Resolve a code-commentary contradiction against the actual contract. Never
silently delete the only evidence of a defect. Do not change behavior during a prose sweep. Report
a necessary code repair unless authorized. If you make a repair, report it separately.

## Delete, consolidate or preserve

Delete what the bar marks. Do not create a bug record, design document or backlog item
only to archive deleted prose. If a fact still affects a contract, decision or future action, keep
it where its reader needs it:

- A local trap or constraint: beside the affected code, stated once.
- Caller-facing usage: in existing public documentation, if the name, signature and an
  interface comment cannot carry it.
- A still-relevant design decision or authorized deferral: in the existing project record. Link
  to it; do not copy it. Preserve unresolved owner decisions.

Keep one authoritative, useful explanation of each rule; remove the repeats. A sentence must
keep its meaning after you remove an internal ID. Do not add an abstraction only to make its comment
unnecessary. First, establish the ambiguity.

Commit messages and PR prose carry intent, constraints and verification in the repository's
required format, not the editing process or each changed line.

## Verify the actual edit

For a comment-only sweep, compare both revisions with a language-aware parser or tokenizer.
Non-comment tokens must match, with significant whitespace kept. Never strip comments with a regex
that can consume strings or URLs. Parsed directives need their own preservation check. Docstring or
string changes are not token-identical: state what changed and run the checks that consume them.

Run affected lint, type, test or documentation checks and repository-required gates. If
deletion can change alignment, check formatting. Regrouped declarations, renames, changed assertion
messages and behavior changes are code changes. Keep them out of a comment-only sweep, and do not
make them outside authorized scope. If a necessary check cannot run, report the gap; never
claim equivalence. An authorized code change may dry the prose it adds.

Report material deletions, retained constraints and actual verification. A standalone cleanup
needs no deletion quota or new receipt. Stop when the scoped prose meets the keep test and relevant
checks pass. New comments must meet the same test. Remove intent notes written before the code once
the code says it.
