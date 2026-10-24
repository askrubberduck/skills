---
name: duck-dry
description: Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive. Use for redundant comments, generated code narration, or commit and PR prose that repeats the diff; before committing or reviewing generated code. Preserve parsed directives. Not ordinary prose editing.
---

# Duck Dry

Remove commentary that repeats the code or records an obsolete story. Keep the facts a maintainer
cannot recover from the code: constraints, external contracts, traps and calibration.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Default to the current task's diff, including staged changes; sweep committed files or a tree only
when named. Report-only means no edits. Local cleanup does not authorize commits or publication.

## Read before deleting

Read the code each comment describes and apply [the prose bar](references/bar.md). Check whether
tools consume the text: directives, licenses, doctests and published docstrings are not disposable.
Fix generated prose at its source, or leave it when the generator is outside scope.

Resolve a code/commentary contradiction against the actual contract. Never silently delete the
only evidence of a defect or change behavior during a prose sweep. Report a necessary code repair
unless already authorized; identify it separately when making it.

## Delete, consolidate or preserve

Delete what the bar marks for deletion; do not create a bug record, design document or backlog
item merely to archive deleted prose. A fact that still affects a contract, decision or future
action stays where its reader needs it:

- A local trap or constraint beside the affected code, stated once.
- Caller-facing usage in existing public documentation when the name, signature and an interface
  comment cannot carry it.
- A still-relevant design decision or authorized deferral in the existing project record; link to
  it rather than copying it. Preserve unresolved owner decisions.

Remove repeated explanations of one rule, keeping the authoritative one useful. Stripping an
internal ID must not leave a meaningless sentence. Do not add an abstraction just to make its
comment unnecessary; first establish the ambiguity.

Commit messages and PR prose carry intent, constraints and verification, not the editing process
or each changed line, in the repository's required format.

## Verify the actual edit

For a comment-only sweep, compare both revisions with a language-aware parser or tokenizer:
non-comment tokens must match, significant whitespace preserved. Never strip comments with a regex
that can consume strings or URLs. Parsed directives need their own preservation check. Docstring or
string changes are not token-identical: state what changed and run the checks that consume them.

Run affected lint, type, test or documentation checks and repository-required gates; check
formatting when deletion can change alignment. Declaration regrouping, renames, changed assertion
messages and behavior changes are code changes: keep them out of a comment-only sweep, and do not
perform them outside authorized scope. If a needed check cannot run, report the gap instead of
claiming equivalence. Prose introduced by an authorized code change can be dried in that change.

Report material deletions, retained constraints and actual verification; a standalone cleanup needs
no deletion quota or new receipt. Stop when the scoped prose meets the keep test and relevant
checks pass. New comments meet the same test: intent notes written before the code come down once
the code says the same thing.
