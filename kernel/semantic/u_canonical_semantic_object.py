"""
u_canonical_semantic_object.py

Canonical Semantic Object (CSO)

The atomic semantic representation produced by
Semantic Reduction before ontology resolution.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CanonicalSemanticObject:

    #
    # Source
    #

    source_text: str

    #
    # Canonical head
    #

    head: str

    #
    # Essential qualifiers
    #

    qualifiers: List[str] = field(default_factory=list)

    #
    # Compound concept
    #

    compound: Optional[str] = None

    #
    # Ontological category
    #

    category: Optional[str] = None

    #
    # Canonical ontology identifier
    #

    concept_id: Optional[str] = None

    #
    # Confidence
    #

    confidence: float = 1.0

    #
    # Utilities
    #

    @property
    def canonical_name(self):

        if self.compound:

            return self.compound

        if self.qualifiers:

            return " ".join(
                self.qualifiers + [self.head]
            )

        return self.head

    def __str__(self):

        return self.canonical_name
