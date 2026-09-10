#!/usr/bin/env python3
"""Render the skill catalog and README table; `validate-distribution.py` checks they are current."""

from __future__ import annotations

import re
from pathlib import Path


CATALOG_HEADER = """# Bring your agent a duck

No native skill discovery? Give this block to any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The duck reads before it speaks. When a task matches a skill below, read its `SKILL.md` and
follow it before proceeding. Challenge the claim, run the check, keep the evidence.
English is the home language; match task intent across languages. Follow the user's
requested language, keeping commands, paths, identifiers, quoted errors and verdicts unchanged.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).
"""


def skill_rows(root: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        text = path.read_text()
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not frontmatter:
            raise ValueError(f"missing frontmatter: {path.relative_to(root)}")
        name_match = re.search(r"^name:\s*(\S+)", frontmatter.group(1), re.M)
        description_match = re.search(r"^description:\s*(.+)", frontmatter.group(1), re.M)
        if not name_match or not description_match:
            raise ValueError(f"missing name or description: {path.relative_to(root)}")
        rows.append(
            (
                name_match.group(1),
                description_match.group(1).strip().strip('"'),
            )
        )
    return rows


def render(root: Path) -> tuple[str, str, int]:
    rows = skill_rows(root)
    catalog = [CATALOG_HEADER]
    catalog.extend(f"- **{name}** — {description}" for name, description in rows)
    catalog_text = "\n".join(catalog) + "\n"

    table = ["| Skill | What it does |", "|---|---|"]
    for name, description in rows:
        human_summary = description.split(". ", 1)[0].rstrip(".")
        table.append(f"| `{name}` | {human_summary} |")
    block = "<!-- skills-table:start -->\n" + "\n".join(table) + "\n<!-- skills-table:end -->"

    readme_path = root / "README.md"
    readme = readme_path.read_text()
    if "<!-- skills-table:start -->" not in readme or "<!-- skills-table:end -->" not in readme:
        raise ValueError("README markers not found — add skills-table markers first")
    rendered_readme = re.sub(
        r"<!-- skills-table:start -->.*?<!-- skills-table:end -->",
        block,
        readme,
        flags=re.S,
    )
    return catalog_text, rendered_readme, len(rows)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    catalog_text, readme_text, count = render(root)
    (root / "AGENTS-CATALOG.md").write_text(catalog_text)
    (root / "README.md").write_text(readme_text)
    print(f"wrote AGENTS-CATALOG.md + README table ({count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
