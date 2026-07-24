"""
u_state.py

Runtime Constitutional State

Represents one instantaneous constitutional
state of the TACE kernel.
"""

from dataclasses import dataclass, field
from typing import Set, List

from kernel.tetrahedron.u_primitive import Primitive
from kernel.tetrahedron.u_edge import Edge
from kernel.tetrahedron.u_face import Face


@dataclass
class ConstitutionalState:

    active_primitives: Set[Primitive] = field(default_factory=set)

    active_edges: Set[Edge] = field(default_factory=set)

    active_faces: Set[Face] = field(default_factory=set)

    history: List[str] = field(default_factory=list)

    def activate_primitive(self, primitive):

        self.active_primitives.add(primitive)

    def activate_edge(self, edge):

        self.active_edges.add(edge)

    def activate_face(self, face):

        self.active_faces.add(face)

    def record(self, event):

        self.history.append(event)

    def clear(self):

        self.active_primitives.clear()
        self.active_edges.clear()
        self.active_faces.clear()
        self.history.clear()

    def snapshot(self):

        return {

            "primitives":
                sorted(p.name for p in self.active_primitives),

            "edges":
                len(self.active_edges),

            "faces":
                len(self.active_faces),

            "history":
                list(self.history)

        }
