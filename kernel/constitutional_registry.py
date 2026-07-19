"""
ADR-009

Constitutional Registry

The Constitutional Registry defines the immutable constitutional
elements from which every canonical TACE concept must ultimately derive.

This module contains no AI, no repository access, and no inference.
It is the immutable constitutional foundation of the reasoning engine.
"""

from dataclasses import dataclass
from typing import FrozenSet, Mapping, Tuple


@dataclass(frozen=True)
class ConstitutionalRegistry:
    """
    Immutable constitutional foundation of TACE.
    """

    primitive_concepts: FrozenSet[str]
    primitive_relations: FrozenSet[str]
    primitive_axioms: FrozenSet[str]

    constitutional_dependencies: Mapping[str, Tuple[str, ...]]

    def is_primitive_concept(self, name: str) -> bool:
        return name in self.primitive_concepts

    def is_primitive_relation(self, name: str) -> bool:
        return name in self.primitive_relations

    def is_primitive_axiom(self, name: str) -> bool:
        return name in self.primitive_axioms

    def dependencies(self, concept: str) -> Tuple[str, ...]:
        return self.constitutional_dependencies.get(concept, ())


REGISTRY = ConstitutionalRegistry(

    primitive_concepts=frozenset({

        "God",

        "Being",
        "Intelligence",
        "Operativity",
        "Selectivity",
        "Freedom",
        "Consciousness",

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

    constitutional_dependencies={

        #
        # Primitive concepts
        #

        "God": (),

        "Being": (),
        "Intelligence": (),
        "Operativity": (),
        "Selectivity": (),
        "Freedom": (),
        "Consciousness": (),

        #
        # Canonical concepts
        #

        "Matrix": (
            "Being",
            "Intelligence",
            "Operativity",
            "Selectivity",
        ),

        "Q-Form": (
            "Matrix",
        ),

        "Form": (
            "Matrix",
        ),

        "Substance": (
            "Form",
            "Q-Form",
        ),

        "Silver Bridge": (
            "Matrix",
            "Consciousness",
        ),

        "Potentiality": (
            "Matrix",
        ),

        "Actualization": (
            "Potentiality",
            "Operativity",
        ),

        "Truth": (
            "Being",
            "Intelligence",
        ),

        "Goodness": (
            "Being",
            "Freedom",
        ),

    },

)
