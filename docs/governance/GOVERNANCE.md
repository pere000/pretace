# TACE Project Governance

## Status

Active governance document.

## Document Type

This document is a **project governance document**.  
It is **not** a Constitution and **not** an ADR.

## Purpose

This document defines how the TACE project is governed: decision flow, implementation authority, escalation rules, and change control across constitutions, ADRs, ontology, and repository implementation.

## Governance Baseline

The following artifacts are authoritative and stable unless a validated architectural defect requires formal change:

- TACE Philosophical Constitution
- TACE Semantic Constitution
- TACE Software Constitution
- ADR-001 — Ontology Inheritance Resolver
- ADR-002 — Resolved Concept
- ADR-003 — Interactive Query Pipeline
- ADR-004 — Canonical Reasoning Engine

## Governance Principles

1. Architectural stability is preferred over architectural convenience.
2. Accepted Constitutions and ADRs are normative governance, not optional guidance.
3. Implementation evolves incrementally under accepted architectural contracts.
4. New capabilities should be introduced through new ADRs, not silent redesign of accepted ADRs.

## Architectural Escalation Rule

If an implementation request appears to conflict with an accepted Constitution or ADR:

1. Identify the governing contract.
2. Explain the exact conflict.
3. Classify the issue as implementation defect, architectural defect, incomplete architecture, or new architectural capability.
4. If architecture is sufficient, preserve it in implementation.
5. If architecture is incomplete, propose a new ADR.
6. Amend accepted Constitutions/ADRs only when a genuine architectural defect is demonstrated and no extension can resolve it.

## Development Priorities

Implementation proposals should prioritize:

1. Repository structure
2. Developer experience
3. Implementation quality
4. Performance
5. Testing
6. Future ADR candidates (when needed)

## Change Control Scope

This document governs project process and decision protocol.  
It does not redefine constitutional ontology, semantic, or software contracts.

## See Also

- `docs/developer/DEVELOPMENT_MODE.md`
- `docs/architecture/ROADMAP.md`
