#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse, StreamingResponse
import sqlite3
import subprocess
import time
import csv
import io
import zipfile
from datetime import datetime, timezone

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

app = FastAPI(
    title="TACE",
    description="TACE-Aquinas Conceptual Ecosystem",
    version="0.1"
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


@app.get("/ontology/modules")
def ontology_modules():

    conn = sqlite3.connect("tace_knowledge.db")

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

    conn = sqlite3.connect("tace_knowledge.db")

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

    conn = sqlite3.connect("tace_knowledge.db")

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

    conn = sqlite3.connect("tace_knowledge.db")
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
    conn = sqlite3.connect("tace_knowledge.db")

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
