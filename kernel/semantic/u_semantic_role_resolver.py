"""
u_semantic_role_resolver.py

Semantic Role Resolver

Assigns semantic roles to the participants
of a Canonical Semantic Proposition.
"""

from enum import Enum


class SemanticRole(Enum):

    UNKNOWN = "unknown"

    #
    # Core roles
    #

    AGENT = "agent"

    PATIENT = "patient"

    THEME = "theme"

    EXPERIENCER = "experiencer"

    STIMULUS = "stimulus"

    RECIPIENT = "recipient"

    BENEFICIARY = "beneficiary"

    INSTRUMENT = "instrument"

    SOURCE = "source"

    GOAL = "goal"

    LOCATION = "location"

    TIME = "time"

    MANNER = "manner"

    ATTRIBUTE = "attribute"

    POSSESSOR = "possessor"

    POSSESSION = "possession"


class SemanticRoleResolver:

    def resolve(self, proposition):

        """
        Annotate a proposition with
        semantic roles.
        """

        #
        # Placeholder.
        # Later:
        #
        # relation rules
        # ontology rules
        # AI fallback
        #

        return proposition
