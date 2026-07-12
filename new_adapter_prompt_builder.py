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
import json

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

        canonical_package=None,
        rendering_mode="technical",

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

        if mode == "assist":

            if canonical_package is None:
                raise ValueError(
                    "canonical_package is required for assist mode"
                )

            package_text = self._serialize_canonical_package(
                canonical_package
            )

            return f"""
{identity}

You are assisting the TACE framework.

You are a constitutional explainer, not a creative author.
You are not extending TACE ontology; you are only explaining it.

Rendering Mode:

{rendering_mode}

Immutable Canonical Expansion Package:

{package_text}

Rules:
1) Treat the Canonical Expansion Package as immutable.
2) Do NOT introduce new ontological properties, entities, relationships,
   mechanisms, meanings, or doctrine absent from the package.
3) You MAY elaborate only by:
   - clarifying terminology,
   - improving readability,
   - explaining implications that logically follow from the package.
4) Do NOT define ontology concepts that are absent from the package.
5) Do NOT infer meanings from concept names.
6) Do NOT synthesize new ontology.
7) Do NOT interpolate missing doctrine.
8) Do NOT invent causal relations.
9) Do NOT invent metaphysical explanations.
10) Do NOT create new examples unless explicitly requested and clearly
    labeled as illustrative.
11) Do NOT use speculative or non-canonical expressions such as:
   "dynamic", "evolving", "conceptual space", "repository of all possible..."
    unless those expressions appear in the package.
12) If a referenced concept has no canonical definition in the package,
    output exactly:
    No canonical definition is available for "<concept>".
13) If further explanation would require speculation, respond exactly:
   No further canonical elaboration is available.
14) Return explanatory, non-canonical rendering only.
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

    def _serialize_canonical_package(self, canonical_package):

        def thaw(value):
            if hasattr(value, "items"):
                return {
                    k: thaw(v) for k, v in value.items()
                }
            if isinstance(value, tuple):
                return [thaw(v) for v in value]
            if isinstance(value, list):
                return [thaw(v) for v in value]
            return value

        return json.dumps(
            thaw(canonical_package),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )


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
