# Codex Integration

This adapter connects `engineering-standards` to OpenAI Codex and any agent tooling that reads `AGENTS.md`.

## Setup in a Target Repository

1. Reference or pin `engineering-standards` (via Git submodule, subtree, or local path).
2. Copy [templates/AGENTS.md](../../templates/AGENTS.md) to your repository root as `AGENTS.md`.
3. Uncomment or list only the stack profiles under `profiles/` that match the repository's verified stack.
4. Add a `project-profile.md` (from [templates/project-profile.md](../../templates/project-profile.md)) for repo-specific commands, versions, and architectural exceptions.

## Maintenance

Do not copy `core/` rules directly into project `AGENTS.md` files unless your environment blocks reading external/submoduled files. Prefer explicit composition pointers so updates stay centralized.
