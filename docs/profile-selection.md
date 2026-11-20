# Profile Selection & Composition

Use **explicit profile composition**: inspect the target repository first ([WORKFLOW.md](../core/WORKFLOW.md)), then load `core/` together with only the profiles matching the verified stack and task.

---

## Profile Catalog

| Domain | Profile | Companion Profiles | Use When |
|---|---|---|---|
| Backend | [python-backend.md](../profiles/backend/python-backend.md) | None | Django (Ninja) or FastAPI backends, Celery, Channels, pytest |
| Backend | [java-springboot.md](../profiles/backend/java-springboot.md) | None | Java 21+ and Spring Boot 3.x+ services, JPA, Flyway/Liquibase |
| Backend | [php-laravel.md](../profiles/backend/php-laravel.md) | None | Supported PHP 8.2–8.5 and Laravel apps: defaults to Laravel 13 (+ PHP 8.3+) for new projects; Laravel 12 is short-term maintenance |
| Backend | [php-laravel-11.md](../profiles/backend/php-laravel-11.md) | None | Legacy-only Laravel 11 apps (security EOL March 12, 2026) — maintenance & upgrades to Laravel 12/13 only |
| Frontend | [react.md](../profiles/frontend/react.md) | None | React + TypeScript SPAs, components, state, Tailwind, accessibility |
| Frontend | [nextjs.md](../profiles/frontend/nextjs.md) | `frontend/react.md` | Next.js App Router or Pages Router, RSC, Server Actions, Route Handlers |
| Mobile | [react-native.md](../profiles/mobile/react-native.md) | None | React Native / Expo apps, Expo Router, offline sync, secure storage |
| Systems | [rust.md](../profiles/systems/rust.md) | None | Rust libraries, CLIs, Tokio/Axum services, SQLx |
| Systems | [tauri.md](../profiles/systems/tauri.md) | `systems/rust.md`, `frontend/react.md` | Tauri v2 desktop apps, typed IPC, capabilities, filesystem boundaries |
| Infrastructure | [devsecops.md](../profiles/infrastructure/devsecops.md) | None | Docker, Compose, Terraform, Ansible, K8s/K3s, CI/CD pipelines |
| AI | [ai-llm.md](../profiles/ai/ai-llm.md) | None | LLM provider adapters, structured outputs, RAG, agent guardrails, evals |

---

## Common Composition Recipes

### 1. Full-Stack Next.js + Python API Monorepo
- `core/*`
- `profiles/frontend/react.md`
- `profiles/frontend/nextjs.md`
- `profiles/backend/python-backend.md`
- `profiles/infrastructure/devsecops.md` (when editing Docker/CI/deployment files)

### 2. AI-Powered FastAPI Service
- `core/*`
- `profiles/backend/python-backend.md`
- `profiles/ai/ai-llm.md`

### 3. Tauri v2 Desktop App with React UI
- `core/*`
- `profiles/systems/rust.md`
- `profiles/frontend/react.md`
- `profiles/systems/tauri.md`

### 4. Laravel + Dockerized CI/CD Application
- `core/*`
- `profiles/backend/php-laravel.md`
- `profiles/infrastructure/devsecops.md`

---

## Selection Rules

- **Never load all profiles by default.** Loading irrelevant stack rules wastes context and introduces conflicting preferences.
- **Follow companion dependencies.** If a profile declares `Companion profiles`, load those companions alongside it.
- **Verify versions in the repository.** Check `package.json`, `pyproject.toml`, `composer.json`, `Cargo.toml`, or `pom.xml`/`build.gradle*` before applying version-specific guidance.
