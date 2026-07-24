"""
u_constitutional_model_builder.py

Constitutional Model Builder

Builds the Constitutional Model from
Canonical Semantic Propositions.
"""

from kernel.constitutional.u_constitutional_model import (
    ConstitutionalModel
)


class ConstitutionalModelBuilder:

    def __init__(self, ontology):

        self.ontology = ontology

    def build(self, semantic_document):

        model = ConstitutionalModel()

        for proposition in semantic_document:

            self.integrate(
                model,
                proposition
            )

        return model

    ##################################################

    def integrate(
        self,
        model,
        proposition
    ):

        #
        # Resolve participants
        #

        subject = self.resolve_profile(
            proposition.subject
        )

        relation = self.resolve_relation(
            proposition.relation
        )

        object_ = self.resolve_profile(
            proposition.object
        )

        #
        # Insert into model
        #

        model.connect(
            subject,
            relation,
            object_
        )

    ##################################################

    def resolve_profile(self, semantic_object):

        return self.ontology.profile(
            semantic_object
        )

    def resolve_relation(self, relation):

        return self.ontology.relation(
            relation
        )
