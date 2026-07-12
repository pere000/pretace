#!/usr/bin/env python3

"""
Knowledge Realizer

Builds canonical answer packages for ADR-003 assistance rendering.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sqlite3
from collections import deque


class KnowledgeRealizer:

    def __init__(self, db_path="tace_knowledge.db"):

        self.db_path = Path(db_path)
        self.max_depth = self._load_max_depth()
        self._concept_names_cache = None
        self._alias_entries_cache = None

    def realize(
        self,
        question,
        explicit=None,
        resolved=None,
        relation_answer=None,
    ):

        if explicit is not None:
            return self._from_explicit(explicit, resolved)

        if relation_answer is not None:
            return self._from_relational(relation_answer)

        return self._undetermined_package()

    def _from_explicit(self, explicit, resolved):

        concept = explicit["concept_name"]
        definition = (explicit.get("definition") or "").strip()

        if definition:
            canonical_answer = f"{concept}: {definition}"
        else:
            canonical_answer = (
                f"{concept}: definition is currently not recorded "
                "in accepted ontology."
            )

        root_concepts = {concept}
        if resolved is not None:
            root_concepts.update(resolved.get("inherited_ontology", []))

        root_concepts.update(
            self._find_concepts_in_text(canonical_answer)
        )

        package = self._build_expansion(root_concepts)
        package["CanonicalAnswer"] = canonical_answer
        package["CanonicalJustification"].insert(
            0,
            "Answer derived from accepted ontology concept record.",
        )

        if explicit.get("relations"):
            package["CanonicalJustification"].append(
                "Related ontology relations were included for semantic context."
            )

        if resolved is not None and resolved.get("inherited_ontology"):
            inherited = ", ".join(resolved["inherited_ontology"])
            package["CanonicalAnswer"] += (
                "\n\nResolved inheritance (ADR-001/ADR-002): "
                f"{concept} IS_A {inherited}."
            )
            root_concepts.update(
                self._find_concepts_in_text(package["CanonicalAnswer"])
            )
            package = self._build_expansion(root_concepts)
            package["CanonicalAnswer"] = canonical_answer + (
                "\n\nResolved inheritance (ADR-001/ADR-002): "
                f"{concept} IS_A {inherited}."
            )
            package["CanonicalJustification"].insert(
                0,
                "Answer derived from accepted ontology concept record.",
            )
            if explicit.get("relations"):
                package["CanonicalJustification"].append(
                    "Related ontology relations were included for semantic context."
                )
            package["CanonicalProvenance"].append(
                {
                    "type": "resolved_concept",
                    "semantic_identity": resolved["semantic_identity"],
                    "canonical_signature": resolved["canonical_signature"],
                    "resolution_policy": resolved["resolution_policy"],
                    "inheritance_graph": resolved["inheritance_graph"],
                    "origin": "ADR-001/ADR-002",
                    "ConstitutionalStatus": "accepted",
                }
            )

        package["ReferencedConcepts"] = sorted(
            self._find_concepts_in_text(package["CanonicalAnswer"]),
            key=str.lower,
        )

        if package["UnresolvedConcepts"]:
            package["ConstitutionalStatus"] = "undetermined"

        return package

    def _from_relational(self, relation_answer):

        relation_concepts = self._extract_concepts_from_provenance(
            relation_answer.get("provenance", [])
        )

        package = self._build_expansion(relation_concepts)
        package["CanonicalAnswer"] = relation_answer["answer"]
        package["CanonicalJustification"] = list(
            relation_answer.get("justification", [])
        )
        package["CanonicalProvenance"] = list(
            relation_answer.get("provenance", [])
        ) + package["CanonicalProvenance"]
        package["ReferencedConcepts"] = sorted(
            self._find_concepts_in_text(package["CanonicalAnswer"]),
            key=str.lower,
        )

        if package["UnresolvedConcepts"]:
            package["ConstitutionalStatus"] = "undetermined"

        return package

    def _undetermined_package(self):
        return {
            "CanonicalAnswer": (
                "Undetermined within TACE: the accepted ontology "
                "does not determine an answer."
            ),
            "CanonicalDefinitions": [],
            "CanonicalRelations": [],
            "CanonicalProvenance": [],
            "CanonicalJustification": [
                "No explicit ontology definition or valid semantic "
                "resolution determined the queried matter."
            ],
            "ConstitutionalStatus": "undetermined",
            "ExpansionDepth": 0,
            "RetrievedConcepts": [],
            "UnresolvedConcepts": [],
            "ReferencedConcepts": [],
        }

    def _build_expansion(self, root_concepts):

        definitions = []
        relations = []
        provenance = []
        retrieved = []
        unresolved = []
        relation_seen = set()

        queue = deque(
            (concept, 0)
            for concept in sorted(c for c in root_concepts if c)
        )
        visited = set()
        max_depth_reached = 0

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            while queue:
                concept, depth = queue.popleft()
                key = concept.lower()

                if key in visited:
                    continue
                visited.add(key)
                max_depth_reached = max(max_depth_reached, depth)

                row = conn.execute(
                    """
                    SELECT concept_name, ontology_module, definition, status
                    FROM concept_records
                    WHERE LOWER(concept_name)=LOWER(?)
                    LIMIT 1
                    """,
                    (concept,),
                ).fetchone()

                if row is None:
                    unresolved.append(concept)
                    continue

                concept_name = row["concept_name"]
                retrieved.append(concept_name)
                definition = (row["definition"] or "").strip()

                definitions.append(
                    {
                        "concept": concept_name,
                        "module": row["ontology_module"],
                        "definition": definition,
                        "ConstitutionalStatus": row["status"] or "unknown",
                    }
                )

                provenance.append(
                    {
                        "type": "concept_definition",
                        "concept": concept_name,
                        "module": row["ontology_module"],
                        "origin": "accepted_ontology",
                        "definition_present": bool(definition),
                        "ConstitutionalStatus": row["status"] or "unknown",
                    }
                )

                rel_rows = conn.execute(
                    """
                    SELECT source_concept, relation_type, target_concept,
                           confidence, notes
                    FROM ontology_relations
                    WHERE LOWER(source_concept)=LOWER(?)
                       OR LOWER(target_concept)=LOWER(?)
                    ORDER BY id
                    """,
                    (concept_name, concept_name),
                ).fetchall()

                for rel in rel_rows:
                    rel_obj = {
                        "source_concept": rel["source_concept"],
                        "relation_type": rel["relation_type"],
                        "target_concept": rel["target_concept"],
                        "confidence": rel["confidence"],
                        "notes": rel["notes"],
                        "ConstitutionalStatus": "accepted",
                    }
                    rel_key = (
                        rel_obj["source_concept"],
                        rel_obj["relation_type"],
                        rel_obj["target_concept"],
                    )
                    if rel_key not in relation_seen:
                        relation_seen.add(rel_key)
                        relations.append(rel_obj)

                if depth >= self.max_depth:
                    continue

                for rel in rel_rows:
                    for next_concept in (
                        rel["source_concept"],
                        rel["target_concept"],
                    ):
                        if next_concept.lower() in visited:
                            continue
                        queue.append((next_concept, depth + 1))

        return {
            "CanonicalAnswer": "",
            "CanonicalDefinitions": definitions,
            "CanonicalRelations": relations,
            "CanonicalProvenance": provenance,
            "CanonicalJustification": [],
            "ConstitutionalStatus": "canonical",
            "ExpansionDepth": max_depth_reached,
            "RetrievedConcepts": sorted(set(retrieved), key=str.lower),
            "UnresolvedConcepts": sorted(set(unresolved), key=str.lower),
            "ReferencedConcepts": [],
        }

    def _extract_concepts_from_provenance(self, provenance):

        concepts = set()
        for item in provenance:
            if not isinstance(item, dict):
                continue
            for key in ("concept", "source_concept", "target_concept"):
                value = item.get(key)
                if value and isinstance(value, str):
                    concepts.add(value)

        return concepts

    def _load_max_depth(self):

        env_value = os.getenv("TACE_EXPANSION_MAX_DEPTH")
        if env_value and env_value.isdigit():
            return max(0, int(env_value))

        runtime_path = Path(__file__).resolve().parent / "new_tace_runtime.json"
        if runtime_path.exists():
            with runtime_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                value = (
                    data.get("ask_tace", {})
                    .get("expansion_max_depth")
                )
                if isinstance(value, int) and value >= 0:
                    return value

        return 2

    def _find_concepts_in_text(self, text):

        if not text:
            return set()

        tokens = self._tokenize(text)
        if not tokens:
            return set()

        matches = []
        alias_entries = self._alias_entries()

        for start in range(len(tokens)):
            for entry in alias_entries:
                phrase_tokens = entry["tokens"]
                end = start + len(phrase_tokens)
                if end > len(tokens):
                    continue
                if [t["norm"] for t in tokens[start:end]] != phrase_tokens:
                    continue
                matches.append(
                    {
                        "concept": entry["concept"],
                        "start": start,
                        "end": end,
                        "length": len(phrase_tokens),
                    }
                )

        matches.sort(
            key=lambda m: (
                -m["length"],
                m["start"],
                m["end"],
                m["concept"].lower(),
            )
        )

        selected = []
        occupied = set()
        for match in matches:
            span = set(range(match["start"], match["end"]))
            if span & occupied:
                continue
            selected.append(match)
            occupied.update(span)

        return {m["concept"] for m in selected}

    def _all_concept_names(self):

        if self._concept_names_cache is not None:
            return self._concept_names_cache

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT concept_name
                FROM concept_records
                """
            ).fetchall()

        self._concept_names_cache = [row["concept_name"] for row in rows]
        return self._concept_names_cache

    def _alias_entries(self):

        if self._alias_entries_cache is not None:
            return self._alias_entries_cache

        entries = []
        seen = set()

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT concept_name, terminology_mapping
                FROM concept_records
                """
            ).fetchall()

        for row in rows:
            concept = row["concept_name"]
            candidates = {
                concept,
                concept.replace("_", " "),
            }
            candidates.update(
                self._aliases_from_mapping(row["terminology_mapping"])
            )

            for candidate in candidates:
                tokens = self._normalize_phrase_to_tokens(candidate)
                if not tokens:
                    continue
                key = (concept.lower(), tuple(tokens))
                if key in seen:
                    continue
                seen.add(key)
                entries.append(
                    {
                        "concept": concept,
                        "tokens": tokens,
                    }
                )

        entries.sort(
            key=lambda e: (
                -len(e["tokens"]),
                e["concept"].lower(),
                " ".join(e["tokens"]),
            )
        )
        self._alias_entries_cache = entries
        return entries

    def _aliases_from_mapping(self, terminology_mapping):

        if not terminology_mapping:
            return set()

        aliases = set()
        parts = terminology_mapping.split(";")
        for part in parts:
            chunk = part.strip()
            if not chunk:
                continue
            if "->" in chunk:
                left = chunk.split("->", 1)[0].strip()
                if left:
                    aliases.add(left)
            else:
                aliases.add(chunk)

        return aliases

    def _normalize_phrase_to_tokens(self, phrase):

        if not phrase:
            return []

        normalized = phrase.lower().replace("_", " ")
        tokens = re.findall(r"[a-z0-9]+", normalized)
        return tokens

    def _tokenize(self, text):

        tokens = []
        for match in re.finditer(r"[A-Za-z0-9_]+", text):
            raw = match.group(0)
            norm = raw.lower().replace("_", " ")
            for part in re.findall(r"[a-z0-9]+", norm):
                tokens.append(
                    {
                        "raw": raw,
                        "norm": part,
                        "start": match.start(),
                        "end": match.end(),
                    }
                )
        return tokens
