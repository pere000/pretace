"""
u_validator.py

TACE Tetrahedral Kernel

Constitutional validator.
"""

from kernel.tetrahedron.u_tetrahedron import Tetrahedron


class Validator:

    def __init__(self, tetrahedron: Tetrahedron):

        self.tetrahedron = tetrahedron

    #
    # Structure
    #

    def validate_structure(self):

        self.tetrahedron.validate()

        return True

    #
    # Primitive
    #

    def validate_primitive(self, primitive):

        return primitive in self.tetrahedron.primitives

    #
    # Edge
    #

    def validate_edge(self, edge):

        return edge in self.tetrahedron.edges

    #
    # Face
    #

    def validate_face(self, face):

        return face in self.tetrahedron.faces

    #
    # Constitutional state
    #

    def validate_activation(self, activation):

        for primitive in activation.active:

            if not self.validate_primitive(primitive):

                return False

        return True

    #
    # Global
    #

    def validate(self, activation=None):

        self.validate_structure()

        if activation:

            return self.validate_activation(activation)

        return True
