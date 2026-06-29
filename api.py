#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import sqlite3
import subprocess
import time

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

