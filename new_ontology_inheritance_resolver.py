#!/usr/bin/env python3

"""
Ontology Inheritance Resolver

ADR-001 component used by the interactive query pipeline.
Produces ADR-002-style resolved concept artifacts.
"""


class OntologyInheritanceResolver:

    def resolve(self, explicit_concept, universe):

        if explicit_concept is None:
            return None

        concept = explicit_concept["concept_name"]
        graph = self._inheritance_graph(universe)

        inherited = self._transitive_parents(concept, graph)

        if not inherited:
            return None

        inherited_sorted = sorted(inherited)

        return {
            "semantic_identity": concept,
            "explicit_ontology": concept,
            "inherited_ontology": inherited_sorted,
            "resolved_relationships": [
                {"subject": concept, "operator": "IS_A", "object": parent}
                for parent in inherited_sorted
            ],
            "semantic_justification": (
                "Inherited ontology derived via IS_A transitivity "
                "using the active universe semantic state."
            ),
            "provenance": [
                {
                    "originating_concept": concept,
                    "originating_relation": "IS_A",
                    "inheritance_path": f"{concept} -> {parent}",
                    "semantic_resolution_basis": "IS_A transitivity",
                }
                for parent in inherited_sorted
            ],
            "resolution_policy": {
                "inheritance": "enabled",
                "precedence": "explicit_over_inherited",
                "conflict_handling": "preserve_explicit",
                "inheritance_depth": "transitive",
            },
            "inheritance_graph": {
                "root": concept,
                "parents": inherited_sorted,
            },
            "conflict_report": [],
            "boundary_markers": {
                "authoritative_ontology": "explicit_concept_record",
                "resolved_inheritance": "derived_is_a",
                "higher_reasoning_layers": "excluded",
            },
            "canonical_signature": (
                f"{concept}|IS_A|{','.join(inherited_sorted)}"
            ),
        }

    def _inheritance_graph(self, universe):

        graph = {}

        for triple in universe.asserted | universe.derived:
            subject, operator, obj = triple
            if operator != "IS_A":
                continue
            graph.setdefault(subject, set()).add(obj)

        return graph

    def _transitive_parents(self, concept, graph):

        visited = set()
        pending = list(graph.get(concept, set()))

        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            pending.extend(graph.get(current, set()))

        return visited
