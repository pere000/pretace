"""
ADR-011
Constitutional Explanation

Produces a canonical textual explanation of a validated
constitutional derivation tree.

This component performs no ontology lookup,
no AI inference,
and no repository access.
"""

from kernel.derivation_node import DerivationNode


class ConstitutionalExplanation:
    """
    Produces canonical explanations of constitutional
    derivation trees.
    """

    def explain(self, tree: DerivationNode) -> str:

        lines: list[str] = []

        self._render(tree, lines, level=0)

        return "\n".join(lines)

    # -------------------------------------------------------------

    def _render(
        self,
        node: DerivationNode,
        lines: list[str],
        level: int,
    ) -> None:

        indent = "    " * level

        if node.primitive:
            state = "primitive"
        elif node.resolved:
            state = "resolved"
        else:
            state = "unresolved"

        lines.append(
            f"{indent}- {node.concept} [{state}]"
        )

        for child in node.children:
            self._render(
                child,
                lines,
                level + 1,
            )
