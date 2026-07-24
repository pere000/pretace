"""
u_canonical_validator.py

Canonical Validator

Determines whether a justified conclusion may
be incorporated into the Canonical Ontology.
"""

class CanonicalValidator:

    def __init__(self, constitution):

        self.constitution = constitution

    ##################################################

    def validate(self, justification):

        report = CanonicalValidationReport()

        report.semantic = self.semantic_validation(
            justification
        )

        report.ontological = self.ontological_validation(
            justification
        )

        report.constitutional = self.constitutional_validation(
            justification
        )

        report.coherence = self.coherence_validation(
            justification
        )

        report.evidence = self.evidence_validation(
            justification
        )

        report.decision = self.decision(report)

        return report

    ##################################################

    def semantic_validation(self, justification):
        ...

    def ontological_validation(self, justification):
        ...

    def constitutional_validation(self, justification):
        ...

    def coherence_validation(self, justification):
        ...

    def evidence_validation(self, justification):
        ...

    def decision(self, report):
        ...
