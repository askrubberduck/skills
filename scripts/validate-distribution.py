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
EXPECTED_VERSION = "0.8.2"
EXPECTED_SKILLS = {
    "nuclear-break",
    "nuclear-campaign",
    "nuclear-cut",
    "nuclear-decide",
    "nuclear-diet",
    "nuclear-dry",
    "nuclear-frame",
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
README_MARKERS = (
    "codex plugin marketplace add askrubberduck/skills",
    "codex plugin add askrubberduck@askrubberduck",
    "gh release view --repo askrubberduck/skills",
    "~/.agents/skills",
    "$askrubberduck:nuclear-run",
    "$nuclear-run",
    "/askrubberduck:nuclear-run",
    "/nuclear-run",
    "agy plugin validate",
    "agy plugin install",
    "agents/openai.yaml",
    f"v{EXPECTED_VERSION}",
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


def require_text(errors: list[str], label: str, value: Any) -> None:
    # Hosts render this string; none of them care what it says, so the wording stays editable.
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing description")


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
    agy = load_json(root, "plugin.json", errors)
    codex = load_json(root, ".codex-plugin/plugin.json", errors)
    claude = load_json(root, ".claude-plugin/plugin.json", errors)
    marketplace = load_json(root, ".agents/plugins/marketplace.json", errors)
    claude_marketplace = load_json(root, ".claude-plugin/marketplace.json", errors)

    require_equal(errors, "Agy manifest", agy, {"name": EXPECTED_NAME})

    for label, manifest in (("Codex manifest", codex), ("Claude manifest", claude)):
        require_equal(errors, f"{label} name", manifest.get("name"), EXPECTED_NAME)
        require_equal(errors, f"{label} version", manifest.get("version"), EXPECTED_VERSION)
        require_text(errors, f"{label} description", manifest.get("description"))
        require_equal(
            errors,
            f"{label} repository",
            manifest.get("repository"),
            "https://github.com/askrubberduck/skills",
        )
        require_equal(errors, f"{label} license", manifest.get("license"), "MIT")

    require_equal(errors, "Codex skills path", codex.get("skills"), "./skills/")
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
        default_prompts = interface.get("defaultPrompt")
        if not isinstance(default_prompts, list) or not 1 <= len(default_prompts) <= 3:
            errors.append("Codex manifest interface: defaultPrompt must contain 1-3 prompts")
        else:
            for prompt in default_prompts:
                if (
                    not isinstance(prompt, str)
                    or "$askrubberduck:" not in prompt
                    or len(prompt) > 128
                ):
                    errors.append(
                        "Codex manifest interface: default prompts must be qualified and at most 128 characters"
                    )

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
        require_equal(
            errors,
            "Codex marketplace policy",
            entry.get("policy"),
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )
        require_equal(errors, "Codex marketplace category", entry.get("category"), "Productivity")

    require_text(errors, "Claude marketplace description", claude_marketplace.get("description"))
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
        require_text(
            errors,
            "Claude marketplace plugin description",
            claude_entries[0].get("description"),
        )

    skill_root = root / "skills"
    found_skills = {path.parent.name for path in skill_root.glob("*/SKILL.md")}
    require_equal(errors, "skill directory set", found_skills, EXPECTED_SKILLS)

    # Cloud sessions clone the repo and read `.claude/skills/`; they never see `~/.claude/skills/`.
    # A skill added to `skills/` without its link is invisible to every cloud session on this repo,
    # and nothing but this check would say so.
    link_root = root / ".claude" / "skills"
    # Dotted entries are host state (agent frameworks write into `.claude/`), never a skill link.
    linked_skills = (
        {path.name for path in link_root.iterdir() if not path.name.startswith(".")}
        if link_root.is_dir()
        else set()
    )
    require_equal(errors, "project skill link set", linked_skills, EXPECTED_SKILLS)
    for name in sorted(linked_skills):
        link = link_root / name
        if not link.is_symlink():
            errors.append(f".claude/skills/{name}: must be a symlink into skills/, not a copy")
        elif str(link.readlink()) != f"../../skills/{name}":
            errors.append(
                f".claude/skills/{name}: links to {str(link.readlink())!r}, expected "
                f"'../../skills/{name}'"
            )

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
        else:
            description_text = description.group(1).strip().strip('"')
            if ". Use " not in description_text:
                errors.append(
                    f"skills/{name}/SKILL.md: description must lead with what it does, then 'Use ...'"
                )
            if description_text.startswith("Use when"):
                errors.append(
                    f"skills/{name}/SKILL.md: description starts with agent-only trigger copy"
                )
            if len(description_text) > 1024:
                errors.append(f"skills/{name}/SKILL.md: description exceeds 1024 characters")

        interface_path = skill_root / name / "agents" / "openai.yaml"
        try:
            interface_text = interface_path.read_text()
        except OSError as exc:
            errors.append(f"skills/{name}/agents/openai.yaml: missing or unreadable: {exc}")
        else:
            interface_match = re.fullmatch(
                r'interface:\n'
                r'  display_name: "([^"\n]+)"\n'
                r'  short_description: "([^"\n]+)"\n'
                r'  default_prompt: "([^"\n]+)"\n',
                interface_text,
            )
            if not interface_match:
                errors.append(
                    f"skills/{name}/agents/openai.yaml: expected display name, short description, and default prompt"
                )
            else:
                display_name, short_description, default_prompt = interface_match.groups()
                expected_display = " ".join(part.capitalize() for part in name.split("-"))
                require_equal(
                    errors,
                    f"skills/{name}/agents/openai.yaml display name",
                    display_name,
                    expected_display,
                )
                if not 25 <= len(short_description) <= 64:
                    errors.append(
                        f"skills/{name}/agents/openai.yaml: short description must be 25-64 characters"
                    )
                if f"$askrubberduck:{name}" not in default_prompt:
                    errors.append(
                        f"skills/{name}/agents/openai.yaml: default prompt must use qualified skill name"
                    )
                if len(default_prompt) > 160:
                    errors.append(
                        f"skills/{name}/agents/openai.yaml: default prompt exceeds 160 characters"
                    )
        body = text[frontmatter.end() :]
        # `nuclear-*` in backticks is reserved: it always means "invoke this skill", never a
        # domain term. Authors needing such a term use prose or another name.
        for prefix, referenced in re.findall(r"`([$/]?)(nuclear-[a-z-]+)`", body):
            if prefix:
                errors.append(
                    f"skills/{name}/SKILL.md: host-prefixed reference {prefix + referenced!r} — "
                    "bodies use the bare frontmatter name"
                )
            if referenced == name:
                continue
            if referenced not in found_skills:
                errors.append(
                    f"skills/{name}/SKILL.md: cross-skill reference {referenced!r} names no installed skill"
                )
        if body.count("```") % 2:
            errors.append(f"skills/{name}/SKILL.md: unbalanced ``` code fence")
        for line in body.splitlines():
            # Excluding backticks is what stops a real ``` fence matching.
            if re.fullmatch(r"\s*``[^\s`]*", line.rstrip()):
                errors.append(
                    f"skills/{name}/SKILL.md: collapsed code fence {line.strip()!r} (expected ```)"
                )
        for hit in re.findall(r"[$/]?askrubberduck:[a-z-]+", body):
            errors.append(
                f"skills/{name}/SKILL.md: namespaced cross-skill reference {hit!r} does not resolve on standalone installs"
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





def replace_in(copy: Path, relative: str, old: str, new: str) -> None:
    path = copy / relative
    path.write_text(path.read_text().replace(old, new, 1))


def self_test(root: Path) -> list[str]:
    failures: list[str] = []
    run_skill = "skills/nuclear-run/SKILL.md"
    review_skill = "skills/nuclear-review/SKILL.md"
    replacements = [
        ("dangling cross-skill reference", run_skill, "`nuclear-proof`", "`nuclear-proofread`"),
        ("namespaced cross-skill reference", run_skill, "`nuclear-proof`", "`$askrubberduck:nuclear-proof`"),
        ("slash-namespaced cross-skill reference", run_skill, "`nuclear-proof`", "`/askrubberduck:nuclear-proof`"),
        ("bare-namespaced cross-skill reference", run_skill, "`nuclear-proof`", "askrubberduck:nuclear-proof"),
        ("dollar-prefixed dangling reference", run_skill, "`nuclear-proof`", "`$nuclear-proofread`"),
        ("host-prefixed skill reference", "skills/nuclear-campaign/SKILL.md", "`nuclear-diet`", "`$nuclear-diet`"),
        ("collapsed code fence", review_skill, "```bash", "``bash"),
        (
            "agent-only description",
            "skills/nuclear-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work without changing anything.",
            "description: Use when work status needs scanning.",
        ),
    ]
    cases: list[tuple[str, Callable[[Path], None]]] = [
        (label, lambda copy, r=rel, o=old, n=new: replace_in(copy, r, o, n))
        for label, rel, old, new in replacements
    ]
    cases += [
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
            "collapsed fence with trailing space",
            lambda copy: (
                replace_in(copy, review_skill, "```bash", "``bash "),
                replace_in(copy, review_skill, "\n   ```\n", "\n   `` \n"),
            ),
        ),
        (
            "malformed manifest",
            lambda copy: (copy / ".codex-plugin" / "plugin.json").write_text("{\n"),
        ),
        ("missing Agy adapter", lambda copy: (copy / "plugin.json").unlink()),
        (
            "malformed Codex skill interface",
            lambda copy: (
                copy / "skills" / "nuclear-run" / "agents" / "openai.yaml"
            ).write_text("interface:\n"),
        ),
        (
            "skill left out of the cloud-session links",
            lambda copy: (copy / ".claude" / "skills" / "nuclear-run").unlink(),
        ),
        (
            # Pins the dotted-entry skip fail-closed: skipping a dotted name must never hide
            # a skill whose real link is gone.
            "skill hidden behind a dotted copy",
            lambda copy: (
                (copy / ".claude" / "skills" / "nuclear-run").unlink(),
                shutil.copytree(
                    copy / "skills" / "nuclear-run",
                    copy / ".claude" / "skills" / ".nuclear-run",
                ),
            ),
        ),
        (
            "dangling cross-skill reference in an appended section",
            lambda copy: (copy / "skills" / "nuclear-sweep" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-sweep" / "SKILL.md").read_text()
                + "\n## Later\n\nThen run `nuclear-proofread`.\n"
            ),
        ),
    ]
    for label, mutate in cases:
        with tempfile.TemporaryDirectory(prefix="askrubberduck-validator-") as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(
                root,
                copy,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "graphify-out", "__pycache__"),
            )
            before = _fingerprint(copy)
            mutate(copy)
            if _fingerprint(copy) == before:
                failures.append(f"self-test mutation changed nothing: {label}")
                continue
            if not validate(copy):
                failures.append(f"self-test did not reject: {label}")
    return failures


def _fingerprint(root: Path) -> dict[str, str]:
    # Symlinks are recorded by target, not followed: rglob does not descend into them, so a
    # deleted or repointed link would otherwise look like a mutation that changed nothing.
    return {
        str(path.relative_to(root)): (
            f"symlink:{path.readlink()}" if path.is_symlink() else path.read_text(errors="replace")
        )
        for path in sorted(root.rglob("*"))
        if path.is_symlink() or path.is_file()
    }


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
