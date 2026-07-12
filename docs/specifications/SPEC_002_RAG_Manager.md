# SPEC-002 — RAG Manager

**Status:** Draft

**Version:** 1.0

**Location:**
`docs/specifications/SPEC_002_RAG_Manager.md`

---

## Governed by

- `docs/constitution/TACE_PHILOSOPHICAL_CONSTITUTION.md`
- `docs/constitution/TACE_SEMANTIC_CONSTITUTION.md`
- `docs/constitution/TACE_SOFTWARE_CONSTITUTION.md`
- `docs/architecture/ADR_001_Ontology_Inheritance_Resolver.md`
- `docs/architecture/ADR_002_Resolved_Concept.md`
- `docs/architecture/ADR_003_Interactive_TACE_Query_Pipeline.md`
- `docs/architecture/ADR_004_Canonical_Reasoning_Engine.md`
- `docs/governance/GOVERNANCE.md`
- `docs/developer/DEVELOPMENT_MODE.md`

---

# 1. Purpose

The RAG Manager provides controlled retrieval of information that may be relevant to a user's query.

Its responsibility is limited to retrieving, organizing, classifying and packaging candidate evidence.

The RAG Manager SHALL NOT:

- perform logical reasoning;
- execute inference;
- modify ontology;
- generate canonical knowledge;
- replace the Canonical Reasoning Engine.

Its output is an **Evidence Package** consumed by ADR-003.

---

# 2. Objectives

The RAG Manager shall:

- retrieve repository documents;
- retrieve ontology artifacts;
- retrieve local documents;
- retrieve external documents;
- preserve provenance;
- classify retrieved evidence;
- rank retrieved evidence;
- package evidence for the Query Pipeline.

---

# 3. Scope

Included

- repository retrieval;
- keyword retrieval;
- semantic retrieval;
- vector retrieval;
- hybrid retrieval;
- provenance;
- evidence packaging.

Excluded

- reasoning;
- ontology mutation;
- rule execution;
- AI explanation;
- canonical answer generation.

---

# 4. Architectural Position

```
User Query
      │
      ▼
Interactive Query Pipeline (ADR-003)
      │
      ▼
RAG Manager
      │
      ▼
Evidence Package
      │
      ▼
Knowledge Realizer
      │
      ▼
Canonical Reasoning Engine (ADR-004)
      │
      ▼
Rendered Response
```

The RAG Manager is purely a Retrieval Layer component.

---

# 5. Functional Phases

## Phase 1 — Repository Retrieval

Retrieve information from:

- Constitutions
- ADRs
- Specifications
- Governance
- Developer documentation
- Ontology documentation
- Repository Browser metadata

Acceptance Criteria

- read-only;
- deterministic;
- provenance preserved.

---

## Phase 2 — Local Knowledge Retrieval

Retrieve:

- local PDFs;
- markdown;
- text files;
- repository documents.

Acceptance Criteria

- original location preserved;
- duplicate detection.

---

## Phase 3 — External Retrieval

Retrieve:

- internet pages;
- academic papers;
- approved external repositories;
- configured connectors.

Acceptance Criteria

- provenance mandatory;
- source clearly identified.

---

## Phase 4 — Evidence Ranking

Rank evidence according to:

1. Canonical repository authority.
2. Repository semantic relevance.
3. External semantic relevance.
4. Recency (when applicable).

Ranking shall be deterministic.

---

## Phase 5 — Evidence Package

Produce an immutable Evidence Package containing:

- query identifier;
- retrieved documents;
- retrieval scores;
- provenance;
- source classification;
- retrieval metadata.

This package is forwarded to ADR-003.

---

# 6. Retrieval Sources

Repository

- Constitutions
- ADRs
- Specifications
- Governance
- Developer documentation
- Ontology documentation

Local

- PDF
- Markdown
- Text
- Repository exports

External

- Approved web search
- Academic repositories
- Configured connectors

---

# 7. Provenance

Every retrieved item shall include:

- source;
- document;
- location;
- retrieval method;
- retrieval timestamp;
- repository/external classification.

Provenance shall never be discarded.

---

# 8. User Interface

The RAG Manager panel shall provide:

- query input;
- retrieval source selector;
- retrieval progress;
- retrieved evidence list;
- provenance viewer;
- evidence statistics.

No reasoning results shall appear.

No AI-generated answer shall appear.

---

# 9. Non-Goals

The RAG Manager is not:

- a chatbot;
- a reasoning engine;
- an ontology browser;
- an ontology editor;
- a knowledge author;
- an AI assistant.

---

# 10. Future Extensions

Future specifications may add:

- embedding management;
- vector database administration;
- connector management;
- multimodal retrieval;
- retrieval analytics;
- cache management;
- citation explorer.

---

# 11. Acceptance Criteria

The RAG Manager is accepted when it:

- retrieves repository information;
- retrieves configured external information;
- preserves provenance;
- produces deterministic Evidence Packages;
- never performs reasoning;
- never modifies ontology;
- integrates with ADR-003.

---

# 12. Governance Constraints

The RAG Manager shall obey all governing Constitutions and accepted ADRs.

Canonical repository artifacts always have higher authority than external sources.

External evidence shall never override:

- Constitutions;
- Accepted Ontology;
- Accepted ADRs;
- Canonical repository knowledge.

Conflicts shall be reported rather than resolved by the RAG Manager.

---

# 13. Out of Scope

The following belong elsewhere:

- Repository Browser (SPEC-001)
- Ontology Browser
- Learning Manager
- Canonical Repository Service (ADR-006)
- Canonical Rule Ontology (ADR-005)
- Canonical Reasoning Engine (ADR-004)
- AI Rendering

---

# End of Specification
