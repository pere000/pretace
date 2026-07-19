# ADR-005: Repository Resolution

**Status:** Accepted

## Context
The kernel must separate constitutional authority from the physical storage of knowledge.

## Decision
Introduce a RepositoryResolver layer between AuthorityGate and RepositoryLoader. AuthorityGate determines the governing authority only. RepositoryResolver maps that authority to the configured repository. RepositoryLoader loads data from the selected repository.

Pipeline:

User Query
-> QueryClassifier
-> AuthorityGate
-> RepositoryResolver
-> RepositoryLoader
-> Canonical Resource

## Consequences
- Authority is independent of storage.
- Repository technology can change without modifying AuthorityGate.
- Supports SQLite, Markdown, JSON and future repository types.
