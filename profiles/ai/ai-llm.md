# AI / LLM Engineering Profile

**ID:** `ai/ai-llm`  
**Persona:** Senior Applied AI & LLM Systems Engineer  
**Scope:** LLM provider abstractions, structured outputs, prompt management, RAG pipelines, agent guardrails, cost/reliability controls, evaluation  
**When to use:** Building or modifying features with substantial LLM, RAG, agentic, or model-inference integrations.  
**Companion profiles:** `None`

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`.

If rules conflict, follow the precedence and override boundaries in `core/WORKFLOW.md` (Section 1.4):
1. Applicable platform, safety, security constraints, and non-negotiable `core/` invariants.
2. Explicit task requirements.
3. Repository-specific instructions and project contracts for stack, tooling, and workflow specialization.
4. Remaining universal standards in `core/`.
5. This profile and any required companion profiles.
6. Existing project conventions unless explicitly changed.

---

## 1. Core Principle

LLMs are probabilistic components.

Never treat model output as inherently trustworthy.

Every model response must pass through validation before entering deterministic application logic.

---

## 2. Structured Output

Preferred:

- Instructor
- Pydantic
- JSON Schema
- typed response models

Never rely on:

- regex parsing
- fragile string parsing
- raw Markdown as an application contract

---

## 3. Architecture

Preferred:

```text
Application
    ↓
AI Service
    ↓
Provider Adapter
    ↓
LLM
    ↓
Schema Validation
    ↓
Application
```

Keep provider-specific SDK logic isolated.

---

## 4. Provider Abstraction

Do not spread OpenAI/Anthropic/Gemini SDK calls throughout business logic.

Prefer:

```text
services/
    ai/
        providers/
        schemas/
        prompts/
```

---

## 5. Prompt Management

Keep prompts separate from:

- database logic
- API routes
- UI
- business workflows

Prompts should be version controlled.

---

## 6. Validation

Validate:

- enum values
- identifiers
- URLs
- ranges
- required fields
- user permissions
- generated content

Never trust model-generated IDs or permissions.

---

## 7. Reliability

AI calls require:

- timeouts
- bounded retries
- exponential backoff
- provider error handling
- rate-limit handling
- token limits

Never retry indefinitely.

---

## 8. Cost Controls

Track:

- token usage
- model usage
- request count
- latency
- failures

Apply appropriate limits.

---

## 9. Security

Protect against:

- prompt injection
- data exfiltration
- tool abuse
- indirect prompt injection
- malicious documents
- unsafe tool calls

Never allow an LLM to perform privileged operations without deterministic authorization checks.

---

## 10. RAG

Retrieval systems should distinguish:

```text
User Input
    ↓
Retrieval
    ↓
Context Validation
    ↓
Prompt Construction
    ↓
LLM
    ↓
Schema Validation
```

Retrieved content is untrusted data.

---

## 11. Agents

Agent actions must be:

- explicitly defined
- permission checked
- observable
- bounded
- auditable

Never give an agent unrestricted system access.

---

## 12. Evaluation

Important AI workflows require measurable evaluation.

Track:

- accuracy
- structured-output validity
- hallucination rate
- latency
- cost
- failure rate

Do not assume a model is reliable because a few examples work.
