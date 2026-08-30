#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil

# ============================================================
# TACE CANONICAL ACCEPTANCE / READING SAFEGUARD
#
# This patch establishes the internal TACE rule that:
#
#   TACE canonical acceptance =
#   explicit acceptance by the TACE author/maintainer.
#
# An explicitly accepted architectural revision supersedes the
# previous formulation that it explicitly replaces.
#
# This patch does NOT alter substantive ontology or tetrahedra.
# ============================================================

ROOT = Path("/media/external_drive/llm/pretace")

ARCHITECTURAL = ROOT / "docs/architecture/TACE_ARCHITECTURAL_AXIOMS.md"
PHILOSOPHICAL = ROOT / "docs/constitution/TACE_PHILOSOPHICAL_CONSTITUTION.md"
SEMANTIC = ROOT / "docs/constitution/TACE_SEMANTIC_CONSTITUTION.md"

DATE = "2026-08-30"

FILES = [
    SEMANTIC,
    ARCHITECTURAL,
    PHILOSOPHICAL,
]


# ============================================================
# CANONICAL TEXT
# ============================================================

SEMANTIC_PATCH = r"""
## Canonical Acceptance and Supersession

TACE canonical acceptance = explicit acceptance by the TACE
author/maintainer.

A proposed TACE architectural change becomes canonical when explicitly
accepted by the TACE author/maintainer.

Once accepted, it SHALL be treated as superseding any previous
formulation that it explicitly replaces.

An explicitly accepted revision SHALL be treated as part of the
canonical TACE architecture even if older documents have not yet been
physically updated.

### Canonical Status of TACE Developments

Future reasoning about TACE SHALL distinguish:

1. **Canonical**
   A formulation explicitly accepted by the TACE author/maintainer.

2. **Proposed**
   A formulation discussed or developed but not explicitly accepted.

3. **Inferred**
   A conclusion derived from canonical material but not itself
   explicitly accepted.

4. **Historical/Superseded**
   A formulation that was previously used or canonical but has been
   explicitly replaced by a later accepted formulation.

Discussion, coherence, repetition, diagrams, session footprints,
working documents, or AI-generated text SHALL NOT by themselves establish
canonical status.

### Supersession Rule

When an explicitly accepted TACE formulation replaces an earlier
formulation, the later accepted formulation SHALL govern future TACE
reasoning.

The superseded formulation MAY remain in historical documents for
provenance, but SHALL NOT be presented as the current canonical
formulation.

### No Silent Reconciliation

When an older formulation and a newer formulation differ, a reasoning
engine SHALL NOT silently merge, reconcile, reinterpret, or average them.

If the newer formulation has been explicitly accepted by the TACE
author/maintainer, it SHALL govern.

If it has not been explicitly accepted, the newer formulation SHALL
remain proposed or inferred.

### Tetrahedral Revision Rule

Any change to a TACE tetrahedron SHALL be treated as an architectural
change.

This includes changes to:

- vertices;
- center of gravity;
- vertex definitions;
- relations among vertices;
- constitutional interpretation;
- ontological function;
- relations to other tetrahedra.

An accepted tetrahedral revision SHALL supersede the previous
formulation that it explicitly replaces.

### Terminological Revision Rule

A newly introduced TACE technical term SHALL NOT silently replace an
existing canonical term.

A new term becomes canonical only through explicit acceptance by the
TACE author/maintainer.

When an accepted term supersedes an earlier term, the earlier term SHALL
be treated as superseded unless both are explicitly retained.

### Conservative Reading Rule

When canonical status cannot be established, reasoning engines SHALL
NOT guess.

They SHALL identify the material as proposed, inferred, historical,
superseded, or undetermined according to its provenance.

Canonical status SHALL NOT be presumed merely from compatibility with
existing TACE ontology.

### Provenance Rule

Generated explanations, AI responses, session discussions, diagrams,
and working notes SHALL NOT be treated as evidence that a proposition
has been canonically accepted.

Canonical acceptance requires explicit acceptance by the TACE
author/maintainer.
"""


ARCHITECTURAL_PATCH = r"""
## Canonical Acceptance and Architectural Revision

TACE canonical acceptance = explicit acceptance by the TACE
author/maintainer.

A proposed TACE architectural change becomes canonical when explicitly
accepted by the TACE author/maintainer.

Once accepted, it SHALL be treated as superseding any previous
formulation that it explicitly replaces.

Future readings of this living architectural document SHALL distinguish
current accepted architecture from historical, superseded, proposed, and
inferred material.

A tetrahedron, vertex, center of gravity, definition, constitutional
relation, or architectural interpretation SHALL NOT be silently changed
or propagated merely because it appears in a discussion, diagram,
session footprint, working document, or generated explanation.

Once explicitly accepted by the TACE author/maintainer, however, the
accepted revision SHALL govern future TACE architectural reasoning and
SHALL supersede the formulation it explicitly replaces.

Historical formulations SHALL remain identifiable for provenance but
SHALL NOT govern current reasoning when superseded.
"""


PHILOSOPHICAL_PATCH = r"""
## Canonical Acceptance of TACE Architectural Revisions

TACE canonical acceptance = explicit acceptance by the TACE
author/maintainer.

A proposed TACE architectural change becomes canonical when explicitly
accepted by the TACE author/maintainer.

Once accepted, it SHALL be treated as superseding any previous
formulation that it explicitly replaces.

This rule concerns the internal canonical architecture and conceptual
ontology of TACE. It does not constitute ecclesial, magisterial, or
external doctrinal authority.

An explicitly accepted TACE architectural revision SHALL therefore be
treated as canonical for subsequent TACE reasoning even when older
documents preserve the superseded formulation for historical or
provenance purposes.
"""


# ============================================================
# HELPERS
# ============================================================

def check_files():
    missing = [str(p) for p in FILES if not p.is_file()]

    if missing:
        print("ERROR: The following required files were not found:")
        for item in missing:
            print("  " + item)
        raise SystemExit(1)


def backup(path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_name(
        f"{path.stem}.backup_{stamp}{path.suffix}"
    )
    shutil.copy2(path, backup_path)
    return backup_path


def append_once(path, patch):
    text = path.read_text(encoding="utf-8")

    # Use the first heading as a unique marker.
    marker = patch.strip().splitlines()[0]

    if marker in text:
        print(f"Already patched: {path}")
        return False

    path.write_text(
        text.rstrip() + "\n\n---\n\n" + patch.strip() + "\n",
        encoding="utf-8"
    )

    print(f"Updated: {path}")
    return True


# ============================================================
# EXECUTION
# ============================================================

print()
print("TACE canonical-governance patch")
print("--------------------------------")
print()

check_files()

print("All three canonical files found.")
print()

# Create backups BEFORE modification.
for path in FILES:
    backup_path = backup(path)
    print(f"Backup: {backup_path}")

print()

# Apply patches.
append_once(SEMANTIC, SEMANTIC_PATCH)
append_once(ARCHITECTURAL, ARCHITECTURAL_PATCH)
append_once(PHILOSOPHICAL, PHILOSOPHICAL_PATCH)

print()
print("Patch completed.")
print()
print("Canonical acceptance is now explicitly defined as:")
print()
print("  explicit acceptance by the TACE author/maintainer")
print()
print("Accepted architectural revisions supersede previous formulations")
print("that they explicitly replace.")
print()
print("No substantive ontology or tetrahedron was modified by this patch.")
