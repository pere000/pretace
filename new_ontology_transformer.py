#!/usr/bin/env python3

"""
Ontology Transformer

Transforms compiler objects into ontology objects.
"""

from new_compiler_linguistic import (
    LinguisticRelation,
    LinguisticEntity,
)

from new_ontology_models import (
    OntologicalRelation,
    OntologicalEntity,
)

from new_knowledge_concept_repository import ConceptRepository


class OntologyTransformer:

    def __init__(self):

        self.repository = ConceptRepository()

    def transform(self, relation: LinguisticRelation):

        # Canonical operator bridge
        #
        # For now, preserve the canonical operator produced
        # by the Soar of the Logos.
        concept = relation.operator

        subject = relation.subject.lexical.strip()
        obj = relation.object.lexical.strip()

        # Canonical case normalization
        subject = subject[:1].upper() + subject[1:]
        obj = obj[:1].upper() + obj[1:]

        return OntologicalRelation(

            subject=OntologicalEntity(
                entity_id=None,
                concept_id=None,
                lexical=subject,
            ),

            operator=concept,

            object=OntologicalEntity(
                entity_id=None,
                concept_id=None,
                lexical=obj,
            ),

        )


if __name__ == "__main__":

    transformer = OntologyTransformer()

    relation = LinguisticRelation(

        subject=LinguisticEntity("John"),

        operator="HAS",

        object=LinguisticEntity("book"),

    )

    print(transformer.transform(relation))
