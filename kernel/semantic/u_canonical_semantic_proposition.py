"""
u_canonical_semantic_proposition.py

Canonical Semantic Proposition (CSP)

Represents one semantically faithful proposition
produced by the Semantic Reduction Engine.
"""

from dataclasses import dataclass, field
from typing import Optional

from kernel.semantic.u_canonical_semantic_object import (
    CanonicalSemanticObject
)

from kernel.semantic.u_canonical_semantic_relation import (
    CanonicalSemanticRelation
)

from kernel.semantic.u_canonical_context import (
    CanonicalContext
)


@dataclass
class CanonicalSemanticProposition:

    #
    # Subject
    #

    subject: CanonicalSemanticObject

    #
    # Predicate
    #

    relation: CanonicalSemanticRelation

    #
    # Object
    #

    object: CanonicalSemanticObject

    #
    # Context
    #

    context: Optional[CanonicalContext] = None

    #
    # Original sentence
    #

    source_text: str = ""

    #
    # Confidence
    #

    confidence: float = 1.0

    def canonical_form(self):

        return (
            f"{self.subject} "
            f"{self.relation} "
            f"{self.object}"
        )

    def __str__(self):

        return self.canonical_form()
