"""
AuthorityGate

Maps a classified query to its governing authority.
"""

from kernel.authority_result import AuthorityResult


class AuthorityGate:

    MAP = {

        "ONTOLOGY": AuthorityResult(
            "ONTOLOGY",
            "Canonical Ontology",
            "new_tace_knowledge.db"
        ),

        "ADR": AuthorityResult(
            "ADR",
            "Architecture Decision Records",
            "docs/adr/"
        ),

        "SEMANTIC_CONSTITUTION": AuthorityResult(
            "SEMANTIC_CONSTITUTION",
            "Semantic Constitution",
            "docs/constitutions/"
        ),

        "SOFTWARE_CONSTITUTION": AuthorityResult(
            "SOFTWARE_CONSTITUTION",
            "Software Constitution",
            "docs/constitutions/"
        ),

        "SESSION_FOOTPRINT": AuthorityResult(
            "SESSION_FOOTPRINT",
            "Session Footprints",
            "docs/session_footprints/"
        ),
    }

    def resolve(self, classification: str) -> AuthorityResult:

        return self.MAP.get(
            classification,
            AuthorityResult(
                classification,
                "Unknown Authority",
                "",
                canonical=False,
            ),
        )
