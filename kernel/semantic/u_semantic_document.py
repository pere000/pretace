"""
u_semantic_document.py

Semantic Document

Represents the complete semantic interpretation
of one input text.
"""

from dataclasses import dataclass, field
from typing import List

from kernel.semantic.u_canonical_semantic_proposition import (
    CanonicalSemanticProposition
)


@dataclass
class SemanticDocument:

    #
    # Original text
    #

    source_text: str

    #
    # Canonical propositions
    #

    propositions: List[
        CanonicalSemanticProposition
    ] = field(default_factory=list)

    #
    # Global confidence
    #

    confidence: float = 1.0

    #
    # Utilities
    #

    def add(self, proposition):

        self.propositions.append(proposition)

    def __len__(self):

        return len(self.propositions)

    def __iter__(self):

        return iter(self.propositions)

    def summary(self):

        return {

            "text": self.source_text,

            "propositions": len(self.propositions),

            "confidence": self.confidence

        }
