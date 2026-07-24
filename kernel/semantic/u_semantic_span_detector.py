"""
u_semantic_span_detector.py

Detects semantic spans that must remain indivisible
during semantic reduction.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SemanticSpan:

    start: int
    end: int

    text: str

    span_type: str

    confidence: float = 1.0


class SemanticSpanDetector:

    def detect(self, text: str) -> List[SemanticSpan]:

        """
        Returns semantic spans.

        This initial version delegates the actual
        extraction to pluggable detectors.
        """

        spans = []

        spans.extend(
            self.detect_compounds(text)
        )

        spans.extend(
            self.detect_named_entities(text)
        )

        spans.extend(
            self.detect_ontology_terms(text)
        )

        return self.merge(spans)

    def detect_compounds(self, text):
        ...

    def detect_named_entities(self, text):
        ...

    def detect_ontology_terms(self, text):
        ...

    def merge(self, spans):
        ...
