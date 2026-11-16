# Reconstruct a mechanism

Use this for an explicitly requested deep simplification or a demonstrated wrong boundary, limited
to the subsystem under discussion. Compare a smaller in-place correction first.

1. Recover the required outcomes and contracts, including failure recovery and known next changes.
2. Separate inputs, decisions, state and side effects in concept. This is analysis, not a demand
   for a class or file per piece.
3. Classify each mechanism as required by the problem or the platform, or accidental.
   Attack duplicate state, parallel paths, mode flags, translation layers and caller order
   obligations.
4. Assemble the smallest path with one owner per rule and state transition. Reuse existing
   facilities. Keep security, validation, accessibility and necessary calibration intact.
5. Replace within the authorized scope and test the contracts. Remove superseded code, config and
   tests that only encode the old mechanism. Preserve tests of required outcomes. Intentional
   behavior changes need explicit checks, not equivalence to the original bug.

The replacement must remove a real obligation or make a realistic change easier, without weaker
contracts. A cleaner look is not enough.
