"""
u_engine.py

TACE Constitutional Engine

The Engine is the only public entry point
for executing the constitutional kernel.
"""

from kernel.execution.u_state import ConstitutionalState
from kernel.constitution.u_constitution import Constitution
from kernel.reasoning.u_mapper import Mapper
from kernel.reasoning.u_inference import Inference
from kernel.reasoning.u_validator import Validator


class Engine:

    def __init__(self, tetrahedron, constitution):

        self.tetrahedron = tetrahedron

        self.constitution = constitution

        self.state = ConstitutionalState()

        self.mapper = Mapper(tetrahedron)

        self.validator = Validator(tetrahedron)

        self.inference = Inference(tetrahedron)

    #
    # Main entry point
    #

    def process(self, event):

        #
        # 1. Map
        #

        mapping = self.mapper.map_event(event)

        #
        # 2. Activate
        #

        for primitive in mapping.primitives:

            self.state.activate_primitive(primitive)

        #
        # 3. Execute Constitution
        #

        self.constitution.evaluate(self.state)

        #
        # 4. Infer
        #

        report = self.inference.evaluate(self.state)

        #
        # 5. Validate
        #

        self.validator.validate(self.state)

        #
        # 6. Record
        #

        self.state.record(event)

        return report
