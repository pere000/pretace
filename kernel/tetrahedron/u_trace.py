"""
u_trace.py

Constitutional Trace

Represents the complete constitutional path
that produced a conclusion.
"""

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class TraceStep:

    stage: str

    object: Any

    description: str


@dataclass
class Trace:

    steps: List[TraceStep] = field(default_factory=list)

    def add(self, stage, obj, description):

        self.steps.append(

            TraceStep(

                stage=stage,

                object=obj,

                description=description

            )

        )

    def summary(self):

        return [

            f"{s.stage}: {s.description}"

            for s in self.steps

        ]

    def __len__(self):

        return len(self.steps)
