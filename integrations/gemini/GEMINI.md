# Gemini CLI / Antigravity Adapter

This file adapts the universal standards in `core/` and stack profiles in `profiles/` for Gemini CLI and Antigravity without duplicating rules.

## Load Core Standards

Read and follow all universal standards:

- `core/ENGINEERING.md`
- `core/PERSONAS.md`
- `core/WORKFLOW.md`
- `core/QUALITY-GATES.md`

If your Gemini environment supports `@` file imports inside a cloned or local `engineering-standards` directory, you can import the core files directly (see [README.md](README.md)).

## Profile Composition

Do not load every profile indiscriminately. Inspect the target repository first per `core/WORKFLOW.md`, then read only the applicable profiles under `profiles/` (for example, `profiles/frontend/react.md` + `profiles/frontend/nextjs.md` for a Next.js app).

If the target repository defines a local `project-profile.md` or repository-level instructions, apply the precedence order in `core/WORKFLOW.md` (Section 1.4).
