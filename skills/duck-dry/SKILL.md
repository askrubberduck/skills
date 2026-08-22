---
name: duck-dry
description: Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive. Use when generated code or tests carry narration, storytelling, or change history in comments, when a comment restates the line under it, when a commit message or PR description narrates instead of carrying what the diff cannot, before committing or reviewing generated code, or the user asks to dry, prune, or de-slop comments or commit prose.
---

# Dry the Comments

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

## Tests get the same pass, harder

Generated tests are where narration collects. A test's name states its intent, so a docstring
restating the name and an `Arrange / Act / Assert` banner set are pure duplication, and a comment
explaining what an assertion asserts is the assertion. What earns its place: why a fixture value
is *that* value — the boundary it sits on — the defect id a regression test pins, and why tests
must run in a given order. A skip's why goes in the skip reason the framework already prints,
never in a comment beside it.

## Then prove nothing broke

A comment sweep is not free. Run the project's gates — lint, type check, the whole suite, and the
doc build if it publishes from docstrings. Read the diff: every changed line is a comment line
unless a disposition 2 code fix was the point and is stated. A deleted directive surfaces as a new
lint or type error, never as a worse comment, so an unrun gate after a sweep is an unverified claim
like any other. The diff plus the green gates is the receipt; there is no artifact to write.

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
