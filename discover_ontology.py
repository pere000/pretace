#!/usr/bin/env python3

"""
discover_ontology.py

Scans a repository looking for possible ontology concept definitions.

Usage:

    python discover_ontology.py .

Output:

    ontology_discovery.md
"""

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

OUTPUT = ROOT / "ontology_discovery.md"

EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".sql"
}

# ---------------------------------------------------------

def add(concepts, concept, definition, filename):
    concept = concept.strip()

    if not concept:
        return

    if len(concept) > 80:
        return

    if concept.lower() in {
        "definition",
        "status",
        "scope",
        "references",
        "module"
    }:
        return

    concepts.setdefault(concept, []).append(
        (filename, definition.strip())
    )

# ---------------------------------------------------------

concepts = {}

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if file.suffix.lower() not in EXTENSIONS:
        continue

    try:
        text = file.read_text(errors="ignore")
    except Exception:
        continue

    lines = text.splitlines()

    for i, line in enumerate(lines):

        # ---------------------------------------
        # Markdown
        #
        # ## Matrix
        # Definition: ....
        #
        # ---------------------------------------

        m = re.match(r"^##+\s+(.+)$", line)

        if m:

            concept = m.group(1)

            definition = ""

            for j in range(i + 1, min(i + 8, len(lines))):

                if lines[j].strip():

                    definition += lines[j].strip() + " "

            add(concepts, concept, definition, file)

        # ---------------------------------------
        # Python dict
        #
        # "Matrix":
        #
        # ---------------------------------------

        m = re.match(r'^\s*"([^"]+)"\s*:\s*{?', line)

        if m:

            concept = m.group(1)

            definition = ""

            for j in range(i + 1, min(i + 10, len(lines))):

                if "definition" in lines[j].lower():

                    definition = lines[j]

                    break

            add(concepts, concept, definition, file)

        # ---------------------------------------
        # SQL
        #
        # INSERT ...
        #
        # ---------------------------------------

        if "INSERT INTO concept_records" in line:

            add(
                concepts,
                "SQL Definition",
                line,
                file
            )

# ---------------------------------------------------------

with OUTPUT.open("w", encoding="utf8") as out:

    out.write("# Ontology Discovery Report\n\n")

    out.write(f"Repository: {ROOT}\n\n")

    out.write(f"Concepts discovered: {len(concepts)}\n\n")

    out.write("---\n\n")

    for concept in sorted(concepts):

        out.write(f"# {concept}\n\n")

        for filename, definition in concepts[concept]:

            out.write(f"Source: `{filename}`\n\n")

            if definition:

                out.write(f"{definition}\n\n")

        out.write("\n---\n\n")

print()
print("Ontology discovery completed.")
print(f"Report written to: {OUTPUT}")
print()
