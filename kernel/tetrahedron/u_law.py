"""
u_law.py

TACE Constitutional Law

A constitutional law expresses an immutable ontological relation
that governs the behavior of the tetrahedral kernel.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Law(ABC):

    name: str

    description: str

    category: str

    @abstractmethod
    def applies(self, context):

        """
        Determines whether this law is relevant
        to the current context.
        """
        pass

    @abstractmethod
    def evaluate(self, context):

        """
        Returns the result of evaluating
        this constitutional law.
        """
        pass

    def __repr__(self):

        return f"<Law {self.name}>"
