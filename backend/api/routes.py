from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
import shutil
import os
from services.data_processing import DataProcessor
from services.export_service import generate_pdf_summary
from agents.data_agent import analyze_dataframe, generate_executive_summary
from agents.db_agent import analyze_sql_database

router = APIRouter()

# DTOs
class QueryRequest(BaseModel):
    query: str
    file_path: str = None
    db_uri: str = None

class SummaryRequest(BaseModel):
    file_path: str

# Temp storage for uploads
UPLOAD_DIR = "/app/data/uploads" if os.environ.get("PYTHONUNBUFFERED") else "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handles CSV/Excel file uploads and returns the file path."""
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only CSV or Excel files allowed.")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"status": "success", "file_path": file_path, "filename": file.filename}

@router.post("/query")
async def query_data(req: QueryRequest):
    """Executes a Natural Language Query against a file or a DB URI."""
    try:
        if req.file_path:
            df = DataProcessor.process_file(req.file_path)
            result = analyze_dataframe(df, req.query)
            return {"query": req.query, "result": result}
            
        elif req.db_uri:
            result = analyze_sql_database(req.db_uri, req.query)
            return {"query": req.query, "result": result}
            
        else:
            raise HTTPException(status_code=400, detail="Must provide either file_path or db_uri")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def get_summary(req: SummaryRequest):
    """Generates an Autonomous Executive Summary and returns it, along with a PDF link."""
    try:
        df = DataProcessor.process_file(req.file_path)
        summary_text = generate_executive_summary(df)
        
        # Also generate PDF
        pdf_path = generate_pdf_summary(summary_text, filename=f"summary_{os.path.basename(req.file_path)}.pdf")
        
        return {
            "summary": summary_text,
            "pdf_path": pdf_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
