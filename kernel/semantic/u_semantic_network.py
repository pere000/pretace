"""
u_semantic_network.py

Semantic Network

Maintains the semantic representation of a text
prior to ontology resolution.
"""

from collections import defaultdict

from kernel.semantic.u_semantic_node import SemanticNode
from kernel.semantic.u_semantic_edge import SemanticEdge


class SemanticNetwork:

    def __init__(self):

        #
        # Semantic identities
        #

        self.nodes = {}

        #
        # Semantic assertions
        #

        self.edges = []

        #
        # Fast lookup
        #

        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)

    #####################################################
    # Nodes
    #####################################################

    def add_node(self, node: SemanticNode):

        if node.id not in self.nodes:

            self.nodes[node.id] = node

        return self.nodes[node.id]

    #####################################################
    # Edges
    #####################################################

    def add_edge(self, edge: SemanticEdge):

        self.edges.append(edge)

        self.outgoing[edge.source.id].append(edge)

        self.incoming[edge.target.id].append(edge)

    #####################################################
    # Search
    #####################################################

    def node(self, node_id):

        return self.nodes.get(node_id)

    def neighbours(self, node):

        return [
            edge.target
            for edge in self.outgoing[node.id]
        ]

    #####################################################
    # Statistics
    #####################################################

    @property
    def node_count(self):

        return len(self.nodes)

    @property
    def edge_count(self):

        return len(self.edges)
