#!/usr/bin/env python3

"""
TACE Query Engine

Priority

    Ontology
        ↓
    Universe
        ↓
    Reasoner
        ↓
    Local AI
"""

from new_adapter_session import TACESession
from new_ontology_query import OntologyQuery
from new_universe_query import UniverseQuery
from new_reasoning_query import ReasoningQuery
from new_constructor_constructor import Constructor


class QueryEngine:

    def __init__(self):

        self.ai = TACESession()
        self.ontology = OntologyQuery()
        self.universe = UniverseQuery()
        self.reasoner = ReasoningQuery()
        self.constructor = Constructor()

    def ask(self, universe, question):

        #
        # Ontology
        #
        answer = self.ontology.lookup(question)

        if answer is not None:
            return {"source":"Ontology","answer":answer}

        #
        # Universe
        #
        answer = self.universe.lookup(universe, question)

        if answer is not None:
            return {"source":"Universe","answer":answer}

        #
        # Reasoner
        #
        answer = self.reasoner.lookup(universe, question)

        if answer is not None:
            return {"source":"Reasoner","answer":answer}

        #
        # Constructor
        #
        subject = (
            question.lower()
            .replace("what is ", "")
            .replace("what is a ", "")
            .replace("what is an ", "")
            .replace("?", "")
            .strip()
        )

        answer = self.constructor.construct(
            universe,
            subject,
        )

        if answer is not None:

            return {
                "source":"TACE Constructor",
                "answer":answer,
            }

        #
        # Local AI
        #
        answer = self.ai.ask(
            universe,
            question,
            mode="fallback",
        )

        return {
            "source":"Local AI",
            "answer":answer,
            "note":"This information comes from the Local AI and has NOT yet become TACE knowledge."
        }


if __name__ == "__main__":

    from pipeline.engine import TACEEngine

    engine = TACEEngine()

    engine.learn("John possesses the book.")

    query = QueryEngine()

    print("1) Ontology")
    print(query.ask(engine.universe, "What is Matrix?"))

    print("\n2) Universe")
    print(query.ask(engine.universe, "Who possesses the book?"))

    print("\n3) Reasoner")
    engine.universe.derived.append(
        type(
            "Derived",
            (),
            {
                "subject": "John",
                "operator": "IS_A",
                "object": "Animal",
            },
        )()
    )
    print(query.ask(engine.universe, "Who is an animal?"))

    print("\n4) Local AI")
    print(query.ask(engine.universe, "Who wrote Hamlet?"))
