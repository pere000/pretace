from kernel.repository_loader import RepositoryLoader

loader = RepositoryLoader()

concept = loader.load(result, "Matrix")

print(concept)
