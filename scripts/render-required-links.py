#!/usr/bin/env python3
"""Regenerate REQUIRED_LINKS in validate-distribution.py from the current skill tree.

Run after intentionally adding or removing a cross-skill link; the diff shows which changed.

Frontmatter is excluded: a `description:` is trigger text, never an instruction the model follows,
so a reference there is decoration rather than an enforceable link.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADER = (
    "# Frozen, not derived at runtime: deriving would make a deleted link invisible.\n"
    "# Regenerate with scripts/render-required-links.py.\n"
)


def collect(root: Path) -> dict[str, list[str]]:
    skills = root / "skills"
    names = {d.name for d in skills.iterdir() if (d / "SKILL.md").exists()}
    links: dict[str, list[str]] = {}
    for d in sorted(skills.iterdir()):
        skill = d / "SKILL.md"
        if not skill.exists():
            continue
        body = re.sub(r"^---\n.*?\n---\n", "", skill.read_text(), flags=re.S)
        found = sorted(
            {r for r in re.findall(r"`[$/]?(nuclear-[a-z-]+)`", body) if r in names and r != d.name}
        )
        if found:
            links[d.name] = found
    return links


def render(links: dict[str, list[str]]) -> str:
    rows = "\n".join(
        f'    "{k}": {{' + ", ".join(f'"{x}"' for x in v) + "}," for k, v in links.items()
    )
    return f"{HEADER}REQUIRED_LINKS = {{\n{rows}\n}}"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    target = root / "scripts" / "validate-distribution.py"
    text = target.read_text()
    # Anchored on the assignment, not on the comment above it: matching prose meant rewording a
    # comment silently broke this script.
    pattern = re.compile(r"(?:^#[^\n]*\n)*^REQUIRED_LINKS = \{.*?\n\}", re.S | re.M)
    if not pattern.search(text):
        print("REQUIRED_LINKS block not found in validate-distribution.py", file=sys.stderr)
        return 1
    links = collect(root)
    updated = pattern.sub(lambda _: render(links), text)
    if updated == text:
        print(f"REQUIRED_LINKS already current ({sum(len(v) for v in links.values())} links)")
        return 0
    target.write_text(updated)
    print(f"wrote REQUIRED_LINKS: {sum(len(v) for v in links.values())} links across {len(links)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
