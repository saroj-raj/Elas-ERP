"""
Simplified upload endpoint for testing - no AI dependencies
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
import pandas as pd

router = APIRouter()

# Create upload directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent
UPLOAD_DIR = ROOT_DIR / "app" / "tmp" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-simple")
async def upload_simple(
    file: UploadFile = File(...),
    domain: str = Form(...),
    intent: str = Form(...),
):
    """Simplified upload endpoint without AI"""
    print(f"\n📤 Simple Upload: {file.filename}")
    
    try:
        # Save file
        file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"✅ Saved to: {file_path}")
        
        # Try to read if CSV or XLSX
        widgets = []
        preview = []
        
        if file.filename.endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
                preview = df.head(10).to_dict('records')
                
                # Create simple widgets
                for col in df.columns[:3]:
                    widgets.append({
                        "type": "table",
                        "title": f"{col} Data",
                        "subtitle": f"Column: {col}"
                    })
                
                print(f"✅ Parsed CSV: {df.shape[0]} rows, {df.shape[1]} cols")
            except Exception as e:
                print(f"⚠️ CSV parse failed: {e}")
        
        elif file.filename.endswith(('.xlsx', '.xls')):
            try:
                # Try to read Excel file - requires openpyxl
                df = pd.read_excel(file_path)
                preview = df.head(10).to_dict('records')
                
                # Create simple widgets
                for col in df.columns[:3]:
                    widgets.append({
                        "type": "table",
                        "title": f"{col} Data",
                        "subtitle": f"Column: {col}"
                    })
                
                print(f"✅ Parsed Excel: {df.shape[0]} rows, {df.shape[1]} cols")
            except Exception as e:
                print(f"⚠️ Excel parse failed: {e}")
                # Still save the file, just don't create widgets
                pass
        
        return JSONResponse({
            "dataset_id": file.filename,
            "widgets": widgets,
            "preview": preview,
            "domain": domain,
            "intent": intent,
            "message": "Upload successful (simple mode)"
        })
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
