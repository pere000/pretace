from kernel.repository_loader import RepositoryLoader
from kernel.repository_resolver import RepositoryResolver


class ConceptResolver:
    """
    Resolves canonical concepts independently of the underlying repository.
    """

    def __init__(self):
        self.repository_resolver = RepositoryResolver()
        self.repository_loader = RepositoryLoader()

    def resolve(self, authority_result, concept_name: str):
        repository_descriptor = self.repository_resolver.resolve(authority_result)

        return self.repository_loader.load(
            repository_descriptor,
            concept_name,
        )
