"""
u_tetrahedron.py

TACE Tetrahedral Kernel

Defines the constitutional tetrahedral structure.
"""

from dataclasses import dataclass
from typing import Tuple

from kernel.tetrahedron.u_primitive import Primitive
from kernel.tetrahedron.u_edge import Edge
from kernel.tetrahedron.u_face import Face


@dataclass
class Tetrahedron:
    """
    Constitutional tetrahedral structure.

    A valid tetrahedron contains:

        4 primitives
        6 edges
        4 faces
    """

    primitives: Tuple[Primitive, Primitive, Primitive, Primitive]

    edges: Tuple[
        Edge, Edge, Edge,
        Edge, Edge, Edge
    ]

    faces: Tuple[
        Face, Face, Face, Face
    ]

    def __post_init__(self):

        self.validate()

    def validate(self):

        if len(self.primitives) != 4:
            raise ValueError(
                "A tetrahedron must contain exactly four primitives."
            )

        if len(self.edges) != 6:
            raise ValueError(
                "A tetrahedron must contain exactly six edges."
            )

        if len(self.faces) != 4:
            raise ValueError(
                "A tetrahedron must contain exactly four faces."
            )

        # Every face must contain exactly three primitives

        for face in self.faces:

            if len(face.primitives) != 3:
                raise ValueError(
                    f"Face '{face.name}' must contain three primitives."
                )

        # Primitive names must be unique

        names = [p.name for p in self.primitives]

        if len(names) != len(set(names)):
            raise ValueError(
                "Primitive names must be unique."
            )

    def primitive(self, name):

        for p in self.primitives:

            if p.name == name:
                return p

        return None

    def summary(self):

        return {

            "primitives":
                [p.name for p in self.primitives],

            "edges":
                len(self.edges),

            "faces":
                len(self.faces)

        }

    def __repr__(self):

        return (
            f"<Tetrahedron "
            f"Primitives={len(self.primitives)} "
            f"Edges={len(self.edges)} "
            f"Faces={len(self.faces)}>"
        )
