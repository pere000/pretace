#!/usr/bin/env python3
"""
TACE Kernel Refactoring
ADR-005 : Repository Resolution

This script performs Steps 3, 4 and 5 automatically.

Changes:
1. RepositoryLoader now receives RepositoryDescriptor.
2. AuthorityResult no longer stores repository paths.
3. test_kernel.py is updated to use RepositoryResolver.

A .bak copy of every modified file is created.
"""

from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
KERNEL = ROOT / "kernel"


def backup(file):
    shutil.copy2(file, file.with_suffix(file.suffix + ".bak"))


# ----------------------------------------------------------
# Step 3
# RepositoryLoader
# ----------------------------------------------------------

loader = KERNEL / "repository_loader.py"

backup(loader)

text = loader.read_text()

text = text.replace(
    "repository = authority_result.repository",
    "repository = repository_descriptor.path"
)

text = text.replace(
    '"SELECT * FROM concept_records WHERE concept_name = ?"',
    'f"SELECT * FROM {repository_descriptor.resource} WHERE concept_name = ?"'
)

text = text.replace(
    "def load(self, authority_result, concept_name):",
    "def load(self, repository_descriptor, concept_name):"
)

loader.write_text(text)

print("✓ repository_loader.py updated")


# ----------------------------------------------------------
# Step 4
# AuthorityResult
# ----------------------------------------------------------

authority = KERNEL / "authority_result.py"

backup(authority)

text = authority.read_text()

text = re.sub(
    r"repository:\s*str\s*\n",
    "",
    text,
)

authority.write_text(text)

print("✓ authority_result.py updated")


# ----------------------------------------------------------
# Step 4b
# AuthorityGate
# ----------------------------------------------------------

gate = KERNEL / "authority_gate.py"

backup(gate)

text = gate.read_text()

text = re.sub(
    r',\s*"new_tace_knowledge\.db"',
    "",
    text,
)

gate.write_text(text)

print("✓ authority_gate.py updated")


# ----------------------------------------------------------
# Step 5
# test_kernel
# ----------------------------------------------------------

test = ROOT / "test_kernel.py"

backup(test)

text = test.read_text()

if "RepositoryResolver" not in text:

    text = text.replace(
        "from kernel.repository_loader import RepositoryLoader",
        "from kernel.repository_loader import RepositoryLoader\n"
        "from kernel.repository_resolver import RepositoryResolver"
    )

    text = text.replace(
        "loader = RepositoryLoader()",
        "resolver = RepositoryResolver()\n"
        "loader = RepositoryLoader()"
    )

    text = text.replace(
        "concept = loader.load(authority, concept_name)",
        "repository = resolver.resolve(authority)\n"
        "concept = loader.load(repository, concept_name)"
    )

test.write_text(text)

print("✓ test_kernel.py updated")

print()
print("ADR-005 refactoring completed successfully.")
print("Backup files (*.bak) created.")
