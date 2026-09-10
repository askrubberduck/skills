# Help the duck speak your language

`README.md` is the English source. Add translations as `README.<language>.md`, using BCP 47
tags such as `ru`, `es`, or `pt-BR`. Link each available language by its own name from every README.

Keep the source's section order, capabilities, limits, and review rules. Translate the duck's
voice naturally: short, direct, curious, and unwilling to accept confidence as proof. Commands,
paths, skill names, and verdicts stay unchanged. Translated skill summaries belong in the README;
the catalog generator owns only the English table.

When the English source changes, check each translation in the same change. Record the SHA-256
of the exact reviewed `README.md` bytes in a hidden `translation-source` comment in each translation.
Refresh that marker only after checking the translation; a matching hash does not prove good prose.
If a translation cannot be updated, leave its marker unchanged and identify it as behind the source.

Before handing off, compare fenced code blocks and skill coverage with the English source, check
relative links and translated heading anchors, and run `python3 scripts/validate-distribution.py`.
Read the rendered Markdown for layout and read the translation for meaning and voice.

README translations do not establish skill routing in that language. Those claims need the
[language evals](evals/README.md). The duck checks its own claims, too.
