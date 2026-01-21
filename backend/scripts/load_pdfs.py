import asyncio
import os
from pathlib import Path
from app.services.pdf_processor import PDFProcessor
from app.services.vector_service import VectorService

async def load_all_pdfs(pdf_directory: str):
    """Load all PDFs from directory into vector store"""
    processor = PDFProcessor()
    vector_service = VectorService()
    
    pdf_files = list(Path(pdf_directory).glob("**/*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    total_chunks = 0
    for pdf_path in pdf_files:
        try:
            print(f"Processing: {pdf_path.name}")
            chunks = await processor.process_pdf(str(pdf_path), pdf_path.name)
            
            count = await vector_service.add_documents(
                texts=[c["text"] for c in chunks],
                metadata=[c["metadata"] for c in chunks]
            )
            
            total_chunks += count
            print(f"  ✓ Added {count} chunks")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\n✓ Total chunks loaded: {total_chunks}")
    
    stats = vector_service.get_stats()
    print(f"✓ Vector DB stats: {stats}")

if __name__ == "__main__":
    # Usage: python scripts/load_pdfs.py
    pdf_dir = "./data/pdfs"  # Put your PDFs here
    asyncio.run(load_all_pdfs(pdf_dir))