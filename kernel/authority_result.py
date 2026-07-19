"""
AuthorityResult

Immutable result produced by AuthorityGate.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorityResult:
    """
    Result of constitutional authority resolution.
    """

    classification: str
    authority: str
    repository: str
    canonical: bool = True

    def __str__(self):
        return (
            f"AuthorityResult("
            f"classification='{self.classification}', "
            f"authority='{self.authority}', "
            f"repository='{self.repository}', "
            f"canonical={self.canonical})"
        )
