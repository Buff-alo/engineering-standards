# Quality Gates, Reporting, and Profile Maintenance

**Version:** 1.0.0  
**Scope:** Verification standards, evidence-based reporting, and profile registry governance  
**Purpose:** Ensure every change is verified proportionally to risk, reported honestly, and kept consistent with the canonical profile registry.

---

## 1. Testing and Quality Gates

Choose verification proportional to the risk and scope of the change.

### Minimum expectations

- Add regression tests for confirmed bugs where practical.
- Test important business rules and edge cases.
- Test authorization boundaries.
- Test failure handling and retry behavior for critical workflows.
- Verify data integrity and transaction behavior where relevant.
- Update tests when intentionally changing behavior.
- Avoid tests that pass only because implementation details are mocked away.
- Prefer deterministic tests and isolated test data.

### Verification sequence

Use the project's established tools to run applicable checks:

1. Focused tests for the changed behavior.
2. Relevant broader unit and integration tests.
3. Static analysis and type checks.
4. Formatting and linting.
5. Build or packaging checks.
6. Migration, schema, or configuration validation where applicable.
7. Security and dependency checks when relevant to the change.

Do not run irrelevant or destructive commands merely to complete a checklist.

If a check cannot run because of unavailable infrastructure, missing credentials, environment limitations, or time constraints, report that explicitly. Distinguish checks that passed, failed, were skipped, or could not execute.

---

## 2. Completion Report

At the end of implementation work, provide a concise, evidence-based report containing:

- **Implemented:** What changed and why.
- **Verification:** Which checks actually ran and their results.
- **Limitations:** Relevant unverified behavior, blocked checks, or known risks.
- **Operational notes:** Required configuration, migrations, or deployment steps, if any.

For reviews, prioritize findings by severity and identify the affected file or code location.

Do not report success merely because code was written. A change is complete when the requested implementation is delivered and its verification status is accurately reported.

---

## 3. Profile Maintenance

Keep `core/` universal and tool-agnostic.

- Put framework-specific dependencies, code patterns, commands, and implementation rules in their relevant `profiles/` files.
- Keep persona definitions and profile-selection logic in [PERSONAS.md](PERSONAS.md) and [WORKFLOW.md](WORKFLOW.md).
- Avoid duplicating the same technical rule across multiple profiles unless the duplication is necessary to make a critical requirement explicit.
- Update the canonical profile registry below and the mapping table in [WORKFLOW.md](WORKFLOW.md) whenever a new stack profile is introduced.
- Keep profile names, IDs, and paths consistent with the repository.
- Review profile instructions for contradictions with `core/` standards.
- Treat versions as project-specific facts, not universal assumptions.
- When a profile specifies a particular framework version, verify that the project actually uses it before applying version-specific guidance.
- Validate changes with `python3 scripts/validate_profiles.py --root . --strict` before committing.

### Canonical profile registry

- `profiles/backend/python-backend.md` — Python backend applications, including Django and FastAPI.
- `profiles/backend/java-springboot.md` — Java and Spring Boot applications.
- `profiles/backend/php-laravel.md` — PHP and Laravel applications, including Laravel 11 compatibility where required.
- `profiles/frontend/react.md` — React and TypeScript web applications.
- `profiles/frontend/nextjs.md` — Next.js App Router, Pages Router, Server Components, Server Actions, Route Handlers, rendering, caching, data access, and deployment.
- `profiles/mobile/react-native.md` — React Native mobile applications.
- `profiles/systems/rust.md` — Rust applications, libraries, and systems programming.
- `profiles/systems/tauri.md` — Tauri desktop applications and Rust/frontend integration.
- `profiles/infrastructure/devsecops.md` — Infrastructure, containers, CI/CD, deployment, and platform engineering.
- `profiles/ai/ai-llm.md` — AI/LLM integrations, model pipelines, and evaluation.

**Final rule:** The universal standards in `core/` define how the engineering agent operates. The selected persona defines its primary engineering perspective. Applicable profiles define the technology-specific standards. The repository and its verified configuration determine the actual implementation context.
