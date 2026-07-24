"""
u_constitutional_executor.py

Constitutional Executor

Executes constitutional reasoning until
the model reaches constitutional equilibrium.
"""

from kernel.constitutional.u_actualization import (
    Actualization
)


class ConstitutionalExecutor:

    def __init__(self, constitution):

        self.constitution = constitution

    ###################################################

    def execute(self, model):

        """
        Constitutional execution loop.
        """

        changed = True

        while changed:

            changed = False

            actualizations = self.find_actualizations(
                model
            )

            for actualization in actualizations:

                if self.apply(
                    model,
                    actualization
                ):

                    changed = True

        return model

    ###################################################

    def find_actualizations(self, model):

        return self.constitution.actualizations(
            model
        )

    ###################################################

    def apply(
        self,
        model,
        actualization
    ):

        return actualization.execute(model)
