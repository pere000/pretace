from kernel.query_classifier import QueryClassifier
from kernel.authority_gate import AuthorityGate
from kernel.concept_resolver import ConceptResolver


class Kernel:
    """
    Public entry point for the TACE kernel.
    """

    def __init__(self):
        self.classifier = QueryClassifier()
        self.authority_gate = AuthorityGate()
        self.concept_resolver = ConceptResolver()

    def resolve(self, concept_name: str):
        classification = self.classifier.classify(
            f"What is {concept_name}?"
        )

        authority = self.authority_gate.resolve(classification)

        return self.concept_resolver.resolve(
            authority,
            concept_name,
        )
