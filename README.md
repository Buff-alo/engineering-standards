# engineering-standards

A modular, version-controlled engineering standards framework for AI-assisted software development.

Instead of scattering duplicated prompt instructions across individual tools, `engineering-standards` separates **universal engineering standards** (`core/`) and **technology stack profiles** (`profiles/`) from **AI coding assistant adapters** (`integrations/`).

---

## Architecture at a Glance

| Layer | Purpose | Examples |
|---|---|---|
| **Core** (`core/`) | Tool-agnostic principles, personas, workflows, quality gates | `ENGINEERING.md`, `PERSONAS.md`, `WORKFLOW.md`, `QUALITY-GATES.md` |
| **Profiles** (`profiles/`) | Stack-specific architecture, security, concurrency, and testing rules | `backend/python-backend.md`, `frontend/nextjs.md`, `systems/rust.md` |
| **Integrations** (`integrations/`) | Thin adapters mapping core + profiles to specific AI tools | `gemini/`, `claude/`, `codex/` |
| **Templates** (`templates/`) | Copy-ready starter files for target repositories | `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `project-profile.md` |
| **Validation** (`scripts/`) | Automated consistency checks for links, metadata, and registries | `validate_profiles.py` |

---

## Explicit Profile Composition

Load `core/` plus **only** the profiles matching your project's verified stack:

### Next.js Application
- [core/ENGINEERING.md](core/ENGINEERING.md)
- [core/PERSONAS.md](core/PERSONAS.md)
- [core/WORKFLOW.md](core/WORKFLOW.md)
- [core/QUALITY-GATES.md](core/QUALITY-GATES.md)
- [profiles/frontend/react.md](profiles/frontend/react.md)
- [profiles/frontend/nextjs.md](profiles/frontend/nextjs.md)

### Django / FastAPI Backend
- [core/ENGINEERING.md](core/ENGINEERING.md)
- [core/PERSONAS.md](core/PERSONAS.md)
- [core/WORKFLOW.md](core/WORKFLOW.md)
- [core/QUALITY-GATES.md](core/QUALITY-GATES.md)
- [profiles/backend/python-backend.md](profiles/backend/python-backend.md)

### Rust + Tauri Desktop Application
- [core/ENGINEERING.md](core/ENGINEERING.md)
- [core/PERSONAS.md](core/PERSONAS.md)
- [core/WORKFLOW.md](core/WORKFLOW.md)
- [core/QUALITY-GATES.md](core/QUALITY-GATES.md)
- [profiles/systems/rust.md](profiles/systems/rust.md)
- [profiles/frontend/react.md](profiles/frontend/react.md)
- [profiles/systems/tauri.md](profiles/systems/tauri.md)

See [docs/profile-selection.md](docs/profile-selection.md) for the full selection guide.

---

## Quick Start

1. **Choose an integration:**
   - Gemini CLI / Antigravity: [integrations/gemini/README.md](integrations/gemini/README.md)
   - Claude Code: [integrations/claude/README.md](integrations/claude/README.md)
   - Codex / `AGENTS.md`: [integrations/codex/README.md](integrations/codex/README.md)
2. **Pin a version in your project:** Copy the matching starter from [templates/](templates/) and optionally add `project-profile.md` for local overrides. See [docs/customization.md](docs/customization.md).
3. **Validate repository standards:**

```bash
python3 scripts/validate_profiles.py --root . --strict
python3 -m unittest discover -s scripts -v
```

---

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Profile Selection & Composition](docs/profile-selection.md)
- [Pinning & Customization](docs/customization.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
