"""
u_semantic_classifier.py

Semantic Classifier

Assigns semantic categories to detected concepts
before ontology resolution.
"""

from enum import Enum


class SemanticCategory(Enum):

    UNKNOWN = "unknown"

    ENTITY = "entity"

    PERSON = "person"

    PLACE = "place"

    EVENT = "event"

    ACTION = "action"

    QUALITY = "quality"

    FACULTY = "faculty"

    RELATION = "relation"

    SUBSTANCE = "substance"

    CONCEPT = "concept"

    PRIMITIVE = "primitive"

    AUTHORITY = "authority"

    SOURCE = "source"

    CITATION = "citation"

    TEMPORAL = "temporal"


class SemanticClassifier:

    def classify(self, span):

        """
        Returns the semantic category
        of a detected span.
        """

        #
        # Initially simple rules.
        #
        # Later:
        #
        # ontology
        # dictionaries
        # AI
        #

        return SemanticCategory.UNKNOWN
