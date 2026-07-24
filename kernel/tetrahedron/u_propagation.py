"""
u_propagation.py

TACE Tetrahedral Kernel

Constitutional propagation engine.
"""

from kernel.tetrahedron.u_activation import Activation


class Propagation:

    def __init__(self, tetrahedron):

        self.tetrahedron = tetrahedron

        self.activation = Activation(tetrahedron)

    def activate(self, primitive):

        """
        Activate a primitive and propagate
        according to constitutional rules.
        """

        if self.activation.is_active(primitive):
            return

        self.activation.activate(primitive)

        self._propagate(primitive)

    def _propagate(self, primitive):

        name = primitive.name

        #
        # Constitutional Rules
        #

        if name == "Matrix":

            qform = self.tetrahedron.primitive("Q-Form")

            if qform:
                self.activate(qform)

        elif name == "Silver Bridge":

            consciousness = self.tetrahedron.primitive(
                "Consciousness"
            )

            if consciousness:
                self.activate(consciousness)

        elif name == "Consciousness":

            bridge = self.tetrahedron.primitive(
                "Silver Bridge"
            )

            if bridge:
                self.activate(bridge)

    def active(self):

        return self.activation.active_names()

    def clear(self):

        self.activation.clear()
