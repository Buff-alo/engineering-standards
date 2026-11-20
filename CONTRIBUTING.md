# Contributing to engineering-standards

Contributions that improve clarity, correctness, security rigor, and cross-tool consistency are welcome.

---

## Design Principles for Changes

1. **Keep `core/` universal and tool-agnostic.** Framework-specific dependencies, patterns, and CLI commands belong in `profiles/`, never in `core/`.
2. **Keep `integrations/` thin.** Tool adapters (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`) must point to `core/` and `profiles/` rather than duplicating rules.
3. **Avoid machine-local assumptions.** Never commit personal filesystem paths, internal secrets, or unconfigurable local hostnames inside `core/` or `profiles/`.
4. **Preserve explicit precedence and core invariants.** Project-specific contracts may specialize tooling, versions, and architecture, but MUST NOT silently weaken security, privacy, data integrity, or honest verification invariants. Safety and security constraints override everything.

---

## Adding or Updating a Stack Profile

Every profile under `profiles/<domain>/<name>.md` MUST:

1. Include the standard metadata header:
   - `**ID:** \`<domain>/<name>\``
   - `**Persona:** <Exact persona name from core/PERSONAS.md>`
   - `**Scope:** <Technologies and responsibilities>`
   - `**When to use:** <Clear trigger conditions>`
   - `**Companion profiles:** \`<domain>/<other>.md\` (or \`None\`)`
2. Include the `## Profile Contract` section referencing `core/`.
3. Register the new profile in:
   - [core/QUALITY-GATES.md](core/QUALITY-GATES.md) (Canonical profile registry)
   - [core/WORKFLOW.md](core/WORKFLOW.md) (Profile mapping table)
   - [docs/profile-selection.md](docs/profile-selection.md) (Selection matrix, if applicable)
4. If the profile introduces a new discipline, add its primary persona to [core/PERSONAS.md](core/PERSONAS.md).

---

## Required Verification Before Opening a PR

Run the structural consistency validator, integration/template checks, packaging syntax check, and unit tests, ensuring zero errors or strict-mode warnings:

```bash
python3 scripts/validate_profiles.py --root . --strict
python3 scripts/check_integrations_and_templates.py --root .
python3 -m unittest discover -s scripts -v
bash -n scripts/package_release.sh
```

Document any breaking or behavioral changes under `[Unreleased]` in [CHANGELOG.md](CHANGELOG.md) following Semantic Versioning.

---

## Automated Versioning and Releases

This repository uses `master` as its default integration branch and [Conventional Commits](https://www.conventionalcommits.org/) with `release-please` on `master`:

- `fix: ...` → Patch bump (`1.0.x`)
- `feat: ...` → Minor bump (`1.x.0`)
- `feat!: ...` or `BREAKING CHANGE:` footer → Major bump (`x.0.0`)

Merging qualifying commits to `master` opens or updates a Release PR that synchronizes `VERSION`, `.release-please-manifest.json`, `CHANGELOG.md`, and `core/*.md` version headers. Merging that Release PR automatically creates the `vX.Y.Z` Git tag, publishes the GitHub Release, and attaches `.tar.gz`, `.zip`, and `SHA256SUMS.txt` assets.

> **Note on branch protection:** Because PRs opened with the default `GITHUB_TOKEN` do not trigger `pull_request` workflows (`ci.yml`), `.github/workflows/release.yml` runs the full validation suite before releasing. If you enable required PR status checks on `master`, configure `release.yml` with a GitHub App token so Release PRs trigger `ci.yml` directly.
