"""
u_canonical_recognition_engine.py

Canonical Recognition Engine

Identifies semantic spans that correspond to
canonical ontology concepts.
"""

from typing import List

from kernel.semantic.u_semantic_span import SemanticSpan


class CanonicalRecognitionEngine:

    def __init__(self, ontology):

        self.ontology = ontology

    def recognize(self, spans: List[SemanticSpan]):

        """
        Returns recognized canonical spans.
        """

        recognized = []

        for span in spans:

            concept = self.lookup(span.text)

            if concept:

                span.canonical = True
                span.concept = concept

            recognized.append(span)

        return recognized

    def lookup(self, text):

        """
        Ontology lookup.

        Exact matching first.

        Synonyms later.

        AI fallback much later.
        """

        return self.ontology.find(text)
