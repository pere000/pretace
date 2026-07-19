"""
RepositoryLoader

Loads canonical resources from the repository selected by RepositoryResolver.
"""

import sqlite3

from kernel.concept_record import ConceptRecord


class RepositoryLoader:
    """Loads authoritative data from supported repository types."""

    def load(self, repository_descriptor, concept_name: str):
        repository = repository_descriptor.path

        if repository.endswith(".db"):
            conn = sqlite3.connect(repository)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(
                f"SELECT * FROM {repository_descriptor.resource} "
                f"WHERE concept_name = ?",
                (concept_name,),
            )

            row = cur.fetchone()
            conn.close()

            if row is None:
                return None

            return ConceptRecord(
                concept_name=row["concept_name"],
                definition=row["definition"],
                ontology_module=row["ontology_module"],
                status=row["status"],
            )

        raise RuntimeError(f"Unsupported repository: {repository}")
