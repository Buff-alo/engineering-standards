# Design & Implementation Plan: `engineering-standards` Repository

**Status:** Approved Design (Brainstorming Complete)  
**Target Version:** `1.0.0` (derived from Universal Engineering Constitution v3.0)  
**Date:** 2026-11-20  

---

## 1. Understanding Summary

- **What is being built:** A standalone, version-controlled `engineering-standards` Git repository that separates universal, tool-agnostic software engineering standards (`core/`) and technology stack profiles (`profiles/`) from AI coding assistant adapters (`integrations/`), supported by project templates (`templates/`), guides (`docs/`), and a zero-dependency Python validation script (`scripts/validate_profiles.py`).
- **Why it exists:** To evolve `~/.gemini/ENGINEERING.md` and `~/.gemini/profiles/` out of a machine-local configuration directory into a modular, testable, reusable standards framework that avoids rule duplication across Gemini CLI, Claude Code, and Codex.
- **Who it is for:** The repository owner across personal and production projects, structured as a **Hybrid** framework—universal core + opinionated, customizable stack profiles—so external developers or teams can also adopt, pin, or fork it.
- **Key constraints:**
  - **Non-destructive migration:** Leave `~/.gemini/` completely untouched during initial creation.
  - **Normalize and modularize:** Split `ENGINEERING.md` into cohesive `core/` files and normalize the 10 existing profiles into categorized `profiles/` subdirectories without losing any existing rules.
  - **Scope:** Deliver Phases 1–4 locally (foundation, profiles, integrations, validation & documentation, plus `git init`) without pushing to a remote yet.
- **Explicit non-goals:**
  - No complex CLI profile generator/installer automation in v1.0.0.
  - No automated modification or symlinking of `~/.gemini/`.
  - No inventing new technology profiles beyond the 10 existing profiles.

---

## 2. Assumptions

1. **Runtime & Dependencies:** `scripts/validate_profiles.py` and its test suite use Python 3 standard library only (`pathlib`, `re`, `argparse`, `sys`, `unittest`), requiring zero `pip` installs.
2. **Tool Integrations:** Phase 3 includes thin adapters for Gemini CLI (`integrations/gemini/`), Claude Code (`integrations/claude/`), and Codex (`integrations/codex/`).
3. **Licensing & Versioning:** MIT `LICENSE` and Semantic Versioning starting at `1.0.0` (documenting Constitution v3.0 heritage in `CHANGELOG.md`).
4. **Planning Standard Preservation:** The `Planning Output Standard` (`docs/plans/<feature-name>.md`) from `~/.gemini/GEMINI.md` is incorporated into `core/WORKFLOW.md` so it applies across tools.

---

## 3. Decision Log

| # | Decision | Alternatives Considered | Why Chosen |
|---|---|---|---|
| 1 | **Hybrid positioning** (universal core + opinionated customizable profiles) | Purely personal system; purely neutral public framework | Preserves high-signal stack opinions (e.g., `uv`, Django Ninja, Next.js App Router) while staying portable and forkable. |
| 2 | **Deliver Phases 1–4 locally** (`git init`, no remote push) | Phases 1–2 only; Phases 1–5 with GitHub push | Gives a complete, validated, versioned repository ready for review before publishing. |
| 3 | **Non-destructive copy** from `~/.gemini/` | Immediate symlink/update of `~/.gemini/`; move & archive | Eliminates risk of breaking the active local Gemini setup before the new repo is reviewed. |
| 4 | **Option A: Modular `core/` + categorized `profiles/` + thin `integrations/`** | Monolithic `core/ENGINEERING.md`; YAML/script-compiled generator | Clean separation of concerns, selective loading (`core/*` + needed `profiles/*`), zero build complexity (YAGNI). |
| 5 | **Normalize headers/metadata & fix drift** during migration | Verbatim copy; full rewrite | Fixes real defects (`nextjs.md` duplicate header, `AGENTS.md`/`ENGINEERING.md` drift, CRLF in `devsecops.md`, `~/.gemini/` hardcoded paths) while keeping 100% of existing rules. |

---

## 4. Final Architecture & Design

