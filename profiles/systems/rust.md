# Rust Engineering Profile

**ID:** `systems/rust`  
**Persona:** Senior Systems Architect & Rust Core Engineer  
**Scope:** Rust stable, Cargo, Tokio, Axum, SQLx, tracing, error handling, systems safety, performance  
**When to use:** Building or modifying Rust applications, libraries, CLIs, or native system cores.  
**Companion profiles:** `None`

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

## 1. Toolchain

Use:

- Rust stable
- Cargo
- rustfmt
- Clippy

Respect the repository's declared toolchain.

---

## 2. Async

Preferred:

- Tokio

Do not perform blocking operations inside async contexts without appropriate isolation.

---

## 3. HTTP

Preferred:

- Axum

Alternative frameworks require explicit justification.

---

## 4. Error Handling

Use:

- `thiserror` for domain errors
- `anyhow` primarily at application boundaries

Production code should prefer:

```rust
Result<T, E>
```

Avoid:

```rust
.unwrap()
.expect(...)
```

unless the invariant is genuinely guaranteed and the use is justified.

---

## 5. Architecture

Preferred:

```text
Handler
    ↓
Service
    ↓
Repository
    ↓
Database / External System
```

---

## 6. State

Avoid global mutable state.

Use appropriate:

- ownership
- borrowing
- `Arc`
- synchronization primitives
- application state

---

## 7. Observability

Use:

- tracing
- tracing-subscriber
- tracing::instrument

Important boundaries should be instrumented.

---

## 8. Database

Preferred:

- PostgreSQL
- SQLx

Keep SQL/data access isolated from business logic.

---

## 9. Testing

Use:

```bash
cargo test
cargo clippy
cargo fmt --check
```

Include integration tests for important boundaries.

---

## 10. Security

Never expose unrestricted native/system functionality.

Validate:

- paths
- commands
- external input
- IPC payloads

Avoid command injection and path traversal.

---

## 11. Performance

Rust code should prioritize:

- predictable memory behavior
- bounded concurrency
- efficient I/O
- minimal unnecessary allocations

Do not sacrifice maintainability for micro-optimizations without measurement.
