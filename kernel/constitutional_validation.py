"""
ADR-010
Constitutional Validation

Validates a constitutional derivation tree against the
Constitutional Registry.

This component performs no ontology lookup,
no AI inference,
and no repository access.
"""

from kernel.derivation_node import DerivationNode
from kernel.constitutional_registry import REGISTRY
from kernel.validation_result import ValidationResult


class ConstitutionalValidation:
    """
    Validates constitutional derivation trees.
    """

    def validate(self, tree: DerivationNode) -> ValidationResult:

        violations: list[str] = []

        self._validate(tree, violations)

        return ValidationResult(
            valid=len(violations) == 0,
            violations=tuple(violations),
        )

    # -------------------------------------------------------------

    def _validate(
        self,
        node: DerivationNode,
        violations: list[str],
    ) -> None:

        #
        # Rule 1
        # Primitive concepts cannot have children.
        #

        if node.primitive:

            if node.children:
                violations.append(
                    f"{node.concept}: primitive concept has children."
                )

            return

        #
        # Rule 2
        # Registry consistency.
        #

        expected = REGISTRY.dependencies(node.concept)

        actual = tuple(
            child.concept
            for child in node.children
        )

        if expected != actual:

            violations.append(
                f"{node.concept}: constitutional dependencies do not match registry."
            )

        #
        # Rule 3
        # Resolved nodes require resolved descendants.
        #

        if node.resolved:

            unresolved = [
                child.concept
                for child in node.children
                if not child.resolved
            ]

            if unresolved:

                violations.append(
                    f"{node.concept}: resolved node contains unresolved descendants ({', '.join(unresolved)})."
                )

        #
        # Rule 4
        # Recursive validation.
        #

        for child in node.children:

            self._validate(
                child,
                violations,
            )