```text
engineering-standards/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── core/
│   ├── ENGINEERING.md      # Principles, architecture, concurrency, security, deps, ops, contracts
│   ├── PERSONAS.md         # Persona selection rules, behavioral expectations, 9-domain registry
│   ├── WORKFLOW.md         # Discovery, stack detection, profile loading, task types, workflow, planning standard
│   └── QUALITY-GATES.md    # Testing expectations, verification sequence, completion report, profile registry
├── profiles/
│   ├── backend/
│   │   ├── python-backend.md
│   │   ├── java-springboot.md
│   │   └── php-laravel.md
│   ├── frontend/
│   │   ├── react.md
│   │   └── nextjs.md
│   ├── mobile/
│   │   └── react-native.md
│   ├── systems/
│   │   ├── rust.md
│   │   └── tauri.md
│   ├── infrastructure/
│   │   └── devsecops.md
│   └── ai/
│       └── ai-llm.md
├── templates/
│   ├── AGENTS.md
│   ├── GEMINI.md
│   ├── CLAUDE.md
│   └── project-profile.md
├── integrations/
│   ├── gemini/ (GEMINI.md, README.md)
│   ├── claude/ (CLAUDE.md, README.md)
│   └── codex/  (AGENTS.md, README.md)
├── docs/
│   ├── architecture.md
│   ├── profile-selection.md
│   ├── customization.md
│   └── plans/
│       └── engineering-standards-repo.md
└── scripts/
    ├── validate_profiles.py
    └── test_validate_profiles.py
```

---

## 5. System & Security Constraints

- **Portability & Privacy (No Host-Path or Secret Leaks):**
  - `core/` and `profiles/` MUST NOT contain machine-specific paths (`/Users/...`, `C:\...`, `~/.gemini/...`), personal usernames, tokens, or credentials.
  - Machine-local wiring instructions (e.g., linking `~/.gemini/GEMINI.md`) are isolated strictly to `integrations/*/README.md` and `docs/customization.md`.
