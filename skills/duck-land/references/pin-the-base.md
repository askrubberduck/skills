# Pin the base at merge time

Read this before a landing merges a PR or pushes directly. The merge must FAIL if the base moved
after the precondition check. Verify that the mechanism blocks; never infer it from its name.

Prove it once per host, mechanism and CLI version, on a throwaway remote copy:

1. Against a stationary base, run the exact invocation with its expected-base argument. Record the
   success.
2. Advance the base, rerun it, and record the quoted refusal.

Keep both: a refusal alone also fits bad credentials. Record the proof as
`merge-pin-<host>.md` at the durable records home, with the invocation string, CLI version and
date. Reuse it while both match; if either changes, re-prove it.

If no throwaway remote is possible, use only a mechanism whose vendor documentation names the
base-SHA comparison for that exact operation. Record it as tier `documentary` and rely on
`duck-land`'s step 2 read-back.

Pin an explicitly recorded base SHA, never a ref: a background fetch refreshes refs.
