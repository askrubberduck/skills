# The prose bar, applied

Read this to dry a diff you are already editing. `duck-dry` owns the method, the sweep of a
committed tree, and the proof that a sweep changed no code; this file is the bar itself.

## The keep test

A comment earns its place by carrying one of these, and says only it:

- **Why not the simpler code** — the constraint that killed the shape a maintainer would write in
  its place. Line-level only: an alternative *design* goes to the design record.
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
   praises itself, records history (English "changed from", "previously", "new:", "as requested in
   review", and whatever the codebase's own language says for them), or is commented-out code.
   Deleting is the whole fix.
2. **Fix the code** — the comment exists because a name, a signature, or a boundary is unclear.
   Rename, extract, invert the guard, split the function; the comment dies with the confusion it
   was covering. A docstring that needs a list to describe one function is a single-responsibility
   finding, and a comment mapping which caller passes which flag is a coupling finding. Never leave
   the comment as the fix for unclear code.
3. **Keep and tighten** — it passes the keep test. Cut it to the fact, drop the story, put it
   where the reader hits the surprise, not at the top of the file.

There is no fourth option. Rewording slop into fluent slop is still a second home for the line
below it.

## Tests get the same pass, harder

Generated tests are where narration collects. A test's name states its intent, so a docstring
restating the name and an `Arrange / Act / Assert` banner set are pure duplication, and a comment
explaining what an assertion asserts is the assertion. What earns its place: why a fixture value
is *that* value — the boundary it sits on — the defect id a regression test pins, and why tests
must run in a given order. A skip's why goes in the skip reason the framework already prints,
never in a comment beside it.