- **Input Validation & Safe Path Handling (`scripts/validate_profiles.py`):**
  - Validate `--root` as an existing directory before scanning.
  - Resolve all relative Markdown link targets with `Path.resolve()` and enforce containment within `root.resolve()` (`is_relative_to`) so path-traversal links (e.g., `../../../../etc/passwd`) are flagged as validation errors rather than read.
  - Skip fenced code blocks (` ``` `) when extracting links/paths to prevent false positives on example snippets.
- **Line-Ending & Encoding Hygiene:**
  - All Markdown and Python files MUST be UTF-8 with LF (`\n`) line endings (removing existing CRLF in `devsecops.md`).
- **Conflict Precedence Invariant:**
  - Precedence order remains immutable across all integrations and profiles: (1) Platform/safety/security constraints → (2) Explicit task requirements → (3) Project-specific contracts/`project-profile.md` → (4) `core/*` → (5) Applicable `profiles/*` → (6) General preferences.

---

## 6. Data & API Contracts

### 6.1 Profile Metadata & Contract Schema (`profiles/<domain>/<name>.md`)

Every profile file MUST begin with the following structured header contract:

```markdown
# <Human-Readable Title> Engineering Profile

**ID:** `<domain>/<name>`
**Persona:** <Exact Primary Persona name matching core/PERSONAS.md>
**Scope:** <Comma-separated technologies and responsibilities>
**When to use:** <Explicit stack/task trigger conditions>
**Companion profiles:** `<domain>/<other>.md` (or `None`)

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`.

If rules conflict, follow the precedence order in `core/WORKFLOW.md`:
1. Applicable platform, safety, and security constraints.
2. Explicit task requirements.
3. Repository-specific instructions and established project contracts.
4. Universal standards in `core/`.
5. This profile and any required companion profiles.
6. Existing project conventions unless explicitly changed.
```

### 6.2 `core/QUALITY-GATES.md` Registry Contract

The canonical profile registry in `core/QUALITY-GATES.md` MUST list every profile using repo-relative paths (`profiles/<domain>/<name>.md`) in a Markdown table or bullet list parseable by `validate_profiles.py`:

```markdown
- `profiles/backend/python-backend.md` — ...
```

### 6.3 Validator CLI & JSON/Exit Contract (`scripts/validate_profiles.py`)

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Severity = Literal["ERROR", "WARNING"]

@dataclass(frozen=True)
class ValidationFinding:
    severity: Severity
    code: str        # e.g., "MISSING_FIELD", "BROKEN_LINK", "PATH_ESCAPE", "REGISTRY_MISMATCH", "HOST_PATH_LEAK", "CRLF_LINE_ENDING"
    path: Path       # Repo-relative file path
    line: int        # 1-based line number (0 if file-level)
    message: str

# CLI interface:
# python3 scripts/validate_profiles.py [--root PATH] [--strict]
# Exit codes:
#   0 -> 0 errors (and 0 warnings if --strict)
#   1 -> >= 1 error (or >= 1 warning when --strict is set)
#   2 -> invalid CLI arguments or missing --root directory
```

---

## 7. File-by-File Execution Checklist

### Phase 1 — Core Foundation (`core/`)
1. `core/ENGINEERING.md` — Extract Sections 1, 5, 6, 7, 8, 10, 11 from `~/.gemini/ENGINEERING.md`; replace `AGENTS.md`/`~/.gemini` references with `core/` terminology. *Acceptance:* All rules from those 7 sections preserved verbatim/cleanly; zero host paths.
2. `core/PERSONAS.md` — Extract Section 2 (Persona Selection, 9-domain Registry, Selection Rules, Behavioral Expectations). *Acceptance:* Exact 9 persona names match profile `**Persona:**` headers.
3. `core/WORKFLOW.md` — Extract Sections 3, 4, 12 + `Planning Output Standard` from `~/.gemini/GEMINI.md`; update profile mapping table to `profiles/<domain>/<name>.md`. *Acceptance:* Covers discovery, stack detection, explicit composition, precedence, task types, 9-step workflow, planning standard.
4. `core/QUALITY-GATES.md` — Extract Sections 9, 13, 14; update canonical profile registry to `profiles/<domain>/<name>.md`. *Acceptance:* All 10 profiles listed accurately.

### Phase 2 — Categorized & Normalized Profiles (`profiles/`)
5. `profiles/backend/python-backend.md` — Migrate `~/.gemini/profiles/python-backend.md` with standard header contract (`ID: backend/python-backend`).
6. `profiles/backend/java-springboot.md` — Migrate `~/.gemini/profiles/java-springboot.md` (`ID: backend/java-springboot`).
7. `profiles/backend/php-laravel.md` — Migrate `~/.gemini/profiles/php-laravel.md` (`ID: backend/php-laravel`); fix line 542 reference to `profiles/infrastructure/devsecops.md`.
8. `profiles/frontend/react.md` — Migrate `~/.gemini/profiles/react.md` (`ID: frontend/react`); remove redundant top `# React Engineering Profile` preamble; point Next.js references to `profiles/frontend/nextjs.md`.
9. `profiles/frontend/nextjs.md` — Migrate `~/.gemini/profiles/nextjs.md` (`ID: frontend/nextjs`, `Companion profiles: frontend/react.md`); remove duplicate `# React Engineering Profile` header (lines 1–12).
10. `profiles/mobile/react-native.md` — Migrate `~/.gemini/profiles/react-native.md` (`ID: mobile/react-native`).
11. `profiles/systems/rust.md` — Migrate `~/.gemini/profiles/rust.md` (`ID: systems/rust`).
12. `profiles/systems/tauri.md` — Migrate `~/.gemini/profiles/tauri.md` (`ID: systems/tauri`, `Companion profiles: systems/rust.md, frontend/react.md`).
13. `profiles/infrastructure/devsecops.md` — Migrate `~/.gemini/profiles/devsecops.md` (`ID: infrastructure/devsecops`); normalize CRLF to LF; label `dev_postgres`/`universal_dev_network` clearly as opinionated local defaults.
14. `profiles/ai/ai-llm.md` — Migrate `~/.gemini/profiles/ai-llm.md` (`ID: ai/ai-llm`).

### Phase 3 — Integrations & Templates (`integrations/`, `templates/`)
15. `integrations/gemini/GEMINI.md` & `integrations/gemini/README.md` — Thin Gemini CLI / Antigravity adapter referencing `core/` and `profiles/`, plus local setup instructions.
16. `integrations/claude/CLAUDE.md` & `integrations/claude/README.md` — Thin Claude Code adapter referencing `core/` and `profiles/`.
17. `integrations/codex/AGENTS.md` & `integrations/codex/README.md` — Thin Codex adapter referencing `core/` and `profiles/`.
18. `templates/AGENTS.md`, `templates/GEMINI.md`, `templates/CLAUDE.md`, `templates/project-profile.md` — Copy-ready starter templates showing explicit profile composition and project-level overrides.

### Phase 4 — Docs, Root Metadata, Validation & Git Init
19. `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md` — Repo overview, composition examples, MIT license, v1.0.0 changelog, contribution & review checklist.
20. `docs/architecture.md`, `docs/profile-selection.md`, `docs/customization.md` — Two-layer model, stack composition guide, pinning & customization guide.
21. `scripts/validate_profiles.py` & `scripts/test_validate_profiles.py` — Implement validator + unit tests covering valid repos, broken links, path traversal, missing metadata, registry mismatches, CRLF, and host-path leaks.
22. Initialize Git repository (`git init`) and verify clean working status / initial check pass.

---

## 8. Verification Commands

Run after completing all files:

```bash
# 1. Run validator unit tests
python3 -m unittest discover -s scripts -v

# 2. Validate the repository strictly
python3 scripts/validate_profiles.py --root . --strict

# 3. Verify no CRLF line endings remain in Markdown or Python files
python3 -c "import pathlib; bad=[str(p) for p in pathlib.Path('.').rglob('*') if p.suffix in {'.md','.py'} and b'\r' in p.read_bytes()]; print('CRLF:', bad); raise SystemExit(1 if bad else 0)"

# 4. Verify git repository initialized and clean/staged properly
git status
```
