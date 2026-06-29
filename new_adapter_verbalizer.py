#!/usr/bin/env python3

"""
Canonical Operator -> Natural Language verb

Temporary implementation.

Later this will query the ontology database.
"""


class Verbalizer:

    def __init__(self):

        self.verbs = {

            "Possession": "possesses",

            "Existence": "is",

            "Identity": "is",

        }

    def verb(self, concept_name):

        return self.verbs.get(
            concept_name,
            concept_name.lower()
        )


if __name__ == "__main__":

    v = Verbalizer()

    print(v.verb("Possession"))
    print(v.verb("Existence"))
    print(v.verb("Identity"))
    print(v.verb("Unknown"))
