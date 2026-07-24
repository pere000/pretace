"""
u_transaction.py

Constitutional Transaction

A transaction is an atomic execution of one constitutional instruction.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any


@dataclass
class Transaction:

    instruction: Any

    start_time: datetime = field(default_factory=datetime.utcnow)

    end_time: datetime | None = None

    success: bool = False

    messages: List[str] = field(default_factory=list)

    events: List[Any] = field(default_factory=list)

    result: Any = None

    def add_message(self, message: str):

        self.messages.append(message)

    def add_event(self, event):

        self.events.append(event)

    def commit(self, result=None):

        self.success = True
        self.result = result
        self.end_time = datetime.utcnow()

    def rollback(self, reason):

        self.success = False
        self.result = reason
        self.end_time = datetime.utcnow()

    @property
    def duration(self):

        if self.end_time is None:
            return None

        return self.end_time - self.start_time
