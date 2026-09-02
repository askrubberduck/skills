---
name: duck-proof
description: Give 'completed' work a skeptical second pass before anyone trusts it; 'it should work' is not evidence. Use when an implementation claims completion, the evidence is mostly "it should work", the user asks to verify or prove the work, or before handing a change to an independent review gate.
---

You do not declare victory, you prove it. "It should work" is not a claim, it is a confession that
you have not looked. Diff the candidate against its recorded base and read every changed line before
section 1 — `git diff <base>..<candidate>` for a committed candidate, plus `git diff` and
`git diff --staged` for uncommitted work. Bare `git diff` sees neither staged nor committed changes,
so on a committed candidate it reports nothing and proves nothing.

## 0. Check the ledger first

Your memory is not your context window. Read the repo's **defect ledger**
(`docs/defect-classes.md`, or wherever the repo keeps it; create it on first use). Every class
recorded there is one you attack by default, without a reviewer teaching it to you again. A repo
whose conventions bar such a file and name no other home makes the ledger's location an owner
decision — queue it via `duck-decide`, state that the pass ran ledgerless, and never resolve
the conflict by silently skipping the ledger or silently creating the file.

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

- Every caller and dependent of a signature you changed.
- TODOs: handle now or delete and own the debt. There is no later.
- The sad path, not just the happy one.
- A case the suite does not cover, which a green suite cannot tell you about.

## 4. Read the diff, and read what the gates said

`git diff` in full, every changed line. The gates are the caller's — `duck-run`'s Verify stage
runs them — so confirm they ran against this code and read their output, not their exit status.
Errors dismissed
as "unrelated" may not be. Cannot run it? Say so explicitly — never substitute confidence for
execution.

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
- **One home per fact.** Fixed in two places means two things to keep true. A comment restating
  the code is that duplication in prose — run `duck-dry` over the diff; nothing checks a
  comment, so a stale one ships.

**Line count is a smell, never a target.** A shrinking diff that tangles the flow is worse than a
growing one that untangles it. "It removed lines" is not a defense.

Finding nothing is a legitimate outcome; say so. This pass earns you the dispatch, never the
approval — you remain the doer, not the judge, and trust-touching work goes to `duck-review`.

**Not the judge is a limit on authority, never on scrutiny.** The doer is expected to validate the
work, question the solution, and attack its own reasoning as hard as any reviewer would; the one
thing the doer may not do is authorize the result. Saving the hard questions for the gate is how a
candidate arrives unvalidated and the round gets spent rediscovering what the doer already
suspected.

## Leave the receipt

Write what you checked and found to `proof-<unit>.md` — `proof-rN.md` when a review consumes it —
in the **project's durable records home**, the same place its decisions and review reports live.
Resolve that location in order: the repo's instructions, including anywhere outside the tree; else
its existing convention; else ask. **Never the scratchpad**, which dies with the session and is
unreadable to the new session the gate runs in; and **never a commit on the candidate branch**,
because that advances the head past the SHA the authorization covers.

One line per numbered section — what you attacked, what survived, what you fixed — each line citing
its artifact (file:line, test name, command run), or the word skipped with the reason; a skip
without a reason is an omission. "Nothing found" plus the artifact showing the
attack ran is a legitimate receipt; no receipt is not. `duck-review` hands the receipt to its
reviewers as a claim to attack; a missing artifact makes the associated claim unverifiable.

An unwritten pass is indistinguishable from a skipped one. Callers check for the file, not for
your confidence: `duck-review` refuses every dispatch without `proof-rN.md`, including a new
review after a material fix. Producing it is the caller's job; refusing
without it is the gate's.
