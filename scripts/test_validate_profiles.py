"""Unit tests for scripts/validate_profiles.py."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from validate_profiles import main, validate_repository


def build_minimal_valid_repo(root: Path) -> None:
    """Create a minimal valid engineering-standards repository fixture."""
    (root / "core").mkdir(parents=True, exist_ok=True)
    (root / "profiles/backend").mkdir(parents=True, exist_ok=True)
    (root / "integrations/gemini").mkdir(parents=True, exist_ok=True)
    (root / "templates").mkdir(parents=True, exist_ok=True)

    (root / "core/ENGINEERING.md").write_text("# Universal Principles\n", encoding="utf-8")
    (root / "core/PERSONAS.md").write_text(
        "# Personas\n\n## 2. Persona Registry\n\n"
        "| Domain | Primary persona | Responsibilities |\n"
        "|---|---|---|\n"
        "| Python | Senior Backend Engineer | APIs |\n",
        encoding="utf-8",
    )
    (root / "core/WORKFLOW.md").write_text(
        "# Workflow\n\n- `profiles/backend/python-backend.md`\n",
        encoding="utf-8",
    )
    (root / "core/QUALITY-GATES.md").write_text(
        "# Quality Gates\n\n- `profiles/backend/python-backend.md`\n",
        encoding="utf-8",
    )
    (root / "profiles/backend/python-backend.md").write_text(
        "# Python Profile\n\n"
        "**ID:** `backend/python-backend`\n"
        "**Persona:** Senior Backend Engineer\n"
        "**Scope:** Python\n"
        "**When to use:** Python backend\n"
        "**Companion profiles:** `None`\n\n"
        "## Profile Contract\n\nSupplements `core/ENGINEERING.md`.\n",
        encoding="utf-8",
    )


class ValidateProfilesTests(unittest.TestCase):
    """Tests covering positive and negative validation paths."""

    def test_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            findings = validate_repository(root)
            self.assertEqual(findings, [])
            self.assertEqual(main(["--root", str(root), "--strict"]), 0)

    def test_broken_relative_link_and_path_escape_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "core/ENGINEERING.md").write_text(
                "# Principles\n\n"
                "See [missing](NOPE.md) and [escape](../../../etc/passwd).\n"
                "```markdown\n[ignored](DOES_NOT_EXIST.md)\n```\n",
                encoding="utf-8",
            )
            codes = {f.code for f in validate_repository(root)}
            self.assertIn("BROKEN_LINK", codes)
            self.assertIn("PATH_ESCAPE", codes)

    def test_missing_metadata_and_unknown_persona_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "profiles/backend/python-backend.md").write_text(
                "# Python Profile\n\n"
                "**ID:** `backend/wrong-id`\n"
                "**Persona:** Imaginary Persona\n"
                "**Companion profiles:** `backend/does-not-exist.md`\n\n"
                "## Profile Contract\n",
                encoding="utf-8",
            )
            codes = {f.code for f in validate_repository(root)}
            self.assertIn("MISSING_FIELD", codes)
            self.assertIn("ID_MISMATCH", codes)
            self.assertIn("UNKNOWN_PERSONA", codes)
            self.assertIn("MISSING_COMPANION", codes)

    def test_registry_mismatch_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "core/QUALITY-GATES.md").write_text(
                "# Quality Gates\n\n- `profiles/backend/ghost.md`\n",
                encoding="utf-8",
            )
            codes = {f.code for f in validate_repository(root)}
            self.assertIn("UNREGISTERED_PROFILE", codes)
            self.assertIn("STALE_REGISTRY_ENTRY", codes)

    def test_host_path_leak_and_crlf_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "core/ENGINEERING.md").write_bytes(
                b"# Principles\r\n\r\nCheck ~/.gemini/profiles/foo.md\r\n"
            )
            codes = {f.code for f in validate_repository(root)}
            self.assertIn("CRLF_LINE_ENDING", codes)
            self.assertIn("HOST_PATH_LEAK", codes)

    def test_missing_root_returns_exit_2(self) -> None:
        self.assertEqual(main(["--root", "/nonexistent/path/xyz123"]), 2)

    def test_version_sync_passes_when_aligned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
            (root / ".release-please-manifest.json").write_text('{\n  ".": "1.2.3"\n}\n', encoding="utf-8")
            (root / "core/ENGINEERING.md").write_text(
                "# Universal Principles\n\n**Version:** 1.2.3 (Constitution Heritage: v3.0) <!-- x-release-please-version -->\n",
                encoding="utf-8",
            )
            (root / "core/PERSONAS.md").write_text(
                "# Personas\n\n**Version:** 1.2.3 <!-- x-release-please-version -->\n\n## 2. Persona Registry\n\n"
                "| Domain | Primary persona | Responsibilities |\n"
                "|---|---|---|\n"
                "| Python | Senior Backend Engineer | APIs |\n",
                encoding="utf-8",
            )
            (root / "core/WORKFLOW.md").write_text(
                "# Workflow\n\n**Version:** 1.2.3 <!-- x-release-please-version -->\n\n- `profiles/backend/python-backend.md`\n",
                encoding="utf-8",
            )
            (root / "core/QUALITY-GATES.md").write_text(
                "# Quality Gates\n\n**Version:** 1.2.3 <!-- x-release-please-version -->\n\n- `profiles/backend/python-backend.md`\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_repository(root), [])

    def test_version_sync_detects_mismatches_and_invalid_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_minimal_valid_repo(root)
            (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
            (root / ".release-please-manifest.json").write_text('{\n  ".": "1.2.0"\n}\n', encoding="utf-8")
            (root / "core/ENGINEERING.md").write_text(
                "# Universal Principles\n\n**Version:** 1.0.0\n",
                encoding="utf-8",
            )
            codes = {f.code for f in validate_repository(root)}
            self.assertIn("VERSION_MISMATCH", codes)

            (root / "VERSION").write_text("not-a-semver\n", encoding="utf-8")
            codes_invalid = {f.code for f in validate_repository(root)}
            self.assertIn("INVALID_VERSION", codes_invalid)


if __name__ == "__main__":
    unittest.main()
