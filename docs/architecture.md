# Architecture Overview

`engineering-standards` is structured into two core normative layers and one adapter layer so engineering standards remain consistent regardless of which AI coding assistant or project consumes them.

---

## 1. Layer Separation

```text
+-------------------------------------------------------+
|  Integrations & Project Templates                     |
|  integrations/{gemini,claude,codex}/  |  templates/   |
+-------------------------------------------------------+
            | references (never duplicates)
            v
+---------------------------+---------------------------+
|  Core Standards (core/)   |  Stack Profiles           |
|  - ENGINEERING.md         |  profiles/                |
|  - PERSONAS.md            |  - backend/               |
|  - WORKFLOW.md            |  - frontend/              |
|  - QUALITY-GATES.md       |  - mobile/                |
|                           |  - systems/               |
|                           |  - infrastructure/        |
|                           |  - ai/                    |
+---------------------------+---------------------------+
```

### Why Separate `core/` from `integrations/`?

1. **Single source of truth:** Updating a concurrency or security rule in `core/ENGINEERING.md` automatically applies to Gemini CLI, Claude Code, and Codex without syncing multiple instruction files.
2. **Selective context loading:** Agents load `core/` plus only the stack profiles verified in the target repository's manifests and lockfiles, keeping context focused and reducing contradictory guidance.
3. **Tool portability:** Adopting a new AI coding assistant only requires adding a thin adapter directory under `integrations/`.

---

## 2. Conflict Precedence Hierarchy

When instructions from different sources overlap, resolve conflicts using the precedence defined in [WORKFLOW.md](../core/WORKFLOW.md):

1. Applicable platform, safety, and security constraints.
2. Explicit task requirements, within those constraints.
3. Repository-specific instructions and established project contracts (e.g., `project-profile.md`).
4. Universal standards in `core/`.
5. Applicable stack profiles (`profiles/`) and documented project conventions.
6. General engineering preferences.

---

## 3. Personas vs. Profiles

- **Personas** ([PERSONAS.md](../core/PERSONAS.md)) define *who owns the technical judgment* for a task (for example, Senior Backend & Distributed Systems Engineer).
- **Profiles** (`profiles/`) define *technology-specific implementation rules* (for example, Django Ninja + `select_for_update()`, or Next.js App Router RSC boundaries).

A cross-stack task assigns **one primary persona** and consults specialist perspectives and companion profiles as needed.
