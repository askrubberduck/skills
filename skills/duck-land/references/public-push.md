# Scan a first public push

Read this when a landing is a repository's first push to a public remote, or the one that flips
it public. `$SP` is the scratch directory `duck-review`'s dispatch mechanics defines.

Push the refs into a throwaway bare repository first
(`git init --bare "$SP/pub.git" && git push "$SP/pub.git" <refs>`), then read every object there
as stored — `git -C "$SP/pub.git" rev-list --objects --all | cut -d' ' -f1 |
git -C "$SP/pub.git" cat-file --batch | grep -a -c <pattern>` — and locate a hit with
`git -C "$SP/pub.git" grep -a <pattern> $(git -C "$SP/pub.git" rev-list --all)` and
`git -C "$SP/pub.git" log --all --grep=<pattern>`. The throwaway receives exactly what the public
remote would.

Every view of the working repository has hidden something in a gate round: the current tree
misses a file added and deleted before the push, `git grep` reads no messages, `log -p` skips a
merge's own content without `-m` and any file under a `.gitattributes -diff` rule, and `cat-file`
obeys a local `git replace` that the push ignores.

The list to scan for: private repo and product names, machine-local paths (`~/…`), internal URLs,
and codenames that outlived the rename of the files carrying them. Derive the list from the
machine rather than guessing — the other remotes, the sibling private repos, the codenames in
the history.
