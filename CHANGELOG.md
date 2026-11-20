# Changelog

All notable changes to `engineering-standards` are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0](https://github.com/Buff-alo/engineering-standards/compare/v1.0.0...v1.1.0) (2026-11-20)


### Features

* strengthen validation, template checks, and release packaging ([386a78f](https://github.com/Buff-alo/engineering-standards/commit/386a78fe4b5193e6f7981ff2e98ef64d381408b0))


### Bug Fixes

* enforce non-negotiable invariants and Laravel lifecycle ([8939a13](https://github.com/Buff-alo/engineering-standards/commit/8939a13beb30f8ef2516f6e0c249d077719a82d3))

## [1.0.0] - 2026-11-20

### Added
- Initial standalone `engineering-standards` framework repository derived from Universal Engineering Constitution v3.0.
- Modular `core/` standards layer:
  - `core/ENGINEERING.md` (mission, architecture, data integrity, security, dependencies, ops, API contracts)
  - `core/PERSONAS.md` (persona selection rules and 10-entry persona registry)
  - `core/WORKFLOW.md` (repository discovery, stack detection, explicit composition, conflict precedence, implementation workflow, Planning Output Standard)
  - `core/QUALITY-GATES.md` (verification expectations, completion report contract, canonical profile registry)
- Categorized and normalized stack profiles under `profiles/`:
  - `backend/python-backend.md`, `backend/java-springboot.md`, `backend/php-laravel.md`
  - `frontend/react.md`, `frontend/nextjs.md`
  - `mobile/react-native.md`
  - `systems/rust.md`, `systems/tauri.md`
  - `infrastructure/devsecops.md`
  - `ai/ai-llm.md`
- Thin AI assistant adapters in `integrations/gemini/`, `integrations/claude/`, and `integrations/codex/`.
- Copy-ready project starter templates in `templates/` (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `project-profile.md`).
- Architecture, profile selection, and customization documentation in `docs/`.
- Zero-dependency validator and unit test suite (`scripts/validate_profiles.py`, `scripts/test_validate_profiles.py`).

### Fixed
- Removed duplicate `# React Engineering Profile` header from `profiles/frontend/nextjs.md`.
- Removed redundant top preamble from `profiles/frontend/react.md`.
- Aligned persona names across `core/PERSONAS.md`, `profiles/backend/java-springboot.md`, and `profiles/systems/tauri.md`.
- Updated `profiles/backend/php-laravel.md` container infrastructure reference to `profiles/infrastructure/devsecops.md`.
- Normalized CRLF line endings to LF in `profiles/infrastructure/devsecops.md`.
- Replaced machine-local profile paths with repository-relative paths across `core/` and `profiles/`.
