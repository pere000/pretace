from kernel.repository_descriptor import RepositoryDescriptor


from kernel.config import ONTOLOGY_DB
class RepositoryResolver:

    MAP = {
        "Canonical Ontology": RepositoryDescriptor(
            name="Canonical Ontology",
            repository_type="sqlite",
            path=str(ONTOLOGY_DB),
            resource="concept_records",
        ),
    }

    def resolve(self, authority_result):
        return self.MAP[authority_result.authority]