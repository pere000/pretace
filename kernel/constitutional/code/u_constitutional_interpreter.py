"""
u_constitutional_interpreter.py

Constitutional Interpreter

Executes the Constitutional Code over a
Constitutional Model.
"""

class ConstitutionalInterpreter:

    def __init__(self, code):

        self.code = code

    ##################################################

    def execute(self, model):

        """
        Execute all constitutional sections
        in canonical order.
        """

        self.execute_identity(model)

        self.execute_nature(model)

        self.execute_dependencies(model)

        self.execute_capabilities(model)

        self.execute_laws(model)

        self.execute_constraints(model)

        self.execute_theorems(model)

        return model

    ##################################################

    def execute_identity(self, model):
        ...

    def execute_nature(self, model):
        ...

    def execute_dependencies(self, model):
        ...

    def execute_capabilities(self, model):
        ...

    def execute_laws(self, model):
        ...

    def execute_constraints(self, model):
        ...

    def execute_theorems(self, model):
        ...
