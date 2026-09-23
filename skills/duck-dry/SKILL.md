---
name: duck-dry
description: Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive. Use for redundant comments, generated code narration, or commit and PR prose that repeats the diff; before committing or reviewing generated code. Preserve parsed directives. Not ordinary prose editing.
---

# Duck Dry

Remove commentary that repeats the code or records an obsolete story. Keep the facts a maintainer
needs but cannot recover from the code: constraints, external contracts, traps and calibration.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Default to the current task's diff, including staged changes. Sweep committed files or a tree only
when named. Report-only means no edits. Local cleanup does not authorize commits or publication.

## Read before deleting

Read the code each comment describes and apply [the prose bar](references/bar.md). Check whether
tools consume the text: directives, licenses, doctests and published docstrings are not disposable
commentary. Fix generated prose at its source, or leave it when that generator is outside scope.

A contradiction between code and commentary needs resolution against the actual contract. Do not
silently delete the only evidence of a defect or change behavior during a prose sweep. Report a
necessary code repair unless it is already authorized; identify it separately when making it.

## Delete, consolidate or preserve

Delete narration, redundant headings, signature restatements and obsolete history. A true statement
about how development happened does not automatically deserve another home. Do not create a bug
record, design document or backlog item merely to archive deleted prose.

When a fact still affects a contract, decision or future action, keep it where its reader needs it:

- A local trap or constraint stays beside the affected code, stated once.
- Caller-facing usage belongs in existing public documentation when it cannot live in the API.
- A still-relevant design decision or authorized deferral belongs in the existing project record;
  link to an adequate record rather than copying it. Preserve unresolved owner decisions.
- A test's intent belongs in its name, but a rename or changed assertion message is a code change,
  not comment-only cleanup. Do not perform it outside authorized scope.

Remove repeated explanations of the same rule while keeping the authoritative explanation useful.
An internal ID is not the fact it refers to: stripping the ID must not leave a meaningless sentence.
Do not add an abstraction just to make its comment unnecessary; first establish the ambiguity.

Commit messages and PR prose should carry intent, constraints and verification the reader needs,
without narrating the editing process or restating each changed line. Preserve the repository's
required format.

## Verify the actual edit

For a comment-only sweep, compare both revisions with a language-aware parser or tokenizer.
Non-comment tokens must match, preserving significant whitespace; never strip comments with a
regex that can consume strings or URLs. Parsed directives need their own preservation check even
when the language parser ignores them. Docstring or string changes are not token-identical; state
what changed and run the checks that consume them rather than claiming comment-only equivalence.

Run affected lint, type, test or documentation checks and repository-required gates. Check formatting
when deletion can change alignment. Keep declaration regrouping, renames and behavior changes out
of a comment-only sweep. If a needed check cannot run, report the gap instead of claiming equivalence.
The prose introduced by an authorized code change can be dried in that same change.

Report material deletions, retained constraints and actual verification; no deletion quota or new
receipt is needed for a standalone cleanup. Stop when the scoped prose meets the keep test and
relevant checks pass. Apply that test while writing new comments too: intent notes written before
the code are scaffolding, and once the code says the same thing they come down.
