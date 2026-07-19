#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse, StreamingResponse
import sqlite3
from pathlib import Path
import subprocess
import time
import csv
import io
import zipfile
from datetime import datetime, timezone
from new_query_engine import QueryEngine
from new_universe_universe import Universe

from kernel.config import ONTOLOGY_DB
ALLOWED_CONCEPT_FIELDS = {
    "definition",
    "assumptions",
    "scope",
    "historical_development",
    "tace_transformation",
    "references_text",
}

class OntologyUpdateRequest(BaseModel):
    module: str
    concept: str
    field: str
    value: str


class OntologyExportRequest(BaseModel):
    module: str


class AskTACERequest(BaseModel):
    question: str
    assist: bool = False
    rendering_mode: str = "technical"


app = FastAPI(
    title="TACE",
    description="TACE-Aquinas Conceptual Ecosystem",
    version="0.1"
)

_ask_tace_query_engine = QueryEngine()
_ask_tace_universe = Universe()
_docs_root = Path("docs").resolve()

# Expose the trash directory. see also lin 4 from ... StaticFiles
app.mount(
    "/trash",
    StaticFiles(directory="trash"),
    name="trash",
)

@app.get("/")
def root():
    return {
        "application": "TACE-Aquinas Conceptual Ecosystem",
        "status": "running"
    }


@app.get("/ui")
def ui():
    return FileResponse("index.html")


@app.get("/ping")
def ping():
    return {
        "ping": "pong"
    }


@app.get("/about")
def about():
    return {
        "application": "TACE-Aquinas Conceptual Ecosystem",
        "backend": "FastAPI",
        "version": "0.1"
    }


@app.get("/resources/catalog")
def resources_catalog():
    return {
        "title": "Resources",
        "groups": [
            {
                "id": "constitutions",
                "name": "Constitutions",
                "items": [
                    {
                        "id": "philosophical_constitution",
                        "label": "Philosophical Constitution",
                        "viewer": "document",
                        "path": "constitution/TACE_PHILOSOPHICAL_CONSTITUTION.md",
                    },
                    {
                        "id": "semantic_constitution",
                        "label": "Semantic Constitution",
                        "viewer": "document",
                        "path": "constitution/TACE_SEMANTIC_CONSTITUTION.md",
                    },
                    {
                        "id": "software_constitution",
                        "label": "Software Constitution",
                        "viewer": "document",
                        "path": "constitution/TACE_SOFTWARE_CONSTITUTION.md",
                    },
                ],
            },
            {
                "id": "architecture",
                "name": "Architecture",
                "items": [
                    {
                        "id": "adr_ledger",
                        "label": "Architecture Decision Records",
                        "viewer": "adr_ledger",
                    },
                    {
                        "id": "roadmap",
                        "label": "Roadmap",
                        "viewer": "document",
                        "path": "architecture/ROADMAP.md",
                    },
                ],
            },
            {
                "id": "governance",
                "name": "Governance",
                "items": [
                    {
                        "id": "governance_document",
                        "label": "Governance Manual",
                        "viewer": "document",
                        "path": "governance/GOVERNANCE.md",
                    },
                    {
                        "id": "development_mode",
                        "label": "Development Mode",
                        "viewer": "document",
                        "path": "developer/DEVELOPMENT_MODE.md",
                    },
                ],
            },
            {
                "id": "ontology",
                "name": "Ontology",
                "items": [
                    {
                        "id": "ontology_browser",
                        "label": "Ontology Browser",
                        "viewer": "ontology_browser",
                    },
                    {
                        "id": "ontology_modules",
                        "label": "Ontology Modules",
                        "viewer": "ontology_browser",
                    },
                    {
                        "id": "ontology_concepts",
                        "label": "Concepts",
                        "viewer": "ontology_browser",
                    },
                    {
                        "id": "ontology_relations",
                        "label": "Relations",
                        "viewer": "document",
                        "path": "architecture/ADR_002_Resolved_Concept",
                    },
                    {
                        "id": "ontology_rules",
                        "label": "Rules",
                        "viewer": "note",
                        "message": "Not yet available.",
                    },
                ],
            },
            {
                "id": "documentation",
                "name": "Documentation",
                "items": [
                    {
                        "id": "documentation_index",
                        "label": "Documentation Index",
                        "viewer": "document",
                        "path": "INDEX.md",
                    },
                    {
                        "id": "book",
                        "label": "The Book",
                        "viewer": "note",
                        "message": "The Book folder is currently empty.",
                    },
                    {
                        "id": "developer_documentation",
                        "label": "Developer Documentation",
                        "viewer": "document",
                        "path": "developer/DEVELOPMENT_MODE.md",
                    },
                ],
            },
            {
                "id": "history",
                "name": "History",
                "items": [
                    {
                        "id": "session_footprints",
                        "label": "Session Footprints",
                        "viewer": "session_footprints",
                    },
                    {
                        "id": "repository_statistics",
                        "label": "Repository Statistics (optional)",
                        "viewer": "note",
                        "message": "",
                    },
                ],
            },
        ],
    }


