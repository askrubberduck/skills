---
name: duck-dry
description: Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive. Use when generated code or tests carry narration, storytelling, or change history in comments, when a comment restates the line under it, when a commit message or PR description narrates instead of carrying what the diff cannot, before committing or reviewing generated code, or the user asks to dry, prune, or de-slop comments or commit prose.
---

# Duck Dry

The compiler, the type checker, and the tests check the code. **Nothing checks a comment.** It is a
hand-maintained second home for a fact, and the next edit falsifies it in silence — so a comment
that repeats what the code already says is not documentation, it is duplication with a decay rate.
Default: delete. The bar to keep: one fact the code cannot carry, written for a reader who knows
the language.

Volume is not the target and neither is zero. A quota — "cut half the comments" — replaces
judgment with a number. The unit of work is one comment against the keep test.

## Target

The diff by default: `git diff`, `git diff --staged`, or `<base>..<candidate>`. Drying your own
uncommitted diff needs no ceremony — those comments were never anyone's baseline. A file or tree
already committed is swept only when named, and **that sweep is its own commit** — mixed into a
behavior change, a code fix rides in hidden among prose deletions where no reviewer will find it,
and a repo-wide pass churns blame across code nobody touched.

## The keep test

A comment earns its place by carrying one of these, and says only it:

- **Why not the simpler code** — the constraint that killed the shape a maintainer would write in
  its place. Line-level only: an alternative *design* goes to the design record, per the moved
  rule below.
- **An external contract** — a wire format, an API's documented quirk at the version the project
  pins, a spec section, an ordering the protocol demands.
- **A trap** — non-obvious ordering or lifetime, concurrency, precision or units, a security
  property, a bound the input must satisfy, the invariant a dense algorithm maintains.
- **A knob** — a tuned constant and what to tune it against. Hardware, timing, and money carry
  values no model derives.
- **A deliberate ceiling** — the shortcut, the limit it accepts, and the upgrade path.

What survives is dry: present tense, one or two lines, the fact and not the journey to it.

## Say it once

The largest single win in a swept file is rarely a bad comment — it is one good fact restated on
five declarations. State it where the reader first hits it and delete the other four; a fact with
five homes decays in four of them. Hunt for this deliberately, because every copy reads fine alone
and only the sweep ever sees them together.

## Load-bearing comments are code

Some comments are parsed by a tool, not read by a person: shebangs, encoding cookies, linter and
type-checker directives, compiler and generator pragmas, build-file syntax directives, formatter
guards, license and SPDX headers, doctests, and docstrings a doc build publishes. **Ask whether
anything parses it.** If yes it is code: deleting it changes behavior, breaks the build, or strips
a license, and no comment-quality argument touches it.

## One of three dispositions per comment

1. **Delete** — it restates the code, narrates the next line, banners a section, apologizes for or
   praises itself, records history ("changed from", "previously", "new:", "as requested in review"),
   or is commented-out code. Deleting is the whole fix.
2. **Fix the code** — the comment exists because a name, a signature, or a boundary is unclear.
   Rename, extract, invert the guard, split the function; the comment dies with the confusion it
   was covering. A docstring that needs a list to describe one function is a single-responsibility
   finding, and a comment mapping which caller passes which flag is a coupling finding. Never leave
   the comment as the fix for unclear code.
3. **Keep and tighten** — it passes the keep test. Cut it to the fact, drop the story, put it
   where the reader hits the surprise, not at the top of the file.

There is no fourth option. Rewording slop into fluent slop is still a second home for the line
below it.

## A comment that contradicts the code is a bug report

When the two disagree one of them is wrong, and which one is not yet known — a doc naming a helper
that no longer exists, a claim of sorted output over an unsorted return, a doc block left above the
wrong function by a rename. Resolve it against the code and fix whichever lost. Deleting the
comment quietly discards the only evidence that something is off, and a sweep surfaces these in
bulk because nothing else in the toolchain reads comments; route them out rather than swallowing
them in the deletion count.

## A true fact is moved, never dropped

