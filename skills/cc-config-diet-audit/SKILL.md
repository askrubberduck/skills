---
name: cc-config-diet-audit
description: Use when the user asks to health-check their Claude Code setup, find extensions that cost context but never get used, deduplicate memory files against checked-in instructions, or trim CLAUDE.md/AGENTS.md bloat.
---

# Claude Code Config Diet Audit

Everything always-loaded (CLAUDE.md chain, memory index, plugin skill descriptions, hooks context)
is billed every turn of every session. The audit's product is deletions.

## Audit

1. **Installation health**: `claude doctor` if available; version, plugin cache integrity, broken
   symlinks in `~/.claude/skills/`.
2. **Always-loaded inventory**: user + project CLAUDE.md/AGENTS.md (follow `@includes`), memory
   index, enabled plugins. Estimate each block's size; rank by cost.
3. **Usage cross-check**: grep recent session transcripts (`~/.claude/projects/<dir>/*.jsonl`) for
   each plugin/skill actually invoked. Loaded-never-invoked for weeks = disable candidate.
4. **Dedupe**: local memory files repeating checked-in CLAUDE.md facts — keep the checked-in copy,
   delete the memory. Same for AGENTS.md vs copilot-instructions duplication: one canonical file,
   others reference it.
5. **Trim to non-derivable**: a CLAUDE.md line earns its place only if a fresh session could NOT
   derive it from the repo (structure, commands visible in package files, git history are all
   derivable — cut). Owner decisions, invariants, and workflow rules stay.
6. Present cuts as one list with per-item size saved; apply on approval; direct writes to
   `~/.claude/**` and `.claude/**` are otherwise fine.

## Common mistakes

- Trimming rules the owner put there deliberately — when a line reads like a decision, ask, don't cut.
- Deleting the checked-in copy and keeping the local memory — backwards; checked-in wins (it serves
  every agent, not one machine).
- Auditing config but not memory index growth — a bloated always-loaded memory index is the same
  disease with a different filename.
