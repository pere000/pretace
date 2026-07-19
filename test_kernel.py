from kernel.primitive_derivation import PrimitiveDerivation
from kernel.constitutional_validation import ConstitutionalValidation
from kernel.constitutional_explanation import ConstitutionalExplanation

pd = PrimitiveDerivation()
cv = ConstitutionalValidation()
ce = ConstitutionalExplanation()

concepts = [
    "Being",
    "Intelligence",
    "Operativity",
    "Selectivity",
    "Matrix",
    "Form",
    "Q-Form",
    "Substance",
]

for concept in concepts:

    print("=" * 70)
    print(concept)

    tree = pd.derive(concept)

    result = cv.validate(tree)

    print("VALID:", result.valid)

    if result.violations:
        print("Violations:")
        for v in result.violations:
            print("  -", v)

    print()
    print(ce.explain(tree))
    print()

print("=" * 70)
print("All tests finished.")
