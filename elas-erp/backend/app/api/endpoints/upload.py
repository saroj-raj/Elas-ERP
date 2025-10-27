import os, uuid, shutil, json
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import duckdb
import numpy as np
from datetime import datetime
from pathlib import Path
from backend.app.services.dashboard_generator import generate_quick_viz

router = APIRouter()

UPLOAD_DIR = "app/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Log file in PROJECT ROOT
ROOT_DIR = Path(__file__).parent.parent.parent.parent  # Go up to project root
GROQ_LOG_FILE = ROOT_DIR / "GROQ_DEBUG.log"


def log_upload_info(message: str):
    """Write upload info to Groq debug log file in project root"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(GROQ_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    domain: str = Form(...),
    intent: str = Form(...),
):
    log_upload_info("\n" + "="*80)
    log_upload_info("📤 NEW UPLOAD REQUEST")
    log_upload_info("="*80)
    log_upload_info(f"📁 File: {file.filename}")
    log_upload_info(f"🏢 Domain: {domain}")
    log_upload_info(f"🎯 Intent: {intent}")
    
    print("\n" + "="*80)
    print("📤 UPLOAD ENDPOINT CALLED")
    print("="*80)
    print(f"📁 File: {file.filename}")
    print(f"🏢 Domain: {domain}")
    print(f"🎯 Intent: {intent}")
    
    if not file.filename or not file.filename.lower().endswith((".csv",".tsv",".txt",".xlsx",".xls")):
        raise HTTPException(status_code=400, detail="Only CSV/TSV/XLSX supported in demo")

    fpath = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(fpath, "wb") as out:
        shutil.copyfileobj(file.file, out)
    
    log_upload_info(f"💾 Saved to: {fpath}")
    print(f"💾 Saved to: {fpath}")
    
    # Load and log preview of uploaded data
    try:
        con = duckdb.connect()
        preview_df = con.execute(f"SELECT * FROM read_csv_auto('{fpath}') LIMIT 5").fetch_df()
        log_upload_info(f"\n📊 UPLOADED FILE PREVIEW (first 5 rows):")
        log_upload_info("-"*80)
        log_upload_info(preview_df.to_string())
        log_upload_info("-"*80)
    except Exception as e:
        log_upload_info(f"⚠️ Could not preview file: {e}")

    # Generate widget proposals
    log_upload_info("\n🤖 Calling generate_quick_viz...")
    print("\n🤖 Calling generate_quick_viz...")
    widgets = generate_quick_viz(csv_path=fpath, domain=domain, intent=intent)
    log_upload_info(f"✅ Generated {len(widgets)} widgets")
    print(f"✅ Generated {len(widgets)} widgets")

    # Return a small preview sample so the client can render Vega-Lite immediately
    preview_rows: List[Dict[str, Any]] = []
    try:
        print("\n📊 Loading preview data with DuckDB...")
        con = duckdb.connect()
        # read_csv_auto also handles TSV/TXT
        df = con.execute(f"SELECT * FROM read_csv_auto('{fpath}') LIMIT 200").fetch_df()
        
        # Convert to JSON-serializable format (handle NaN, Timestamp, etc.)
        df = df.replace({np.nan: None})  # Replace NaN with None
        preview_rows = json.loads(df.to_json(orient="records", date_format="iso"))
        
        print(f"✅ Loaded {len(preview_rows)} preview rows")
        if preview_rows:
            print(f"📋 Columns: {list(preview_rows[0].keys())}")
    except Exception as e:
        # ignore preview failure; widgets can still be shown with empty data
        print(f"⚠️ Preview failed: {e}")
        import traceback
        traceback.print_exc()
        preview_rows = []

    response_data = {
        "dataset_id": os.path.basename(fpath),
        "widgets": widgets,
        "preview": preview_rows,
        "domain": domain,
        "intent": intent,
    }
    
    print("\n📦 Response summary:")
    print(f"   - Dataset ID: {response_data['dataset_id']}")
    print(f"   - Widgets: {len(response_data['widgets'])}")
    print(f"   - Preview rows: {len(response_data['preview'])}")
    print("="*80 + "\n")
    
    return JSONResponse(response_data)
