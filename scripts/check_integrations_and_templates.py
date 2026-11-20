#!/usr/bin/env python3
"""Verify integration adapters, starter templates, workflows, and release packaging manifest."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

CORE_FILES = (
    "ENGINEERING.md",
    "PERSONAS.md",
    "WORKFLOW.md",
    "QUALITY-GATES.md",
)

INTEGRATION_ADAPTERS = (
    Path("integrations/gemini/GEMINI.md"),
    Path("integrations/claude/CLAUDE.md"),
    Path("integrations/codex/AGENTS.md"),
)

STARTER_TEMPLATES = (
    Path("templates/AGENTS.md"),
    Path("templates/GEMINI.md"),
    Path("templates/CLAUDE.md"),
)

REQUIRED_WORKFLOWS = (
    Path(".github/workflows/ci.yml"),
    Path(".github/workflows/release.yml"),
)

EXPECTED_PACKAGE_DIRS = ("core", "profiles", "integrations", "templates")
EXPECTED_PACKAGE_ROOT_FILES = ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE", "VERSION")
EXPECTED_DEFAULT_BRANCH = "master"
MAX_ADAPTER_LINES = 80


@dataclass(frozen=True)
class CheckFinding:
    """Single integration, template, or workflow check failure."""

    code: str
    path: Path
    message: str

    def format(self) -> str:
        """Render finding in a concise CLI format."""
        return f"[ERROR] {self.code} {self.path} - {self.message}"


def check_integration_adapters(root: Path, findings: list[CheckFinding]) -> None:
    """Ensure every AI tool adapter loads all core files, references profiles, and stays thin."""
    for rel in INTEGRATION_ADAPTERS:
        path = root / rel
        if not path.is_file():
            findings.append(CheckFinding("MISSING_ADAPTER", rel, "Integration adapter file is missing."))
            continue
        text = path.read_text(encoding="utf-8")
        for core_name in CORE_FILES:
            if f"core/{core_name}" not in text:
                findings.append(
                    CheckFinding(
                        "ADAPTER_MISSING_CORE_REF",
                        rel,
                        f"Adapter does not reference 'core/{core_name}'.",
                    )
                )
        if "profiles/" not in text:
            findings.append(
                CheckFinding("ADAPTER_MISSING_PROFILES_REF", rel, "Adapter does not reference 'profiles/'.")
            )
        line_count = len(text.splitlines())
        if line_count > MAX_ADAPTER_LINES:
            findings.append(
                CheckFinding(
                    "ADAPTER_TOO_LARGE",
                    rel,
                    f"Adapter is {line_count} lines (limit {MAX_ADAPTER_LINES}); keep rules in core/ and profiles/.",
                )
            )


def check_templates(root: Path, findings: list[CheckFinding]) -> None:
    """Ensure starter templates use <STANDARDS_ROOT> placeholders and preserve override boundaries."""
    for rel in STARTER_TEMPLATES:
        path = root / rel
        if not path.is_file():
            findings.append(CheckFinding("MISSING_TEMPLATE", rel, "Starter template file is missing."))
            continue
        text = path.read_text(encoding="utf-8")
        for core_name in CORE_FILES:
            expected = f"<STANDARDS_ROOT>/core/{core_name}"
            if expected not in text:
                findings.append(
                    CheckFinding(
                        "TEMPLATE_MISSING_CORE_REF",
                        rel,
                        f"Template does not reference '{expected}'.",
                    )
                )
        if "<STANDARDS_ROOT>/profiles/" not in text:
            findings.append(
                CheckFinding(
                    "TEMPLATE_MISSING_PROFILE_PLACEHOLDER",
                    rel,
                    "Template does not show '<STANDARDS_ROOT>/profiles/' composition placeholder.",
                )
            )
        if "project-profile.md" not in text:
            findings.append(
                CheckFinding(
                    "TEMPLATE_MISSING_OVERRIDE_REF",
                    rel,
                    "Template does not reference 'project-profile.md'.",
                )
            )

    override_rel = Path("templates/project-profile.md")
    override_path = root / override_rel
    if not override_path.is_file():
        findings.append(CheckFinding("MISSING_TEMPLATE", override_rel, "project-profile.md template is missing."))
    else:
        override_text = override_path.read_text(encoding="utf-8")
        if "non-negotiable core invariants" not in override_text.lower():
            findings.append(
                CheckFinding(
                    "TEMPLATE_MISSING_INVARIANT_GUARD",
                    override_rel,
                    "project-profile.md template must state the non-negotiable core invariant boundary.",
                )
            )


def check_workflows_and_packaging(root: Path, findings: list[CheckFinding]) -> None:
    """Check workflow default-branch consistency and release-packaging manifest coverage."""
    branch_line_re = re.compile(r"^\s*-\s*(master|main)\s*$")

    for rel in REQUIRED_WORKFLOWS:
        path = root / rel
        if not path.is_file():
            continue
        branches = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            match = branch_line_re.match(line)
            if match:
                branches.add(match.group(1))
        if branches and branches != {EXPECTED_DEFAULT_BRANCH}:
            findings.append(
                CheckFinding(
                    "WORKFLOW_BRANCH_MISMATCH",
                    rel,
                    f"Workflow targets {sorted(branches)} instead of expected '{EXPECTED_DEFAULT_BRANCH}'.",
                )
            )

    pkg_rel = Path("scripts/package_release.sh")
    pkg_path = root / pkg_rel
    if pkg_path.is_file():
        pkg_text = pkg_path.read_text(encoding="utf-8")
        for item in EXPECTED_PACKAGE_DIRS + EXPECTED_PACKAGE_ROOT_FILES:
            if item not in pkg_text:
                findings.append(
                    CheckFinding(
                        "PACKAGE_MISSING_ENTRY",
                        pkg_rel,
                        f"Release packaging script does not reference required entry '{item}'.",
                    )
                )


def run_checks(root: Path) -> list[CheckFinding]:
    """Run all integration, template, workflow, and packaging checks."""
    findings: list[CheckFinding] = []
    check_integration_adapters(root, findings)
    check_templates(root, findings)
    check_workflows_and_packaging(root, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Check integration adapters, templates, workflows, and release packaging alignment."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Path to engineering-standards repository root (default: .)",
    )
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(f"Error: root path '{args.root}' is not an existing directory.", file=sys.stderr)
        return 2

    findings = run_checks(args.root)
    for finding in findings:
        print(finding.format())

    print(f"Integration & template check summary: {len(findings)} error(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
