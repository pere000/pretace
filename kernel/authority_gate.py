"""
AuthorityGate

Maps a classified query to its governing authority.
"""

from kernel.authority_result import AuthorityResult


class AuthorityGate:

    MAP = {

        "ONTOLOGY": AuthorityResult(
            classification="ONTOLOGY",
            authority="Canonical Ontology",
        ),

        "ADR": AuthorityResult(
            classification="ADR",
            authority="Architecture Decision Records",
        ),

        "SEMANTIC_CONSTITUTION": AuthorityResult(
            classification="SEMANTIC_CONSTITUTION",
            authority="Semantic Constitution",
        ),

        "SOFTWARE_CONSTITUTION": AuthorityResult(
            classification="SOFTWARE_CONSTITUTION",
            authority="Software Constitution",
        ),

        "SESSION_FOOTPRINT": AuthorityResult(
            classification="SESSION_FOOTPRINT",
            authority="Session Footprints",
        ),
    }

    def resolve(self, classification: str) -> AuthorityResult:

        return self.MAP.get(
            classification,
            AuthorityResult(
                classification=classification,
                authority="Unknown Authority",
                canonical=False,
            ),
        )