def _safe_docs_path(relative_path: str) -> Path:
    candidate = (_docs_root / relative_path).resolve()
    if not str(candidate).startswith(str(_docs_root)):
        raise HTTPException(status_code=400, detail="Invalid documentation path")
    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="Documentation file not found")
    return candidate


def _document_title_for_path(relative_path: str) -> str:
    titles = {
        "INDEX.md": "Documentation Index",
        "constitution/TACE_PHILOSOPHICAL_CONSTITUTION.md": "Philosophical Constitution",
        "constitution/TACE_SEMANTIC_CONSTITUTION.md": "Semantic Constitution",
        "constitution/TACE_SOFTWARE_CONSTITUTION.md": "Software Constitution",
        "governance/GOVERNANCE.md": "Governance Manual",
        "developer/DEVELOPMENT_MODE.md": "Development Mode",
        "architecture/ROADMAP.md": "Roadmap",
    }

    return titles.get(relative_path, Path(relative_path).stem.replace("_", " ").title())


@app.get("/resources/document/{doc_path:path}")
def resources_document(doc_path: str):
    path = _safe_docs_path(doc_path)
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unsupported document encoding")

    return {
        "path": str(path.relative_to(_docs_root)),
        "title": _document_title_for_path(str(path.relative_to(_docs_root))),
        "content": content,
    }


@app.get("/resources/adr-ledger")
def resources_adr_ledger():
    items = []
    for path in sorted((_docs_root / "architecture").glob("ADR_*")):
        if path.is_file():
            stem = path.name.replace("ADR_", "ADR ", 1).replace("_", " ")
            items.append(
                {
                    "label": stem,
                    "path": f"architecture/{path.name}",
                }
            )

    return {"items": items}


@app.get("/resources/session-footprints")
def resources_session_footprints():
    items = []
    for path in sorted((_docs_root / "session_footprints").glob("*")):
        if path.is_file():
            label = path.stem.replace("SESSION_FOOTPRINT_", "Session Footprint ").replace("_", " ")
            items.append(
                {
                    "label": label,
                    "path": f"session_footprints/{path.name}",
                }
            )

    return {"items": items}







@app.get("/resources/folder/{folder}")
def resources_folder(folder: str):

    directory = _docs_root / folder

    if not directory.exists():
        return {"items": []}

    items = []

    for path in sorted(directory.glob("*")):
        if path.is_file():
            items.append({
                "label": path.stem.replace("_", " "),
                "path": f"{folder}/{path.name}"
            })

    return {"items": items}


