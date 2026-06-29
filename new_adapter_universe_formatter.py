#!/usr/bin/env python3

"""
Universe Formatter

Converts the TACE Universe into
canonical text suitable for AI input.
"""

from new_adapter_realizer import SemanticRealizer


class UniverseFormatter:

    def __init__(self):

        self.realizer = SemanticRealizer()

    def format(self, universe):

        lines = []

        for relation in universe.relations:

            lines.append(
                self.realizer.realize(relation)
            )

        return "\n".join(lines)


if __name__ == "__main__":

    from universe.models import UniverseRelation
    from ontology.models import (
        OntologicalEntity,
        OntologicalConcept,
    )

    class DummyUniverse:

        def __init__(self):

            self.relations = [

                UniverseRelation(

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

            ]

    formatter = UniverseFormatter()

    print(
        formatter.format(
            DummyUniverse()
        )
    )
