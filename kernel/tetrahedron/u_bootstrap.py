"""
u_bootstrap.py

Builds the initial TACE constitutional kernel.
"""

from kernel.ontology.u_primitive import Primitive
from kernel.ontology.u_edge import Edge
from kernel.ontology.u_face import Face
from kernel.ontology.u_tetrahedron import Tetrahedron

from kernel.constitution.u_constitution import Constitution

from kernel.execution.u_engine import Engine


class Bootstrap:

    @staticmethod
    def build():

        #
        # Primitives
        #

        matrix = Primitive(
            name="Matrix",
            definition="Universal Principle of Ontological Possibility",
            semantic_role="Possibility",
            universal_function="Universal Transformer"
        )

        qform = Primitive(
            name="Q-Form",
            definition="Universal Principle of Ontological Selectivity",
            semantic_role="Selectivity",
            universal_function="Universal Filter"
        )

        bridge = Primitive(
            name="Silver Bridge",
            definition="Universal Principle of Ontological Correspondence",
            semantic_role="Correspondence",
            universal_function="Universal Transducer"
        )

        consciousness = Primitive(
            name="Consciousness",
            definition="Universal Principle of Intentional Actualization",
            semantic_role="Intentional Actualization",
            universal_function="Universal Creativity"
        )

        #
        # Edges
        #

        edges = (
            ...
        )

        #
        # Faces
        #

        faces = (
            ...
        )

        tetrahedron = Tetrahedron(

            primitives=(
                matrix,
                qform,
                bridge,
                consciousness
            ),

            edges=edges,

            faces=faces

        )

        constitution = Constitution()

        #
        # Register laws here
        #

        # constitution.register(MatrixDeterminesQForm())

        return Engine(

            tetrahedron,

            constitution

        )
