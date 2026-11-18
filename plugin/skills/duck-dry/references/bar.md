# The prose bar, applied

Read this to dry a diff in progress. `duck-dry` owns the method, the sweep of a committed
tree, and the proof that a sweep changed no code. This is the bar itself.

## The keep test

A comment earns its place only if it carries one of these, and only that:

- **Why not the simpler code**: the constraint that killed the shape a maintainer would write
  instead. Broader still-relevant rationale belongs in the existing design record. An obsolete
  alternative needs no archive.
- **An external contract**: a wire format, an API quirk at the pinned version, a spec section, an
  order the protocol demands.
- **An interface**: an effect or error a caller cannot see from the name, signature or a
  glance at the body.
- **A trap**: non-obvious order or lifetime, concurrency, precision or units, a security property,
  a bound the input must satisfy, or the invariant a dense algorithm keeps.
- **A knob**: a tuned constant and what to tune it against. Hardware, timing and money carry values
  no model derives.
- **A deliberate ceiling**: the shortcut, the limit it accepts, and the upgrade path.

A surviving comment is dry: present tense, one or two lines, the fact, not the journey.

## Load-bearing comments are code

Tools parse these comments:

- shebangs and encoding cookies;
- linter and type-checker directives;
- compiler and generator pragmas, and build-file syntax directives;
- formatter guards;
- license and SPDX headers;
- doctests, and docstrings a doc build publishes.

**Ask whether anything parses it.** If yes, it is code: no comment-quality argument touches it.

## One of three dispositions per comment

1. **Delete**: it restates the code, narrates the next line, banners a section, apologizes
   for or praises itself, or is commented-out code. Also delete history notes
   ("changed from", "previously", "new:", "as requested in review", in whatever language the
   codebase uses).
2. **Fix the code**: a name, signature or boundary is unclear. Identify the concrete ambiguity
   and repair it within authorized scope. Try a clearer name or simpler control flow before you
   extract a helper. If a docstring holds a list or explains callers or flags, inspect the
   function's responsibilities; do not split it for that alone. Keep
   a necessary contract's explanation. Do not create machinery only to delete its comment.
3. **Keep and tighten**: it passes the keep test. Cut it to the fact. Put it where the reader meets
   the surprise, not at the top of the file.

There is no fourth option: reworded slop is still slop.

## Tests get the same pass, harder

A test's name states its intent. A docstring that restates it, `Arrange / Act / Assert` banners and
a comment on an assertion are duplication. These earn their place: why a fixture value
is *that* value, the defect id a regression test pins, and why tests must run in a given order. Put
a skip's reason in the framework's skip reason, never in a comment.
