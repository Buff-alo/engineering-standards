# Project Engineering Profile

**Project:** `<project-name>`  
**Standards Version:** `v1.0.0`  
**Primary Persona:** `<Persona from core/PERSONAS.md>`  
**Active Profiles:**
- `profiles/<domain>/<profile>.md`

---

## 1. Verified Runtime & Tooling

- **Language / Runtime:** `<e.g., Python 3.13, Node 22 LTS, Rust 1.83>`
- **Package Manager:** `<e.g., uv, pnpm, cargo, composer>`
- **Framework(s):** `<e.g., Next.js 15 App Router, Django 5.1 + Django Ninja>`
- **Database / Cache:** `<e.g., PostgreSQL 16, Redis 7>`

---

## 2. Authoritative Verification Commands

```bash
# Tests
<command>

# Type checks & static analysis
<command>

# Formatting & linting
<command>

# Build
<command>
```

---

## 3. Approved Deviations & Local Conventions

Document any intentional override of a stack profile rule here (per precedence level 3 in `core/WORKFLOW.md`):

- **Rule overridden:** `<profile & section>`
- **Local convention:** `<what this repository does instead>`
- **Justification:** `<why this override is required>`

---

## 4. Critical Invariants & Operational Notes

- **Concurrency / Data invariants:** `<e.g., ledger mutations require SELECT ... FOR UPDATE>`
- **Security boundaries:** `<e.g., auth enforced via server session middleware + resource policies>`
- **Required local services:** `<e.g., docker compose up -d postgres redis>`
