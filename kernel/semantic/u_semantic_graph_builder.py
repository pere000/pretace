"""
u_semantic_graph_builder.py

Constructs a SemanticGraph from one or more
Canonical Semantic Propositions.
"""

from kernel.semantic.u_semantic_graph import SemanticGraph


class SemanticGraphBuilder:

    def __init__(self):

        pass

    def build(self, document):

        graph = SemanticGraph()

        for proposition in document:

            self._insert_proposition(
                graph,
                proposition
            )

        return graph

    #
    # Internal
    #

    def _insert_proposition(
        self,
        graph,
        proposition
    ):

        #
        # Shared nodes
        #

        subject = graph.get_or_create_node(
            proposition.subject
        )

        relation = graph.get_or_create_relation(
            proposition.relation
        )

        object_ = graph.get_or_create_node(
            proposition.object
        )

        graph.connect(
            subject,
            relation,
            object_
        )

        #
        # Nested propositions
        #

        if hasattr(proposition.object, "proposition"):

            self._insert_proposition(
                graph,
                proposition.object.proposition
            )
