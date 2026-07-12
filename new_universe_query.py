#!/usr/bin/env python3

"""
Universe Query

Answers questions using the current Universe
without consulting the AI.
"""

class UniverseQuery:

    def lookup(self, universe, question):

        q = question.lower()

        #
        # Who possesses X?
        #
        if "who" in q and "possess" in q:

            for relation in universe.relations:

                if relation.operator.name == "Possession":

                    return (
                        relation.subject.lexical +
                        " possesses the " +
                        relation.object.lexical + "."
                    )

        return None


if __name__ == "__main__":

    from pipeline.engine import TACEEngine

    engine = TACEEngine()

    universe = engine.learn(
        "John possesses the book."
    )

    query = UniverseQuery()

    print(

        query.lookup(

            universe,

            "Who possesses the book?"

        )

    )
