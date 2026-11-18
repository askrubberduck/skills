# Scan a first public push

Read this when a landing is a repository's first push to a public remote, or the push that makes
it public. `$SP` is the scratch directory `duck-review`'s dispatch mechanics defines.

Build a throwaway bare repository of what will be public:

- For a first push, run `git init --bare "$SP/pub.git"`.
- For a visibility flip, run `git clone --mirror <remote> "$SP/pub.git"`: every existing ref goes
  public too.

Push the refs (`git push "$SP/pub.git" <refs>`). Then read every object as stored:
`git -C "$SP/pub.git" rev-list --objects --all | cut -d' ' -f1 |
git -C "$SP/pub.git" cat-file --batch | grep -a -c <pattern>`. Locate a hit with
`git -C "$SP/pub.git" grep -a <pattern> $(git -C "$SP/pub.git" rev-list --all)` and
`git -C "$SP/pub.git" log --all --grep=<pattern>`.

Scan the throwaway, not the working repository:

- The current tree misses a file added and deleted before the push.
- `git grep` reads no messages.
- `log -p` skips a merge's own content without `-m`, and any file under a `.gitattributes -diff`
  rule.
- `cat-file` obeys a local `git replace` that the push ignores.

Scan for private repo and product names, machine-local paths (`~/…`), internal URLs, and
codenames that outlived their files' rename. Derive the list from the machine (other
remotes, sibling private repos, codenames in history); never guess.
