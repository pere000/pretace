#!/usr/bin/env python3

"""
TACE Universe State

Represents the current ontological state.
"""

from new_ontology_models import OntologicalRelation


class UniverseState:

    def __init__(self):

        self.entities = {}

        self.asserted_relations = set()

        self.derived_relations = set()

    def add_relation(
        self,
        relation: OntologicalRelation,
        derived=False,
    ):

        self.entities[
            relation.subject.lexical
        ] = relation.subject

        self.entities[
            relation.object.lexical
        ] = relation.object

        triple = (

            relation.subject.lexical,

            relation.operator,

            relation.object.lexical,

        )

        if derived:

            self.derived_relations.add(triple)

        else:

            self.asserted_relations.add(triple)

    @property
    def relations(self):

        return self.asserted_relations | self.derived_relations

    def statistics(self):

        return {

            "entities": len(self.entities),

            "asserted": len(self.asserted_relations),

            "derived": len(self.derived_relations),

            "relations": len(self.relations),

        }

    def show(self):

        print("\nEntities:")

        for e in sorted(self.entities):

            print(" ", e)

        print("\nAsserted:")

        for r in sorted(self.asserted_relations):

            print(" ", r)

        print("\nDerived:")

        for r in sorted(self.derived_relations):

            print(" ", r)

        print("\nStatistics:")

        print(self.statistics())
