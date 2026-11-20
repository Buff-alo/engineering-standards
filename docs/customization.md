# Pinning & Customization

`engineering-standards` is designed as a hybrid framework: a stable, universal `core/` paired with opinionated `profiles/` that projects and teams can pin, extend, or override safely.

---

## 1. Pinning a Release in Your Project

### Option A: Git Submodule (Recommended for Teams)

```bash
git submodule add <repo-url> .standards
git -C .standards checkout v1.0.0
```

Then copy a starter file from [templates/](../templates/) (`AGENTS.md`, `GEMINI.md`, or `CLAUDE.md`) to your repository root and replace `<STANDARDS_ROOT>` with `.standards`.

### Option B: Local Shared Checkout (Single Developer)

Keep one local clone (for example, `~/Workspace/engineering-standards`) checked out to a release tag (`v1.0.0`), and point your global tool config (`~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`) to it as described in [integrations/](../integrations/gemini/README.md).

---

## 2. Customizing Without Forking

Do not edit `core/` or `profiles/` directly in downstream repositories when a project-specific exception is needed. Instead:

1. Copy [templates/project-profile.md](../templates/project-profile.md) to `project-profile.md` in your repository root.
2. Record:
   - Authoritative runtime versions and package manager commands.
   - Any deliberate specialization or deviation from a stack profile (for example, using a custom Docker network name instead of `universal_dev_network`, or retaining an existing framework library).
3. Under [WORKFLOW.md](../core/WORKFLOW.md) Section 1.4, repository-specific contracts govern **project specialization** (versions, tooling, commands, and stack defaults) ahead of stack profiles and general `core/` conventions, **but MUST NOT silently weaken non-negotiable core invariants** (security, privacy, authorization, data integrity, safety, or honest test verification). Any exception to a core invariant requires an explicit, documented risk assessment and compensating controls.

---

## 3. Forking for Organization-Wide Defaults

If your organization wants different opinionated defaults across all repositories (for example, Poetry instead of `uv`, or Vue instead of React):

1. Fork `engineering-standards`.
2. Modify or add profiles under `profiles/`.
3. Update the canonical registry in [QUALITY-GATES.md](../core/QUALITY-GATES.md) and mapping table in [WORKFLOW.md](../core/WORKFLOW.md).
4. Run `python3 scripts/validate_profiles.py --root . --strict` in CI to catch broken links or registry drift.
5. Tag your internal release (`v1.0.0-org.1` or `v1.1.0`).
