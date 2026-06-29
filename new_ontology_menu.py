#!/usr/bin/env python3

import logging

logging.getLogger().setLevel(logging.CRITICAL)

from new_ontology_manager import OntologyManager
from new_concept_editor import ConceptEditor


def hr():
    print("=" * 60)


def show_field(title, value):

    print(title)
    print("-" * len(title))

    if value is None:
        print()

    else:

        text = str(value).strip()

        if text:
            print(text)
        else:
            print()

    print()


def concept_view(om, concept_name):

    while True:

        concept = om.get_concept(concept_name)

        if concept is None:

            print("\nConcept not found.")
            return

        print()
        hr()
        print(f"Concept : {concept['concept_name']}")
        print(f"Module  : {concept['ontology_module']}")
        hr()
        print()

        show_field("Definition", concept["definition"])
        show_field("Source Tradition", concept["source_tradition"])
        show_field("Assumptions", concept["assumptions"])
        show_field("Scope", concept["scope"])
        show_field("Terminology Mapping", concept["terminology_mapping"])
        show_field("Historical Development", concept["historical_development"])
        show_field("TACE Transformation", concept["tace_transformation"])
        show_field("References", concept["references_text"])
        show_field("Status", concept["status"])

        print("-" * 60)
        print("0           Return")
        print("-" * 60)

        if input("Option: ").strip() == "0":
            return


def main():

    om = OntologyManager()

    while True:

        modules = om.get_modules()

        print()
        hr()
        print("                    ONTOLOGY MANAGER")
        hr()
        print()

        for i, module in enumerate(modules, 1):
            print(f"{i:2}. {module['module_name']}")

        print()
        print("-" * 60)
        print("<number>    Open ontology module")
        print("0           Return")
        print("-" * 60)

        cmd = input("Option: ").strip()

        if cmd == "0":
            return

        if not cmd.isdigit():
            print("\nInvalid option.")
            continue

        idx = int(cmd) - 1

        if idx < 0 or idx >= len(modules):
            print("\nInvalid module.")
            continue

        module = modules[idx]

        while True:

            concepts = om.get_concepts(module["module_name"])

            print()
            hr()
            print(f"MODULE: {module['module_name']}")
            hr()
            print()

            if concepts:

                for i, concept in enumerate(concepts, 1):
                    print(f"{i:3}. {concept['concept_name']}")

            else:
                print("(No concepts)")

            print()
            print("-" * 60)
            print("<number>    Open concept")
            print("0           Return")
            print("-" * 60)

            cmd = input("Option: ").strip()

            if cmd == "0":
                break

            if not cmd.isdigit():
                print("\nInvalid option.")
                continue

            idx = int(cmd) - 1

            if idx < 0 or idx >= len(concepts):
                print("\nInvalid concept.")
                continue

            ConceptEditor().run(
                concepts[idx]["concept_name"]
            )


if __name__ == "__main__":
    main()
