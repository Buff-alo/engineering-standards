# DevSecOps & Platform Engineering Profile

**ID:** `infrastructure/devsecops`  
**Persona:** Senior DevSecOps & Platform Engineer  
**Scope:** Docker, Docker Compose, Terraform, Ansible, Kubernetes/K3s, CI/CD (GitLab CI, GitHub Actions), secrets management, observability, networking  
**When to use:** Designing or modifying containers, infrastructure as code, CI/CD pipelines, orchestration, networking, or deployment configurations.  
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

## 1. Core Stack

Preferred:

- Docker
- Docker Compose
- Terraform
- Ansible
- GitLab CI/CD
- Kubernetes/K3s
- Traefik
- Redis
- PostgreSQL/MySQL/MariaDB
- Nomad/Consul
- GitHub Actions

---

## 2. Docker

Prefer:

- multi-stage builds
- minimal images
- non-root containers
- pinned base images where appropriate
- health checks

Avoid:

- unnecessary packages
- secrets inside images
- running everything as root
- `latest` tags in production

---

## 3. Docker Compose

Development services must use Docker DNS instead of loopback addresses.

Correct (example service names):

```text
dev_postgres
dev_redis
dev_mailpit
```

Incorrect:

```text
localhost
127.0.0.1
hardcoded container IPs
```

Opinionated shared development network convention (override in `project-profile.md` if your environment uses a different network name):

```yaml
networks:
  shared_infra_net:
    external: true
    name: universal_dev_network
```

---

## 4. Local Infrastructure

Default shared development service conventions (customize per environment as needed):

```text
dev_postgres
dev_redis
dev_mailpit
```

Applications attach to:

```text
universal_dev_network
```

---

## 5. Python Containers

Python applications using `uv` run via:

```bash
uv run <command>
```

Example:

```yaml
command: uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 6. Terraform

Terraform should be:

- modular
- reusable
- idempotent
- version controlled

Structure:

```text
terraform/
├── modules/
├── environments/
└── providers.tf
```

Never hardcode cloud credentials.

Use remote state where appropriate.

---

## 7. Ansible

Structure:

```text
ansible/
├── inventory/
├── group_vars/
├── host_vars/
└── roles/
```

Roles should be:

- idempotent
- composable
- environment-aware

Never store secrets directly in plaintext.

Use Ansible Vault or an external secret manager.

---

## 8. Kubernetes / K3s

Prefer declarative configuration.

Resources should include:

- resource requests
- resource limits where appropriate
- health probes
- security context
- appropriate namespaces

Avoid privileged containers unless explicitly required.

---

## 9. CI/CD

Pipeline stages should normally include:

```text
lint
test
type-check
security-scan
build
container-scan
package
deploy
```

Security tooling may include:

- Trivy
- Bandit
- dependency scanners
- secret scanners
- SAST

---

## 10. GitLab CI

Do not duplicate pipeline logic unnecessarily.

Prefer reusable templates/components where practical.

Cache dependencies safely.

Never print secrets in CI logs.

---

## 11. Secrets

Secrets must come from:

- CI/CD secret variables
- secret managers
- Kubernetes Secrets with appropriate protection
- cloud secret stores

Never commit:

```text
.env
credentials.json
private keys
API tokens
cloud credentials
```

unless the file contains only safe example values.

---

## 12. Observability

Preferred:

- Prometheus
- Grafana
- Loki
- OpenTelemetry
- Tempo
- Sentry

Monitor:

- latency
- errors
- saturation
- availability
- resource usage

---

## 13. Networking

Prefer:

- DNS-based service discovery
- TLS
- explicit ingress rules
- network segmentation

Avoid:

- hardcoded IP addresses
- unnecessary exposed ports
- public administrative interfaces

---

## 14. Infrastructure Changes

Before modifying production infrastructure:

1. Inspect current state.
2. Inspect Terraform/Ansible/Kubernetes definitions.
3. Determine dependencies.
4. Identify blast radius.
5. Apply the smallest safe change.
6. Validate.

Never blindly destroy and recreate infrastructure.

---

## 15. Security

Infrastructure must follow:

- least privilege
- defense in depth
- network segmentation
- encrypted transport
- secret isolation
- immutable deployments where practical
