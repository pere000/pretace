"""
ADR-009
Primitive Derivation Engine

Constructs the constitutional derivation tree of a canonical concept.

This component is deterministic.
It performs no AI inference, no database access,
and never modifies the ontology.
"""

from kernel.concept_record import ConceptRecord
from kernel.derivation_node import DerivationNode
from kernel.constitutional_registry import REGISTRY


class PrimitiveDerivation:
    """
    Primitive Derivation Engine.

    Input:
        ConceptRecord

    Output:
        DerivationNode

    The returned tree represents the constitutional
    derivation of the concept.

    Validation of the tree is performed later by the
    Constitutional Validator.
    """

    def derive(self, concept: ConceptRecord) -> DerivationNode:
        """
        Entry point.
        """

        return self._derive(concept.concept_name)

    # -------------------------------------------------------------

    def _derive(self, concept_name: str) -> DerivationNode:
        """
        Recursive constitutional derivation.

        Current version:
            • Primitive concepts become leaves.
            • Non-primitive concepts become unresolved nodes.

        Future versions will recursively derive
        constitutional dependencies from ontology relations.
        """

        if REGISTRY.is_primitive_concept(concept_name):
            return DerivationNode(
                concept=concept_name,
                primitive=True,
                resolved=True,
                children=(),
            )

        return DerivationNode(
            concept=concept_name,
            primitive=False,
            resolved=False,
            children=(),
        )
