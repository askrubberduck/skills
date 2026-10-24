# Reconstruct a mechanism

Use this for an explicitly requested deep simplification or a demonstrated wrong boundary, bounded
to the subsystem under discussion. Compare with a smaller in-place correction first.

1. Recover the required outcomes and contracts, including failure recovery and known next changes.
2. Separate inputs, decisions, state and side effects conceptually; this is analysis, not a
   demand for a class or file per piece.
3. Classify mechanisms as required by the problem, required by the platform, or accidental. Attack
   duplicate state, parallel paths, mode flags, translation layers and caller ordering obligations.
4. Assemble the smallest path with one owner per rule and state transition. Reuse existing
   facilities; keep security, validation, accessibility and necessary calibration intact.
5. Replace within the authorized scope, test the contracts, and remove superseded code, config and
   tests that only encode the old mechanism. Preserve tests of required outcomes. Intentional
   behavior changes need explicit checks, not equivalence to the original bug.

The replacement must remove a real obligation or make a realistic change easier without weakening
the contracts; looking cleaner is not enough.
