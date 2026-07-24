"""
u_face.py

TACE Tetrahedral Kernel

A Face represents an irreducible triadic constitutional subsystem.
"""

from dataclasses import dataclass
from typing import Tuple

from kernel.tetrahedron.u_primitive import Primitive
from kernel.tetrahedron.u_edge import Edge


@dataclass(frozen=True)
class Face:
    """
    Triangular constitutional subsystem.

    A Face is composed of exactly three primitives and the
    three constitutional edges that connect them.
    """

    name: str

    primitives: Tuple[Primitive, Primitive, Primitive]

    edges: Tuple[Edge, Edge, Edge]

    semantic_role: str

    description: str = ""

    def contains(self, primitive: Primitive) -> bool:
        return primitive in self.primitives

    def primitive_names(self):
        return tuple(p.name for p in self.primitives)

    def __repr__(self):

        names = ", ".join(self.primitive_names())

        return f"<Face {self.name}: [{names}]>"
