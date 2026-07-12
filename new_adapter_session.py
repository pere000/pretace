#!/usr/bin/env python3

"""
TACE Session

Build Prompt
      ↓
Local AI
      ↓
Answer
"""

from new_adapter_prompt_builder import PromptBuilder
from new_adapter_ollama_client import OllamaClient


class TACESession:

    def __init__(self):

        self.builder = PromptBuilder()

        self.ai = OllamaClient()

    def ask(

        self,

        universe,

        question,

        mode="tace",

        canonical_package=None,
        rendering_mode="technical",

    ):

        prompt = self.builder.build(

            universe,

            question,

            mode,

            canonical_package=canonical_package,
            rendering_mode=rendering_mode,

        )

        return self.ai.ask(prompt)


if __name__ == "__main__":

    from new_pipeline_engine import TACEEngine

    engine = TACEEngine()

    engine.learn(
        "John possesses the book."
    )

    universe = engine.universe

    session = TACESession()

    print("===== TACE =====\n")

    print(

        session.ask(

            universe,

            "Who possesses the book?",

            mode="tace",

        )

    )

    print("\n===== FALLBACK =====\n")

    print(

        session.ask(

            universe,

            "Who wrote Hamlet?",

            mode="fallback",

        )

    )
