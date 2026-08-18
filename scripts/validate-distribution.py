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
EXPECTED_VERSION = "1.1.0"
EXPECTED_SKILLS = {
    "duck-break",
    "duck-campaign",
    "duck-cut",
    "duck-decide",
    "duck-diet",
    "duck-dry",
    "duck-frame",
    "duck-land",
    "duck-learn",
    "duck-pingpong",
    "duck-plan",
    "duck-proof",
    "duck-race",
    "duck-review",
    "duck-roast",
    "duck-run",
    "duck-scan",
    "duck-sweep",
}
README_MARKERS = (
    "codex plugin marketplace add askrubberduck/skills",
    "codex plugin add askrubberduck@askrubberduck",
    "gh release view --repo askrubberduck/skills",
    "~/.agents/skills",
    "$askrubberduck:duck-run",
    "$duck-run",
    "/askrubberduck:duck-run",
    "/duck-run",
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
        # Bytes, not text mode: universal-newline translation rewrites a lone '\r' to '\n'
        # on read, so text mode can never see the byte that breaks real hosts' parsers.
        text = path.read_bytes().decode("utf-8", errors="replace")
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not frontmatter:
            errors.append(f"skills/{name}/SKILL.md: missing frontmatter")
            continue
        # The whole frontmatter shape is validated, not just the first match per key:
        # YAML is last-key-wins, so a duplicate 'description:' or an indented continuation
        # line changes what a host loads while first-match regexes keep validating the
        # original. Exactly two single-line keys, nothing else.
        fm_lines = frontmatter.group(1).split("\n")
        for key in ("name", "description"):
            if sum(1 for line in fm_lines if line.startswith(f"{key}:")) != 1:
                errors.append(
                    f"skills/{name}/SKILL.md: frontmatter must declare {key} exactly once"
                )
        for line in fm_lines:
            if not line.startswith(("name:", "description:")):
                errors.append(
                    f"skills/{name}/SKILL.md: unexpected frontmatter line "
                    "(continuation lines and extra keys are rejected)"
                )
                break
        declared = re.search(r"^name:\s*(\S+)", frontmatter.group(1), re.M)
        # Spaces only: \s would eat leading control characters the guard below must see.
        description = re.search(r"^description:[ ]*(.+)", frontmatter.group(1), re.M)
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
            # Hosts parse frontmatter with real YAML parsers (Psych, PyYAML); a ': ' becomes a
            # mapping, ' #' truncates, and a leading indicator character errors or nils the
            # description — each drops the skill silently. Enumerating bad characters lost three
            # review rounds, so this is a whitelist: a single-line scalar that starts with a
            # letter and avoids ': ', ' #', and a trailing ':' is valid under the YAML plain-
            # scalar grammar; everything outside that proven subset is rejected.
            # The raw capture, never stripped first: str.strip() removes \x0b/\x0c-class
            # whitespace, hiding trailing control characters from the scan below.
            raw = description.group(1)
            # Whitelist closure, not a blacklist: a block-context plain scalar fails only on
            # (a) an indicator as first character — the letter rule; (b) ': ' or a trailing
            # ':' — banned; (c) ' #' — banned; (d) tabs, control characters, and the Unicode
            # line breaks NEL/LS/PS — all non-printable per str.isprintable, banned wholesale.
            # What remains is printable content no YAML parser misreads.
            if (
                not raw[:1].isalpha()
                or any(not char.isprintable() for char in raw)
                or ": " in raw
                or " #" in raw
                or raw.rstrip(" ").endswith(":")
            ):
                errors.append(
                    f"skills/{name}/SKILL.md: description is not a YAML-safe plain scalar "
                    "(start with a letter; printable characters only, no ': ', no ' #', no trailing ':')"
                )

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
        # `duck-*` in backticks is reserved: it always means "invoke this skill", never a
        # domain term. Authors needing such a term use prose or another name.
        for prefix, referenced in re.findall(r"`([$/]?)(duck-[a-z-]+)`", body):
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
    run_skill = "skills/duck-run/SKILL.md"
    review_skill = "skills/duck-review/SKILL.md"
    replacements = [
        ("dangling cross-skill reference", run_skill, "`duck-proof`", "`duck-proofread`"),
        ("namespaced cross-skill reference", run_skill, "`duck-proof`", "`$askrubberduck:duck-proof`"),
        ("slash-namespaced cross-skill reference", run_skill, "`duck-proof`", "`/askrubberduck:duck-proof`"),
        ("bare-namespaced cross-skill reference", run_skill, "`duck-proof`", "askrubberduck:duck-proof"),
        ("dollar-prefixed dangling reference", run_skill, "`duck-proof`", "`$duck-proofread`"),
        ("host-prefixed skill reference", "skills/duck-campaign/SKILL.md", "`duck-diet`", "`$duck-diet`"),
        ("collapsed code fence", review_skill, "```bash", "``bash"),
        (
            "YAML-breaking description colon",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready: blocked and remaining work",
        ),
        (
            "YAML-nil description leading hash",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: # Find ready, blocked, and remaining work",
        ),
        (
            "YAML-breaking description leading indicator",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: ] Find ready, blocked, and remaining work",
        ),
        (
            "quoted description",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            'description: "Find ready, blocked, and remaining work',
        ),
        (
            "YAML-breaking description tab separator",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready:\tblocked, and remaining work",
        ),
        (
            "YAML-truncating description tab comment",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready\t#blocked, and remaining work",
        ),
        (
            "YAML-breaking description carriage return",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready\r- blocked, and remaining work",
        ),
        (
            "duplicate description key",
            "skills/duck-scan/SKILL.md",
            "name: duck-scan",
            "name: duck-scan\ndescription: hidden duplicate wins in last-key-wins parsers",
        ),
        (
            "frontmatter continuation line",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready,\n  blocked, and remaining work",
        ),
        (
            # At the true end of the line: an inline control character never met the r7
            # str.strip() bug, so only a trailing one proves the raw-capture fix holds.
            "YAML-rejected trailing vertical tab",
            "skills/duck-scan/SKILL.md",
            "or asks whether a named work item is ready.",
            "or asks whether a named work item is ready.\x0b",
        ),
        (
            "YAML-rejected NEL line break",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready\u0085- blocked, and remaining work",
        ),
        (
            "YAML-breaking description dash",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: - Find ready, blocked, and remaining work",
        ),
        (
            "YAML-truncating description comment",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work",
            "description: Find ready #blocked and remaining work",
        ),
        (
            "agent-only description",
            "skills/duck-scan/SKILL.md",
            "description: Find ready, blocked, and remaining work without changing anything; looking is free.",
            "description: Use when work status needs scanning.",
        ),
    ]
    expected_errors = {
        "dangling cross-skill reference": "names no installed skill",
        "namespaced cross-skill reference": "does not resolve on standalone installs",
        "slash-namespaced cross-skill reference": "does not resolve on standalone installs",
        "bare-namespaced cross-skill reference": "does not resolve on standalone installs",
        "dollar-prefixed dangling reference": "bodies use the bare frontmatter name",
        "host-prefixed skill reference": "bodies use the bare frontmatter name",
        "collapsed code fence": "collapsed code fence",
        "YAML-breaking description colon": "not a YAML-safe plain scalar",
        "YAML-breaking description dash": "not a YAML-safe plain scalar",
        "YAML-nil description leading hash": "not a YAML-safe plain scalar",
        "YAML-breaking description leading indicator": "not a YAML-safe plain scalar",
        "quoted description": "not a YAML-safe plain scalar",
        "YAML-breaking description tab separator": "not a YAML-safe plain scalar",
        "YAML-truncating description tab comment": "not a YAML-safe plain scalar",
        "YAML-breaking description carriage return": "not a YAML-safe plain scalar",
        "YAML-rejected trailing vertical tab": "not a YAML-safe plain scalar",
        "YAML-rejected NEL line break": "not a YAML-safe plain scalar",
        "duplicate description key": "exactly once",
        "frontmatter continuation line": "unexpected frontmatter line",
        "YAML-truncating description comment": "not a YAML-safe plain scalar",
        "agent-only description": "agent-only trigger copy",
        "version mismatch": "version",
        "escaping marketplace path": "Codex marketplace source path",
        "collapsed fence with trailing space": "collapsed code fence",
        "malformed manifest": "invalid or unreadable JSON",
        "missing Agy adapter": "Agy manifest",
        "malformed Codex skill interface": "expected display name",
        "skill left out of the cloud-session links": "project skill link set",
        "skill hidden behind a dotted copy": "project skill link set",
        "dangling cross-skill reference in an appended section": "names no installed skill",
    }
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
                copy / "skills" / "duck-run" / "agents" / "openai.yaml"
            ).write_text("interface:\n"),
        ),
        (
            "skill left out of the cloud-session links",
            lambda copy: (copy / ".claude" / "skills" / "duck-run").unlink(),
        ),
        (
            # Pins the dotted-entry skip fail-closed: skipping a dotted name must never hide
            # a skill whose real link is gone.
            "skill hidden behind a dotted copy",
            lambda copy: (
                (copy / ".claude" / "skills" / "duck-run").unlink(),
                shutil.copytree(
                    copy / "skills" / "duck-run",
                    copy / ".claude" / "skills" / ".duck-run",
                ),
            ),
        ),
        (
            "dangling cross-skill reference in an appended section",
            lambda copy: (copy / "skills" / "duck-sweep" / "SKILL.md").write_text(
                (copy / "skills" / "duck-sweep" / "SKILL.md").read_text()
                + "\n## Later\n\nThen run `duck-proofread`.\n"
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
            errors = validate(copy)
            if not errors:
                failures.append(f"self-test did not reject: {label}")
                continue
            expected = expected_errors.get(label)
            if expected is None:
                failures.append(f"self-test case has no expected error: {label}")
            elif not any(expected in error for error in errors):
                failures.append(
                    f"self-test rejected for the wrong reason: {label} (wanted {expected!r})"
                )
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
