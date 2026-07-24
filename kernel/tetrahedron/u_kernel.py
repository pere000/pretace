"""
u_kernel.py

Public API of the TACE Kernel.
"""

from kernel.bootstrap.u_bootstrap import Bootstrap
from kernel.protocol.u_instruction import (
    Instruction,
    Opcode
)


class Kernel:

    def __init__(self):

        self.engine = Bootstrap.build()

    #
    # Public API
    #

    def assert_proposition(self, proposition):

        instruction = Instruction(

            opcode=Opcode.ASSERT,

            operand=proposition

        )

        return self.engine.execute(instruction)

    def query(self, query):

        instruction = Instruction(

            opcode=Opcode.QUERY,

            operand=query

        )

        return self.engine.execute(instruction)

    def explain(self, judgement):

        instruction = Instruction(

            opcode=Opcode.EXPLAIN,

            operand=judgement

        )

        return self.engine.execute(instruction)

    def validate(self):

        instruction = Instruction(

            opcode=Opcode.VALIDATE

        )

        return self.engine.execute(instruction)
