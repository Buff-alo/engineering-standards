#!/usr/bin/env python3
"""Validate engineering-standards repository structure, profiles, links, and hygiene."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Literal

Severity = Literal["ERROR", "WARNING"]

REQUIRED_CORE_FILES = (
    Path("core/ENGINEERING.md"),
    Path("core/PERSONAS.md"),
    Path("core/WORKFLOW.md"),
    Path("core/QUALITY-GATES.md"),
)

REQUIRED_PROFILE_FIELDS = (
    "ID",
    "Persona",
    "Scope",
    "When to use",
    "Companion profiles",
)

LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BACKTICK_PATH_RE = re.compile(r"`((?:core|profiles)/[A-Za-z0-9_./-]+\.md)`")
FIELD_RE = re.compile(r"^\*\*([A-Za-z ]+):\*\*\s*(.+?)\s*$")
PROFILE_PATH_RE = re.compile(r"profiles/[a-z0-9-]+/[a-z0-9-]+\.md")
HOST_PATH_PATTERNS = (
    re.compile(r"/Users/"),
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"~/\.gemini"),
    re.compile(r"~/\.claude"),
)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
CORE_VERSION_RE = re.compile(r"^\*\*Version:\*\*\s*([^\s<(]+)")


@dataclass(frozen=True)
class ValidationFinding:
    """Single validation issue discovered in the repository."""

    severity: Severity
    code: str
    path: Path
    line: int
    message: str

    def format(self) -> str:
        """Render finding in a concise CLI format."""
        loc = f"{self.path}:{self.line}" if self.line > 0 else str(self.path)
        return f"[{self.severity}] {self.code} {loc} - {self.message}"


def iter_non_fenced_lines(text: str) -> Iterable[tuple[int, str]]:
    """Yield (1-based line_no, line) outside triple-backtick fenced code blocks."""
    in_fence = False
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield idx, line


def extract_personas(personas_file: Path) -> set[str]:
    """Parse primary persona names from core/PERSONAS.md registry table."""
    if not personas_file.is_file():
        return set()
    personas: set[str] = set()
    in_registry = False
    for _, line in iter_non_fenced_lines(personas_file.read_text(encoding="utf-8")):
        stripped = line.strip()
        if stripped.startswith("## 2. Persona Registry"):
            in_registry = True
            continue
        if in_registry and stripped.startswith("## "):
            break
        if in_registry and stripped.startswith("|") and not stripped.startswith("|---"):
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cols) >= 2 and cols[0] != "Domain":
                personas.add(cols[1])
    return personas


def extract_profile_metadata(text: str) -> dict[str, tuple[int, str]]:
    """Extract **Key:** Value header fields outside fenced code blocks."""
    fields: dict[str, tuple[int, str]] = {}
    for line_no, line in iter_non_fenced_lines(text):
        match = FIELD_RE.match(line.strip())
        if match:
            key = match.group(1).strip()
            val = match.group(2).strip()
            if key not in fields:
                fields[key] = (line_no, val)
        if line.strip().startswith("## 1."):
            break
    return fields


def check_structure(root: Path, findings: list[ValidationFinding]) -> None:
    """Verify required top-level directories and core files exist and are non-empty."""
    for rel_path in REQUIRED_CORE_FILES:
        target = root / rel_path
        if not target.is_file():
            findings.append(
                ValidationFinding("ERROR", "MISSING_CORE_FILE", rel_path, 0, "Required core file is missing.")
            )
        elif not target.read_text(encoding="utf-8").strip():
            findings.append(
                ValidationFinding("ERROR", "EMPTY_FILE", rel_path, 0, "Required core file is empty.")
            )

    for rel_dir in (Path("profiles"), Path("integrations"), Path("templates")):
        target_dir = root / rel_dir
        if not target_dir.is_dir():
            findings.append(
                ValidationFinding("ERROR", "MISSING_DIR", rel_dir, 0, "Required directory is missing.")
            )


def discover_profiles(root: Path, findings: list[ValidationFinding]) -> list[Path]:
    """Return sorted repo-relative paths of profile files under profiles/<domain>/<name>.md."""
    profiles_dir = root / "profiles"
    if not profiles_dir.is_dir():
        return []

    discovered: list[Path] = []
    for path in sorted(profiles_dir.rglob("*.md")):
        rel = path.relative_to(root)
        if len(rel.parts) != 3:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "INVALID_PROFILE_LOCATION",
                    rel,
                    0,
                    "Profiles must live at profiles/<domain>/<name>.md.",
                )
            )
            continue
        discovered.append(rel)
    return discovered


def check_profiles(
    root: Path,
    profile_paths: list[Path],
    known_personas: set[str],
    findings: list[ValidationFinding],
) -> None:
    """Validate metadata contract, persona alignment, and companion links for every profile."""
    profile_set = set(profile_paths)

    for rel in profile_paths:
        text = (root / rel).read_text(encoding="utf-8")
        fields = extract_profile_metadata(text)

        for required in REQUIRED_PROFILE_FIELDS:
            if required not in fields:
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "MISSING_FIELD",
                        rel,
                        0,
                        f"Missing required metadata field '**{required}:**'.",
                    )
                )

        if "ID" in fields:
            line_no, raw_id = fields["ID"]
            clean_id = raw_id.strip("`")
            expected_id = f"{rel.parts[1]}/{rel.stem}"
            if clean_id != expected_id:
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "ID_MISMATCH",
                        rel,
                        line_no,
                        f"Profile ID '{clean_id}' does not match path '{expected_id}'.",
                    )
                )

        if "Persona" in fields and known_personas:
            line_no, persona = fields["Persona"]
            if persona not in known_personas:
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "UNKNOWN_PERSONA",
                        rel,
                        line_no,
                        f"Persona '{persona}' is not listed in core/PERSONAS.md.",
                    )
                )

        if "Companion profiles" in fields:
            line_no, companions_raw = fields["Companion profiles"]
            if companions_raw.strip("`").lower() != "none":
                for item in [c.strip().strip("`") for c in companions_raw.split(",")]:
                    if not item:
                        continue
                    candidate = Path("profiles") / item if not item.startswith("profiles/") else Path(item)
                    if candidate not in profile_set:
                        findings.append(
                            ValidationFinding(
                                "ERROR",
                                "MISSING_COMPANION",
                                rel,
                                line_no,
                                f"Companion profile '{item}' does not exist at '{candidate}'.",
                            )
                        )

        if "## Profile Contract" not in text:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "MISSING_CONTRACT",
                    rel,
                    0,
                    "Profile is missing '## Profile Contract' section.",
                )
            )

        h1_lines = [
            ln for ln, line in iter_non_fenced_lines(text) if line.startswith("# ")
        ]
        if len(h1_lines) != 1:
            findings.append(
                ValidationFinding(
                    "WARNING",
                    "MULTIPLE_H1" if len(h1_lines) > 1 else "MISSING_H1",
                    rel,
                    h1_lines[0] if h1_lines else 0,
                    f"Expected exactly 1 H1 heading, found {len(h1_lines)}.",
                )
            )


def check_registries(
    root: Path,
    profile_paths: list[Path],
    findings: list[ValidationFinding],
) -> None:
    """Verify core/QUALITY-GATES.md and core/WORKFLOW.md list all and only existing profiles."""
    actual = {str(p.as_posix()) for p in profile_paths}

    registry_files = (
        Path("core/QUALITY-GATES.md"),
        Path("core/WORKFLOW.md"),
    )

    for rel_file in registry_files:
        full_path = root / rel_file
        if not full_path.is_file():
            continue
        text = full_path.read_text(encoding="utf-8")
        referenced = set(PROFILE_PATH_RE.findall(text))

        for missing_from_doc in sorted(actual - referenced):
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "UNREGISTERED_PROFILE",
                    rel_file,
                    0,
                    f"Profile '{missing_from_doc}' exists on disk but is missing from {rel_file}.",
                )
            )

        for missing_on_disk in sorted(referenced - actual):
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "STALE_REGISTRY_ENTRY",
                    rel_file,
                    0,
                    f"Registered profile '{missing_on_disk}' does not exist on disk.",
                )
            )


def check_links_and_hygiene(root: Path, findings: list[ValidationFinding]) -> None:
    """Check Markdown links, repo-relative backtick paths, CRLF endings, and host-path leaks."""
    resolved_root = root.resolve()

    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root)

        if path.suffix in {".md", ".py"}:
            raw_bytes = path.read_bytes()
            if b"\r" in raw_bytes:
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "CRLF_LINE_ENDING",
                        rel,
                        0,
                        "File contains CR/CRLF line endings; use LF.",
                    )
                )

        if path.suffix != ".md":
            continue

        text = path.read_text(encoding="utf-8")
        in_normative_layer = rel.parts[0] in {"core", "profiles"}

        for line_no, line in iter_non_fenced_lines(text):
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path_str = target.split("#", 1)[0]
                if not target_path_str:
                    continue
                candidate = (path.parent / target_path_str).resolve()
                if not candidate.is_relative_to(resolved_root):
                    findings.append(
                        ValidationFinding(
                            "ERROR",
                            "PATH_ESCAPE",
                            rel,
                            line_no,
                            f"Link '{target}' resolves outside repository root.",
                        )
                    )
                    continue
                if not candidate.exists():
                    findings.append(
                        ValidationFinding(
                            "ERROR",
                            "BROKEN_LINK",
                            rel,
                            line_no,
                            f"Broken relative link '{target}'.",
                        )
                    )

            for match in BACKTICK_PATH_RE.finditer(line):
                quoted = match.group(1)
                if "<" in quoted or "*" in quoted:
                    continue
                target = (root / quoted).resolve()
                if not target.is_relative_to(resolved_root) or not target.exists():
                    findings.append(
                        ValidationFinding(
                            "ERROR",
                            "BROKEN_REFERENCE",
                            rel,
                            line_no,
                            f"Referenced path '{quoted}' does not exist.",
                        )
                    )

            if in_normative_layer:
                for pat in HOST_PATH_PATTERNS:
                    if pat.search(line):
                        findings.append(
                            ValidationFinding(
                                "ERROR",
                                "HOST_PATH_LEAK",
                                rel,
                                line_no,
                                f"Machine-local path pattern '{pat.pattern}' is not allowed in {rel.parts[0]}/.",
                            )
                        )


def check_version_sync(root: Path, findings: list[ValidationFinding]) -> None:
    """Verify VERSION, .release-please-manifest.json, and core/*.md versions stay aligned."""
    version_file = root / "VERSION"
    manifest_file = root / ".release-please-manifest.json"

    if not version_file.exists() and not manifest_file.exists():
        return

    canonical_version: str | None = None
    if not version_file.is_file():
        findings.append(
            ValidationFinding("ERROR", "MISSING_VERSION_FILE", Path("VERSION"), 0, "VERSION file is missing.")
        )
    else:
        raw_version = version_file.read_text(encoding="utf-8").strip()
        if not SEMVER_RE.match(raw_version):
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "INVALID_VERSION",
                    Path("VERSION"),
                    1,
                    f"VERSION '{raw_version}' is not a valid SemVer string.",
                )
            )
        else:
            canonical_version = raw_version

    if not manifest_file.is_file():
        findings.append(
            ValidationFinding(
                "ERROR",
                "MISSING_MANIFEST",
                Path(".release-please-manifest.json"),
                0,
                ".release-please-manifest.json is missing.",
            )
        )
    else:
        try:
            manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "INVALID_MANIFEST",
                    Path(".release-please-manifest.json"),
                    1,
                    f"Invalid JSON in .release-please-manifest.json: {exc}.",
                )
            )
        else:
            manifest_version = manifest_data.get(".") if isinstance(manifest_data, dict) else None
            if not isinstance(manifest_version, str) or not SEMVER_RE.match(manifest_version):
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "INVALID_MANIFEST",
                        Path(".release-please-manifest.json"),
                        1,
                        "Manifest '.' entry must be a valid SemVer string.",
                    )
                )
            elif canonical_version is not None and manifest_version != canonical_version:
                findings.append(
                    ValidationFinding(
                        "ERROR",
                        "VERSION_MISMATCH",
                        Path(".release-please-manifest.json"),
                        1,
                        f"Manifest version '{manifest_version}' does not match VERSION '{canonical_version}'.",
                    )
                )

    if canonical_version is None:
        return

    for rel_core in REQUIRED_CORE_FILES:
        core_path = root / rel_core
        if not core_path.is_file():
            continue
        found_line: int | None = None
        found_version: str | None = None
        for line_no, line in iter_non_fenced_lines(core_path.read_text(encoding="utf-8")):
            match = CORE_VERSION_RE.match(line.strip())
            if match:
                found_line = line_no
                found_version = match.group(1)
                break
        if found_version is None:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "VERSION_MISMATCH",
                    rel_core,
                    0,
                    f"Missing '**Version:** {canonical_version}' header.",
                )
            )
        elif found_version != canonical_version:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    "VERSION_MISMATCH",
                    rel_core,
                    found_line or 0,
                    f"Header version '{found_version}' does not match VERSION '{canonical_version}'.",
                )
            )


def validate_repository(root: Path) -> list[ValidationFinding]:
    """Run all validation checks against root and return findings."""
    findings: list[ValidationFinding] = []
    check_structure(root, findings)
    known_personas = extract_personas(root / "core/PERSONAS.md")
    profile_paths = discover_profiles(root, findings)
    check_profiles(root, profile_paths, known_personas, findings)
    check_registries(root, profile_paths, findings)
    check_links_and_hygiene(root, findings)
    check_version_sync(root, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Validate engineering-standards repository structure, profiles, and links."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Path to engineering-standards repository root (default: .)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (non-zero exit code).",
    )
    args = parser.parse_args(argv)

    root = args.root
    if not root.is_dir():
        print(f"Error: root path '{root}' is not an existing directory.", file=sys.stderr)
        return 2

    findings = validate_repository(root)
    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARNING"]

    for finding in findings:
        print(finding.format())

    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s).")
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
