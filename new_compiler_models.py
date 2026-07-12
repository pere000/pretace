#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass(slots=True)
class Reduction:

    lexical_unit: str
    lemma: str

    semantic_family: str

    canonical_operator: str

    abstract_operator: str


if __name__ == "__main__":

    r = Reduction(
        lexical_unit="possesses",
        lemma="possess",
        semantic_family="HAS",
        canonical_operator="HAS",
        abstract_operator="𝒯₁",
    )

    print(r)
