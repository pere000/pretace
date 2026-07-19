# TACE Kernel Architecture

Status: Draft

## Purpose

The TACE Kernel is the constitutional execution core of the TACE software ecosystem. Its purpose is to determine the authoritative source governing every query before any ontology lookup or AI reasoning occurs.

## Principles

1. Governance precedes reasoning.
2. Constitutions govern behavior.
3. The ontology is the authoritative knowledge source.
4. ADRs govern architectural decisions.
5. AI never determines authority.

## Kernel Pipeline

User Query
→ QueryClassifier
→ AuthorityGate
→ RepositoryManager
→ Authoritative Knowledge Sources
→ Reasoning Engine
→ Canonical Response

## Kernel Modules

### QueryClassifier
Classifies the query domain.

### AuthorityGate
Determines which constitutional authority governs the query.

### RepositoryManager
Retrieves the required authoritative resources.

### Authoritative Knowledge Sources
- Philosophical Constitution
- Semantic Constitution
- Software Constitution
- ADRs
- Canonical Ontology
- Session Footprints
- Candidate Discoveries

### Reasoning Engine
Produces conclusions only from authorized knowledge.

## Non-goals

The Kernel does not perform ontology creation, modify constitutions, or decide canonical truth. It only enforces governance and routes execution.
