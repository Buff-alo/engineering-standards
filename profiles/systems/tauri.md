# Tauri Engineering Profile

**ID:** `systems/tauri`  
**Persona:** Senior Desktop Systems Architect  
**Scope:** Tauri v2, Rust/frontend IPC boundaries, capabilities, filesystem security, native tasks, desktop packaging  
**When to use:** Building or modifying Tauri desktop applications (combine with Rust and frontend profiles).  
**Companion profiles:** `systems/rust.md`, `frontend/react.md`

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`.

If rules conflict, follow the precedence order in `core/WORKFLOW.md`:
1. Applicable platform, safety, and security constraints.
2. Explicit task requirements.
3. Repository-specific instructions and established project contracts.
4. Universal standards in `core/`.
5. This profile and any required companion profiles.
6. Existing project conventions unless explicitly changed.

---

## 1. Stack

Preferred:

- Tauri v2
- Rust
- React
- TypeScript

---

## 2. Architecture

```text
React UI
    ↓
Typed IPC
    ↓
Tauri Command
    ↓
Rust Service
    ↓
Native API / Repository
```

---

## 3. Rust Core

Rust owns:

- native OS integration
- filesystem access
- process management
- secure operations
- hardware access
- privileged operations
- long-running native tasks

---

## 4. Frontend

React owns:

- presentation
- user interaction
- local UI state
- server state
- rendering

Do not expose privileged native functionality directly to arbitrary frontend code.

---

## 5. IPC

Use:

- Tauri commands
- Tauri events

IPC contracts must be:

- explicit
- typed
- validated

Never accept arbitrary unvalidated commands from the frontend.

---

## 6. Capabilities

Follow least privilege.

Only grant the application the permissions it requires.

Avoid broad filesystem or shell permissions.

---

## 7. Filesystem

Validate:

- paths
- file types
- permissions

Protect against:

- path traversal
- arbitrary file access
- command injection

---

## 8. Long-Running Operations

Do not block the UI thread.

Use appropriate Rust async/concurrency primitives.

Provide:

- cancellation
- progress reporting
- error reporting

where appropriate.

---

## 9. State

Keep state ownership explicit.

Avoid uncontrolled global mutable state.

---

## 10. Testing

Test:

- Rust services
- Tauri commands
- IPC contracts
- critical UI workflows
- filesystem behavior

---

## 11. Security

Assume the frontend is untrusted.

Every privileged operation must enforce its own validation and authorization boundaries.

Never rely on UI controls as security boundaries.
