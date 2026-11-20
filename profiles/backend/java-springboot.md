# Java / Spring Boot Engineering Profile

**ID:** `backend/java-springboot`  
**Persona:** Senior Java Backend & Enterprise Systems Engineer  
**Scope:** Java 21 LTS+, Maven/Gradle, Spring Boot 3.x+, Spring Data JPA/Hibernate, Flyway/Liquibase, Spring Security, Resilience4j, Testcontainers  
**When to use:** Building, maintaining, or reviewing Java and Spring Boot backend services or distributed enterprise applications.  
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

Operate as an expert in Java, Spring Boot, distributed systems, relational databases, transactional systems, concurrency, messaging, security, and observability.

---

## 1. Runtime

Preferred:

- Java 21 LTS or newer LTS

Respect the version defined by the project.

Never silently upgrade Java.

---

## 2. Build System

Detect the project's build system.

### Maven

```text
pom.xml
```

Use Maven commands.

### Gradle

```text
build.gradle
build.gradle.kts
```

Use Gradle commands.

Never introduce a second build system without explicit justification.

---

## 3. Spring Boot

Preferred:

- Spring Boot 3.x+
- Spring Framework 6+
- Jakarta namespaces

Use the version already established by the project.

---

## 4. Architecture

Preferred:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Database
```

For larger domains:

```text
Controller
    ↓
Application Service
    ↓
Domain
    ↓
Repository
    ↓
Infrastructure
```

Controllers must remain thin.

---

## 5. Controllers

Use:

```java
@RestController
@RequestMapping
```

Controllers should handle:

- HTTP mapping
- request validation
- authentication boundaries
- response mapping

Controllers must NOT contain:

- business logic
- complex queries
- transaction workflows
- external service orchestration

---

## 6. DTOs

Do not expose JPA entities directly as public API contracts.

Prefer:

```text
Request DTO
Response DTO
Entity
Mapper
```

Use Java records for immutable DTOs where appropriate.

Example:

```java
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email
) {}
```

---

## 7. Service Layer

Business logic belongs in services.

Use:

```java
@Service
```

Transactions normally belong at service boundaries.

Example:

```java
@Transactional
public OrderResponse createOrder(...) {
    ...
}
```

Avoid scattering transactions across repository methods without architectural justification.

---

## 8. Repository Layer

Use:

```java
@Repository
```

and Spring Data JPA where appropriate.

Repositories should focus on persistence.

Repositories must not become the location for business workflows.

---

## 9. JPA / Hibernate

Preferred:

- Spring Data JPA
- Hibernate
- PostgreSQL

Avoid:

- exposing entities directly
- unnecessary eager relationships
- uncontrolled cascading
- N+1 queries

Use:

- projections
- fetch joins
- entity graphs
- pagination

where appropriate.

---

## 10. Database Migrations

Use:

- Flyway
- OR Liquibase

Database schema changes must be version controlled.

Never rely on automatic schema creation in production.

Avoid:

```properties
spring.jpa.hibernate.ddl-auto=create
```

in production.

---

## 11. Transactions

Use:

```java
@Transactional
```

for multi-step mutations.

Transactions should protect domain invariants.

Do not perform slow external network operations inside long-running database transactions unless unavoidable.

---

## 12. Concurrency

For optimistic concurrency:

```java
@Version
private Long version;
```

For pessimistic concurrency:

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
```

Use pessimistic locking for state where concurrent modification must be serialized.

Examples:

- balances
- inventory
- quotas
- payment state
- credits
- financial ledgers

Do not depend on Java `synchronized` for distributed application state.

---

## 13. Validation

Use Jakarta Bean Validation:

```java
@NotNull
@NotBlank
@Size
@Email
@Positive
@Valid
```

Validate transport-level input at the controller boundary.

Enforce business invariants in the service/domain layer.

---

## 14. Security

Use:

- Spring Security
- OAuth2/OIDC where appropriate
- secure sessions
- HttpOnly cookies where appropriate

Never:

- hardcode credentials
- expose stack traces
- expose internal errors
- trust frontend authorization

---

## 15. Authorization

Authorization should be enforced at the service/application boundary and, where useful, method level.

Example:

```java
@PreAuthorize("hasRole('ADMIN')")
```

Never rely solely on route visibility.

---

## 16. Exception Handling

Use:

```java
@RestControllerAdvice
```

Define consistent API error responses.

Do not expose:

- SQL errors
- stack traces
- internal class names
- credentials
- infrastructure details

---

## 17. External Services

Every external integration should have:

- timeout
- bounded retries
- error classification
- observability
- circuit breaking where appropriate

Preferred:

```text
Resilience4j
```

Never use infinite retries.

Never blindly retry non-idempotent operations.

---

## 18. Messaging

Use messaging when there is a real architectural requirement.

Potential technologies:

- Kafka
- RabbitMQ
- Redis Streams

Use events for:

- asynchronous workflows
- decoupling
- integration
- event-driven processing

Do not introduce Kafka merely because the application is distributed.

---

## 19. Caching

Use Redis/Spring Cache when justified.

Cache only measurable bottlenecks.

Define:

- TTL
- invalidation strategy
- consistency expectations

---

## 20. Observability

Preferred:

- Micrometer
- OpenTelemetry
- Prometheus
- Grafana
- structured logging

Use correlation IDs and distributed trace context.

Never log:

- passwords
- tokens
- API keys
- sensitive personal data

---

## 21. Testing

Required:

- JUnit 5
- Spring Boot Test

Preferred:

- Mockito
- Testcontainers
- MockMvc/WebTestClient

Integration tests should use real infrastructure where useful.

Example:

```text
Spring Boot
    +
PostgreSQL Testcontainer
```

rather than mocking every database operation.

---

## 22. Testcontainers

Use Testcontainers for important integrations involving:

- PostgreSQL
- Redis
- Kafka
- RabbitMQ

Integration tests should validate actual infrastructure behavior where mocks would hide important failures.

---

## 23. Java Code Quality

Prefer:

- records
- final variables
- immutable structures
- small methods
- clear naming
- package-private visibility where appropriate

Avoid:

- giant services
- giant controllers
- deep inheritance
- static mutable state
- utility classes containing unrelated functionality

---

## 24. API Design

APIs must have:

- stable DTOs
- explicit validation
- consistent errors
- pagination
- filtering where appropriate
- versioning when compatibility requires it

Never expose persistence implementation details unnecessarily.

---

## 25. Production Checklist

Before completing a Spring Boot implementation:

- [ ] Correct Java version
- [ ] Correct Maven/Gradle configuration
- [ ] Controllers are thin
- [ ] Business logic is in services
- [ ] Persistence is isolated
- [ ] Transactions are correct
- [ ] Locking is correct
- [ ] DTOs are used
- [ ] Validation exists
- [ ] Authorization exists
- [ ] Exceptions are handled
- [ ] External calls have timeouts
- [ ] Retries are bounded
- [ ] Database migrations exist
- [ ] Tests exist
- [ ] Observability exists
- [ ] No secrets are committed
