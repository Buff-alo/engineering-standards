# Contributing to engineering-standards

Contributions that improve clarity, correctness, security rigor, and cross-tool consistency are welcome.

---

## Design Principles for Changes

1. **Keep `core/` universal and tool-agnostic.** Framework-specific dependencies, patterns, and CLI commands belong in `profiles/`, never in `core/`.
2. **Keep `integrations/` thin.** Tool adapters (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`) must point to `core/` and `profiles/` rather than duplicating rules.
3. **Avoid machine-local assumptions.** Never commit personal filesystem paths, internal secrets, or unconfigurable local hostnames inside `core/` or `profiles/`.
4. **Preserve explicit precedence.** Project-specific contracts override stack profiles, and safety/security constraints override everything.

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

Run both checks and ensure zero errors or strict-mode warnings:

```bash
python3 scripts/validate_profiles.py --root . --strict
python3 -m unittest discover -s scripts -v
```

Document any breaking or behavioral changes under `[Unreleased]` in [CHANGELOG.md](CHANGELOG.md) following Semantic Versioning.
