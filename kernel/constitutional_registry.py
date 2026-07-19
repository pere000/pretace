"""
ADR-009
Constitutional Registry

The Constitutional Registry defines the immutable constitutional
elements from which every canonical TACE concept must ultimately derive.

This module is the constitutional foundation of the reasoning engine.
It contains no AI, no repository access, and no inference.
"""

from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class ConstitutionalRegistry:
    """
    Immutable constitutional foundation of TACE.
    """

    primitive_concepts: FrozenSet[str]
    primitive_relations: FrozenSet[str]
    primitive_axioms: FrozenSet[str]

    def is_primitive_concept(self, name: str) -> bool:
        return name in self.primitive_concepts

    def is_primitive_relation(self, name: str) -> bool:
        return name in self.primitive_relations

    def is_primitive_axiom(self, name: str) -> bool:
        return name in self.primitive_axioms


REGISTRY = ConstitutionalRegistry(

    primitive_concepts=frozenset({

        "God",
        "Matrix",
        "Q-Form",
        "Form",
        "Substance",
        "Silver Bridge",
        "Consciousness",
        "Actualization",
        "Potentiality",
        "Truth",
        "Goodness",

    }),

    primitive_relations=frozenset({

        "actualizes",
        "participates_in",
        "instantiates",
        "mediates",
        "depends_on",
        "grounds",

    }),

    primitive_axioms=frozenset({

        "A-001",
        "A-002",
        "A-003",

    }),

)
