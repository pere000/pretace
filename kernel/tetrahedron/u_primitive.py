"""
u_primitive.py

TACE Core

Defines the fundamental ontological primitive from which all
canonical TACE vertices are derived.

Author: TACE Project
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Primitive:
    """
    An irreducible ontological principle.

    A Primitive is not a concept, object, or substance.
    It is a constitutional principle that participates
    in the tetrahedral architecture.
    """

    name: str
    definition: str
    semantic_role: str
    universal_function: str

    # Constitutional relations
    outgoing: List[str] = field(default_factory=list)
    incoming: List[str] = field(default_factory=list)

    # Optional metadata
    metadata: Dict[str, str] = field(default_factory=dict)

    def is_source(self) -> bool:
        """Returns True if the primitive has outgoing relations."""
        return len(self.outgoing) > 0

    def is_target(self) -> bool:
        """Returns True if the primitive has incoming relations."""
        return len(self.incoming) > 0

    def degree(self) -> int:
        """Number of constitutional relations."""
        return len(self.outgoing) + len(self.incoming)

    def describe(self) -> str:
        """Human-readable summary."""

        return (
            f"{self.name}\n"
            f"Definition : {self.definition}\n"
            f"Role       : {self.semantic_role}\n"
            f"Function   : {self.universal_function}\n"
            f"Outgoing   : {self.outgoing}\n"
            f"Incoming   : {self.incoming}"
        )
