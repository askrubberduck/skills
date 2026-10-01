# Pin the base at merge time

Read this before a landing merges a PR or pushes directly. The merge must FAIL when the base moved
since the precondition check: verify that your mechanism blocks, never infer it from its name.

Prove it once per host, mechanism and CLI version on a throwaway copy of the remote: run the exact
invocation with its expected-base argument against a stationary base and record the success, then
advance the base and record the refusal, quoted. Keep both observations: a refusal alone also fits
bad credentials. The record is `merge-pin-<host>.md` at the durable records home, with the
invocation string, CLI version and date. Reuse it while the invocation and version match; re-prove
when either changes.

Where no throwaway remote is possible, use only a mechanism whose vendor documentation names the
base-SHA comparison for that exact operation, record that as tier `documentary`, and rely on the
read-back in `duck-land`'s step 2.

Pin an explicitly recorded base SHA, never a ref: a background fetch refreshes a ref.
