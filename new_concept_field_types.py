FIELD_TYPES = {

    "definition":
        "Definition",

    "source_tradition":
        "Source Tradition",

    "assumptions":
        "Foundational Assumption",

    "scope":
        "Domain Scope",

    "terminology_mapping":
        "Terminology Mapping",

    "historical_development":
        "Historical Narrative",

    "tace_transformation":
        "Preservation Mapping",

    "references_text":
        "Source Attribution",

    "status":
        "Repository State"
}


FIELD_EDITABLE = {

    "definition": True,

    "source_tradition": True,

    "assumptions": True,

    "scope": True,

    "terminology_mapping": True,

    "historical_development": True,

    "tace_transformation": True,

    "references_text": True,

    "status": False
}


def field_type(
    field_name
):

    return FIELD_TYPES.get(
        field_name,
        "Unknown"
    )


def field_editable(
    field_name
):

    return FIELD_EDITABLE.get(
        field_name,
        False
    )


def field_value(
    value
):

    if value is None:
        return "[PENDING CURATION]"

    if not str(value).strip():
        return "[PENDING CURATION]"

    return value
