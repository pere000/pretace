"""
ADR-009
Primitive Derivation Engine

Constructs the constitutional derivation tree of a canonical concept.

This component is deterministic.
It performs no AI inference, no database access,
and never modifies the ontology.
"""

from kernel.derivation_node import DerivationNode
from kernel.constitutional_registry import REGISTRY


class PrimitiveDerivation:
    """
    Primitive Derivation Engine.

    The returned tree represents the constitutional
    derivation of the concept.

    Validation of the tree is performed later by the
    Constitutional Validator.
    """

    def derive(self, concept_name: str) -> DerivationNode:
        """
        Entry point.
        """
        return self._derive(concept_name)

    def _derive(self, concept_name: str) -> DerivationNode:
        """
        Recursive constitutional derivation.
        """

        if REGISTRY.is_primitive_concept(concept_name):
            return DerivationNode(
                concept=concept_name,
                primitive=True,
                resolved=True,
                children=(),
            )

        dependencies = REGISTRY.dependencies(concept_name)

        if not dependencies:
            return DerivationNode(
                concept=concept_name,
                primitive=False,
                resolved=False,
                children=(),
            )

        children = tuple(
            self._derive(dep)
            for dep in dependencies
        )

        resolved = all(child.resolved for child in children)

        return DerivationNode(
            concept=concept_name,
            primitive=False,
            resolved=resolved,
            children=children,
        )
