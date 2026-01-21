
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.vector_service import VectorService
import tempfile
from pydantic import BaseModel

import os

router = APIRouter()

class PDFUploadResponse(BaseModel):
    filename: str
    chunks_processed: int
    status: str

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF"""
    try:
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Process PDF
        processor = PDFProcessor()
        chunks = await processor.process_pdf(tmp_path, file.filename)
        
        # Store in vector DB
        vector_service = VectorService()
        count = await vector_service.add_documents(
            texts=[c["text"] for c in chunks],
            metadata=[c["metadata"] for c in chunks]
        )
        
        # Cleanup
        os.unlink(tmp_path)
        
        return PDFUploadResponse(
            filename=file.filename,
            chunks_processed=count,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove/{filename}")
async def remove_pdf(filename: str):
    """Remove PDF from vector store"""
    try:
        vector_service = VectorService()
        await vector_service.delete_by_source(filename)
        return {"status": "deleted", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
