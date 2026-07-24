"""
u_instruction.py

Constitutional Instruction Set (CIS)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any


class Opcode(Enum):

    #
    # Runtime
    #

    ASSERT = "ASSERT"

    RETRACT = "RETRACT"

    ACTIVATE = "ACTIVATE"

    DEACTIVATE = "DEACTIVATE"

    #
    # Reasoning
    #

    INFER = "INFER"

    VALIDATE = "VALIDATE"

    EXPLAIN = "EXPLAIN"

    QUERY = "QUERY"

    #
    # Ontology
    #

    REGISTER = "REGISTER"

    LOAD = "LOAD"

    SAVE = "SAVE"


@dataclass(frozen=True)
class Instruction:

    opcode: Opcode

    operand: Any = None

    metadata: dict | None = None
