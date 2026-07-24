"""
u_metamodel.py

TACE Metamodel

Defines the constitutional categories that every
ontological object must belong to.
"""

from enum import Enum
from dataclasses import dataclass


class MetaCategory(Enum):

    #
    # Ontological
    #

    PRIMITIVE = "Primitive"

    EDGE = "Edge"

    FACE = "Face"

    TETRAHEDRON = "Tetrahedron"

    #
    # Constitutional
    #

    AXIOM = "Axiom"

    LAW = "Law"

    CONSTRAINT = "Constraint"

    THEOREM = "Theorem"

    #
    # Runtime
    #

    EVENT = "Event"

    STATE = "State"

    TRANSACTION = "Transaction"

    #
    # Reasoning
    #

    PROPOSITION = "Proposition"

    QUERY = "Query"

    JUDGEMENT = "Judgement"

    TRACE = "Trace"


@dataclass(frozen=True)
class MetaObject:

    identifier: str

    category: MetaCategory

    version: str = "1.0"
