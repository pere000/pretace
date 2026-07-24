"""
u_canonical_semantic_relation.py

Canonical Semantic Relation (CSR)

Represents the semantic relation extracted from
natural language before ontology resolution.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CanonicalSemanticRelation:

    #
    # Original text
    #

    source_text: str

    #
    # Canonical verb
    #

    head: str

    #
    # Canonical ontology relation
    #

    canonical_relation: Optional[str] = None

    #
    # Relation family
    #

    family: Optional[str] = None

    #
    # Voice
    #

    voice: str = "active"

    #
    # Polarity
    #

    polarity: str = "affirmative"

    #
    # Modality
    #

    modality: str = "assertive"

    #
    # Tense
    #

    tense: Optional[str] = None

    #
    # Confidence
    #

    confidence: float = 1.0

    def __str__(self):

        return self.head
