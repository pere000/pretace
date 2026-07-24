"""
u_constitutional_transition_validator.py

Constitutional Transition Validator

Determines whether a proposed constitutional
transition is admissible according to the
constitutional ontology.
"""

from dataclasses import dataclass


@dataclass
class ValidationResult:

    valid: bool

    violated_laws: list

    violated_constraints: list

    warnings: list

    explanation: str = ""


class ConstitutionalTransitionValidator:

    def __init__(self, constitution):

        self.constitution = constitution

    ####################################################

    def validate(
        self,
        model,
        transition
    ):

        violated_laws = []

        violated_constraints = []

        warnings = []

        #
        # Evaluate laws
        #

        for law in transition.required_laws:

            if not law.satisfied(model):

                violated_laws.append(law)

        #
        # Evaluate constraints
        #

        for constraint in transition.constraints:

            if not constraint.satisfied(model):

                violated_constraints.append(
                    constraint
                )

        valid = (
            len(violated_laws) == 0
            and
            len(violated_constraints) == 0
        )

        return ValidationResult(

            valid=valid,

            violated_laws=violated_laws,

            violated_constraints=violated_constraints,

            warnings=warnings
        )
