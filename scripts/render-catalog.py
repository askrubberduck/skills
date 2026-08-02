#!/usr/bin/env python3
"""Render AGENTS-CATALOG.md and the README skills table from skills/*/SKILL.md frontmatter."""
import re, glob, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = []
for p in sorted(glob.glob(os.path.join(root, 'skills', '*', 'SKILL.md'))):
    t = open(p).read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    name = re.search(r'^name:\s*(\S+)', m.group(1), re.M).group(1)
    desc = re.search(r'^description:\s*(.+)', m.group(1), re.M).group(1).strip().strip('"')
    rows.append((name, desc))

catalog = ["""# Skills catalog

Paste-ready block for any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The following skills provide specialized instructions for specific tasks. When a task matches a
skill's description, read the `SKILL.md` at the listed path and follow it before proceeding.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).
"""]
for name, desc in rows:
    catalog.append(f"- **{name}** — {desc}")
open(os.path.join(root, 'AGENTS-CATALOG.md'), 'w').write('\n'.join(catalog) + '\n')

table = ["| Skill | Use when |", "|---|---|"]
for name, desc in rows:
    short = desc.split('. ')[0].removeprefix('Use when ').rstrip('.')
    table.append(f"| `{name}` | {short} |")
readme_path = os.path.join(root, 'README.md')
readme = open(readme_path).read()
block = "<!-- skills-table:start -->\n" + '\n'.join(table) + "\n<!-- skills-table:end -->"
new = re.sub(r'<!-- skills-table:start -->.*?<!-- skills-table:end -->', block, readme, flags=re.S)
if new == readme and block not in readme:
    raise SystemExit("README markers not found — add skills-table markers first")
open(readme_path, 'w').write(new)
print(f"wrote AGENTS-CATALOG.md + README table ({len(rows)} skills)")
