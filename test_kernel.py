from kernel.query_classifier import QueryClassifier
from kernel.authority_gate import AuthorityGate
from kernel.repository_loader import RepositoryLoader
from kernel.repository_resolver import RepositoryResolver

query = "What is Matrix?"

# Step 1: Classify the query
classifier = QueryClassifier()
classification = classifier.classify(query)

# Step 2: Resolve the governing authority
gate = AuthorityGate()
result = gate.resolve(classification)

# Step 3: Load the canonical concept
resolver = RepositoryResolver()
loader = RepositoryLoader()
concept = loader.load(result, "Matrix")

print("=" * 60)
print("Query         :", query)
print("Classification:", classification)
print("Authority     :", result)
print("=" * 60)

if concept:
    print("Concept Name :", concept["concept_name"])
    print("Definition   :", concept["definition"])
else:
    print("Concept not found.")
