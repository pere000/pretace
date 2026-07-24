"""
u_proposition.py

Canonical proposition for the TACE kernel.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Proposition:
    """
    Canonical representation of knowledge.
    """

    subject: str
    predicate: str
    object: str

    ontology: List[str] = field(default_factory=list)

    metadata: Dict[str, str] = field(default_factory=dict)

    confidence: float = 1.0

    def triple(self):

        return (
            self.subject,
            self.predicate,
            self.object,
        )

    def add_primitive(self, primitive):

        if primitive not in self.ontology:
            self.ontology.append(primitive)

    def primitives(self):

        return tuple(self.ontology)

    def __repr__(self):

        return (
            f"<Proposition "
            f"{self.subject} "
            f"{self.predicate} "
            f"{self.object}>"
        )
