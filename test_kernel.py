from kernel.kernel import Kernel

kernel = Kernel()

query = "What is Matrix?"
concept = kernel.resolve("Matrix")

print("=" * 60)
print("Query :", query)
print("=" * 60)

if concept:
    print("Concept Name :", concept.concept_name)
    print("Definition   :", concept.definition)
else:
    print("Concept not found.")
