"""
u_inference.py

TACE Tetrahedral Kernel

Constitutional inference engine.
"""

from kernel.tetrahedron.u_propagation import Propagation


class Inference:

    def __init__(self, tetrahedron):

        self.tetrahedron = tetrahedron
        self.propagation = Propagation(tetrahedron)

    def activate(self, primitive):

        self.propagation.activate(primitive)

    def active_primitives(self):

        return self.propagation.active()

    def active_faces(self):
        """
        Return the faces whose three primitives
        are all active.
        """

        active = set(self.propagation.active())

        result = []

        for face in self.tetrahedron.faces:

            names = {p.name for p in face.primitives}

            if names.issubset(active):
                result.append(face)

        return result

    def complete(self):
        """
        True if all primitives are active.
        """

        return len(self.propagation.active()) == 4

    def report(self):

        return {

            "active_primitives":
                self.propagation.active(),

            "active_faces":
                [f.name for f in self.active_faces()],

            "complete":
                self.complete()

        }