@app.post("/run")
def run():

    p = subprocess.Popen(
        ["python", "pre_tace.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    time.sleep(1)

    output = p.stdout.read(400)

    p.kill()

    return {
        "stdout": output
    }


@app.post("/ask")
def ask_tace(payload: AskTACERequest):

    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    if payload.assist:
        question = f"assist: {question}"

    return _ask_tace_query_engine.ask(
        _ask_tace_universe,
        question,
        assist=payload.assist,
        rendering_mode=payload.rendering_mode,
    )


@app.get("/ontology/modules")
def ontology_modules():

    conn = sqlite3.connect(str(ONTOLOGY_DB))

    cur = conn.cursor()

    cur.execute("""
        SELECT module_name
        FROM ontology_modules
        ORDER BY module_name
    """)

    modules = [r[0] for r in cur.fetchall()]

    conn.close()

    return modules



@app.get("/ontology/module/{module}")
def ontology_module(module: str):

    conn = sqlite3.connect(str(ONTOLOGY_DB))

    cur = conn.cursor()

    cur.execute("""
        SELECT concept_name
        FROM concept_records
        WHERE ontology_module=?
        ORDER BY concept_name
    """, (module,))

    concepts = [r[0] for r in cur.fetchall()]

    conn.close()

    return concepts



@app.get("/ontology/concept/{module}/{concept}")
def ontology_concept(module: str, concept: str):

    conn = sqlite3.connect(str(ONTOLOGY_DB))

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM concept_records
        WHERE ontology_module=?
          AND concept_name=?
    """,(module,concept))

    row = cur.fetchone()

    conn.close()

    if row is None:
        return {}

    return dict(row)


@app.post("/ontology/update")
def ontology_update(payload: OntologyUpdateRequest):

    if payload.field not in ALLOWED_CONCEPT_FIELDS:
        raise HTTPException(status_code=400, detail="Field not allowed")

    conn = sqlite3.connect(str(ONTOLOGY_DB))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM concept_records WHERE ontology_module=? AND concept_name=?",
        (payload.module, payload.concept),
    )

    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Concept not found")

    cur.execute(
        f"UPDATE concept_records SET {payload.field}=? WHERE ontology_module=? AND concept_name=?",
        (payload.value, payload.module, payload.concept),
    )
    conn.commit()

    cur.execute(
        "SELECT * FROM concept_records WHERE ontology_module=? AND concept_name=?",
        (payload.module, payload.concept),
    )
    row = cur.fetchone()
    conn.close()

    return dict(row) if row else {}


EXPORT_TABLES = [
    {
        "table": "ontology_modules",
        "csv": "ontology_modules.csv",
        "filter_column": "module_name",
    },
    {
        "table": "concept_records",
        "csv": "concept_records.csv",
        "filter_column": "ontology_module",
    },
]


IMPORT_SH_PLACEHOLDER = """#!/usr/bin/env bash
set -euo pipefail

echo "Standalone importing is not yet available."
exit 1
"""


def _get_table_schema(conn, table_name):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type='table'
          AND name=?
        """,
        (table_name,),
    )
    row = cur.fetchone()
    if row is None or row[0] is None:
        raise HTTPException(
            status_code=500,
            detail=f"Missing schema for table: {table_name}",
        )

    sql = row[0].strip()
    if not sql.endswith(";"):
        sql += ";"
    return sql


def _table_csv_bytes(conn, table_name, filter_column, module_name):
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table_name} WHERE {filter_column}=?",
        (module_name,),
    )
    rows = cur.fetchall()
    headers = [col[0] for col in cur.description]

    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(headers)
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def _build_manifest(module_name, table_mappings):
    lines = [
        f"MODULE={module_name}",
        "MODULE_VERSION=1.0",
        "PACKAGE_VERSION=1.0",
        "AUTHOR=Pere Alemán",
        "",
    ]

    for mapping in table_mappings:
        lines.append(f"TABLE={mapping['table']}:{mapping['csv']}")

    return "\n".join(lines) + "\n"


def _build_readme(module_name, table_mappings):
    table_lines = "\n".join([
        f"- {mapping['csv']}" for mapping in table_mappings
    ])
    exported_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    return f"""# TACE Portable Ontology Module Package

Module name: {module_name}
Module version: 1.0
Package version: 1.0
Export date: {exported_at}

## Package purpose
This package transports one TACE ontology module in a portable format.

## Package contents
- manifest.tace
- schema.sql
{table_lines}
- README.md
- import.sh

## Supported database systems
- SQLite
- PostgreSQL
- MariaDB / MySQL

## General import procedure
1. Extract this .tace package with a ZIP tool.
2. Review manifest.tace for module and table mapping information.
3. Standalone import via import.sh is not yet available in this version.
4. Keep this package for a future official standalone importer release.
"""


def _build_tace_package(module_name):
    conn = sqlite3.connect(str(ONTOLOGY_DB))

    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM ontology_modules WHERE module_name=?",
        (module_name,),
    )
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Module not found")

    manifest_text = _build_manifest(module_name, EXPORT_TABLES)
    readme_text = _build_readme(module_name, EXPORT_TABLES)

    schema_parts = []
    csv_parts = []

    for mapping in EXPORT_TABLES:
        table_name = mapping["table"]
        csv_name = mapping["csv"]
        filter_column = mapping["filter_column"]

        schema_parts.append(_get_table_schema(conn, table_name))
        csv_parts.append((
            csv_name,
            _table_csv_bytes(conn, table_name, filter_column, module_name),
        ))

    conn.close()

    schema_sql = "\n\n".join(schema_parts) + "\n"

    package_bytes = io.BytesIO()
    with zipfile.ZipFile(
        package_bytes,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        zf.writestr("manifest.tace", manifest_text.encode("utf-8"))
        zf.writestr("schema.sql", schema_sql.encode("utf-8"))
        for csv_name, csv_bytes in csv_parts:
            zf.writestr(csv_name, csv_bytes)
        zf.writestr("README.md", readme_text.encode("utf-8"))
        zf.writestr("import.sh", IMPORT_SH_PLACEHOLDER.encode("utf-8"))

    package_bytes.seek(0)
    return package_bytes


@app.post("/ontology/export")
def ontology_export(payload: OntologyExportRequest):
    package_stream = _build_tace_package(payload.module)
    filename = f"{payload.module}.tace"

    return StreamingResponse(
        package_stream,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )