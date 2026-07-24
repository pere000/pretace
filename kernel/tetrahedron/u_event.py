"""
u_event.py

Constitutional Event

Every change in the runtime is represented
as an immutable event.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class ConstitutionalEvent:

    type: str

    source: str

    payload: Dict[str, Any]

    timestamp: datetime = datetime.utcnow()

    def __repr__(self):

        return (
            f"<Event "
            f"{self.type} "
            f"from {self.source}>"
        )
