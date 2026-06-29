#!/usr/bin/env python3

from new_compiler_database import LexiconDB
from new_compiler_models import Reduction


class Resolver:

    def __init__(self):
        self.db = LexiconDB()

    def resolve(self, lexical_unit: str) -> Reduction | None:

        data = self.db.resolve(lexical_unit)

        if data is None:
            return None

        return Reduction(
            lexical_unit=data["lexical_unit"],
            lemma=data["lemma"],
            semantic_family=data["semantic_family"],
            canonical_operator=data["canonical_operator"],
            abstract_operator=data["abstract_operator"],
        )


if __name__ == "__main__":

    resolver = Resolver()

    print(resolver.resolve("possesses"))
