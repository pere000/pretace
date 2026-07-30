# ADR-005: Unified Deployment Architecture

**Status:** Accepted

**Version:** 1.0

**Date:** 2026-07-30

**Category:** Architecture

---

# Abstract

This Architectural Decision Record establishes the canonical deployment architecture of the Theory of Actualized Conscious Experience (TACE).

The objective is to guarantee that TACE remains a single, constitutionally consistent system regardless of its execution environment. Deployment shall never alter the behavior, ontology, reasoning, or constitutional validation of the Runtime.

This ADR defines the architectural separation between the Runtime, its interfaces, and its inference subsystem.

---

# 1. Motivation

TACE is designed as a canonical ontological reasoning system.

Such a system must not evolve into independent desktop, cloud, server, or container implementations.

Multiple implementations inevitably diverge, increasing maintenance complexity and threatening constitutional consistency.

Instead, TACE shall possess a single Runtime capable of execution in multiple environments without modification.

Deployment is therefore considered an operational concern rather than an architectural concern.

---

# 2. Decision

TACE SHALL maintain a single canonical codebase.

Every supported deployment SHALL execute exactly the same Runtime.

Deployment-specific behavior SHALL be introduced exclusively through configuration.

No deployment target SHALL require modifications to the source code.

---

# 3. Architectural Principles

The architecture is divided into three independent layers.

```
                    Presentation Layer
──────────────────────────────────────────────────────

Web Interface
Desktop Interface
Command Line Interface
Future Interfaces

──────────────────────────────────────────────────────
                    Service Layer
──────────────────────────────────────────────────────

REST API
Configuration
Authentication
Inference Interface
Persistence

──────────────────────────────────────────────────────
                     Core Runtime
──────────────────────────────────────────────────────

Runtime
Query Engine
Canonical Validation
Reasoner
Learning
Ontology
Repository
Knowledge Engine
Semantic Processing

──────────────────────────────────────────────────────
```

The Core Runtime SHALL remain completely independent of every presentation technology.

The Presentation Layer SHALL never perform reasoning or ontology processing.

---

# 4. Canonical Runtime

The Runtime is the unique executable representation of TACE.

Every execution environment SHALL invoke the same Runtime.

Examples include:

- Native execution
- Docker
- Podman
- Kubernetes
- Virtual Machine
- Bare-metal server

No deployment-specific code SHALL exist inside the Runtime.

---

# 5. REST Architecture

The Runtime SHALL expose a stable HTTP REST interface.

Every client communicates exclusively through this interface.

Possible clients include:

- Web browser
- Desktop application
- Command-line tools
- External services
- Research software

The REST API constitutes the canonical public interface of TACE.

---

# 6. Deployment Model

Deployment SHALL be configuration-driven.

Typical deployment profiles include:

## Local Development

- SQLite
- Ollama
- localhost

## Personal Server

- SQLite or PostgreSQL
- Ollama
- HTTPS

## Institutional Server

- PostgreSQL
- Shared storage
- HTTPS

## Kubernetes Cluster

- PostgreSQL
- Distributed storage
- Load balancing
- Multiple Runtime instances

The Runtime SHALL remain identical in every deployment profile.

---

# 7. Inference Runtime Independence

TACE SHALL remain completely independent of any particular inference model.

The Runtime SHALL communicate exclusively through a single **Inference Daemon Interface**.

The Runtime SHALL neither know nor depend upon the internal implementation of the daemon.

Inference execution is therefore separated from ontology and reasoning.

---

## Canonical Inference Daemon

The canonical inference daemon adopted by TACE is:

**Ollama**

The Runtime SHALL communicate with Ollama exclusively through its stable HTTP interface.

No direct coupling between TACE and individual models SHALL exist.

---

## Model Selection

Users remain free to install and select any model supported by the daemon.

Examples include:

- qwen3
- llama3
- deepseek
- mistral
- future compatible models

Changing the active model SHALL require configuration changes only.

The Runtime SHALL remain unchanged.

---

## Responsibilities

### Runtime

The Runtime is responsible for:

- ontology
- canonical validation
- reasoning
- semantic processing
- learning
- repository management
- query execution

### Inference Daemon

The daemon is responsible for:

- model loading
- inference execution
- memory allocation
- GPU utilization
- model lifecycle
- model switching

This separation preserves the constitutional independence of TACE.

---

## Architectural Relationship

```
                   TACE Runtime
                         │
              Inference Daemon Interface
                         │
                    Ollama Daemon
                         │
        ┌────────────┬────────────┬────────────┐
        │            │            │
      qwen3       llama3      deepseek
```

TACE never communicates directly with individual models.

---

# 8. Containerization

TACE SHALL provide a single canonical container image.

Example:

```
ghcr.io/tace/tace
```

The image SHALL execute the complete Runtime.

The container SHALL require no rebuilding for different deployment targets.

Containerization is considered a packaging mechanism, not an architectural variation.

---

# 9. Cloudflare Architecture

Cloudflare Pages SHALL host only the Presentation Layer.

```
Browser
     │
Cloudflare Pages
     │
 HTTPS
     │
REST API
     │
TACE Runtime
```

Cloudflare SHALL never execute ontology processing or reasoning.

All canonical processing occurs inside the Runtime.

---

# 10. Persistence

Persistent resources belong exclusively to the Runtime.

Examples include:

- Ontology
- SQLite
- PostgreSQL
- Knowledge Repository
- Semantic Indexes
- Learning Repository
- Configuration

The Presentation Layer SHALL remain stateless.

---

# 11. Configuration

All operational differences SHALL be expressed through configuration.

Examples include:

- database engine
- inference model
- inference daemon address
- storage location
- authentication
- networking
- logging
- caching

Configuration SHALL never modify constitutional behavior.

---

# 12. Benefits

This architecture guarantees:

- one codebase
- one Runtime
- one REST API
- one ontology
- one reasoning engine
- one container image
- multiple deployment targets
- reproducible deployments
- constitutional consistency
- simplified maintenance

---

# 13. Consequences

Future development SHALL prioritize:

1. Consolidation of the Runtime.
2. Stabilization of the REST API.
3. Separation of presentation logic.
4. Consolidation of the Inference Daemon Interface.
5. Docker image generation.
6. Podman compatibility.
7. Automated container publication.
8. Deployment documentation.

---

# 14. Relationship to Existing ADRs

This ADR complements the existing architectural decisions.

It governs deployment architecture only.

It neither modifies nor supersedes:

- ADR-001
- ADR-002
- ADR-003
- ADR-004

Those ADRs continue to define the constitutional behavior of ontology, reasoning, and query processing.

---

# Constitutional Principle

**The Runtime is unique.**

Deployment is merely a mode of execution.

No deployment environment possesses its own implementation of TACE.

There exists only one canonical Runtime, executed under different operational configurations while preserving identical constitutional behavior.
