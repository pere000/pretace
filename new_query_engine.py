#!/usr/bin/env python3

"""
Interactive Ask TACE Query Engine

Canonical pipeline:

    Query Intake
        ↓
    Constitutional Authority Gate
        ↓
    Explicit Ontology Retrieval
        ↓
    Semantic Resolution (ADR-001 + ADR-002)
        ↓
    Semantic Validation
        ↓
    Knowledge Realizer
        ↓
    Controlled AI Assistance (optional)
        ↓
    Final Response
"""

from __future__ import annotations

from datetime import datetime, timezone
import re
import sqlite3
from types import MappingProxyType
import uuid

import requests

from new_adapter_session import TACESession
from new_knowledge_realizer import KnowledgeRealizer
from new_ontology_inheritance_resolver import OntologyInheritanceResolver
from new_ontology_query import OntologyQuery


class QueryEngine:

    RENDERING_MODES = {
        "technical",
        "academic",
        "educational",
        "popular",
        "child",
    }

    def __init__(self):

        self.ontology = OntologyQuery()
        self.resolver = OntologyInheritanceResolver()
        self.realizer = KnowledgeRealizer()
        self.ai = TACESession()

    def ask(
        self,
        universe,
        question,
        assist=False,
        rendering_mode="technical",
    ):

        trace_id = str(uuid.uuid4())
        normalized, inline_assist, inline_mode = self._query_intake(question)
        assist_requested = assist or inline_assist
        selected_mode = inline_mode or (rendering_mode or "technical")
        selected_mode = selected_mode.lower().strip()

        if not normalized:
            return self._error(
                trace_id,
                "empty_query",
                "Question is empty after normalization.",
            )
        if selected_mode not in self.RENDERING_MODES:
            return self._error(
                trace_id,
                "invalid_rendering_mode",
                f"Unsupported rendering mode: {selected_mode}",
            )

        try:
            self._authority_gate(normalized)

            explicit = self._explicit_ontology_retrieval(normalized)
            resolved = self._semantic_resolution(universe, explicit)
            relational = self._relational_lookup(universe, normalized)

            canonical = self._knowledge_realization(
                normalized,
                explicit,
                resolved,
                relational,
            )
            self._semantic_validation(canonical)

            response = self._package_response(
                trace_id=trace_id,
                question=normalized,
                canonical=canonical,
            )

            if (
                response["status"] == "canonical"
                and assist_requested
            ):
                immutable_package = self._freeze_package(
                    response["CanonicalExpansionPackage"]
                )
                verification = self._verify_canonical_package(
                    immutable_package
                )
                if not verification["ok"]:
                    missing = verification.get(
                        "missing_definition_concepts", []
                    )
                    if missing:
                        response["assisted_explanation"] = "\n".join(
                            [
                                f'No canonical definition is available for "{concept}".'
                                for concept in missing
                            ]
                        )
                    response["justification"].append(
                        "AI assistance skipped: "
                        + "; ".join(verification["errors"])
                    )
                    return response

                try:
                    assistance = self._controlled_ai_assistance(
                        universe=universe,
                        canonical_package=immutable_package,
                        rendering_mode=selected_mode,
                    )
                except requests.RequestException as exc:
                    response["justification"].append(
                        "AI assistance was requested but unavailable: "
                        f"{exc}"
                    )
                    return response

                if assistance is not None:
                    response["status"] = "assisted"
                    response["assisted_explanation"] = assistance
                    response["source_decomposition"].append(
                        "ai_assistance_non_canonical"
                    )
                    response["justification"].append(
                        "AI assistance added as non-canonical explanation "
                        "after canonical answer construction."
                    )

            return response

        except sqlite3.Error as exc:
            return self._error(
                trace_id,
                "ontology_storage_error",
                str(exc),
            )
        except ValueError as exc:
            return self._error(
                trace_id,
                "pipeline_validation_error",
                str(exc),
            )

    def _query_intake(self, question):
        normalized = (question or "").strip()
        assist_requested = self._should_assist(normalized)
        mode = None

        for candidate in self.RENDERING_MODES:
            marker = f"[assist:{candidate}]"
            if marker in normalized.lower():
                normalized = re.sub(
                    re.escape(marker),
                    "",
                    normalized,
                    flags=re.IGNORECASE,
                ).strip()
                assist_requested = True
                mode = candidate
                break

        if normalized.lower().startswith("assist:"):
            tail = normalized.split(":", 1)[1].strip()
            assist_requested = True
            mode_match = re.match(
                r"^(technical|academic|educational|popular|child)\s*:\s*(.+)$",
                tail,
                flags=re.IGNORECASE,
            )
            if mode_match:
                mode = mode_match.group(1).lower()
                normalized = mode_match.group(2).strip()
            else:
                normalized = tail

        normalized = normalized.replace("[assist]", "").strip()

        return normalized, assist_requested, mode

    def _authority_gate(self, question):
        if not question:
            raise ValueError("Query failed constitutional authority gate.")

    def _explicit_ontology_retrieval(self, question):
        return self.ontology.lookup(question)

    def _semantic_resolution(self, universe, explicit):
        if explicit is None:
            return None
        return self.resolver.resolve(explicit, universe)

    def _semantic_validation(self, canonical):
        status = canonical["ConstitutionalStatus"]
        if status not in {"canonical", "undetermined"}:
            raise ValueError("Invalid canonical status emitted.")
        if not canonical["CanonicalAnswer"]:
            raise ValueError("Canonical answer text cannot be empty.")

    def _knowledge_realization(
        self,
        question,
        explicit,
        resolved,
        relational,
    ):
        return self.realizer.realize(
            question=question,
            explicit=explicit,
            resolved=resolved,
            relation_answer=relational,
        )

    def _controlled_ai_assistance(
        self,
        universe,
        canonical_package,
        rendering_mode,
    ):
        return self.ai.ask(
            universe,
            "",
            mode="assist",
            canonical_package=canonical_package,
            rendering_mode=rendering_mode,
        )

    def _package_response(
        self,
        trace_id,
        question,
        canonical,
    ):
        return {
            "source": "Ask TACE Pipeline",
            "status": canonical["ConstitutionalStatus"],
            "answer": canonical["CanonicalAnswer"],
            "source_decomposition": [
                "canonical expansion package",
                "knowledge realizer",
            ],
            "justification": canonical["CanonicalJustification"],
            "provenance": canonical["CanonicalProvenance"],
            "trace_id": trace_id,
            "question": question,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "CanonicalExpansionPackage": canonical,
        }

    def _error(self, trace_id, code, detail):
        return {
            "source": "Ask TACE Pipeline",
            "status": "error",
            "answer": (
                "Error: the query pipeline could not complete processing."
            ),
            "source_decomposition": ["error"],
            "justification": [
                "Operational failure prevented successful processing.",
            ],
            "provenance": [],
            "trace_id": trace_id,
            "error": {
                "code": code,
                "detail": detail,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _should_assist(self, question):
        q = question.lower().strip()
        if q.startswith("assist:") or "[assist]" in q:
            return True
        return any(
            f"[assist:{mode}]" in q
            for mode in self.RENDERING_MODES
        )

    def _freeze_package(self, value):
        if isinstance(value, dict):
            return MappingProxyType(
                {k: self._freeze_package(v) for k, v in value.items()}
            )
        if isinstance(value, list):
            return tuple(self._freeze_package(v) for v in value)
        return value

    def _verify_canonical_package(self, package):

        errors = []

        retrieved = set(package["RetrievedConcepts"])
        unresolved = tuple(package["UnresolvedConcepts"])
        definitions = tuple(package["CanonicalDefinitions"])
        provenance = tuple(package["CanonicalProvenance"])
        referenced = set(package.get("ReferencedConcepts", ()))

        if unresolved:
            errors.append(
                "Unresolved concepts remain: " + ", ".join(unresolved)
            )

        provenance_concepts = {
            p.get("concept")
            for p in provenance
            if hasattr(p, "get") and p.get("concept")
        }
        missing_provenance = sorted(
            concept for concept in retrieved
            if concept not in provenance_concepts
        )
        if missing_provenance:
            errors.append(
                "Missing provenance for concepts: "
                + ", ".join(missing_provenance)
            )

        invalid_origin = []
        for item in provenance:
            if not hasattr(item, "get"):
                continue
            if item.get("type") != "concept_definition":
                continue
            if item.get("origin") != "accepted_ontology":
                invalid_origin.append(item.get("concept", "?"))
        if invalid_origin:
            errors.append(
                "Definitions not sourced from accepted ontology: "
                + ", ".join(sorted(set(invalid_origin)))
            )

        definition_concepts = {
            item.get("concept")
            for item in definitions
            if hasattr(item, "get")
        }
        empty_definition_concepts = {
            item.get("concept")
            for item in definitions
            if hasattr(item, "get")
            and item.get("concept")
            and not (item.get("definition") or "").strip()
        }
        undefined = sorted(
            concept for concept in retrieved
            if concept not in definition_concepts
        )
        if undefined:
            errors.append(
                "Referenced concepts missing definitions: "
                + ", ".join(undefined)
            )

        referenced_missing = sorted(
            concept for concept in referenced
            if concept not in definition_concepts
            or concept in empty_definition_concepts
        )
        if referenced_missing:
            errors.append(
                "Referenced concepts in canonical answer lack canonical "
                "definitions: " + ", ".join(referenced_missing)
            )

        referenced_missing_provenance = sorted(
            concept for concept in referenced
            if concept not in provenance_concepts
        )
        if referenced_missing_provenance:
            errors.append(
                "Referenced concepts in canonical answer lack provenance: "
                + ", ".join(referenced_missing_provenance)
            )

        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "missing_definition_concepts": referenced_missing,
        }

    def _relational_lookup(self, universe, question):

        q = question.lower()

        possession = self._who_possesses(universe, q)
        if possession is not None:
            return possession

        isa = self._who_is_a(universe, q)
        if isa is not None:
            return isa

        return None

    def _who_possesses(self, universe, q):
        if "who" not in q or "possess" not in q:
            return None

        match = re.search(
            r"who\s+possess(?:es)?\s+(?:the\s+|a\s+|an\s+)?(.+?)\??$",
            q,
        )
        if not match:
            return None

        target_lower = match.group(1).strip().lower()
        if not target_lower:
            return None

        for relation in universe.relations:
            if relation.operator not in {"HAS", "Possession"}:
                continue
            if relation.object.lexical.lower() != target_lower:
                continue

            return {
                "answer": (
                    f"{relation.subject.lexical} possesses "
                    f"{relation.object.lexical}."
                ),
                "source_decomposition": ["asserted relation"],
                "justification": [
                    "Answer derived from asserted universe relation."
                ],
                "provenance": [
                    {
                        "type": "universe_relation",
                        "subject": relation.subject.lexical,
                        "operator": relation.operator,
                        "object": relation.object.lexical,
                    }
                ],
            }

        return None

    def _who_is_a(self, universe, q):
        if "who" not in q or " is " not in f" {q} ":
            return None

        match = re.search(r"who\s+is\s+(?:an?\s+)?([a-z0-9_\- ]+)\??", q)
        if not match:
            return None

        target = match.group(1).strip().lower()
        if not target:
            return None

        subjects = []
        provenance = []

        for subject, operator, obj in sorted(universe.derived):
            if operator != "IS_A":
                continue
            if obj.lower() != target:
                continue
            subjects.append(subject)
            provenance.append(
                {
                    "type": "derived_relation",
                    "subject": subject,
                    "operator": operator,
                    "object": obj,
                }
            )

        if subjects:
            joined = ", ".join(subjects)
            return {
                "answer": f"{joined} is {target.capitalize()}.",
                "source_decomposition": ["reasoned derivation"],
                "justification": [
                    "Answer derived from transitive IS_A reasoning."
                ],
                "provenance": provenance,
            }

        return None

if __name__ == "__main__":

    from new_pipeline_engine import TACEEngine

    engine = TACEEngine()
    query = QueryEngine()

    print(query.ask(engine.universe, "What is Matrix?"))
