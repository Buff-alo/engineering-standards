# Python Backend Engineering Profile

**ID:** `backend/python-backend`  
**Persona:** Senior Backend & Distributed Systems Engineer  
**Scope:** Python 3.13+, `uv`, Django, Django Ninja, FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery, Django Channels, pytest  
**When to use:** Building or modifying Python backend services, APIs, background workers, or data-access layers (Django or FastAPI).  
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

## 1. Runtime

Preferred:

- Python 3.13+

Respect the project's declared Python version.

---

## 2. Package Management

`uv` is mandatory for new or `uv`-managed Python backend projects.

Use:

```bash
uv add <package>
uv remove <package>
uv sync
uv run <command>
```

Never use:

```text
pip
pipenv
poetry
```

---

## 3. Django

Preferred stack:

- Django
- Django Ninja
- Uvicorn
- PostgreSQL
- Redis
- Celery
- Django Channels

STRICTLY FORBIDDEN:

- Django REST Framework

---

## 4. Django Architecture

```text
API Router
    ↓
Service
    ↓
Selector
    ↓
ORM
```

Reads:

```text
Router → Selector → QuerySet
```

Writes:

```text
Router → Service → Transaction → Model
```

---

## 5. Service Layer

`services.py` contains:

- business logic
- mutations
- transaction workflows
- concurrency control
- task dispatch

API handlers remain thin.

---

## 6. Selectors

`selectors.py` contains:

- read-only query logic
- query optimization
- reusable query access

Selectors must NEVER mutate state.

---

## 7. Pydantic Schemas

Use Django Ninja + Pydantic for API contracts.

Never expose ORM objects directly as uncontrolled API responses.

---

## 8. Concurrency

For critical shared state:

```python
with transaction.atomic():
    obj = (
        Model.objects
        .select_for_update()
        .get(pk=object_id)
    )
```

Use for:

- balances
- credits
- inventory
- quotas
- payment state
- usage counters

---

## 9. Celery

Tasks must:

- be thin
- be idempotent
- be retry-safe
- delegate business logic to services

Use transaction hooks where necessary:

```python
transaction.on_commit(...)
```

---

## 10. Channels

Use:

- Django Channels
- Redis channel layers

Never broadcast uncommitted state.

---

## 11. FastAPI

Use when the project explicitly selects FastAPI.

Preferred:

- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis

Architecture:

```text
APIRouter
    ↓
Service
    ↓
Repository
    ↓
Database
```

---

## 12. Async

Use async for genuinely asynchronous I/O.

Do not mix blocking database or network operations into async event loops.

---

## 13. Testing

Preferred:

- pytest
- pytest-django
- HTTPX
- integration tests

Critical workflows require:

- transaction tests
- concurrency tests
- authentication tests
- WebSocket tests
