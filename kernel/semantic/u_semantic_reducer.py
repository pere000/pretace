"""
u_semantic_reducer.py

Semantic Reduction Engine

Transforms natural language into Canonical Semantic
Propositions (CSP).
"""

from kernel.semantic.u_canonical_semantic_object import (
    CanonicalSemanticObject
)

from kernel.semantic.u_canonical_semantic_relation import (
    CanonicalSemanticRelation
)

from kernel.semantic.u_canonical_semantic_proposition import (
    CanonicalSemanticProposition
)

from kernel.semantic.u_canonical_context import (
    CanonicalContext
)


class SemanticReducer:

    def __init__(self):

        pass

    def reduce(self, sentence):

        """
        Main entry point.
        """

        #
        # 1 Parse
        #

        parsed = self.parse(sentence)

        #
        # 2 Subject
        #

        subject = self.extract_subject(parsed)

        #
        # 3 Predicate
        #

        relation = self.extract_relation(parsed)

        #
        # 4 Object
        #

        obj = self.extract_object(parsed)

        #
        # 5 Context
        #

        context = self.extract_context(parsed)

        return CanonicalSemanticProposition(

            subject=subject,

            relation=relation,

            object=obj,

            context=context,

            source_text=sentence

        )

    #
    # Methods implemented later
    #

    def parse(self, sentence):
        ...

    def extract_subject(self, parsed):
        ...

    def extract_relation(self, parsed):
        ...

    def extract_object(self, parsed):
        ...

    def extract_context(self, parsed):
        ...
