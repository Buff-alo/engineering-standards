# Graph Report - engineering-standards  (2026-11-20)

## Corpus Check
- 38 files · ~21,262 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 431 nodes · 532 edges · 29 communities (28 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `96031e5b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- validate_profiles.py
- README.md
- Next.js Engineering Profile
- Java / Spring Boot Engineering Profile
- PHP / Laravel Engineering Profile
- React & Frontend Engineering Profile
- 2. Task Classification and Execution
- release-please-config.json
- DevSecOps & Platform Engineering Profile
- Python Backend Engineering Profile
- AI / LLM Engineering Profile
- React Native Engineering Profile
- Rust Engineering Profile
- Tauri Engineering Profile
- Universal Engineering Principles
- Common Composition Recipes
- engineering-standards
- Quality Gates, Reporting, and Profile Maintenance
- Pinning & Customization
- Engineering Personas
- Architecture Overview
- Claude Code Adapter
- CLAUDE.md — Project Claude Code Instructions
- check_integrations_and_templates.py
- Project Engineering Profile
- Contributing to engineering-standards
- AGENTS.md — Project Engineering Instructions
- AGENTS.md — Codex Adapter
- package_release.sh

## God Nodes (most connected - your core abstractions)
1. `Java / Spring Boot Engineering Profile` - 27 edges
2. `PHP / Laravel Engineering Profile` - 23 edges
3. `Next.js Engineering Profile` - 22 edges
4. `validate_repository()` - 20 edges
5. `DevSecOps & Platform Engineering Profile` - 17 edges
6. `Python Backend Engineering Profile` - 15 edges
7. `React & Frontend Engineering Profile` - 15 edges
8. `AI / LLM Engineering Profile` - 14 edges
9. `React Native Engineering Profile` - 13 edges
10. `Rust Engineering Profile` - 13 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `argparse`  [EXTRACTED]
  scripts/validate_profiles.py →   _Bridges community 0 → community 23_

## Import Cycles
- None detected.

## Communities (29 total, 1 thin omitted)

### Community 0 - "validate_profiles.py"
Cohesion: 0.08
Nodes (14): build_minimal_valid_repo(), ValidateProfilesTests, check_links_and_hygiene(), check_profiles(), check_registries(), check_structure(), check_version_sync(), discover_profiles() (+6 more)

### Community 1 - "README.md"
Cohesion: 0.07
Nodes (22): [1.0.0] - 2026-11-20, Added, Changelog, Fixed, Claude Code Integration, Maintenance, Option 1: Per-Project Setup, Option 2: User-Level Setup (`~/.claude/CLAUDE.md`) (+14 more)

### Community 2 - "Next.js Engineering Profile"
Cohesion: 0.06
Nodes (31): 10. Environment and Configuration, 11. Forms and Mutations, 12. TanStack Query and Client State, 13. Styling, Images, and Fonts, 14. SEO and Metadata, 15. Security, 16. Testing and Quality Gates, 17. Deployment and Runtime (+23 more)

### Community 3 - "Java / Spring Boot Engineering Profile"
Cohesion: 0.07
Nodes (29): 10. Database Migrations, 11. Transactions, 12. Concurrency, 13. Validation, 14. Security, 15. Authorization, 16. Exception Handling, 17. External Services (+21 more)

### Community 4 - "PHP / Laravel Engineering Profile"
Cohesion: 0.07
Nodes (28): 10. Authentication and Authorization, 11. Application Security, 12. Configuration and Environment, 13. Caching, 14. File and Object Storage, 15. Frontend Integration, 16. Testing, 17. Code Quality (+20 more)

### Community 5 - "React & Frontend Engineering Profile"
Cohesion: 0.09
Nodes (22): 10. Forms and User Interaction, 11. Testing, 12. Project Organization, 13. Quality Gate, 1. Preferred Frontend Stack, 2. TypeScript Standards, 3. Component Architecture, 4. State Management (+14 more)

### Community 6 - "2. Task Classification and Execution"
Cohesion: 0.11
Nodes (18): 1.1 Inspect before changing, 1.2 Detect the actual stack, 1.3 Load only applicable profiles, 1.4 Resolve conflicting instructions, 1. Repository Discovery and Profile Loading, 2. Task Classification and Execution, 3. Implementation Workflow, 4. Planning Output Standard (+10 more)

### Community 7 - "release-please-config.json"
Cohesion: 0.33
Nodes (5): bump-minor-pre-major, bump-patch-for-minor-pre-major, packages, release-type, $schema

### Community 8 - "DevSecOps & Platform Engineering Profile"
Cohesion: 0.12
Nodes (17): 10. GitLab CI, 11. Secrets, 12. Observability, 13. Networking, 14. Infrastructure Changes, 15. Security, 1. Core Stack, 2. Docker (+9 more)

### Community 9 - "Python Backend Engineering Profile"
Cohesion: 0.09
Nodes (20): 1. Legacy & End-of-Life Status, 2. Laravel 11 Compatibility Rules, 3. Incremental Upgrade Path (11 → 12 → 13), PHP / Laravel 11 Legacy Compatibility Profile, Profile Contract, 10. Channels, 11. FastAPI, 12. Async (+12 more)

### Community 10 - "AI / LLM Engineering Profile"
Cohesion: 0.13
Nodes (14): 10. RAG, 11. Agents, 12. Evaluation, 1. Core Principle, 2. Structured Output, 3. Architecture, 4. Provider Abstraction, 5. Prompt Management (+6 more)

### Community 11 - "React Native Engineering Profile"
Cohesion: 0.14
Nodes (13): 10. Testing, 11. Build & Deployment, 1. Stack, 2. Navigation, 3. State, 4. Secure Storage, 5. API Architecture, 6. Networking (+5 more)

### Community 12 - "Rust Engineering Profile"
Cohesion: 0.14
Nodes (13): 10. Security, 11. Performance, 1. Toolchain, 2. Async, 3. HTTP, 4. Error Handling, 5. Architecture, 6. State (+5 more)

### Community 13 - "Tauri Engineering Profile"
Cohesion: 0.14
Nodes (13): 10. Testing, 11. Security, 1. Stack, 2. Architecture, 3. Rust Core, 4. Frontend, 5. IPC, 6. Capabilities (+5 more)

### Community 14 - "Universal Engineering Principles"
Cohesion: 0.22
Nodes (9): 1. Mission and Operating Principles, 2. Architecture and Separation of Concerns, 3. Data Integrity and Concurrency, 4. Security and Privacy, 5. Dependencies and Tooling, 6. Configuration, Observability, and Operations, 7. Documentation and API Contracts, Non-negotiable rules (Core Invariants) (+1 more)

### Community 15 - "Common Composition Recipes"
Cohesion: 0.25
Nodes (8): 1. Full-Stack Next.js + Python API Monorepo, 2. AI-Powered FastAPI Service, 3. Tauri v2 Desktop App with React UI, 4. Laravel + Dockerized CI/CD Application, Common Composition Recipes, Profile Catalog, Profile Selection & Composition, Selection Rules

### Community 16 - "engineering-standards"
Cohesion: 0.25
Nodes (8): Architecture at a Glance, Django / FastAPI Backend, Documentation, engineering-standards, Explicit Profile Composition, Next.js Application, Quick Start, Rust + Tauri Desktop Application

### Community 17 - "Quality Gates, Reporting, and Profile Maintenance"
Cohesion: 0.29
Nodes (7): 1. Testing and Quality Gates, 2. Completion Report, 3. Profile Maintenance, Canonical profile registry, Minimum expectations, Quality Gates, Reporting, and Profile Maintenance, Verification sequence

### Community 18 - "Pinning & Customization"
Cohesion: 0.33
Nodes (6): 1. Pinning a Release in Your Project, 2. Customizing Without Forking, 3. Forking for Organization-Wide Defaults, Option A: Git Submodule (Recommended for Teams), Option B: Local Shared Checkout (Single Developer), Pinning & Customization

### Community 19 - "Engineering Personas"
Cohesion: 0.40
Nodes (5): 1. Select One Primary Persona, 2. Persona Registry, 3. Persona-Selection Rules, 4. Behavioral Expectations, Engineering Personas

### Community 20 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): 1. Layer Separation, 2. Conflict Precedence Hierarchy, 3. Personas vs. Profiles, Architecture Overview, Why Separate `core/` from `integrations/`?

### Community 21 - "Claude Code Adapter"
Cohesion: 0.40
Nodes (4): Claude Code Adapter, Mandatory Core Standards, Precedence, Stack Profile Selection

### Community 22 - "CLAUDE.md — Project Claude Code Instructions"
Cohesion: 0.40
Nodes (4): 1. Core Standards, 2. Active Stack Profiles, 3. Project Context, CLAUDE.md — Project Claude Code Instructions

### Community 23 - "check_integrations_and_templates.py"
Cohesion: 0.12
Nodes (8): check_integration_adapters(), check_templates(), check_workflows_and_packaging(), CheckFinding, main(), run_checks(), build_valid_integration_fixture(), CheckIntegrationsAndTemplatesTests

### Community 24 - "Project Engineering Profile"
Cohesion: 0.40
Nodes (5): 1. Verified Runtime & Tooling, 2. Authoritative Verification Commands, 3. Approved Deviations & Local Conventions, 4. Critical Invariants & Operational Notes, Project Engineering Profile

### Community 25 - "Contributing to engineering-standards"
Cohesion: 0.40
Nodes (5): Adding or Updating a Stack Profile, Automated Versioning and Releases, Contributing to engineering-standards, Design Principles for Changes, Required Verification Before Opening a PR

### Community 26 - "AGENTS.md — Project Engineering Instructions"
Cohesion: 0.40
Nodes (4): 1. Core Standards, 2. Active Stack Profiles, 3. Project Overrides, AGENTS.md — Project Engineering Instructions

### Community 27 - "AGENTS.md — Codex Adapter"
Cohesion: 0.50
Nodes (3): AGENTS.md — Codex Adapter, Explicit Profile Composition, Universal Standards

## Knowledge Gaps
- **263 isolated node(s):** `$schema`, `release-type`, `bump-minor-pre-major`, `bump-patch-for-minor-pre-major`, `packages` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 295 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Next.js Engineering Profile` connect `Next.js Engineering Profile` to `README.md`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **What connects `$schema`, `release-type`, `bump-minor-pre-major` to the rest of the system?**
  _263 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `validate_profiles.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08078231292517007 - nodes in this community are weakly interconnected._
- **Why does `Java / Spring Boot Engineering Profile` connect `Java / Spring Boot Engineering Profile` to `README.md`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Should `README.md` be split into smaller, more focused modules?**
  _Cohesion score 0.07419712070874862 - nodes in this community are weakly interconnected._
- **Why does `PHP / Laravel Engineering Profile` connect `PHP / Laravel Engineering Profile` to `README.md`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Should `Next.js Engineering Profile` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._