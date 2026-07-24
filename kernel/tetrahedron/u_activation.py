"""
u_activation.py

TACE Tetrahedral Kernel

Constitutional activation engine.
"""

from dataclasses import dataclass
from typing import Set

from kernel.tetrahedron.u_primitive import Primitive
from kernel.tetrahedron.u_tetrahedron import Tetrahedron


@dataclass
class Activation:

    tetrahedron: Tetrahedron

    active: Set[Primitive]

    def __init__(self, tetrahedron):

        self.tetrahedron = tetrahedron
        self.active = set()

    def activate(self, primitive):

        self.active.add(primitive)

    def deactivate(self, primitive):

        self.active.discard(primitive)

    def clear(self):

        self.active.clear()

    def is_active(self, primitive):

        return primitive in self.active

    def active_names(self):

        return sorted(
            p.name
            for p in self.active
        )

    def __repr__(self):

        return (
            f"<Activation "
            f"{self.active_names()}>"
        )