- The war story of the bug — symptom, wrong hypothesis, what finally caught it — belongs in the
  bug's work-item record; in the code it is dead weight the next edit silently falsifies, and in
  the commit message it is storytelling. **Commit messages and PR descriptions carry the same bar
  as comments: only what the diff cannot** — intent, constraint, trap, receipt — never narration,
  process story, or a restated diff.
- The rejected *design* — the shape the change did not take, and why — belongs in the design
  record beside the work item.
- Usage a caller needs before reading the code belongs in the published docs.
- What a test is for belongs in its name.
- A deferral belongs in the project's registry, with the marker the repo already greps for.
- **One exception to "only what the diff cannot": a deletion nobody could search for.** When a
  commit removes a record — a backlog item under `duck-cut`, a registry entry — the removed text
  goes in the message. The diff carries it, but only to a reader who already knows it existed, and
  that is the one case where restating the diff buys retrievability instead of duplicating it.
- An id is not the fact it tagged. Strip `#NNN`, a ticket key, or an internal plan reference and
  the sentence around it often points at nothing — "the plan above names the four cases" now names
  none. Restate what the tag guarded in its own terms, or cut the sentence with it.

## Tests get the same pass, harder

Generated tests are where narration collects. A test's name states its intent, so a docstring
restating the name and an `Arrange / Act / Assert` banner set are pure duplication, and a comment
explaining what an assertion asserts is the assertion. What earns its place: why a fixture value
is *that* value — the boundary it sits on — the defect id a regression test pins, and why tests
must run in a given order. A skip's why goes in the skip reason the framework already prints,
never in a comment beside it.

## Then prove nothing broke

A comment sweep is not free. Run the project's gates — lint, type check, the whole suite, and the
doc build if it publishes from docstrings. A deleted directive surfaces as a new lint or type
error, never as a worse comment, so an unrun gate after a sweep is an unverified claim like any
other.

**Reading the diff is not the proof.** A sweep is the one diff a reviewer skims, so establish
comment-only mechanically: strip comments from both revisions and diff what is left, ignoring
whitespace. Every non-comment line must be byte-identical unless a code change was the point and is
stated — a disposition 2 fix, or a fact moved into a string the code already prints. Strip with
something that parses the language — its own AST printer, a tree-sitter comment query — never a
regex on `//` or `#`: it eats URLs and string contents, failing on the string case below. Run it
per file across the whole sweep; it is the only thing that catches a code edit riding among prose
deletions.

Three ways a comment edit silently becomes a code edit, each of which reads as pure deletion:

- **The formatter realigns.** A comment between aligned fields — in a struct, a composite literal,
  a `var`/`const` block, any run the formatter pads into columns — separates two alignment groups.
  Delete it and the formatter re-aligns every name around it. The strip-and-diff above cannot see
  this, because it ignores whitespace; run the formatter's own check as a second gate and put a
  blank line back where the comment was if it complains.
- **Declarations get merged.** Hoisting two constants into one block so they can share a comment is
  a refactor wearing a comment edit's clothes.
- **A string is not a comment.** Prose inside an assertion message, an error constructor, or a test
  name reads exactly like a comment in a diff and is code. Editing one — moving a skip's why into
  the skip reason, renaming a test to carry its intent — is a stated code change, never a silent
  one riding in the deletion count.

The diff, the mechanical check, and the green gates are the receipt; there is no artifact to write.

## While writing, not after

The cheapest pass is the one that never runs: the keep test applies before the comment is typed. No
per-function header blocks, no section banners, no changelog in the code, no tutorial voice ("we now
iterate over…"), no docstring restating the signature above it.

## Common mistakes

- Deleting the comment and keeping the code that needed one — the comment was the symptom.
- Cutting a directive, license header, or published docstring because it reads like noise.
- Editing comments in a generated file; the generator wins the next run. Fix the generator or leave
  it.
- Adding a comment because a reviewer asked for one, when the finding was that the code is unclear.
- Cutting a line that reads like an owner's decision or a policy. That is not the doer's to delete;
  ask.
- Reporting a comment count as the result. The result is what the code no longer needs explained.
- Reading a low deletion count as proof a file is done. A file whose survivors are all traps is
  done; a file nobody opened is not. Tell them apart by which comments were actually read.
