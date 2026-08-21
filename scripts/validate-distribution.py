#!/usr/bin/env python3
"""Validate the structure of the cross-host askrubberduck skill/plugin distribution.

Structure only: what exists, what links to what, what shape a file has, and whether generated
files match their source. This gate never judges content — not wording, not length, not whether
a description reads well. A host that fails to *load* a skill is this script's problem; a skill
that loads and reads badly is a review's problem.

Stdlib only, deliberately: CI runs `setup-python` with no install step, so a dependency here is
a dependency the gate has to grow a pip step for.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable

NAME = "askrubberduck"
# Fixed by convention and not this gate's business beyond parsing: a manifest that loads is a
# manifest install can read. What it says is set; that it is JSON is what can break.
MANIFESTS = (
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
)


def load_json(root: Path, relative: str, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads((root / relative).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative}: invalid or unreadable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{relative}: root must be an object")
        return {}
    return value


def check_codex(codex: dict[str, Any], errors: list[str]) -> None:
    """The only manifest with structure beyond parsing: it points at the skills directory,
    declares the UI interface Codex renders, and must not quietly grow capabilities."""
    where = ".codex-plugin/plugin.json"
    if codex.get("skills") != "./skills/":
        errors.append(f'{where}: skills must be "./skills/", got {codex.get("skills")!r}')
    for key in ("mcpServers", "apps", "hooks"):
        if key in codex:
            errors.append(f"{where}: unrequested capability {key!r}")

    interface = codex.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{where}: interface must be an object")
        return
    missing = [field for field in ("displayName", "shortDescription", "longDescription",
                                   "developerName", "category", "capabilities", "defaultPrompt")
               if not interface.get(field)]
    if missing:
        errors.append(f"{where}: interface missing {', '.join(missing)}")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append(f"{where}: defaultPrompt must contain 1-3 prompts")


def check_skill_tree(root: Path, errors: list[str]) -> set[str]:
    """The skill set is whatever is on disk. The invariant is that every one of them is linked."""
    found = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    if not found:
        errors.append("skills/: no skills found")

    # Cloud sessions clone the repo and read `.claude/skills/`; they never see `~/.claude/skills/`.
    # A skill added to `skills/` without its link is invisible to every cloud session on this repo,
    # and nothing but this check would say so.
    link_root = root / ".claude" / "skills"
    # Dotted entries are host state (agent frameworks write into `.claude/`), never a skill link.
    linked = ({p.name for p in link_root.iterdir() if not p.name.startswith(".")}
              if link_root.is_dir() else set())
    for name in sorted(found - linked):
        errors.append(f".claude/skills/{name}: missing link — the skill is invisible to cloud sessions")
    for name in sorted(linked - found):
        errors.append(f".claude/skills/{name}: link to a skill that does not exist")
    for name in sorted(linked & found):
        link, target = link_root / name, f"../../skills/{name}"
        if not link.is_symlink():
            errors.append(f".claude/skills/{name}: must be a symlink into skills/, not a copy")
        elif str(link.readlink()) != target:
            errors.append(f".claude/skills/{name}: links to {str(link.readlink())!r}, "
                          f"expected {target!r}")
    return found


def check_skill(root: Path, name: str, found: set[str], errors: list[str]) -> None:
    where = f"skills/{name}/SKILL.md"
    text = (root / where).read_text(errors="replace")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not frontmatter:
        errors.append(f"{where}: missing frontmatter")
        return

    # Hosts parse this with a real YAML parser, which is last-key-wins: a duplicate key or an
    # indented continuation line changes what loads while a first-match regex keeps validating
    # the original. Comparing the whole key sequence catches duplicates, extra keys, wrong
    # order, and continuation lines at once — a continuation has no `key:` so it fails the split.
    lines = frontmatter.group(1).split("\n")
    if [line.split(":", 1)[0] for line in lines] != ["name", "description"]:
        errors.append(f"{where}: frontmatter must be exactly a name: line then a description: line")
    else:
        values = dict(line.split(":", 1) for line in lines)
        if values["name"].strip() != name:
            errors.append(f"{where}: frontmatter name must match directory")
        if not values["description"].strip():
            errors.append(f"{where}: missing description")

    interface_path = root / "skills" / name / "agents" / "openai.yaml"
    try:
        interface_text = interface_path.read_text()
    except OSError as exc:
        errors.append(f"skills/{name}/agents/openai.yaml: missing or unreadable: {exc}")
    else:
        wanted = ["display_name", "short_description", "default_prompt"]
        keys = re.findall(r"^\s+([a-z_]+):", interface_text, re.M)
        if not interface_text.startswith("interface:") or keys != wanted:
            errors.append(f"skills/{name}/agents/openai.yaml: expected an interface block with "
                          f"{', '.join(wanted)}")

    body = text[frontmatter.end():]
    # `duck-*` in backticks is reserved: it always means "invoke this skill", never a domain
    # term. A prefixed or namespaced form hard-fails on a standalone install.
    for prefix, referenced in re.findall(r"`([$/]?)(duck-[a-z-]+)`", body):
        if prefix:
            errors.append(f"{where}: host-prefixed reference {prefix + referenced!r} — "
                          "bodies use the bare frontmatter name")
        if referenced != name and referenced not in found:
            errors.append(f"{where}: cross-skill reference {referenced!r} names no installed skill")
    for hit in re.findall(r"[$/]?askrubberduck:[a-z-]+", body):
        errors.append(f"{where}: namespaced cross-skill reference {hit!r} "
                      "does not resolve on standalone installs")
    if body.count("```") % 2:
        errors.append(f"{where}: unbalanced ``` code fence")


def check_generated(root: Path, readme: str, errors: list[str]) -> None:
    script = root / "scripts" / "render-catalog.py"
    namespace: dict[str, Any] = {"__name__": "render_catalog"}
    try:
        exec(compile(script.read_text(), str(script), "exec"), namespace)
        catalog_expected, readme_expected, _ = namespace["render"](root)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"generated catalog validation failed: {exc}")
        return
    if (root / "AGENTS-CATALOG.md").read_text() != catalog_expected:
        errors.append("AGENTS-CATALOG.md: generated content is stale")
    if readme != readme_expected:
        errors.append("README.md: generated skills table is stale")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    readme = (root / "README.md").read_text()
    manifests = {relative: load_json(root, relative, errors) for relative in MANIFESTS}
    check_codex(manifests[".codex-plugin/plugin.json"], errors)
    found = check_skill_tree(root, errors)
    for name in sorted(found):
        check_skill(root, name, found, errors)
    check_generated(root, readme, errors)
    return sorted(errors)


def rewrite_json(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_text())
    mutate(value)
    path.write_text(json.dumps(value, indent=2) + "\n")


def edit(copy: Path, relative: str, old: str, new: str) -> None:
    path = copy / relative
    path.write_text(path.read_text().replace(old, new, 1))


# One corruption per structural check, as (label, expected error fragment, mutation). A gate
# nobody proves is a gate nobody has — CI runs this, so a deleted check fails loudly here.
SCAN = "skills/duck-scan/SKILL.md"
RUN = "skills/duck-run/SKILL.md"
CASES: list[tuple[str, str, Callable[[Path], None]]] = [
    ("invalid manifest JSON", "invalid or unreadable JSON",
     lambda c: (c / ".codex-plugin/plugin.json").write_text("{")),
    ("codex skills path", 'skills must be "./skills/"',
     lambda c: rewrite_json(c / ".codex-plugin/plugin.json", lambda m: m.__setitem__("skills", "./x/"))),
    ("codex unrequested capability", "unrequested capability",
     lambda c: rewrite_json(c / ".codex-plugin/plugin.json", lambda m: m.__setitem__("hooks", {}))),
    ("codex interface field", "interface missing",
     lambda c: rewrite_json(c / ".codex-plugin/plugin.json",
                            lambda m: m["interface"].__setitem__("category", ""))),
    ("codex default prompts", "defaultPrompt must contain 1-3",
     lambda c: rewrite_json(c / ".codex-plugin/plugin.json",
                            lambda m: m["interface"].__setitem__("defaultPrompt", []))),
    ("skill removed", "link to a skill that does not exist",
     lambda c: shutil.rmtree(c / "skills/duck-cut")),
    ("project link missing", "missing link",
     lambda c: (c / ".claude/skills/duck-cut").unlink()),
    ("project link is a copy", "must be a symlink",
     lambda c: ((c / ".claude/skills/duck-cut").unlink(), (c / ".claude/skills/duck-cut").mkdir())),
    ("project link repointed", "links to",
     lambda c: ((c / ".claude/skills/duck-cut").unlink(),
                (c / ".claude/skills/duck-cut").symlink_to("../../skills/duck-run"))),
    ("missing frontmatter", "missing frontmatter", lambda c: (c / SCAN).write_text("# none\n")),
    ("duplicate description key", "frontmatter must be exactly",
     lambda c: edit(c, SCAN, "description:", "description: dupe\ndescription:")),
    ("frontmatter extra key", "frontmatter must be exactly",
     lambda c: edit(c, SCAN, "description:", "extra: 1\ndescription:")),
    ("frontmatter continuation line", "frontmatter must be exactly",
     lambda c: edit(c, SCAN, "\n---\n", "\n  continued\n---\n")),
    ("name does not match directory", "must match directory",
     lambda c: edit(c, SCAN, "name: duck-scan", "name: duck-scanner")),
    ("openai interface shape", "expected an interface block",
     lambda c: (c / "skills/duck-scan/agents/openai.yaml").write_text("interface:\n")),
    ("dangling cross-skill reference", "names no installed skill",
     lambda c: edit(c, RUN, "`duck-proof`", "`duck-proofread`")),
    ("host-prefixed skill reference", "bodies use the bare frontmatter name",
     lambda c: edit(c, RUN, "`duck-proof`", "`$duck-proof`")),
    ("namespaced skill reference", "does not resolve on standalone installs",
     lambda c: edit(c, RUN, "`duck-proof`", "askrubberduck:duck-proof")),
    ("unbalanced code fence", "unbalanced",
     lambda c: (c / "skills/duck-review/SKILL.md").write_text(
         (c / "skills/duck-review/SKILL.md").read_text() + "\n```bash\nstray\n")),
    ("stale generated catalog", "stale", lambda c: (c / "AGENTS-CATALOG.md").write_text("# stale\n")),
]


def fingerprint(root: Path) -> dict[str, str]:
    # Symlinks are recorded by target, not followed: rglob does not descend into them, so a
    # deleted or repointed link would otherwise look like a mutation that changed nothing.
    return {
        str(path.relative_to(root)): (
            f"symlink:{path.readlink()}" if path.is_symlink() else path.read_text(errors="replace")
        )
        for path in sorted(root.rglob("*"))
        if path.is_symlink() or path.is_file()
    }


def self_test(root: Path) -> list[str]:
    failures: list[str] = []
    for label, expected, mutate in CASES:
        with tempfile.TemporaryDirectory(prefix="askrubberduck-validator-") as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(root, copy, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", "graphify-out", "__pycache__"))
            before = fingerprint(copy)
            mutate(copy)
            if fingerprint(copy) == before:
                failures.append(f"self-test mutation changed nothing: {label}")
                continue
            errors = validate(copy)
            if not errors:
                failures.append(f"self-test did not reject: {label}")
            elif not any(expected in error for error in errors):
                failures.append(f"self-test rejected for the wrong reason: {label} "
                                f"(wanted {expected!r}, got {errors})")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true",
                        help="prove common corruptions are rejected")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent

    errors = validate(root)
    if not errors and args.self_test:
        errors.extend(self_test(root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    suffix = " and corruption self-tests" if args.self_test else ""
    skills = len(list((root / "skills").glob("*/SKILL.md")))
    print(f"distribution validation passed ({skills} skills{suffix})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
