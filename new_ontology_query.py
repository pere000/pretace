#!/usr/bin/env python3

"""
Ontology Query

Query service backed by accepted ontology storage.
"""

from pathlib import Path
import re
import sqlite3


class OntologyQuery:

    def __init__(self):

        self.db_path = Path(__file__).resolve().parent / "tace_knowledge.db"

    def lookup(self, question):

        concept = self._extract_concept(question)
        print("CONCEPT:", repr(concept))
        
        if concept is None:
            return None

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        concept_row = conn.execute(
            """
            SELECT *
            FROM concept_records
            WHERE LOWER(concept_name) = LOWER(?)
            LIMIT 1
            """,
            (concept,),
        ).fetchone()
        print("ROW FOUND:", concept_row is not None)

        if concept_row is None:
            conn.close()
            return None

        concept_name = concept_row["concept_name"]

        relation_rows = conn.execute(
            """
            SELECT source_concept, relation_type, target_concept, confidence, notes
            FROM ontology_relations
            WHERE LOWER(source_concept) = LOWER(?)
               OR LOWER(target_concept) = LOWER(?)
            ORDER BY id
            """,
            (concept_name, concept_name),
        ).fetchall()

        conn.close()

        return {
            **dict(concept_row),
            "relations": [dict(row) for row in relation_rows],
        }

    def _extract_concept(self, question):

        q = question.strip()

        if not q:
            return None

        canonical = self._from_patterns(q)
        if canonical is not None:
            return canonical

        return self._from_known_concepts(q)

    def _from_patterns(self, question):

        patterns = [
            r"^\s*what\s+is\s+(?:an?\s+)?(.+?)\s*\??\s*$",
            r"^\s*define\s+(.+?)\s*\??\s*$",
            r"^\s*who\s+is\s+(?:an?\s+)?(.+?)\s*\??\s*$",
        ]

        for pattern in patterns:
            match = re.match(pattern, question, flags=re.IGNORECASE)
            if not match:
                continue
                
            print("MATCH:", repr(match.group(1)))                
                
            return self._normalize_concept_candidate(match.group(1))

        return None

    def _from_known_concepts(self, question):

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT concept_name
            FROM concept_records
            """
        ).fetchall()

        conn.close()

        q = question.lower()

        for row in rows:
            concept_name = row["concept_name"]
            variants = {
                concept_name.lower(),
                concept_name.lower().replace("_", " "),
            }
            if any(variant in q for variant in variants):
                return concept_name

        return None

    def _normalize_concept_candidate(self, raw):
        return raw.strip().rstrip("?")



if __name__ == "__main__":

    query = OntologyQuery()

    print(query.lookup("What is Matrix?"))
    print(query.lookup("What is Q-Form?"))
    print(query.lookup("Who wrote Hamlet?"))
