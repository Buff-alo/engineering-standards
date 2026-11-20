# Gemini CLI & Antigravity Integration

This adapter connects `engineering-standards` to Gemini CLI and Antigravity without duplicating the rules in `core/` or `profiles/`.

## Option 1: Global Setup (`~/.gemini/GEMINI.md`)

Clone or check out `engineering-standards` to a stable path on your machine (for example, `~/Workspace/engineering-standards`), then point `~/.gemini/GEMINI.md` to it:

```markdown
# Global Engineering Standards

Read and follow the universal standards from `~/Workspace/engineering-standards/core/`:
- `ENGINEERING.md`
- `PERSONAS.md`
- `WORKFLOW.md`
- `QUALITY-GATES.md`

Select and read only the applicable stack profiles in `~/Workspace/engineering-standards/profiles/` based on the repository you are inspecting.
```

If using Gemini CLI with `@import` support, you can import the core files directly using paths relative to `~/.gemini/` or your workspace.

## Option 2: Per-Project Setup

Copy [templates/GEMINI.md](../../templates/GEMINI.md) to your project root as `GEMINI.md` and list only the profiles your project uses. Optionally pair it with [templates/project-profile.md](../../templates/project-profile.md) for project-specific versions, commands, and overrides.

## Maintenance

- Never edit rules inside `GEMINI.md` when the rule belongs in `core/` or `profiles/`.
- Keep `GEMINI.md` limited to discovery pointers, profile composition, and Gemini-specific tool behavior.
