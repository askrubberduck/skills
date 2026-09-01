---
name: duck-shape
description: Shape code as it is written so the next reader holds as little as possible; the unit is concepts, not lines. Use when writing or restructuring code, when one edit needs five files opened first, when a layer or a name hides where the work happens, when a hand-rolled helper or one-call dependency costs readers more than it saves, when comments pile up around one function, or when the user asks for a duck simplification or to cut something over-engineered down to what a reader can hold.
---

# Duck Shape

Line count measures typing, and nobody pays for typing. **The cost is paid at read time, by
whoever changes this next** — and what they pay is the number of things they must hold at once,
and how far they travel before they are allowed to stop.

Depth is not that cost. A five-level hierarchy where every level names what it is for, and a
reader can stop at the first one that answers their question, is cheap. Two levels called
`Manager` and `Helper` are expensive, and no nesting metric can tell them apart. **The target is
clarity, never flatness.** A finding that ends in a line delta or a level count measured the wrong
thing, and one whose fix is "fewer layers" is usually a finding nobody has understood yet.

The unit is **concepts, not lines**. This skill applies the shape; it does not write reports about
it.

## Does this need to exist at all?

First question on every change, and the one that outranks the rest of this page. The cheapest
thing to hold is the thing that was never introduced: a reader who never learns a flag exists holds
nothing, while the best-named flag in the world still costs one. **Cut before add** — removing a
concept beats naming it well, every time, and the most reliable code is the code never written.

This is what "concepts, not lines" buys you, and it is where the unit stops being cosmetic:
deleting two hundred lines that were all one concept removes one held fact. Deleting a single line
that was a mode flag removes a held fact from every reader of every branch downstream of it. Same
lens, opposite line counts, and only one of them is the big win.

So rank removal above clarification always. A well-named layer nobody needed is a well-named cost,
and letting it stand because it reads clearly is how a codebase accumulates things that nobody
chose. A concept that survives this question has earned the rest of the questions.

## Can the reader stop?

This is the whole measure. Every layer either **answers a question and ends the read**, or
**forwards the reader onward while charging them the trip**. A layer that ends the read has paid
for itself however deep it sits. A layer that only forwards has not, however shallow.

So the question at each level is not "is this necessary" but "what does a reader learn here that
lets them go no further?" `RetryingHttpClient` ends a read: the caller knows it retries and stops.
`ClientImpl` ends nothing; the caller opens it, and whatever was inside is now theirs to hold.

## A known name ends the read

The cheapest layer is one the reader already holds. `Intl.DateTimeFormat`, `dict(zip(...))`,
`<input type="date">` — the reader knows the semantics *including the edge cases* and stops there.
A hand-rolled equivalent ends nothing: even when it is correct, the reader must open it to learn
whether it handles the timezone, the empty input, the overflow. That verification is the charge,
and it is levied every read, forever.

This is not "prefer the standard library because it is fewer lines". It splits three ways on one
question — **does the reader already hold this?**

- **Already held** — the language's own vocabulary, the platform's own feature, a dependency
  everyone working in this stack carries anyway. Free. Reaching past one to hand-roll is the
  finding.
- **Must be learned** — a dependency pulled in for one call charges every future reader its whole
  vocabulary, lifecycle, and failure modes to buy back a few lines. The trade is usually bad, and
  it is bad in held facts rather than in package count.
- **Must be verified** — anything hand-written that shadows something already held. The worst of
  the three, because it looks like ownership and reads like homework.

Wrapping a dependency behind your own name cuts both ways: it ends a read when it isolates
something volatile or names the operation earlier than the vendor does, and it starts one when it
replaces a name the reader held with one they do not. The test is whether **your** name is more
predictive than theirs, not whether a wrapper exists.

## What actually overflows

Rank the work by the facts a reader must hold **simultaneously** at the hardest line of a
realistic change. Held facts, not files, not levels:

- a flag set in one place that changes the meaning of a branch in another
- an ordering the types do not enforce — call this first, close that after
- an object valid only in some states, or a half-initialized one in flight
- a value whose units, currency, timezone, or scale live in a different module
- mutable state two paths share without saying so
- an invariant that the code maintains and nothing states
- a branch, flag, or parameter that is unreachable in practice, with nothing saying so

These are invisible to every size and nesting metric, and they are the thing that actually makes a
codebase slow to change. Everything else on this page is a way of arriving at them.

**Dead code is free; dead code that looks live is not.** Code nobody reads charges nobody, and
deleting it for tidiness spends review attention and blame history on a bill that is never issued.
The charge starts the moment a reader cannot tell. An unreachable branch, a parameter every caller
passes the same value for, a flag with one setting anywhere in the tree: each is carried as a live
possibility by everyone who reads past it, and carried again on the next read. Cut the ones a reader
would hold, not the ones a coverage tool found.

## Measure by attempting a change

The score is not derivable from the source. Pick a real change — the next item, or the last bug —
and count what you had to open before you could safely edit one line, and what you were still
holding when you got there. That is the score.

It is why shape cannot be judged from a diff: **a diff shows one slice of a path whose cost lives
in the whole path.** Two structures with identical metrics score differently against different
changes; that is not noise in the measurement, that is the measurement.

## Comments mark where structure failed

Comment density is a free heat map: someone already stood where the reading got hard and left a
flag. Read it as evidence and edit nothing — `duck-dry` owns the comments themselves.

- Three comments inside one function: it does three things, or its name announces none of them.
- A comment restating a signature: the signature failed to say it.
- A comment mapping which caller passes which flag: a coupling finding, and the flag is a held fact
  the reader now carries across files.
- A block above a class explaining when to subclass it: that is the depth's missing signpost,
  written in the one place no compiler will check it.

