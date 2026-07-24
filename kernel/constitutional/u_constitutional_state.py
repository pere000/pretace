"""
u_constitutional_state.py

Constitutional State

Represents the constitutional state of the current
reasoning session.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from kernel.constitutional.u_constitutional_profile import (
    ConstitutionalProfile
)


@dataclass
class ConstitutionalState:

    #
    # Active constitutional profiles
    #

    profiles: Dict[
        str,
        ConstitutionalProfile
    ] = field(default_factory=dict)

    #
    # Active laws
    #

    active_laws: List[str] = field(default_factory=list)

    #
    # Active constraints
    #

    active_constraints: List[str] = field(default_factory=list)

    #
    # Current propositions
    #

    propositions: List = field(default_factory=list)

    #
    # Current judgements
    #

    judgements: List = field(default_factory=list)

    #
    # Runtime metadata
    #

    metadata: Dict = field(default_factory=dict)

    ####################################################

    def add_profile(self, profile):

        self.profiles[
            profile.concept_id
        ] = profile

    def profile(self, concept_id):

        return self.profiles.get(concept_id)
