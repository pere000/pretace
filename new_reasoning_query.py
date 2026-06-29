#!/usr/bin/env python3

"""
Reasoning Query

Answers questions using derived knowledge.
"""

class ReasoningQuery:

    def lookup(self, universe, question):

        q = question.lower()

        #
        # Example:
        #
        # Who is an animal?
        #
        if "animal" in q:

            for relation in universe.derived:

                if (
                    relation.operator == "IS_A"
                    and relation.object == "Animal"
                ):

                    return (
                        relation.subject +
                        " is an Animal."
                    )

        return None


if __name__ == "__main__":

    from universe.universe import Universe

    from reasoning.models import DerivedRelation

    universe = Universe()

    universe.derived.append(

        DerivedRelation(

            subject="John",

            operator="IS_A",

            object="Animal",

            rule="IS_A_TRANSITIVITY",

            premises=(),

        )

    )

    query = ReasoningQuery()

    print(

        query.lookup(

            universe,

            "Who is an animal?"

        )

    )
