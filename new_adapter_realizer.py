#!/usr/bin/env python3

"""
TACE Semantic Realizer

Canonical Language
        ↓
Natural Language
"""

from new_ontology_models import (
    OntologicalRelation,
    OntologicalEntity,
    OntologicalConcept,
)

from new_adapter_verbalizer import Verbalizer


class SemanticRealizer:

    def __init__(self):

        self.verbalizer = Verbalizer()

    def realize(self, relation: OntologicalRelation) -> str:

        # Migration compatibility:
        # operator may be an OntologicalConcept or a canonical operator string.

        operator = relation.operator

        if hasattr(operator, "name"):
            operator = operator.name

        verb = self.verbalizer.verb(operator)

        return (
            f"{relation.subject.lexical} "
            f"{verb} "
            f"{relation.object.lexical}."
        )


if __name__ == "__main__":

    relation = OntologicalRelation(

        subject=OntologicalEntity(
            entity_id=None,
            concept_id=None,
            lexical="John",
        ),

        operator=OntologicalConcept(
            concept_id=1,
            module="TACE",
            name="Possession",
        ),

        object=OntologicalEntity(
            entity_id=None,
            concept_id=None,
            lexical="book",
        ),
    )

    realizer = SemanticRealizer()

    print(realizer.realize(relation))
