"""
ADR-009
Derivation Node

Immutable representation of a constitutional derivation tree.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DerivationNode:
    """
    A node in a constitutional derivation tree.
    """

    concept: str
    primitive: bool
    resolved: bool
    children: Tuple["DerivationNode", ...] = ()
