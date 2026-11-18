---
name: duck-land
description: Merge approved work, run a described release process when asked, record what landed, and clean up the branch and worktree; landed means nothing left behind. Use when the user authorizes landing, merging or a release — of gate-passed work, or with the gate waived ("PR, admin merge, release, no gate") — when a gate-passed PR or version bump is ready, when the user asks what the landing or the push itself will check first, including a push that makes a repository public, or when merged work was never recorded in status or outcome documentation.
---

# Duck Land

This is the ship step: after the gate passes, merge, record and clean up. A merge without a
recorded outcome is work the repo forgot; a record without a verified merge is fiction.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

A passed gate establishes readiness, not permission to merge. Use the endpoint the owner
authorized: a request only to push or prepare a PR does not authorize a merge or branch deletion.

Merged-but-unrecorded work enters at the read-back: verify what is on the default branch, record
it, name any evidence that can no longer be recovered, and merge nothing.

## Preconditions (fail closed — any miss stops the landing)

- The gate returned **`APPROVE`** per the repo's policy, with a receipt that records the required
  different-family reviewer identities, evidence and adjudication.
  [`duck-review`](../duck-review/SKILL.md) produces that authorization; any gate that yields the
  same proof qualifies. `NOTE`, a raw reviewer approval, and "probably fine" are not gate-passed
  states.
- **The branch head and PR head, where present, equal the candidate SHA** the authorization
  covers. Follow repository commit conventions; a pre-squash is not required. A commit rewrite
  before the merge changes that SHA and requires renewed verification and authorization. The
  remote default branch is not part of this check; step 2 verifies where it ended up.
- Verify the base again: `git fetch`, then compare origin/<base> to what the branch started from.
  **If the base advanced, integration produces a new head nobody authorized.** Integrate it, rerun
  the repo's checks, and **re-authorize the resulting SHA** the same way as this landing
  ([`duck-review`](../duck-review/SKILL.md)'s release-gate path, or the owner's renewed written
  waiver).
- CI is green on the exact head you merge.
- **Commit messages and the PR description meet [`duck-dry`](../duck-dry/SKILL.md)'s prose bar**
  before the merge; a squash promotes the description into the commit body.
- **For a repository's first push to a public remote, or the push that makes it public, scan the
  bytes the push will transfer, never the working repository's view of them**, per
  [the public-push scan](references/public-push.md).
- **A precondition the owner directs you to waive must be waived in writing before the landing.**
  Record the precondition and the owner's decision where the repo keeps decisions, if it does.
  Step 3's outcome record **names what was waived**. Only the owner waives, and only a named
  precondition; a waiver is never a blanket exemption.
- **A registry entry is not an authorization unless it says who authorized it**
  ([`duck-scan`](../duck-scan/SKILL.md)'s attribution rule).

## Land

1. Merge per the repository's written conventions and enforced policy. Ask the remote for its
   rules; commit history alone imposes no merge method or commit count. If neither specifies a
   method, use the sole method the remote allows. If several remain, follow the owner's stated
   preference; without one, the owner chooses.
   - **Policy.** Where the host exposes server-side rules
     (`gh api repos/<owner>/<repo>/rulesets`, branch protection), they are the policy, whether or
     not your account can bypass them. **A landing this run cannot make within the rules is an
     owner decision, never a route around them** ([`duck-decide`](../duck-decide/SKILL.md)).
   - **Shape.** Use the permitted merge method and commit format. Do not rewrite a reviewed
     candidate to match inferred history.
   - **Pin the base.** Merge, or push directly where policy permits, **pinning the base at merge
     time** with a mechanism proven to refuse a moved base, per
     [pinning the base](references/pin-the-base.md).
2. **Confirm the merge landed.** Read back that the new SHA is on the default branch and **its
   tree matches the candidate tree**. Read the push's full output, not its exit status: an
   objection the remote prints inside a green push ("Changes must be made through a pull request")
   is a finding. On a mismatch, the landed commit goes through the gate before you record it. This
   step runs **after** the branch has moved, so it cannot hold a deployment a push triggers.
3. Record one outcome per landing where the repo keeps truth (shipped log, status doc, delivery
   board): PR number, candidate SHA, landed SHA, what changed. If that record lives in the repo,
   this landing's authorization covers its landing by the same route.
4. Close or queue obligations the change touched. Queue items that need the owner's sign-off
   for [`duck-decide`](../duck-decide/SKILL.md); the doer never closes them.
5. Clean up: load [`duck-sweep`](../duck-sweep/SKILL.md) and follow its step 3 against the
   recorded candidate and landed SHAs. Before removal, check
   `git status --short --untracked-files=all --ignored`. Unknown files stay kept until the owner
   decides. Verify kept files at their durable home. Delete nothing on a classifier's guess. If a
   cleanup is held on a queued `duck-sweep` keep decision, the landing is still complete and
   recorded, and step 3's entry names the pending worktree. Record a resumable boundary. If the
   host and task allow, continue other authorized work.

## Release

A release runs a described process, never one this skill invents. Two places can describe it:

1. The repository's own release procedure. Find it by what it says (versioning, tagging,
   publishing), not by file name. Its rules come first.
2. `[release].procedure` (default unset) in `~/.askrubberduck/config.toml`, or a bare `procedure` in
   the origin's `[repo."<origin>"]` table: a path to a procedure the owner keeps outside the
   repository. It fills what the repository leaves open and replaces a repository rule only where
   it says so. Quote nothing from it into public text.

If you found a procedure, a release request authorizes what it describes as well as the merge.
These rules still apply:

- The preconditions still bind.
- The gate covers the last release tag through the candidate
  ([`duck-review`](../duck-review/SKILL.md)'s code-release target).
- Last, the landing reads back what the procedure produced.
- Step 3's record names the version and tag.

If you found none, the request is a landing (merge, read back, record, clean up), and the report
says no release procedure was found. Tagging and publishing wait for one.

## Common mistakes

- You leave the worktree "for reference". The record is the reference; the worktree is debt.
- You skip the base check because the branch is "fresh". It was fresh only at your last fetch.
