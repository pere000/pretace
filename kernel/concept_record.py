from dataclasses import dataclass


@dataclass(frozen=True)
class ConceptRecord:
    concept_name: str
    definition: str
    ontology_module: str
    status: str
