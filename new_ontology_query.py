#!/usr/bin/env python3

"""
Ontology Query

Temporary lookup service.

Later this will query the ontology repository/database.
"""

class OntologyQuery:

    def __init__(self):

        self.definitions = {

            "matrix":
                "Global rule-structured space of admissible state transitions across all possible configurations of reality.",

            "q-form":
                "Formal possibility encoding layer governing admissible material instantiations.",

            "silver bridge":
                "Epistemological-ontological bridge relating acts of consciousness to quantum soma patterns.",

        }

    def lookup(self, question):

        q = question.lower()

        for concept, definition in self.definitions.items():

            if concept in q:

                return definition

        return None


if __name__ == "__main__":

    query = OntologyQuery()

    print(query.lookup("What is Matrix?"))
    print(query.lookup("What is Q-Form?"))
    print(query.lookup("Who wrote Hamlet?"))
