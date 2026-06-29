#!/usr/bin/env python3

"""
Compiler layer.

These classes represent ONLY what the compiler knows.
No ontology knowledge is allowed here.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LinguisticEntity:
    """
    An entity recognized in the sentence.

    It carries only linguistic information.
    """

    lexical: str


@dataclass(slots=True)
class LinguisticRelation:
    """
    Output of the compiler.

    The operator is a canonical operator,
    not an ontology concept.
    """

    subject: LinguisticEntity

    operator: str

    object: LinguisticEntity


if __name__ == "__main__":

    relation = LinguisticRelation(

        subject=LinguisticEntity(
            lexical="John"
        ),

        operator="HAS",

        object=LinguisticEntity(
            lexical="book"
        )

    )

    print(relation)
