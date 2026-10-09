---
name: duck-land
description: Use when a change has passed its review gate, the user authorizes landing, merging or a release, an authorized gate-passed PR or version bump is ready, or merged work was never recorded in status or outcome documentation.
---

# Duck Land

The ship step: gate passed → merge → record → clean. A merge without a recorded outcome is work
the repo forgot; a record without a verified merge is fiction.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and
machine-readable verdicts.
Load a linked skill when the current step requires its procedure, then follow the named section
within existing authority. A routing mention alone does not require loading every skill.

A passed gate establishes readiness, not permission to merge. Use the endpoint already authorized
by the user: a request only to push or prepare a PR does not authorize merging or branch deletion.

Work that already merged and was never recorded enters at the read-back: verify what is on the
default branch, record it, and name any evidence that can no longer be recovered. It needs no
candidate branch and merges nothing.

## Preconditions (fail closed — any miss stops the landing)

- The gate actually returned **`APPROVE`** per the repo's policy, and its receipt records the
  required different-family reviewer identities, evidence, and adjudication —
  [`duck-review`](../duck-review/SKILL.md) is how
  this collection produces that authorization; any gate yielding the same proof qualifies.
  `NOTE`, a raw reviewer approval, and "probably fine" are not gate-passed states.
- **The branch head and PR head, where present, equal the candidate SHA** — the exact commit the
  authorization covers. Follow repository commit conventions; no pre-squash is required by this skill.
  Rewriting commits before merge changes that SHA and requires renewed verification and authorization. The remote default branch
  is what landing moves, not part of this equality check; step 2 verifies where it ended up.
- Re-verify the base: `git fetch`, compare origin/<base> to what was branched from. **If it
  advanced, integrating it produces a new head nobody authorized** — conflict resolutions and
  semantic merges ride in unexamined. Integrate, re-run the repo's checks, and **re-authorize the
  resulting SHA** the same way this landing was authorized — [`duck-review`](../duck-review/SKILL.md)'s
  release-gate path, or
  the owner's renewed written waiver; landing on the strength of the old authorization merges an
  unexamined diff.
- CI green on the exact head being merged.
- **Commit messages and the PR description meet [`duck-dry`](../duck-dry/SKILL.md)'s prose bar**,
  checked before
  merge: a squash merge promotes the description into the commit body, so slop in either ships
  into history.
- **Where this landing is a repository's first push to a public remote — or the one that flips it
  public — scan the bytes the push will transfer, where they land, never the working
  repository's view of them**, as [the public-push scan](references/public-push.md) lays out. A
  leaked reference is public the moment it pushes; a later deletion leaves it in the history and
  in every clone.
- **A precondition the owner directs you to waive is waived only in writing before the landing** —
  which precondition, and the owner's decision, recorded where the repo keeps decisions at the
  moment it is given; step 3's outcome record then **names what was waived**. Waiving is the
  owner's call on a named precondition, never the doer's, and never a blanket exemption from the
  rest; a waiver a reviewer discovers afterward is a second violation, not a footnote.
- **A registry entry is not an authorization unless it says who authorized it** —
  [`duck-scan`](../duck-scan/SKILL.md)'s
  attribution rule: never read an unattributed entry as permission.

## Land

1. Merge per the repository's written conventions and enforced policy. Ask the remote for its
   rules; commit history alone does not impose a merge method or commit count.
   If neither specifies a method, use the sole method allowed by the remote. If several
   remain, follow the owner's stated preference; without one, the owner chooses the method.
   - **Policy.** Server-side rules are the actual policy where the host exposes them
     (`gh api repos/<owner>/<repo>/rulesets`, branch protection). A rule the
     remote enforces is the policy whether or not your account can get past it; **a landing this
     run cannot make within the rules is an owner decision, never a route around them** —
     [`duck-decide`](../duck-decide/SKILL.md).
   - **Shape.** Use the repository's permitted merge method and commit format. Do not rewrite a
     reviewed candidate merely to match inferred history.
   - **Pin the base.** Use that merge method, or direct push where repository policy permits, **pinning
     the base at merge time** with a mechanism proven to refuse a moved base, as [pinning the
     base](references/pin-the-base.md) lays out.
2. **Confirm the merge landed**: the new SHA is on the default branch and **its tree matches the
   candidate tree** — read it back, don't assume. Read the push's full output too, not its exit
   status: the remote prints policy objections ("Changes must be made through a pull request")
   even when the ref moves, and an objection inside a green push is a finding, never noise. On a
   mismatch the landed commit goes through the gate before it is recorded. It runs **after** the
   branch has moved, so it cannot hold a deployment that a push triggers.
3. Record the outcome where the repo keeps truth: shipped log / status doc / delivery board — with
   PR number, candidate SHA, landed SHA, and what changed. One recorded outcome per landing. Where
   that record lives in the repo, landing it by the same route is part of this landing's
   authorization.
4. Close or queue obligations the change touched — the doer never closes an item that needs the
   owner's sign-off; queue those ([`duck-decide`](../duck-decide/SKILL.md) presents them).
5. Clean up: load [`duck-sweep`](../duck-sweep/SKILL.md) and follow step 3 against the recorded
   candidate and landed SHAs.
   Before removal, check `git status --short --untracked-files=all --ignored`; unknown files stay
   kept until the owner decides, and kept files must be verified at their durable home. Never
   delete against a classifier's guess. A cleanup held on a queued
   [`duck-sweep`](../duck-sweep/SKILL.md) keep decision leaves the landing complete and recorded, with
   the pending worktree
   named in step 3's entry. Record a resumable boundary; continue other authorized work if the
   host and task allow it.

## Release

A release runs the process someone described, never one this skill invents: people version, tag
and publish differently. Two places can describe it:

1. The repository's own release procedure. Find it by what it says — versioning, tagging,
   publishing — not by a file name. Its rules come first.
2. `[release].procedure` (default unset) in `~/.askrubberduck/config.toml`, or a bare `procedure` in
   the origin's `[repo."<origin>"]` table: a path to a procedure the owner keeps outside the
   repository. It fills what the repository leaves open, and replaces a repository rule only where
   it says so. Quote nothing from it into public text.

Found one: a request to release authorizes what the procedure describes as well as the merge. The
preconditions above still bind, the gate covers the last release tag through the candidate
([`duck-review`](../duck-review/SKILL.md)'s code-release target), and the landing ends by reading back
what the procedure produced; step 3's outcome record names the version and tag.

Found none: the request is a landing — merge, read back, record, clean up — and the report says
no release procedure was found. Tagging and publishing wait for one.

## Common mistakes

- Leaving the worktree "for reference" — the record is the reference; the worktree is debt.
- Skipping the base re-verify because the branch is "fresh" — fresh was true when you last fetched.
