"""
ADR-010

Validation Result

Represents the outcome of constitutional validation.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ValidationResult:
    """
    Result produced by ConstitutionalValidation.
    """

    valid: bool

    violations: Tuple[str, ...] = ()
