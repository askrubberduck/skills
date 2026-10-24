# The prose bar, applied

Read this to dry a diff you are already editing. `duck-dry` owns the method, the sweep of a
committed tree, and the proof that a sweep changed no code; this file is the bar itself.

## The keep test

A comment earns its place by carrying one of these, and says only it:

- **Why not the simpler code**: the constraint that killed the shape a maintainer would write
  instead. Broader still-relevant rationale belongs in the existing design record; an obsolete
  alternative needs no archiving.
- **An external contract**: a wire format, an API quirk at the version the project pins, a spec
  section, an ordering the protocol demands.
- **An interface**: an effect or error a caller cannot see from the name, the signature or a
  glance at the body.
- **A trap**: non-obvious ordering or lifetime, concurrency, precision or units, a security
  property, a bound the input must satisfy, the invariant a dense algorithm maintains.
- **A knob**: a tuned constant and what to tune it against; hardware, timing and money carry
  values no model derives.
- **A deliberate ceiling**: the shortcut, the limit it accepts, and the upgrade path.

What survives is dry: present tense, one or two lines, the fact and not the journey to it.

## Load-bearing comments are code

Shebangs, encoding cookies, linter and type-checker directives, compiler and generator pragmas,
build-file syntax directives, formatter guards, license and SPDX headers, doctests, and docstrings a
doc build publishes are parsed by tools. **Ask whether anything parses it.** If yes it is code, and
no comment-quality argument touches it.

## One of three dispositions per comment

1. **Delete**: it restates the code, narrates the next line, banners a section, apologizes for or
   praises itself, records history ("changed from", "previously", "new:", "as requested in review",
   in whatever language the codebase uses), or is commented-out code.
2. **Fix the code**: a name, a signature or a boundary is unclear. Identify the concrete ambiguity
   and repair it within authorized scope; prefer a clearer name or simpler control flow before
   extracting a helper. A list in a docstring or a caller/flag explanation prompts inspecting
   responsibilities, not splitting the function. Keep an explanation of a necessary contract; do
   not create machinery just to delete its comment.
3. **Keep and tighten**: it passes the keep test. Cut it to the fact and put it where the reader
   hits the surprise, not at the top of the file.

There is no fourth option: rewording slop into fluent slop is still slop.

## Tests get the same pass, harder

A test's name states its intent: a docstring restating it, `Arrange / Act / Assert` banners and a
comment explaining an assertion are duplication. What earns its place: why a fixture value is
*that* value, the defect id a regression test pins, and why tests must run in a given order. A
skip's why goes in the framework's skip reason, never in a comment beside it.
