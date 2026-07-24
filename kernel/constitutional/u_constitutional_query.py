"""
u_constitutional_query.py

Constitutional Query Service

Provides read-only navigation and inspection of the Constitutional Model.
This class performs no inference and no validation.
"""

from collections import deque


class ConstitutionalQuery:
    """
    Read-only query interface over a ConstitutionalModel.
    """

    def __init__(self, model):
        self._model = model

    # ---------------------------------------------------------
    # Entity existence
    # ---------------------------------------------------------

    def contains(self, concept: str) -> bool:
        """
        Returns True if the concept exists in the model.
        """
        return concept in self._model.entities

    # ---------------------------------------------------------
    # Primitive ancestry
    # ---------------------------------------------------------

    def primitives(self, concept: str) -> list[str]:
        """
        Returns the primitive ancestry of a concept.

        Example:
            Human -> [Substance, LivingBeing, Animal]
        """

        result = []
        current = self._model.entities.get(concept)

        while current is not None:

            primitive = getattr(current, "primitive", None)

            if primitive is None:
                break

            result.append(primitive)

            current = self._model.entities.get(primitive)

        return result

    # ---------------------------------------------------------
    # Shortest constitutional path
    # ---------------------------------------------------------

    def path(self, source: str, target: str) -> list[str]:
        """
        Returns the shortest constitutional path
        between two concepts.
        """

        if source == target:
            return [source]

        visited = set()
        queue = deque([(source, [source])])

        while queue:

            node, history = queue.popleft()

            if node in visited:
                continue

            visited.add(node)

            neighbours = self._model.neighbours(node)

            for neighbour in neighbours:

                if neighbour == target:
                    return history + [neighbour]

                queue.append(
                    (neighbour, history + [neighbour])
                )

        return []

    # ---------------------------------------------------------
    # Common primitive ancestry
    # ---------------------------------------------------------

    def common_primitives(
        self,
        left: str,
        right: str,
    ) -> list[str]:
        """
        Returns primitives shared by both concepts.
        """

        a = set(self.primitives(left))
        b = set(self.primitives(right))

        return sorted(a.intersection(b))

    # ---------------------------------------------------------
    # Neighbours
    # ---------------------------------------------------------

    def neighbours(self, concept: str) -> list[str]:
        """
        Returns adjacent constitutional entities.
        """

        return self._model.neighbours(concept)

    # ---------------------------------------------------------
    # Relations
    # ---------------------------------------------------------

    def relations(self, concept: str):
        """
        Returns all constitutional relations
        involving the concept.
        """

        return self._model.relations(concept)

    # ---------------------------------------------------------
    # Entity
    # ---------------------------------------------------------

    def entity(self, concept: str):
        """
        Returns the constitutional entity itself.
        """

        return self._model.entities.get(concept)
