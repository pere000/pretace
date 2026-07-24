"""
u_constitutional_dynamics.py

Constitutional Dynamics

Applies lawful transformations to a
Constitutional Model.
"""

from kernel.constitutional.u_constitutional_model import (
    ConstitutionalModel
)


class ConstitutionalDynamics:

    def __init__(self, constitution):

        self.constitution = constitution

    ##################################################

    def apply(self, model, event):

        """
        Applies one constitutional event.
        """

        applicable = self.constitution.find_laws(
            model,
            event
        )

        for law in applicable:

            law.execute(
                model,
                event
            )

        return model
