#!/usr/bin/env python3
"""
TACE Concept Editor

Reusable controller shared by:

    Repository Browser
    Ontology Menu

This module owns the interaction loop.

It does NOT know where it was called from.
"""

from new_concept_repository import ConceptRepository
from new_concept_view_v2 import ConceptViewV2


class ConceptEditor:

    EDITABLE_FIELDS = [

        "definition",

        "source_tradition",

        "assumptions",

        "scope",

        "terminology_mapping",

        "historical_development",

        "tace_transformation",

        "references_text"
    ]

    def __init__(self):

        self.repo = ConceptRepository()

        self.view = ConceptViewV2()

    def run(
        self,
        concept_name
    ):

        while True:

            data = self.repo.show_concept(
                concept_name
            )

            if data is None:

                print("\\nConcept not found.")
                return

            self.view.show_concept(
                concept_name,
                data
            )

            print()

            print("<number>    Edit field")
            print("0            Return")

            cmd = input("Option: ").strip()

            if cmd == "0":
                return

            if not cmd.isdigit():
                continue

            sel = cmd

            idx = int(sel) - 1

            if (
                idx < 0
                or
                idx >= len(
                    self.EDITABLE_FIELDS
                )
            ):
                continue

            field = self.EDITABLE_FIELDS[
                idx
            ]

            print()

            print(
                "Current value:"
            )

            print(
                data.get(
                    field,
                    ""
                )
            )

            print()

            new_value = input(
                "New value: "
            )

            confirm = input(
                "Confirm (y/n): "
            ).strip().lower()

            if confirm != "y":
                continue

            backup = (
                self.repo
                .backup_database()
            )

            ok = (
                self.repo
                .update_field(
                    concept_name,
                    field,
                    new_value
                )
            )

            print()

            print(
                f"Backup: {backup}"
            )

            print()

            print(
                "UPDATED"
                if ok
                else
                "UPDATE FAILED"
            )

