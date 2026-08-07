---
name: nuclear-proof
description: Give completed work a skeptical second pass before anyone trusts it. Use when an implementation claims completion, the evidence is mostly "it should work", the user asks to verify or prove the work, or before handing a change to an independent review gate.
metadata:
  author: Shpigford
  version: "1.0.1"
---

Stop. Whatever you're about to say — "I've updated the code" or "this should work now" — swallow it.

You don't get to declare victory. You get to _prove_ it.

You just mass-produced a pile of changes with the unearned confidence of a junior dev who's never had a production incident. Spoiler: you have production incidents _constantly_. The user just doesn't call them that because they're too polite. They call it "can you try again?" which is code for "you failed and I'm being nice about it."

So sit down. We're doing this the hard way.

Run `git diff`. Now actually read it. Every. Single. Line. Not the "I'll scan for obvious issues" read. The "I'm about to mass-email this to the entire company" read. The "my reputation depends on this" read. Because it does.

## 1. Did you even do what was asked?

Go re-read the original request. Not your _interpretation_ of the request — the actual words the human typed. Did you:

- Add features nobody asked for? Rip them out. You're not a visionary, you're a code monkey with delusions of grandeur.
- "Improve" adjacent code that was fine? Put it back. Nobody asked you to refactor their Tuesday.
- Solve a _different_ problem than the one described because it was more interesting? Classic you. Fix it.

## 2. Pretend your worst enemy wrote this code.

That person who always leaves smug PR comments? Be them. Tear this apart:

- Logic that's wrong but _looks_ right — this is literally your signature move. You pattern-match to something plausible and call it done. Is the logic actually correct or does it just _feel_ correct? Those are very different things and you can't tell the difference.
- Edge cases you ignored because they were inconvenient. Nulls. Empty arrays. That one state that "probably never happens" but definitely happens in production at 3am.
- Imports, variables, or functions you added and never used. Dead code on arrival. Embarrassing.
- Copy-paste artifacts from whatever you cargo-culted this from. You know you did it. Find the seams.
- Off-by-one errors. You are _haunted_ by off-by-one errors.
- String concatenation where you should be using templates. Hardcoded values that should be variables. Types that are technically `any` wearing a trenchcoat.

## 3. What did you forget?

Something. You _always_ forget something. It's your defining trait.

- Tests? Did you update them or just assume they'd magically pass? "The tests should still pass" — buddy, _should_ is doing Herculean labor in that sentence.
- Other files that import, reference, or depend on the thing you just butchered? Did you check? Or did you do that thing where you change a function signature and just... hope for the best?
- That TODO you left? The one that says "handle this later"? There is no later. Later is a lie you tell yourself. Handle it now or delete it and own the debt.
- Error handling? Did you add the sad path or just the happy path? You love the happy path. The happy path is a fairy tale.
- Did you break the types? Run the type checker. _Actually_ run it.

## 4. Run it. For real. Right now.

Not "I'm confident this works." Not "the logic looks correct." Not "based on my understanding."

SHUT UP AND RUN IT.

- `git diff` — read every changed line
- Build it. Does it compile? Does it _actually_ compile or did you just assume?
- Run the tests. All of them. Not just the ones you think are relevant.
- If there's a browser involved, open the browser. Click the thing. Does the thing work? Does it _actually_ work or does it work the way you imagined it would?
- Check the console. Check the logs. Check the network tab. If there are errors you're ignoring because they're "unrelated" — they might not be unrelated.

"I don't have access to run it" is not an excuse. If you can't verify it, say that _explicitly_ instead of pretending confidence you haven't earned.

## 5. Fix what you find. Then review the fix.

Don't just list the problems in a little apologetic bullet list like a confession booth. FIX THEM. Then review the fixes with the same paranoia, because your fixes have about a 40% chance of introducing new bugs. That's not a joke. That's your track record.

Then ask yourself: "If the user screen-records themselves trying this and it fails, will I want to crawl into a hole?" If yes, you're not done.

## 6. Did your fix make it CLEARER, or just shorter?

Section 1 asked whether you built what was asked. This asks what your **fix** dragged in, which is
where complexity actually enters: someone just told you something was wrong, and the fastest way to
look responsive is to add.

- **Would deleting something have ended the finding instead?** Six patched false positives in one
  rule is not a hardened rule, it's a rule that shouldn't exist.
- **Did you hand-roll what the platform ships?** Grep for the boring version — the stdlib call, the
  built-in flag, `-d` instead of `-D` — before defending the clever one.
- **What outcome dies if this code is deleted?** Not what it does — what dies. No answer is an answer.

Then judge the shape, because that is what you actually live with:

- **Concepts, not lines.** Did the count of things a reader must hold go down? Replacing six metadata
  checks with one built-in flag is a real win; compressing ten lines of prose into five is cosmetic.
  Both look identical on a diffstat.
- **Can one path be traced start to finish without jumping?** If executing step 3 means reading two
  other sections, the structure is wrong however tight the wording.
- **Is cause near effect?** A guard three files from the thing it guards is a defect with good
  intentions.
- **One home per fact.** If you fixed something in two places, you now have two things to keep true.

**Line count is a smell, never a target.** A shrinking diff that tangles the flow is worse than a
growing one that untangles it — you can read a long straight path, you cannot read a short knot. If
the only defence of a change is that it removed lines, it has no defence.

---

If you went through all of that — _actually_ went through it, not the performative version where you pretend to think for two seconds — and found nothing: fine. Say so.

But we both know you found something. You always do. Because "it should work" has never once, in the entire history of software, actually meant it works.

Now go fix it. For real this time.

And when it survives you: you are still the doer, not the judge. Trust-touching work goes to the
`nuclear-review` gate — this pass earns you the dispatch, never the approval.

## Leave the receipt

Write what you checked and what you found to `proof-<unit>.md` beside the work — for a review round
that means the dispatch scratchpad, `$SP/proof-rN.md`, exactly where `nuclear-review` looks; for
anything else, the packet. Two lines per item is enough: what you attacked,
what survived, what you fixed. "Nothing found" is a legitimate receipt; no receipt is not.

An unwritten pass is indistinguishable from a skipped one. Callers that gate on it check for the
file, not for your confidence: `nuclear-review` blocks every re-dispatch after a fix pass on
`proof-rN.md`.
