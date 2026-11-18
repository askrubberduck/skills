# Mining the transcript stores

Read this page to count owner prompts. Both stores are JSON lines, one event per row, and mix
the owner's words with host-injected text. Count the first; the second is tool evidence.

**Claude**, `~/.claude/projects/<dir>/<session>.jsonl`. An owner prompt is a row with
`type == "user"` whose `message.content` is a string, or a list that holds `text` parts. A list of
`tool_result` parts is a tool answer. `isMeta` rows are loaded skill bodies. `isCompactSummary`
rows are the host's summary. A slash command arrives as `<command-name>` and `<command-args>` and is
the owner's directive: keep both. A row that opens "Another Claude session sent a message" is a
worker report. Delegated logs are in `<session>/subagents/`, so a one-level glob reports
only roots.

**Codex**, `$CODEX_HOME/sessions/**` and `archived_sessions/**`: every project on the host, so
counts can span projects. Name the workspaces of each count. An owner prompt is a row whose
`payload` has `type == "message"` and `role == "user"`, with its words in `content[].text`. The
first row, `session_meta`, says whose session it is. An `originator` of `codex_exec` is a
non-interactive dispatch, and a spawned agent carries `parent_thread_id`. Count neither. An SDK
originator can be an app that the owner types into, or an automated dispatch. Count it only with
positive evidence of interactive input; otherwise, report it as unknown. Name the counted
originators. A fork names its parent in `forked_from_id` and replays the parent's prompts under new
timestamps. Drop that replayed prefix. Never fold by text alone, which also folds every honest
repeat of a short directive.

Strip only known host-injected wrappers. A pattern that removes any paired tag also removes pasted
owner markup.

Write a one-off extractor over the two globs. It must:

- fold a fork: walk its prompts beside the parent's, and drop the matching prefix;
- keep a fork whose parent is missing or not older, and say so;
- count each session id once;
- print one `partial:` line per class of thing it skipped or kept on doubt: an empty or
  missing store, a malformed row, a prompt without a readable timestamp, a prompt folded as replay.

Keep the extracted rows in scratch, because they hold raw prompt text; only counts reach durable
output. Put every `partial:` line into the report. Also report this limit: the fold drops a fork
prompt that retypes the parent's next one. The store does not mark where replay ends. A store
this page does not describe yields nothing. Locate it first, or mark the result partial.
