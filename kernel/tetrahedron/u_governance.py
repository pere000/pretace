"""
u_governance.py

TACE Constitutional Governance

Controls every modification of the constitutional ontology.
"""

from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):

    ADD = "ADD"

    MODIFY = "MODIFY"

    REMOVE = "REMOVE"

    APPROVE = "APPROVE"

    REJECT = "REJECT"


@dataclass
class ChangeProposal:

    identifier: str

    change_type: ChangeType

    author: str

    target: str

    description: str

    rationale: str

    evidence: list[str]
