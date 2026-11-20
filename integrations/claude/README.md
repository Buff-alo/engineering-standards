# Claude Code Integration

This adapter connects `engineering-standards` to Claude Code (`CLAUDE.md`) without duplicating standards content.

## Option 1: Per-Project Setup

1. Vendor, submodule, or reference `engineering-standards` (pinned to a release tag such as `v1.0.0`).
2. Copy [templates/CLAUDE.md](../../templates/CLAUDE.md) to your project root as `CLAUDE.md`.
3. Update the profile list in `CLAUDE.md` to include only the profiles relevant to that repository.
4. Optionally copy [templates/project-profile.md](../../templates/project-profile.md) to document project-specific versions, commands, and exceptions.

## Option 2: User-Level Setup (`~/.claude/CLAUDE.md`)

Point `~/.claude/CLAUDE.md` to your local checkout of `engineering-standards/core/` and instruct Claude Code to load only matching stack profiles from `engineering-standards/profiles/` after inspecting each repository.

## Maintenance

Keep `CLAUDE.md` focused on file pointers, profile composition, and Claude Code workflow hooks. All engineering rules live in `core/` and `profiles/`.
