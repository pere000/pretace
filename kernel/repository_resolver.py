from kernel.repository_descriptor import RepositoryDescriptor


class RepositoryResolver:

    MAP = {
        "Canonical Ontology": RepositoryDescriptor(
            name="Canonical Ontology",
            repository_type="sqlite",
            path="new_tace_knowledge.db",
            resource="concept_records",
        ),
    }

    def resolve(self, authority_result):
        return self.MAP[authority_result.authority]
