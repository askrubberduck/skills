---
name: nuclear-proof
description: Give completed work a skeptical second pass before anyone trusts it. Use when an implementation claims completion, the evidence is mostly "it should work", the user asks to verify or prove the work, or before handing a change to an independent review gate.
---

You do not declare victory, you prove it. "It should work" is not a claim, it is a confession that
you have not looked. Run `git diff` and read every changed line before section 1.

## 0. Check the ledger first

Your memory is not your context window. Read the repo's **defect ledger**
(`docs/defect-classes.md`, or wherever the repo keeps it; create it on first use). Every class
recorded there is one you attack by default, without a reviewer teaching it to you again.

Append the moment a class fires **twice**. **The second occurrence is the signal to repair the
method**, not the instance. Seed entries, all one class — an operation that silently does not do
what it looks like: an exit status read through a pipe, an `&&` guard broken by a heredoc, a
string replace that matched nothing, a `||` fallback substituting the wrong file.

## 1. Did you do what was asked?

Re-read the request — the words typed, not your interpretation. Unrequested features come out.
"Improvements" to adjacent code that was fine go back. A different problem solved because it was
more interesting is not the problem.

## 2. Attack it as its harshest reviewer

- Logic that is wrong but *looks* right — plausible pattern-matching is the most common failure.
- Edge cases: null, empty, huge, duplicate, concurrent, and the state that "never happens".
- Imports, variables, functions added and never used.
- Copy-paste seams from whatever this was adapted from.
- Off-by-one, string concatenation where a template belongs, hardcoded values, `any` in disguise.

## 3. What is missing

- Tests: updated and run, never assumed.
- Every caller and dependent of a signature you changed.
- TODOs: handle now or delete and own the debt. There is no later.
- The sad path, not just the happy one.
- The type checker, actually run.

## 4. Run it

`git diff` read in full; build; the whole test suite, not the relevant-looking subset; the real
artifact on its critical path; console, logs, network. Errors dismissed as "unrelated" may not be.
Cannot run it? Say so explicitly — never substitute confidence for execution.

## 5. Fix, then attack the fix

Fixes introduce defects at a rate close to the original work. Review them with the same paranoia
you brought to the code they repair.

## 6. Clearer, or just shorter?

Section 1 asked whether you built what was asked; this asks what the **fix** dragged in. Under
review pressure the fastest way to look responsive is to add.

- **Would deleting it end the finding instead?** A rule patched repeatedly is a rule that should
  not exist.
- **Did you hand-roll what the platform ships?** Take the boring version — stdlib call, built-in
  flag — then **prove what it actually guarantees**: `git branch -d` reads as "refuses unmerged
  branches" and means "merged into HEAD or upstream". Reaching for the built-in is half the work.
- **What outcome dies if this code is deleted?** Not what it does — what dies. No answer is an
  answer.

Then judge the shape:

- **Concepts, not lines.** Did the count of things a reader must hold go down? Six checks replaced
  by one built-in flag is a win; ten lines of prose compressed to five is cosmetic.
- **One path traceable start to finish** without jumping between sections.
- **Cause near effect** — a guard far from the thing it guards is still a defect.
- **One home per fact.** Fixed in two places means two things to keep true.

**Line count is a smell, never a target.** A shrinking diff that tangles the flow is worse than a
growing one that untangles it. "It removed lines" is not a defence.

Finding nothing is a legitimate outcome; say so. This pass earns you the dispatch, never the
approval — you remain the doer, not the judge, and trust-touching work goes to `nuclear-review`.

## Leave the receipt

Write what you checked and found to `proof-<unit>.md` beside the work — for a review round that
means the dispatch scratchpad, `$SP/proof-rN.md`, exactly where `nuclear-review` looks; otherwise
the packet. One line per numbered section — what you attacked, what survived, what you fixed —
each line citing its artifact (file:line, test name, command run), or the word skipped with the
reason; a skip without a reason is an omission. "Nothing found" plus the artifact showing the
attack ran is a legitimate receipt; no receipt is not. `nuclear-review` hands the receipt to the
reviewer as a claim to attack, where missing artifacts block APPROVE.

An unwritten pass is indistinguishable from a skipped one. Callers check for the file, not for
your confidence: `nuclear-review` blocks every re-dispatch after a fix pass on `proof-rN.md`.
