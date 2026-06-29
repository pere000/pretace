#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass(slots=True)
class Entity:
    """
    Entity identified in the sentence.
    """

    lexical: str
    category: str = "Unknown"
    ontology_id: int | None = None


@dataclass(slots=True)
class OntologyConcept:
    """
    Authoritative ontology concept.

    The ID is the identity.
    The remaining fields are metadata.
    """

    id: int
    module: str
    concept: str


@dataclass(slots=True)
class UniverseRelation:
    """
    Symbolic relation inside the TACE Universe.
    """

    subject: Entity
    operator: OntologyConcept
    object: Entity


if __name__ == "__main__":

    relation = UniverseRelation(

        subject=Entity(
            lexical="John",
            category="Human"
        ),

        operator=OntologyConcept(
            id=1,
            module="TACE",
            concept="Possession"
        ),

        object=Entity(
            lexical="book",
            category="Artifact"
        )

    )

    print(relation)
