#!/usr/bin/env python3
"""Validate the cross-host askrubberduck skill/plugin distribution."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable


EXPECTED_NAME = "askrubberduck"
EXPECTED_VERSION = "0.2.0"
EXPECTED_SKILLS = {
    "nuclear-break",
    "nuclear-campaign",
    "nuclear-cut",
    "nuclear-decide",
    "nuclear-diet",
    "nuclear-land",
    "nuclear-learn",
    "nuclear-plan",
    "nuclear-proof",
    "nuclear-review",
    "nuclear-roast",
    "nuclear-run",
    "nuclear-scan",
    "nuclear-sweep",
}
OUTBOUND_SKILLS = {
    "nuclear-break",
    "nuclear-campaign",
    "nuclear-cut",
    "nuclear-land",
    "nuclear-learn",
    "nuclear-plan",
    "nuclear-proof",
    "nuclear-review",
    "nuclear-roast",
    "nuclear-run",
    "nuclear-scan",
}
SIBLING_MARKERS = (
    "$askrubberduck:<name>",
    "canonical bundled-skill reference",
    "retaining the `askrubberduck:` namespace",
    "deliberate standalone install",
    "side effects start",
)
README_MARKERS = (
    "codex plugin marketplace add askrubberduck/skills",
    "codex plugin add askrubberduck@askrubberduck",
    "--ref v0.2.0",
    "~/.agents/skills",
    "$askrubberduck:nuclear-run",
    "$nuclear-run",
    "Start a new Codex session",
    "v0.2.0",
)


def load_json(root: Path, relative: str, errors: list[str]) -> dict[str, Any]:
    path = root / relative
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative}: invalid or unreadable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{relative}: root must be an object")
        return {}
    return value


def require_equal(errors: list[str], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def require_contained_path(root: Path, label: str, raw_path: Any, errors: list[str]) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path:
        errors.append(f"{label}: missing path")
        return None
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes repository root: {raw_path!r}")
        return None
    if not candidate.exists():
        errors.append(f"{label}: path does not exist: {raw_path!r}")
        return None
    return candidate


def render_expected(root: Path) -> tuple[str, str]:
    script = root / "scripts" / "render-catalog.py"
    namespace: dict[str, Any] = {"__name__": "render_catalog"}
    exec(compile(script.read_text(), str(script), "exec"), namespace)
    render = namespace.get("render")
    if not callable(render):
        raise RuntimeError("scripts/render-catalog.py does not expose render()")
    catalog, readme, _ = render(root)
    return catalog, readme


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    codex = load_json(root, ".codex-plugin/plugin.json", errors)
    claude = load_json(root, ".claude-plugin/plugin.json", errors)
    marketplace = load_json(root, ".agents/plugins/marketplace.json", errors)
    claude_marketplace = load_json(root, ".claude-plugin/marketplace.json", errors)

    for label, manifest in (("Codex manifest", codex), ("Claude manifest", claude)):
        require_equal(errors, f"{label} name", manifest.get("name"), EXPECTED_NAME)
        require_equal(errors, f"{label} version", manifest.get("version"), EXPECTED_VERSION)
        require_equal(
            errors,
            f"{label} repository",
            manifest.get("repository"),
            "https://github.com/askrubberduck/skills",
        )
        require_equal(errors, f"{label} license", manifest.get("license"), "MIT")

    require_equal(errors, "Codex skills path", codex.get("skills"), "./skills/")
    require_contained_path(root, "Codex skills path", codex.get("skills"), errors)
    for forbidden in ("mcpServers", "apps", "hooks"):
        if forbidden in codex:
            errors.append(f"Codex manifest: unrequested capability {forbidden!r}")

    interface = codex.get("interface")
    if not isinstance(interface, dict):
        errors.append("Codex manifest: interface must be an object")
    else:
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "defaultPrompt",
        ):
            if not interface.get(field):
                errors.append(f"Codex manifest interface: missing {field}")

    require_equal(errors, "Codex marketplace name", marketplace.get("name"), EXPECTED_NAME)
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        errors.append("Codex marketplace: expected exactly one plugin object")
    else:
        entry = entries[0]
        require_equal(errors, "Codex marketplace plugin name", entry.get("name"), EXPECTED_NAME)
        source = entry.get("source")
        if not isinstance(source, dict):
            errors.append("Codex marketplace source: expected object")
        else:
            require_equal(errors, "Codex marketplace source kind", source.get("source"), "local")
            require_equal(errors, "Codex marketplace source path", source.get("path"), "./")
            plugin_root = require_contained_path(
                root, "Codex marketplace source path", source.get("path"), errors
            )
            if plugin_root and plugin_root != root.resolve():
                errors.append("Codex marketplace source path: must resolve to the repository root")
        require_equal(
            errors,
            "Codex marketplace policy",
            entry.get("policy"),
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )
        require_equal(errors, "Codex marketplace category", entry.get("category"), "Productivity")

    claude_entries = claude_marketplace.get("plugins")
    if not isinstance(claude_entries, list) or len(claude_entries) != 1:
        errors.append("Claude marketplace: expected exactly one plugin")
    else:
        require_equal(
            errors,
            "Claude marketplace plugin name",
            claude_entries[0].get("name"),
            EXPECTED_NAME,
        )
        require_equal(errors, "Claude marketplace source", claude_entries[0].get("source"), "./")

    skill_root = root / "skills"
    found_skills = {path.parent.name for path in skill_root.glob("*/SKILL.md")}
    require_equal(errors, "skill directory set", found_skills, EXPECTED_SKILLS)
    for name in sorted(found_skills):
        path = skill_root / name / "SKILL.md"
        text = path.read_text()
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not frontmatter:
            errors.append(f"skills/{name}/SKILL.md: missing frontmatter")
            continue
        declared = re.search(r"^name:\s*(\S+)", frontmatter.group(1), re.M)
        description = re.search(r"^description:\s*(.+)", frontmatter.group(1), re.M)
        if not declared or declared.group(1) != name:
            errors.append(f"skills/{name}/SKILL.md: frontmatter name must match directory")
        if not description or not description.group(1).strip():
            errors.append(f"skills/{name}/SKILL.md: missing description")
        body = text[frontmatter.end() :]
        for sibling in sorted(found_skills - {name}):
            if re.search(rf"(?<!askrubberduck:)\b{re.escape(sibling)}\b", body):
                errors.append(
                    f"skills/{name}/SKILL.md: bare cross-skill reference {sibling!r}"
                )
        if name in OUTBOUND_SKILLS:
            for marker in SIBLING_MARKERS:
                if marker not in text:
                    errors.append(
                        f"skills/{name}/SKILL.md: missing sibling-resolution marker {marker!r}"
                    )

    readme = (root / "README.md").read_text()
    for marker in README_MARKERS:
        if marker not in readme:
            errors.append(f"README.md: missing installation marker {marker!r}")

    try:
        catalog_expected, readme_expected = render_expected(root)
        if (root / "AGENTS-CATALOG.md").read_text() != catalog_expected:
            errors.append("AGENTS-CATALOG.md: generated content is stale")
        if readme != readme_expected:
            errors.append("README.md: generated skills table is stale")
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f"generated catalog validation failed: {exc}")

    return sorted(errors)


def rewrite_json(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_text())
    mutate(value)
    path.write_text(json.dumps(value, indent=2) + "\n")


def self_test(root: Path) -> list[str]:
    failures: list[str] = []
    cases: list[tuple[str, Callable[[Path], None]]] = [
        (
            "version mismatch",
            lambda copy: rewrite_json(
                copy / ".claude-plugin" / "plugin.json",
                lambda value: value.__setitem__("version", "9.9.9"),
            ),
        ),
        (
            "escaping marketplace path",
            lambda copy: rewrite_json(
                copy / ".agents" / "plugins" / "marketplace.json",
                lambda value: value["plugins"][0]["source"].__setitem__("path", "../escape"),
            ),
        ),
        (
            "missing sibling resolution",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("$askrubberduck:<name>", "$missing-plugin:<name>", 1)
            ),
        ),
        (
            "bare cross-skill reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("$askrubberduck:nuclear-proof", "nuclear-proof", 1)
            ),
        ),
        (
            "malformed manifest",
            lambda copy: (copy / ".codex-plugin" / "plugin.json").write_text("{\n"),
        ),
    ]
    for label, mutate in cases:
        with tempfile.TemporaryDirectory(prefix="askrubberduck-validator-") as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(
                root,
                copy,
                ignore=shutil.ignore_patterns(".git", "graphify-out", "__pycache__"),
            )
            mutate(copy)
            if not validate(copy):
                failures.append(f"self-test did not reject: {label}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="prove common corruptions are rejected",
    )
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
    print(f"distribution validation passed ({len(EXPECTED_SKILLS)} skills{suffix})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
