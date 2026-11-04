# Help the duck speak your language

`README.md` is the English source. Add translations as `README.<language>.md`, using BCP 47
tags such as `ru`, `es`, or `pt-BR`. Link each available language by its own name from every README.

Keep the source's section order, capabilities, limits, and review rules. Translate the duck's
voice naturally: short, direct, curious, and unwilling to accept confidence as proof. Commands,
paths, skill names, and verdicts stay unchanged. Translated skill summaries belong in the README;
the generator owns `AGENTS-CATALOG.md` and checks skill coverage in the editorial English map.

When the English source changes, check each translation in the same change. Record the SHA-256
of the exact reviewed `README.md` bytes in a hidden `translation-source` comment in each translation.
Refresh that marker only after checking the translation; a matching hash does not prove good prose.
If a translation cannot be updated, leave its marker unchanged and identify it as behind the source.

Before handing off, compare fenced code blocks and skill coverage with the English source, check
relative links and translated heading anchors, and run `python3 scripts/validate-distribution.py`.
Read the rendered Markdown for layout and read the translation for meaning and voice.

README translations do not establish skill routing in that language. Those claims need the
[language evals](evals/README.md). The duck checks its own claims, too.

# Change a contract with its check

A change to how the duck talks to something else ships with a check run against the real thing.

- A parser fixture is a recorded transcript from the real CLI, not output written to match the
  parser.
- A skill description change reports Skill-call counts with and without it.
- A grader is never rewritten in the change whose rule it grades. Change the rule, rerun the old
  grader, then change the grader on its own.

# Release a version

A PR that changes the plugin raises `version` in both `plugin.json` files: minor for a `feat`,
patch for a `fix`. Its squash title ends `(vX.Y.Z) (#N)`, and the body ends `Version X.Y.Z.`

After the merge, run the `release` workflow with the version, the landed SHA, a title and the
notes. It refuses a SHA that is not on master, a version the `plugin.json` files at that SHA do not
carry, and a tag that already exists. Then it tags `vX.Y.Z` and publishes `vX.Y.Z — <title>`. The
notes have two sections: "What changed", one bullet per change with its PR, and "What this release
does not claim": which gate ran with what verdict, or that the owner waived it. Set `latest` to
false when a newer version is already out.
