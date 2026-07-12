from new_concept_field_types import (
    field_type,
    field_value,
    field_editable
)


class ConceptViewV2:

    FIELDS = [

        "definition",

        "assumptions",

        "scope",

        "historical_development",

        "tace_transformation",

        "references_text",

        "status"
    ]

    def show_concept(
        self,
        concept,
        data
    ):

        print(
            f"\n🟣 CONCEPT: {concept}\n"
        )

        for i, field in enumerate(
            self.FIELDS,
            start=1
        ):

            print(
                f"{i}. "
                +
                field.replace(
                    "_",
                    " "
                ).title()
            )


    
    def show_field(
        self,
        field,
        value
    ):

        print(
            f"\nCurrent: {field_value(value)}"
        )



    def field_from_selection(
        self,
        selection
    ):

        try:

            idx = (
                int(selection)
                - 1
            )

        except Exception:

            return None

        if idx < 0:
            return None

        if idx >= len(
            self.FIELDS
        ):
            return None

        return self.FIELDS[
            idx
        ]


    def replace_field(
        self,
        repo,
        concept,
        field,
        new_value
    ):

        backup = (
            repo.backup_database()
        )

        ok = (
            repo.update_field(
                concept,
                field,
                new_value
            )
        )

        return {
            "backup": backup,
            "success": ok
        }