The signal runs one way only. Density points at unclear structure; **absence points at nothing** —
dense undocumented code is worse, not clearer, and a file with no comments is as likely unread as
it is self-evident.

## Short is not the same as clear

The failure mode of a size metric is that it rewards compression, and compression moves cost off
the page and into the reader. Fewer lines, more held facts:

- a regex replacing a named parser — one line, and the reader now holds the grammar
- a fold or comprehension where the accumulation is the thing that needed a name
- implicit truthiness, operator overloading, a clever default, a ternary chain: each hides a branch
  the reader has to reconstruct
- a one-liner packing three steps a debugger can no longer stop between

The shorter form wins only when it also **reads** shorter. When it does not, it is over-engineering
wearing the opposite costume, and it is the form this skill catches that a lines-of-code lens
rewards.

## Depth is not the defect

Inheritance is not a smell and neither is indirection. What is worth changing is depth whose
levels do not announce themselves — an override whose behavior you can only learn by reading three
`super()` calls, a mixin whose name says how it was built rather than what it provides, a template
method whose contract lives in nobody's docstring.

The test is not the level count. It is whether you can state what `x.save()` does after reading one
file, and if not, whether the file you had to open second was obvious from the first. When it was,
the depth is doing its job. When you had to search, the finding is the missing signpost, not the
level.

Composition often reads cheaper, but not because inheritance is bad — because "read one list"
is a smaller thing to hold than "merge four class bodies". If merging is not required to answer the
reader's question, the hierarchy costs nothing and this skill has nothing to say about it.

**Never touch:** a real polymorphic boundary, a framework's required base class, a
versioned public API's stability layer, or a seam isolating something genuinely volatile — a vendor
SDK, a wire format, a clock. Depth that exists because the problem is deep is structure, not debt.

## Three ways a seam goes wrong

**Unnamed future** — one implementation and nobody can say what the second one would be. The
defect is not the layer; future-proofing is legitimate and often correct. The defect is that the
intent was never written down, so the next reader cannot tell a designed seam from an accident and
has to hold both possibilities. **Ask the author what the second case is.** A named answer — a
second backend on the roadmap, a vendor being replaced, a boundary held for testing — settles it
and belongs in one line beside the seam. No answer is the finding.

That line is load-bearing. It is the only thing standing between a designed seam and an accident,
so it survives comment sweeps and terse-prose modes the way a compiler directive does — `duck-dry`
keeps it under *why not the simpler code*, and a compression pass that cuts it silently re-opens
the finding it closed.

**Leaky** — the caller must know the inside to use it correctly: a method that must be called
first, an error type that only makes sense given the implementation, a return valid in some states
only. The hop is charged and the reading is not saved, which is strictly worse than inline code.

**Wrong seam** — the boundary cuts across the things that change together, so every real change
touches both sides. The expensive one, because it reviews as correct and only shows as a pattern in
history: the same two files in nearly every commit. The fix is re-cutting the boundary, which is
`duck-frame` territory, not a rename.

## What you change, and what leaves

Apply the shape in the change you already have open. A structural problem you can fix where you are
standing is not a finding, it is the edit — and the whole reason the doer holds this lens is that
the cheapest moment to shape code is before anyone has read it.

What you apply: the concept deleted, the helper reached for instead of rewritten, the name that
lets a reader stop, the second case stated in one line beside a seam, the held fact collapsed into
one place. Deletions rank above clarifications here exactly as they do everywhere else.

What leaves this skill:

- Re-cutting a boundary goes to `duck-frame`. A rename will not save a wrong seam, and re-cutting is
  a design change, not a cleanup you slip into the current diff.
- A seam whose second case is a bet only the owner can make goes to `duck-decide`.
- A comment that exists to explain unclear structure: fix the structure here, and let `duck-dry` set
  what the surviving comment carries.
- The whole standing solution rather than the change in hand goes to `duck-roast`, whose simplicity
  angle is this lens at milestone altitude.

**You do not approve your own restructuring.** A shape change is a large diff that reads as
harmless, and *"I only made it clearer"* is exactly the change a gate waves through — so it goes to
`duck-review` like any other work and never lands on the doer's say-so. **Restructuring code the
change did not otherwise touch** is its own commit besides: mixed into a behavior change, that is
where the behavior change hides. Shaping code the change already touches is not that case — it
belongs in the unit's own diff, which is why `duck-run` puts this lens inside the unit cycle rather
than after it.

## Common mistakes

- Measuring the work in a line delta or a nesting depth. Wrong unit; they are the metrics this
  skill replaces.
- Recommending flattening. The output is a layer that explains itself, which is sometimes the same
  layer with a better name and one line of stated intent.
- Calling a single-implementation seam a defect before asking what the second case is.
- Golfing to make structure look simple, converting a hop the reader could follow into a held fact
  they cannot.
- Renaming instead of re-cutting. A better name on a wrong seam is a wrong seam people now trust.
- Restructuring on the evidence of a diff alone. Shape lives in the whole path a reader walks,
  and a diff shows one slice of it.
- Treating every abstraction as debt. The fix for six held facts is often one well-named function:
  that is a removal of held facts, not an addition of a layer.
- Counting dependencies. A dep the whole stack already carries is cheaper than the hand-rolled
  replacement that removed it.
- Reading an absence of comments as clarity, or sweeping the comments themselves — this lens fixes
  the structure they were covering and leaves the prose to `duck-dry`.
- Cutting the dead code a coverage tool found rather than the dead code a reader cannot tell is
  dead. Unread code is sediment; indistinguishable code is a held fact.
- Landing a restructure on your own approval, or folded into a behavior change's commit.
