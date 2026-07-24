"""
u_activation_scheduler.py

Activation Scheduler

Evaluates constitutional entities and schedules
lawful actualizations whose preconditions are
currently satisfied.
"""

from collections import deque


class ActivationScheduler:

    def __init__(self, constitution):

        self.constitution = constitution

        self.queue = deque()

    ##################################################

    def schedule(self, model):

        """
        Populate the activation queue from
        the current constitutional model.
        """

        self.queue.clear()

        for entity in model.entities():

            if self.ready(entity):

                self.queue.append(entity)

    ##################################################

    def ready(self, entity):

        """
        True if all constitutional
        preconditions are satisfied.
        """

        return self.constitution.preconditions(
            entity
        )

    ##################################################

    def next(self):

        if self.queue:

            return self.queue.popleft()

        return None
