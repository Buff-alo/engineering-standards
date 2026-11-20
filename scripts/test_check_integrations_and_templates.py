"""Unit tests for scripts/check_integrations_and_templates.py."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from check_integrations_and_templates import main, run_checks


def build_valid_integration_fixture(root: Path) -> None:
    """Create minimal valid integrations, templates, workflows, and packaging script."""
    for rel in (
        "integrations/gemini/GEMINI.md",
        "integrations/claude/CLAUDE.md",
        "integrations/codex/AGENTS.md",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "core/ENGINEERING.md\ncore/PERSONAS.md\ncore/WORKFLOW.md\ncore/QUALITY-GATES.md\nprofiles/\n",
            encoding="utf-8",
        )

    for rel in ("templates/AGENTS.md", "templates/GEMINI.md", "templates/CLAUDE.md"):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "<STANDARDS_ROOT>/core/ENGINEERING.md\n"
            "<STANDARDS_ROOT>/core/PERSONAS.md\n"
            "<STANDARDS_ROOT>/core/WORKFLOW.md\n"
            "<STANDARDS_ROOT>/core/QUALITY-GATES.md\n"
            "<STANDARDS_ROOT>/profiles/<domain>/<profile>.md\n"
            "./project-profile.md\n",
            encoding="utf-8",
        )

    (root / "templates/project-profile.md").write_text(
        "# Project\n\nMUST NOT silently weaken non-negotiable core invariants.\n",
        encoding="utf-8",
    )

    wf_dir = root / ".github/workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    (wf_dir / "ci.yml").write_text("on:\n  push:\n    branches:\n      - master\n", encoding="utf-8")
    (wf_dir / "release.yml").write_text("on:\n  push:\n    branches:\n      - master\n", encoding="utf-8")

    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts/package_release.sh").write_text(
        "core profiles integrations templates README.md CHANGELOG.md CONTRIBUTING.md LICENSE VERSION\n",
        encoding="utf-8",
    )


class CheckIntegrationsAndTemplatesTests(unittest.TestCase):
    """Tests covering positive and negative integration/template/workflow checks."""

    def test_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_integration_fixture(root)
            self.assertEqual(run_checks(root), [])
            self.assertEqual(main(["--root", str(root)]), 0)

    def test_missing_core_ref_in_adapter_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_integration_fixture(root)
            (root / "integrations/claude/CLAUDE.md").write_text(
                "core/ENGINEERING.md\nprofiles/\n",
                encoding="utf-8",
            )
            codes = {f.code for f in run_checks(root)}
            self.assertIn("ADAPTER_MISSING_CORE_REF", codes)

    def test_missing_invariant_guard_and_branch_mismatch_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_integration_fixture(root)
            (root / "templates/project-profile.md").write_text("# Project\n", encoding="utf-8")
            (root / ".github/workflows/ci.yml").write_text(
                "on:\n  push:\n    branches:\n      - main\n",
                encoding="utf-8",
            )
            codes = {f.code for f in run_checks(root)}
            self.assertIn("TEMPLATE_MISSING_INVARIANT_GUARD", codes)
            self.assertIn("WORKFLOW_BRANCH_MISMATCH", codes)

    def test_missing_root_returns_exit_2(self) -> None:
        self.assertEqual(main(["--root", "/nonexistent/path/xyz123"]), 2)


if __name__ == "__main__":
    unittest.main()
