"""
u_mapper.py

Constitutional Mapper

Maps canonical propositions onto the TACE tetrahedral ontology.
"""

from dataclasses import dataclass

from kernel.canonical.u_proposition import Proposition


@dataclass
class MappingResult:

    proposition: Proposition

    primitives: tuple

    edges: tuple

    faces: tuple

    valid: bool = True

    notes: str = ""


class Mapper:

    def __init__(self, tetrahedron):

        self.tetrahedron = tetrahedron

    def map(self, proposition: Proposition):

        primitives = self._map_primitives(proposition)

        edges = self._map_edges(primitives)

        faces = self._map_faces(primitives)

        return MappingResult(
            proposition=proposition,
            primitives=primitives,
            edges=edges,
            faces=faces
        )

    #
    # Primitive Mapping
    #

    def _map_primitives(self, proposition):

        result = []

        for name in proposition.primitives():

            primitive = self.tetrahedron.primitive(name)

            if primitive:

                result.append(primitive)

        return tuple(result)

    #
    # Edge Mapping
    #

    def _map_edges(self, primitives):

        result = []

        names = {p.name for p in primitives}

        for edge in self.tetrahedron.edges:

            if (
                edge.source.name in names
                and
                edge.target.name in names
            ):

                result.append(edge)

        return tuple(result)

    #
    # Face Mapping
    #

    def _map_faces(self, primitives):

        result = []

        names = {p.name for p in primitives}

        for face in self.tetrahedron.faces:

            face_names = {
                p.name
                for p in face.primitives
            }

            if face_names.issubset(names):

                result.append(face)

        return tuple(result)
