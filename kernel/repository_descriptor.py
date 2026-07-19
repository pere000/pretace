from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryDescriptor:
    name: str
    repository_type: str
    path: str
    resource: str
