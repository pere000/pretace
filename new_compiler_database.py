#!/usr/bin/env python3

from pathlib import Path
import sqlite3


class LexiconDB:

    def __init__(self):
        self.db = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "tace_lexicon.db"
        )

    def connect(self):
        return sqlite3.connect(self.db)

    def _query(self, field, value):

        conn = self.connect()
        cur = conn.cursor()

        sql = f"""
        SELECT
            lu.lexical_unit,
            lu.lemma,
            sf.family_name,
            co.operator_name,
            ao.symbol
        FROM lexical_units lu

        JOIN lexical_family_map lfm
            ON lfm.lexical_unit_id = lu.id

        JOIN semantic_families sf
            ON sf.id = lfm.semantic_family_id

        JOIN family_operator_map fom
            ON fom.semantic_family_id = sf.id

        JOIN canonical_operators co
            ON co.id = fom.canonical_operator_id

        JOIN abstract_operators ao
            ON ao.id = co.abstract_operator_id

        WHERE lower(lu.{field}) = lower(?)
        LIMIT 1
        """

        cur.execute(sql, (value,))
        row = cur.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "lexical_unit": row[0],
            "lemma": row[1],
            "semantic_family": row[2],
            "canonical_operator": row[3],
            "abstract_operator": row[4],
        }

    def resolve(self, word):

        result = self._query("lexical_unit", word)

        if result:
            return result

        return self._query("lemma", word)


if __name__ == "__main__":

    db = LexiconDB()

    print(db.resolve("possesses"))
    print(db.resolve("possess"))
