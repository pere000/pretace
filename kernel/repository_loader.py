"""
RepositoryLoader

Loads canonical resources from the repository selected by AuthorityGate.
"""

import sqlite3


class RepositoryLoader:
    """Loads authoritative data from supported repository types."""

    def load(self, authority_result, concept_name: str):
        repository = authority_result.repository

        if repository.endswith(".db"):
            conn = sqlite3.connect(repository)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM concept_records WHERE concept_name = ?",
                (concept_name,),
            )
            row = cur.fetchone()
            conn.close()
            return row

        raise RuntimeError(f"Unsupported repository: {repository}")
