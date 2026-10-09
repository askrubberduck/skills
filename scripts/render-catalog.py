#!/usr/bin/env python3
"""Render the skill catalog and validate the editorial README map; `validate-distribution.py` checks they are current."""

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
language unless they ask otherwise, keeping commands, paths, identifiers, quoted errors and verdicts unchanged.
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


def render(root: Path) -> tuple[str, int]:
    rows = skill_rows(root)
    catalog = [CATALOG_HEADER]
    catalog.extend(f"- **{name}** — {description}" for name, description in rows)
    catalog_text = "\n".join(catalog) + "\n"

    # The README map is editorial prose; discovery metadata belongs in the catalog.
    readme = (root / "README.md").read_text()
    table = re.search(r"<!-- skills-table:start -->.*?<!-- skills-table:end -->",
                      readme, re.S)
    if not table:
        raise ValueError("README skills-table markers not found")
    names = re.findall(r"^\| `([^`]+)` \|", table[0], re.M)
    if sorted(names) != [name for name, _ in rows]:
        raise ValueError("README skills map must list each installed skill once")
    return catalog_text, len(rows)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    catalog_text, count = render(root)
    (root / "AGENTS-CATALOG.md").write_text(catalog_text)
    print(f"wrote AGENTS-CATALOG.md; checked README map ({count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
