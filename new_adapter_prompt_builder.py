#!/usr/bin/env python3

"""
TACE Prompt Builder

Builds prompts for the Local AI.

Modes

TACE
    The answer must come only from the
    TACE Universe.

FALLBACK
    TACE could not answer, therefore the
    Local AI may use its own knowledge.
"""
from new_adapter_universe_formatter import UniverseFormatter
from new_ontology_identity import OntologyIdentity


class PromptBuilder:

    def __init__(self):

        self.formatter = UniverseFormatter()

        self.identity = OntologyIdentity()

    def build(

        self,

        universe,

        question,

        mode="tace",

    ):

        identity = self.identity.text()

        universe_text = self.formatter.format(
            universe
        )

        if mode == "fallback":

            return f"""
{identity}

You are assisting the TACE framework.

The TACE ontology, universe and reasoner
could not answer the following question.

You may use your own knowledge.

If you answer using your own knowledge,
make it clear that this information
comes from the Local AI and has NOT
yet become TACE knowledge.

Current TACE Universe:

{universe_text}

Question:

{question}
"""

        return f"""
{identity}



Current TACE Universe:

{universe_text}

Question:

{question}

Answer ONLY using the TACE Universe.

If the answer is not contained inside
the TACE Universe, reply exactly:

UNKNOWN
"""


if __name__ == "__main__":

    from pipeline.engine import TACEEngine

    engine = TACEEngine()

    universe = engine.learn(
        "John possesses the book."
    )

    builder = PromptBuilder()

    print("===== TACE =====\n")

    print(

        builder.build(

            universe,

            "Who possesses the book?",

            "tace",

        )

    )

    print("\n===== FALLBACK =====\n")

    print(

        builder.build(

            universe,

            "Who wrote Hamlet?",

            "fallback",

        )

    )
