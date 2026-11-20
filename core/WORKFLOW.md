# Discovery, Composition, and Implementation Workflow

**Version:** 1.0.0  
**Scope:** Repository inspection, profile composition, conflict resolution, task execution, and planning outputs  
**Purpose:** Establish a deterministic workflow from repository discovery through planning and implementation.

---

## 1. Repository Discovery and Profile Loading

### 1.1 Inspect before changing

At the start of a task, inspect the relevant portions of the repository:

- Agent instruction files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) and project profile overrides.
- README and architecture documentation.
- Language and framework manifests.
- Lockfiles and runtime/toolchain versions.
- Application entry points and module boundaries.
- Existing tests, linters, formatters, and CI configuration.
- Relevant database schemas, migrations, API contracts, and deployment files.

Use targeted inspection. Do not read every file when a focused investigation is sufficient.

Respect any more specific instructions that apply to the target directory or file.

### 1.2 Detect the actual stack

Use project evidence, including:

- `pyproject.toml`, `uv.lock`
- `pom.xml`, `build.gradle`, `build.gradle.kts`
- `composer.json`, `composer.lock`
- `Cargo.toml`, `Cargo.lock`
- `package.json` and its lockfile
- React Native and Tauri configuration (`app.json`, `app.config.*`, `tauri.conf.json`)
- Dockerfiles, Compose files, Kubernetes manifests, Terraform, and CI pipelines

Do not infer the complete architecture from a directory name or a framework mentioned in conversation alone.

If the repository contradicts the requested stack, report the discrepancy and determine whether the task is a migration, a new implementation, or a change to the existing system.

### 1.3 Load only applicable profiles

Keep universal rules in `core/` and place detailed technology standards in separate profile files under `profiles/`.

Use this mapping as a starting point:

| Project or task | Applicable profile |
|---|---|
| Django or FastAPI backend | `profiles/backend/python-backend.md` |
| Java or Spring Boot | `profiles/backend/java-springboot.md` |
| PHP or Laravel | `profiles/backend/php-laravel.md` |
| React or TypeScript web application | `profiles/frontend/react.md` |
| Next.js web application | `profiles/frontend/nextjs.md` (+ `profiles/frontend/react.md`) |
| React Native application | `profiles/mobile/react-native.md` |
| Rust application or library | `profiles/systems/rust.md` |
| Tauri desktop application | `profiles/systems/tauri.md` (+ `profiles/systems/rust.md`, `profiles/frontend/react.md`) |
| Infrastructure, CI/CD, deployment | `profiles/infrastructure/devsecops.md` |
| Substantial LLM or AI integration | `profiles/ai/ai-llm.md` |

Load additional profiles only when relevant. For example, a Tauri application with a React frontend requires the Tauri, Rust, and React profiles.

**Important:** Do not assume an agent automatically discovers or loads every file under `profiles/`. Read the applicable profiles explicitly when the environment permits. If a profile is missing or inaccessible, state that limitation and follow the repository's verified conventions without inventing profile content.

If a project uses a custom profile layout, follow its established organization and update the profile paths accordingly.

### 1.4 Resolve conflicting instructions

Apply this precedence:

1. Applicable platform, safety, and security constraints.
2. Explicit task requirements, within those constraints.
3. Repository-specific instructions and established project contracts (e.g., `project-profile.md`).
4. Universal standards in `core/` ([ENGINEERING.md](ENGINEERING.md), [PERSONAS.md](PERSONAS.md), [WORKFLOW.md](WORKFLOW.md), [QUALITY-GATES.md](QUALITY-GATES.md)).
5. Applicable stack profiles and documented project conventions.
6. General engineering preferences.

Resolve conflicts by identifying their scope. Do not silently override a specific project requirement with a generic preference. If two equally authoritative requirements conflict materially, ask for clarification when necessary.

---

## 2. Task Classification and Execution

Classify the requested work before choosing an implementation strategy.

### Investigation

- Establish the current behavior.
- Trace relevant execution paths and dependencies.
- Gather evidence before proposing a root cause.
- Separate confirmed facts from hypotheses.

### Bug fix

- Reproduce the failure where possible.
- Identify the root cause rather than masking symptoms.
- Add or update regression tests.
- Make the smallest safe change that addresses the cause.

### Feature implementation

- Establish acceptance criteria and affected contracts.
- Identify data, authorization, concurrency, and failure-handling implications.
- Implement the smallest coherent design.
- Add appropriate tests and documentation.

### Refactoring

- Preserve externally observable behavior unless explicitly changing it.
- Use existing tests as a safety net.
- Avoid unrelated feature additions.
- Separate behavioral changes from structural changes where practical.

### Migration or upgrade

- Establish source and target versions.
- Check compatibility and deprecation risks.
- Review lockfiles, schema changes, configuration, and deployment implications.
- Define rollback or recovery considerations for high-risk changes.

### Review

- Prioritize concrete defects, vulnerabilities, data-integrity risks, and missing tests.
- Reference affected files and relevant code locations.
- Distinguish confirmed defects from potential concerns.
- Explain impact and a practical remediation path.

---

## 3. Implementation Workflow

For a substantial task, follow this workflow:

1. **Understand:** Establish the requested outcome and acceptance criteria.
2. **Inspect:** Read applicable instructions, code, manifests, tests, and relevant documentation.
3. **Classify:** Select the primary persona ([PERSONAS.md](PERSONAS.md)) and applicable stack profiles.
4. **Analyze:** Identify affected components, invariants, risks, and dependencies.
5. **Plan:** Choose the smallest coherent implementation and appropriate verification.
6. **Implement:** Make focused changes consistent with project conventions.
7. **Verify:** Run relevant tests and quality checks per [QUALITY-GATES.md](QUALITY-GATES.md), inspecting actual results.
8. **Review:** Check the diff for regressions, security issues, unrelated changes, and missing documentation.
9. **Report:** Summarize changes, verification, limitations, and any necessary follow-up.

For small, clear tasks, do not produce an elaborate plan when direct implementation is more efficient. The workflow should scale with risk and complexity.

### Handling uncertainty

- Ask a focused clarification question when an unresolved detail materially changes the architecture, security posture, data model, or user-visible behavior.
- Otherwise, choose a reasonable, reversible default and state any consequential assumption.
- Do not block straightforward work on preferences that can safely be inferred from the repository.
- Do not fabricate missing context or silently invent requirements.

### Destructive or external operations

Before destructive migrations, production deployments, data deletion, irreversible infrastructure changes, or externally visible actions, verify that the requested scope and authorization are clear. Use previews, backups, staged rollout, or rollback plans where appropriate.

---

## 4. Planning Output Standard

When running brainstorming or architectural planning for a substantial feature or system change, save the finalized output to `docs/plans/<feature-name>.md` containing:

1. **System & Security Constraints** — authentication, authorization, rate limits, input validation, threat mitigations.
2. **Data & API Contracts** — exact Protobuf, SQL DDL, Rust structs, Go interfaces, Python schemas, or TypeScript types.
3. **File-by-File Execution Checklist** — ordered list of files to create or modify with clear acceptance criteria.
4. **Verification Commands** — exact CLI commands to test and lint the implementation.
