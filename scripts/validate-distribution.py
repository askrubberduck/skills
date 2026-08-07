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
EXPECTED_VERSION = "0.4.5"
EXPECTED_PLUGIN_DESCRIPTION = "Plan, challenge, ship, and clean up complex work"
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
# Frozen, not derived at runtime: deriving would make a deleted link invisible.
# Regenerate with scripts/render-required-links.py.
REQUIRED_LINKS = {
    "nuclear-break": {"nuclear-review"},
    "nuclear-campaign": {"nuclear-diet", "nuclear-plan", "nuclear-sweep"},
    "nuclear-cut": {"nuclear-decide"},
    "nuclear-land": {"nuclear-decide", "nuclear-review", "nuclear-sweep"},
    "nuclear-learn": {"nuclear-proof"},
    "nuclear-plan": {"nuclear-review"},
    "nuclear-proof": {"nuclear-review"},
    "nuclear-review": {"nuclear-break", "nuclear-decide", "nuclear-land", "nuclear-plan", "nuclear-proof"},
    "nuclear-roast": {"nuclear-cut", "nuclear-decide", "nuclear-plan", "nuclear-proof", "nuclear-review"},
    "nuclear-run": {"nuclear-break", "nuclear-plan", "nuclear-proof", "nuclear-review"},
    "nuclear-scan": {"nuclear-campaign", "nuclear-cut"},
}
REQUIRED_CONTRACTS = {
    "nuclear-review": (
        "proof-r1.md",
        "$SP/proof-rN.md",
        "No `proof-rN.md`, no dispatch",
        "break-rN.md",
        "co-authorship line",
        "two reviewers from two different model families",
        "APPROVES in the same round",
        "A REJECT is never an outage",
        "A same-family pass never substitutes",
        "No receipt, no dispatch",
        "a dispatch that was attempted",
        "produced no verdict",
        "evidence recorded beside the verdict",
        "run `nuclear-plan` BEFORE building",
        "Ask what the code is for before you patch it",
        "The growth ratchet",
    ),
    "nuclear-proof": ("proof-<unit>.md", "blocks every re-dispatch after a fix pass"),
    "nuclear-break": (
        "break-rN.md",
        "the suite MUST go red",
        "duplicate, and concurrent inputs",
        "take each named invariant",
        "kill the process mid-operation",
        "not the test harness",
    ),
    "nuclear-plan": (
        "plan-<family>.md",
        "co-authorship line",
        "binding decorrelated CODE gate",
        "including at least one proven different family",
    ),
    "nuclear-campaign": (
        "co-authorship line",
        "never into silence",
        "campaign roster",
        "next iteration an owner",
    ),
    "nuclear-land": (
        "One recorded outcome per landing",
        "merged SHA",
        "proven different-family approval",
        "back through the review gate",
    ),
    "nuclear-sweep": (
        "Both halves are load-bearing",
        "Do not build a cleverer classifier",
        "--untracked-files=all --ignored",
    ),
    "nuclear-run": (
        "proof-<unit>.md",
        "co-authorship line",
        "A turn may end for exactly four reasons",
        "an external block",
        "Anything else: keep going",
    ),
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
    "Start a new Codex session",
    "Start a new host session",
    "v0.4.5",
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
    agy = load_json(root, "plugin.json", errors)
    codex = load_json(root, ".codex-plugin/plugin.json", errors)
    claude = load_json(root, ".claude-plugin/plugin.json", errors)
    marketplace = load_json(root, ".agents/plugins/marketplace.json", errors)
    claude_marketplace = load_json(root, ".claude-plugin/marketplace.json", errors)

    require_equal(errors, "Agy manifest", agy, {"name": EXPECTED_NAME})

    for label, manifest in (("Codex manifest", codex), ("Claude manifest", claude)):
        require_equal(errors, f"{label} name", manifest.get("name"), EXPECTED_NAME)
        require_equal(errors, f"{label} version", manifest.get("version"), EXPECTED_VERSION)
        require_equal(
            errors,
            f"{label} description",
            manifest.get("description"),
            EXPECTED_PLUGIN_DESCRIPTION,
        )
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
        require_equal(
            errors,
            "Codex manifest short description",
            interface.get("shortDescription"),
            EXPECTED_PLUGIN_DESCRIPTION,
        )
        default_prompts = interface.get("defaultPrompt")
        if not isinstance(default_prompts, list) or not 1 <= len(default_prompts) <= 3:
            errors.append("Codex manifest interface: defaultPrompt must contain 1-3 prompts")
        else:
            for prompt in default_prompts:
                if (
                    not isinstance(prompt, str)
                    or not prompt.startswith("Use $askrubberduck:")
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

    require_equal(
        errors,
        "Claude marketplace description",
        claude_marketplace.get("description"),
        EXPECTED_PLUGIN_DESCRIPTION,
    )
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
        require_equal(
            errors,
            "Claude marketplace plugin description",
            claude_entries[0].get("description"),
            EXPECTED_PLUGIN_DESCRIPTION,
        )

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
                if not default_prompt.startswith("Use ") or len(default_prompt) > 160:
                    errors.append(
                        f"skills/{name}/agents/openai.yaml: default prompt must be a short starter prompt"
                    )
        body = text[frontmatter.end() :]
        # `nuclear-*` in backticks is reserved: it always means "invoke this skill", never a
        # domain term. Authors needing such a term use prose or another name.
        referenced_here = set()
        for prefix, referenced in re.findall(r"`([$/]?)(nuclear-[a-z-]+)`", body):
            if prefix:
                errors.append(
                    f"skills/{name}/SKILL.md: host-prefixed reference {prefix + referenced!r} — "
                    "bodies use the bare frontmatter name"
                )
            if referenced == name:
                continue
            referenced_here.add(referenced)
            if referenced not in found_skills:
                errors.append(
                    f"skills/{name}/SKILL.md: cross-skill reference {referenced!r} names no installed skill"
                )
        for required in sorted(REQUIRED_LINKS.get(name, ())):
            if required not in referenced_here:
                errors.append(
                    f"skills/{name}/SKILL.md: required pipeline link to {required!r} is missing"
                )
        # REQUIRED_CONTRACTS phrases are matched against this: store them unwrapped and
        # without emphasis markers.
        flat_body = " ".join(body.replace("*", "").split())
        for contract in REQUIRED_CONTRACTS.get(name, ()):
            occurrences = flat_body.count(contract)
            if occurrences == 0:
                errors.append(
                    f"skills/{name}/SKILL.md: artifact contract {contract!r} was dropped"
                )
            elif occurrences > 1:
                errors.append(
                    f"skills/{name}/SKILL.md: artifact contract {contract!r} occurs {occurrences}x — "
                    "a repeated phrase masks its own deletion; protect a unique one"
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
            "dangling cross-skill reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "`nuclear-proofread`", 1)
            ),
        ),
        (
            "namespaced cross-skill reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "`$askrubberduck:nuclear-proof`", 1)
            ),
        ),
        (
            "slash-namespaced cross-skill reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "`/askrubberduck:nuclear-proof`", 1)
            ),
        ),
        (
            "bare-namespaced cross-skill reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "askrubberduck:nuclear-proof", 1)
            ),
        ),
        (
            "dollar-prefixed dangling reference",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "`$nuclear-proofread`", 1)
            ),
        ),
        (
            "deleted mandatory handoff",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("`nuclear-proof`", "a self-review")
            ),
        ),
        (
            "dropped proof-r1 contract",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("`$SP/proof-r1.md`", "a receipt", 1)
            ),
        ),
        (
            "dropped break-rN contract",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("`break-rN.md`", "its evidence", 1)
            ),
        ),
        (
            "dropped campaign plan contract",
            lambda copy: (copy / "skills" / "nuclear-campaign" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-campaign" / "SKILL.md")
                .read_text()
                .replace("co-authorship line", "plan", 1)
            ),
        ),
        (
            "duplicated contract phrase becomes maskable",
            lambda copy: (copy / "skills" / "nuclear-break" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-break" / "SKILL.md").read_text()
                + "\n\nRestated: the suite MUST go red.\n"
            ),
        ),
        (
            "deleted plan-handoff instruction masked by a later mention",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("run `nuclear-plan` BEFORE building", "plan somehow", 1)
            ),
        ),
        (
            "gutted outage attempt requirement",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("a dispatch that was attempted", "a dispatch", 1)
            ),
        ),
        (
            "host-prefixed skill reference",
            lambda copy: (copy / "skills" / "nuclear-campaign" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-campaign" / "SKILL.md")
                .read_text()
                .replace("`nuclear-diet`", "`$nuclear-diet`", 1)
            ),
        ),
        (
            "deleted round-one receipt rule",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("No receipt, no dispatch", "Receipts are encouraged", 1)
            ),
        ),
        (
            "deleted outage no-verdict definition",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("produced **no verdict**", "was unhelpful", 1)
            ),
        ),
        (
            "truncated turn-end reasons",
            lambda copy: (copy / "skills" / "nuclear-run" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-run" / "SKILL.md")
                .read_text()
                .replace("Anything else: keep going", "Use judgement", 1)
            ),
        ),
        (
            "collapsed fence with trailing space",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("```bash", "``bash ", 1)
                .replace("\n   ```\n", "\n   `` \n", 1)
            ),
        ),
        (
            "deleted plan cross-family quorum",
            lambda copy: (copy / "skills" / "nuclear-plan" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-plan" / "SKILL.md")
                .read_text()
                .replace("proven different family", "any reviewer", 1)
            ),
        ),
        (
            "deleted land different-family precondition",
            lambda copy: (copy / "skills" / "nuclear-land" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-land" / "SKILL.md")
                .read_text()
                .replace("proven\n  different-family approval", "approval", 1)
            ),
        ),
        (
            "deleted same-family substitution ban",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("A same-family pass never substitutes", "Approval stands", 1)
            ),
        ),
        (
            "deleted review quorum gate",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("two reviewers from two different model families", "reviewers", 1)
            ),
        ),
        (
            "deleted break attack substance",
            lambda copy: (copy / "skills" / "nuclear-break" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-break" / "SKILL.md")
                .read_text()
                .replace("the suite MUST go red", "the suite stays green", 1)
            ),
        ),
        (
            "deleted campaign continuity handoff",
            lambda copy: (copy / "skills" / "nuclear-campaign" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-campaign" / "SKILL.md")
                .read_text()
                .replace("never into silence", "and stop", 1)
            ),
        ),
        (
            "deleted land outcome record",
            lambda copy: (copy / "skills" / "nuclear-land" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-land" / "SKILL.md")
                .read_text()
                .replace("merged SHA", "the commit", 1)
            ),
        ),
        (
            "collapsed code fence",
            lambda copy: (copy / "skills" / "nuclear-review" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-review" / "SKILL.md")
                .read_text()
                .replace("```bash", "``bash", 1)
            ),
        ),
        (
            "malformed manifest",
            lambda copy: (copy / ".codex-plugin" / "plugin.json").write_text("{\n"),
        ),
        (
            "missing Agy adapter",
            lambda copy: (copy / "plugin.json").unlink(),
        ),
        (
            "agent-only description",
            lambda copy: (copy / "skills" / "nuclear-scan" / "SKILL.md").write_text(
                (copy / "skills" / "nuclear-scan" / "SKILL.md")
                .read_text()
                .replace(
                    "description: Find ready, blocked, and remaining work without changing anything.",
                    "description: Use when work status needs scanning.",
                    1,
                )
            ),
        ),
        (
            "malformed Codex skill interface",
            lambda copy: (
                copy / "skills" / "nuclear-run" / "agents" / "openai.yaml"
            ).write_text("interface:\n"),
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
            before = _fingerprint(copy)
            mutate(copy)
            if _fingerprint(copy) == before:
                failures.append(f"self-test mutation changed nothing: {label}")
                continue
            if not validate(copy):
                failures.append(f"self-test did not reject: {label}")
    return failures


def _fingerprint(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): path.read_text(errors="replace")
        for path in sorted(root.rglob("*"))
        if path.is_file()
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
