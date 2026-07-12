#!/usr/bin/env python3

"""
TACE Ontology Repository

Single access point to the authoritative ontology.
"""

from pathlib import Path
import sqlite3

from ontology.models import OntologicalConcept


class OntologyRepository:

    def __init__(self):

        self.db = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "tace_lexicon.db"
        )

    def connect(self):
        return sqlite3.connect(self.db)

    def concept(self, concept_id):

        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                module,
                concept
            FROM ontology_concepts
            WHERE id = ?
        """, (concept_id,))

        row = cur.fetchone()

        conn.close()

        if row is None:
            return None

        return OntologicalConcept(
            concept_id=row[0],
            module=row[1],
            name=row[2]
        )


if __name__ == "__main__":

    repo = OntologyRepository()

    print(repo.concept(1))
    print(repo.concept(999))
