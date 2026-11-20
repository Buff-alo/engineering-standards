# Claude Code Adapter

This file adapts the universal standards in `core/` and stack profiles in `profiles/` for Claude Code without duplicating rules.

## Mandatory Core Standards

Before making architectural decisions or writing code, read and follow:

- `core/ENGINEERING.md`
- `core/PERSONAS.md`
- `core/WORKFLOW.md`
- `core/QUALITY-GATES.md`

## Stack Profile Selection

Inspect the repository manifests and lockfiles first (`core/WORKFLOW.md`), then read only the matching profiles under `profiles/`.

## Precedence

Follow `core/WORKFLOW.md` Section 1.4:
1. Platform, safety, and security constraints.
2. Explicit user task requirements.
3. Project-local contracts and overrides (such as `project-profile.md`).
4. `core/` standards.
5. Selected `profiles/`.
