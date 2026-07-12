#!/usr/bin/env python3
"""
TACE Repository Browser (Phase 1)

Read-only presentation layer for exploring ontology modules and concepts.
Uses OntologyManager for explicit repository access (ADR-001).
"""

from new_ontology_manager import OntologyManager


def hr():
    print("=" * 60)


def show_field(title, value):
    print(title)
    print("-" * len(title))

    text = "" if value is None else str(value).strip()
    print(text if text else "(none)")
    print()


def concept_summary(record):
    canonical_identifier = None
    if record.get("id") is not None:
        canonical_identifier = str(record["id"])

    return {
        "concept_name": record["concept_name"],
        "module_name": record["ontology_module"],
        "status": record.get("status") or "",
        "canonical_identifier": canonical_identifier,
        "definition": record.get("definition") or "",
    }


def show_concept_summary(summary):
    hr()
    print("Concept Summary (Read-Only)")
    hr()
    print()
    show_field("Concept Name", summary["concept_name"])
    show_field("Module", summary["module_name"])
    show_field("Status", summary["status"])
    if summary["canonical_identifier"]:
        show_field("Canonical Identifier", summary["canonical_identifier"])
    show_field("Canonical Definition", summary["definition"])


def browse_module(om, module_name):
    concepts = om.get_concepts(module_name)
    expanded = True

    while True:
        print()
        hr()
        print(f"Module: {module_name}")
        print(f"Concepts: {len(concepts)}")
        hr()
        print()
        print("Commands:")
        print("  <number>   Select concept")
        print("  t          Toggle concept list")
        print("  0          Return to modules")
        print()

        if expanded:
            if not concepts:
                print("(no concepts)")
            else:
                for index, concept in enumerate(concepts, start=1):
                    status = concept.get("status") or ""
                    suffix = f" [{status}]" if status else ""
                    print(f"  {index:>3}. {concept['concept_name']}{suffix}")
        else:
            print("(concept list collapsed)")

        print()
        choice = input("Option: ").strip().lower()

        if choice == "0":
            return

        if choice == "t":
            expanded = not expanded
            continue

        if not choice.isdigit():
            continue

        index = int(choice)
        if index < 1 or index > len(concepts):
            continue

        concept_name = concepts[index - 1]["concept_name"]
        record = om.get_concept(concept_name)
        if record is None or record.get("ontology_module") != module_name:
            print("\nConcept not found.")
            continue

        show_concept_summary(concept_summary(record))
        input("\nPress Enter to continue...")


def main():
    om = OntologyManager()

    while True:
        modules = om.get_modules()

        print()
        hr()
        print("Repository Browser (Read-Only)")
        hr()
        print()

        if not modules:
            print("No ontology modules available.")
            return

        for index, module in enumerate(modules, start=1):
            module_name = module["module_name"]
            concept_count = len(om.get_concepts(module_name))
            print(f"  {index:>3}. {module_name} ({concept_count})")

        print()
        print("  0. Exit")
        print()

        choice = input("Select module: ").strip()
        if choice == "0":
            return

        if not choice.isdigit():
            continue

        index = int(choice)
        if index < 1 or index > len(modules):
            continue

        browse_module(om, modules[index - 1]["module_name"])


if __name__ == "__main__":
    main()
