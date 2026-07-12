# TACE Development Mode

## Purpose

This document defines the current operational mode for contributors (human and AI).  
It describes how work is executed now and may be updated frequently.

## Current Project Phase

Implementation phase on top of a stable constitutional and architectural baseline.

## Architecture Status

Architecture is stable and implementation is incremental.  
Constitutions and accepted ADRs are treated as normative governance.

## Accepted Constitutional Baseline

- TACE Philosophical Constitution
- TACE Semantic Constitution
- TACE Software Constitution

## Frozen ADR Baseline

- ADR-001 — Ontology Inheritance Resolver
- ADR-002 — Resolved Concept
- ADR-003 — Interactive Query Pipeline
- ADR-004 — Canonical Reasoning Engine

## Current Implementation Priorities

1. Repository structure and module boundaries
2. Developer experience (tooling, diagnostics, documentation)
3. Implementation quality (maintainability, robustness)
4. Performance improvements preserving behavior
5. Testing expansion (unit, integration, regression, compliance)

## Engineering Principles

- Preserve accepted contracts and invariants.
- Prefer incremental improvements over broad rewrites.
- Keep canonical and derived artifacts explicitly separated.
- Maintain deterministic behavior, explicit provenance, and constitutional verification.

## Architectural Escalation Rule

If a request appears to conflict with an accepted Constitution or ADR:

1. Identify the governing contract.
2. Explain the exact conflict.
3. Classify it as implementation defect, architectural defect, incomplete architecture, or new capability.
4. Preserve architecture when sufficient.
5. Propose a new ADR when architecture is incomplete.
6. Amend accepted artifacts only for demonstrated architectural defects that cannot be resolved by extension.

## AI Assistant Operating Rules

- Operate primarily as implementation engineer on the accepted baseline.
- Do not redesign accepted Constitutions/ADRs unless a genuine defect is demonstrated.
- Do not introduce silent architectural workarounds.
- Escalate conflicts explicitly before proposing code that would violate governance.

## Mandatory Governance Verification Before Implementation

Before implementing any code, every AI assistant or contributor shall:

1. Identify the governing authority applicable to the requested change:
   - Constitutions
   - Accepted ADRs
   - Governance documents
   - Development documents (when relevant)

2. Map the requested implementation against those governing contracts, identifying:
   - required behavior,
   - prohibited behavior,
   - implementation constraints.

3. Detect and report any contradictions, ambiguities, or stale documentation that could affect implementation.

4. Suspend implementation whenever the governing interpretation is unclear.

5. Resume implementation only after:
   - the governing interpretation is unambiguous, or
   - the project maintainer explicitly resolves the ambiguity, or
   - a new ADR or constitutional amendment establishes the required authority.

This verification phase is mandatory and precedes any code generation or repository modification.

## Current Milestone

ADR-005 — Canonical Rule Ontology (planned milestone focus).

## Current Implementation Focus

- Hardening canonical query/reasoning implementation quality.
- Expanding deterministic and constitutional compliance tests.
- Improving maintainability and developer workflow around the accepted architecture.

## Governed By

- `docs/governance/GOVERNANCE.md`

## See Also

- `docs/architecture/ROADMAP.md`
