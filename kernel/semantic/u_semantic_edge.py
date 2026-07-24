"""
u_semantic_edge.py

Semantic Edge

Represents a semantic relation between two
Semantic Nodes.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from kernel.semantic.u_semantic_relation import SemanticRelation
from kernel.semantic.u_semantic_node import SemanticNode


@dataclass
class SemanticEdge:

    #
    # Identity
    #

    id: str

    #
    # Graph
    #

    source: SemanticNode

    target: SemanticNode

    relation: SemanticRelation

    #
    # Source provenance
    #

    source_text: str = ""

    sentence_index: int = 0

    #
    # Confidence
    #

    confidence: float = 1.0

    #
    # Metadata
    #

    metadata: Dict = field(default_factory=dict)

    def __str__(self):

        return (
            f"{self.source}"
            f" --{self.relation}--> "
            f"{self.target}"
        )
