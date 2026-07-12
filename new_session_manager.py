#!/usr/bin/env python3

"""
Persistent Session Manager

The Session Knowledge survives between executions.

The Universe is always rebuilt from this list.
"""

from pathlib import Path
import sqlite3


class SessionManager:

    def __init__(self):

        data = Path(__file__).resolve().parent / "data"
        data.mkdir(exist_ok=True)

        self.db = data / "tace_session.db"


        self._create()

    # -------------------------------------------------

    def connect(self):

        return sqlite3.connect(self.db)

    # -------------------------------------------------

    def _create(self):

        conn = self.connect()

        conn.execute("""

        CREATE TABLE IF NOT EXISTS session_items(

            position INTEGER PRIMARY KEY,

            sentence TEXT NOT NULL

        )

        """)

        conn.commit()

        conn.close()

    # -------------------------------------------------

    def all(self):

        conn = self.connect()

        rows = conn.execute("""

        SELECT sentence

        FROM session_items

        ORDER BY position

        """).fetchall()

        conn.close()

        return [r[0] for r in rows]

    # -------------------------------------------------

    def _rewrite(self, items):

        conn = self.connect()

        conn.execute(
            "DELETE FROM session_items"
        )

        for i, sentence in enumerate(items):

            conn.execute(

                """

                INSERT INTO session_items

                VALUES(?,?)

                """,

                (i, sentence),

            )

        conn.commit()

        conn.close()

    # -------------------------------------------------

    def add(self, text):

        items = self.all()

        items.append(text)

        self._rewrite(items)

    # -------------------------------------------------

    def replace(self, index, text):

        items = self.all()

        items[index] = text

        self._rewrite(items)

    # -------------------------------------------------

    def remove(self, index):

        items = self.all()

        del items[index]

        self._rewrite(items)

    # -------------------------------------------------

    def clear(self):

        conn = self.connect()

        conn.execute(
            "DELETE FROM session_items"
        )

        conn.commit()

        conn.close()


if __name__ == "__main__":

    s = SessionManager()

    print(s.all())
