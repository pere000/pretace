#!/usr/bin/env python3
"""
TACE Ontology Manager

Backend service for ontology access.

This module contains NO user interface and must never be
executed directly. It is intended to be used only by
ontology_menu.py.
"""

from pathlib import Path
import sqlite3


DB_PATH = Path("new_tace_knowledge.db")


class OntologyManager:
    """
    Backend access to the ontology repository.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # -----------------------------------------------------
    # Ontology modules
    # -----------------------------------------------------

    def get_modules(self):
        """
        Return every ontology module.
        """

        with self._connect() as conn:

            cur = conn.execute(
                """
                SELECT
                    id,
                    module_name,
                    COALESCE(description,'') AS description
                FROM ontology_modules
                ORDER BY module_name
                """
            )

            return [dict(row) for row in cur.fetchall()]

    def get_module(self, module_name):
        """
        Return one ontology module.
        """

        with self._connect() as conn:

            cur = conn.execute(
                """
                SELECT
                    id,
                    module_name,
                    COALESCE(description,'') AS description
                FROM ontology_modules
                WHERE module_name = ?
                """,
                (module_name,)
            )

            row = cur.fetchone()

            return dict(row) if row else None

    # -----------------------------------------------------
    # Concepts
    # -----------------------------------------------------

    def get_concepts(self, module_name):
        """
        Return all concepts belonging to one ontology module.
        """

        with self._connect() as conn:

            cur = conn.execute(
                """
                SELECT
                    id,
                    concept_name,
                    status
                FROM concept_records
                WHERE ontology_module = ?
                ORDER BY concept_name
                """,
                (module_name,)
            )

            return [dict(row) for row in cur.fetchall()]

    def get_concept(self, concept_name):

        with self._connect() as conn:

            cur = conn.execute(
                """
                SELECT *
                FROM concept_records
                WHERE concept_name = ?
                """,
                (concept_name,)
            )

            row = cur.fetchone()

            return dict(row) if row else None
