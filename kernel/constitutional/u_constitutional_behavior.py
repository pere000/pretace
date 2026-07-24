"""
u_constitutional_behavior.py

Constitutional Behavior

Encapsulates the lawful behavior associated with
a Constitutional Entity.
"""

from abc import ABC, abstractmethod


class ConstitutionalBehavior(ABC):

    def __init__(self, entity):

        self.entity = entity

    ##################################################

    @abstractmethod
    def applicable(self, model):

        """
        Is this behavior currently applicable?
        """

        ...

    ##################################################

    @abstractmethod
    def execute(self, model):

        """
        Applies the constitutional transformation.
        """

        ...

    ##################################################

    @abstractmethod
    def priority(self):

        """
        Execution priority.
        """

        ...
