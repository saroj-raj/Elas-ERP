import os, uuid, shutil
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import duckdb
from backend.app.services.dashboard_generator import generate_quick_viz

router = APIRouter()

UPLOAD_DIR = "app/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    domain: str = Form(...),
    intent: str = Form(...),
):
    if not file.filename or not file.filename.lower().endswith((".csv",".tsv",".txt",".xlsx",".xls")):
        raise HTTPException(status_code=400, detail="Only CSV/TSV/XLSX supported in demo")

    fpath = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(fpath, "wb") as out:
        shutil.copyfileobj(file.file, out)

    # Generate widget proposals
    widgets = generate_quick_viz(csv_path=fpath, domain=domain, intent=intent)

    # Return a small preview sample so the client can render Vega-Lite immediately
    preview_rows: List[Dict[str, Any]] = []
    try:
        con = duckdb.connect()
        # read_csv_auto also handles TSV/TXT
        preview_rows = con.execute(
            f"SELECT * FROM read_csv_auto('{fpath}') LIMIT 200"
        ).fetch_df().to_dict(orient="records")
    except Exception:
        # ignore preview failure; widgets can still be shown with empty data
        preview_rows = []

    return JSONResponse({
        "dataset_id": os.path.basename(fpath),
        "widgets": widgets,
        "preview": preview_rows,
        "domain": domain,
        "intent": intent,
    })
