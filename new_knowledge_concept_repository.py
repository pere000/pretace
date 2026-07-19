import sqlite3


from kernel.config import ONTOLOGY_DB
class ConceptRepository:

    def __init__(
        self,
        db_path=str(ONTOLOGY_DB)
    ):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(
            self.db_path
        )

        conn.row_factory = (
            sqlite3.Row
        )

        return conn

    def list_modules(
        self
    ):

        conn = self._conn()

        rows = conn.execute(
            """
            SELECT module_name
            FROM ontology_modules
            ORDER BY module_name
            """
        ).fetchall()

        conn.close()

        return [
            r["module_name"]
            for r in rows
        ]

    def list_concepts(
        self,
        module=None
    ):

        conn = self._conn()

        if module:

            rows = conn.execute(
                """
                SELECT concept_name
                FROM concept_records
                WHERE ontology_module=?
                ORDER BY concept_name
                """,
                (module,)
            ).fetchall()

        else:

            rows = conn.execute(
                """
                SELECT concept_name
                FROM concept_records
                ORDER BY concept_name
                """
            ).fetchall()

        conn.close()

        return [
            r["concept_name"]
            for r in rows
        ]

    def show_concept(
        self,
        concept
    ):

        conn = self._conn()

        row = conn.execute(
            """
            SELECT *
            FROM concept_records
            WHERE concept_name=?
            """,
            (concept,)
        ).fetchone()

        conn.close()

        return (
            dict(row)
            if row
            else None
        )

    def show_module(
        self,
        module
    ):

        conn = self._conn()

        rows = conn.execute(
            """
            SELECT *
            FROM concept_records
            WHERE ontology_module=?
            ORDER BY concept_name
            """,
            (module,)
        ).fetchall()

        conn.close()

        return [
            dict(r)
            for r in rows
        ]

    def update_field(
        self,
        concept,
        field,
        value
    ):

        allowed = {

            "definition",

            "source_tradition",

            "assumptions",

            "scope",

            "terminology_mapping",

            "historical_development",

            "tace_transformation",

            "references_text"
        }

        if field not in allowed:

            return False

        conn = self._conn()

        conn.execute(
            f"""
            UPDATE concept_records
            SET {field}=?
            WHERE concept_name=?
            """,
            (
                value,
                concept
            )
        )

        conn.commit()

        conn.close()

        return True

    def backup_database(
        self
    ):

        from shutil import copy2
        from datetime import datetime
        from pathlib import Path

        src = Path(
            self.db_path
        )

        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        dst = src.parent / (
            f"tace_knowledge_backup_{stamp}.db"
        )

        copy2(
            src,
            dst
        )

        return str(dst)