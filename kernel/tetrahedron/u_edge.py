"""
u_edge.py

TACE Tetrahedral Kernel

Constitutional relation between two ontological primitives.
"""

from dataclasses import dataclass

from kernel.tetrahedron.u_primitive import Primitive


@dataclass(frozen=True)
class Edge:
    """
    Constitutional relation between two primitives.
    """

    source: Primitive
    target: Primitive

    relation: str

    reversible: bool = False

    constitutional: bool = True

    description: str = ""

    def is_bidirectional(self) -> bool:
        return self.reversible

    def __repr__(self):
        arrow = "<->" if self.reversible else "->"

        return (
            f"{self.source.name} "
            f"{arrow} "
            f"{self.target.name}"
            f" ({self.relation})"
        )
