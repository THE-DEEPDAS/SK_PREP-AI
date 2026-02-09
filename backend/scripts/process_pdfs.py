import asyncio
import sys
sys.path.append('..')
from app.services.pdf_processor import PDFProcessor
from app.services.vector_service import VectorService
from pathlib import Path

async def process():
    vs = VectorService()
    await vs.initialize()
    pp = PDFProcessor()
    
    for pdf in Path("data/pdfs/ncert").glob("*.pdf"):
        print(f"Processing {pdf.name}...")
        chunks = await pp.process_pdf(str(pdf), pdf.name)
        texts = [c['text'] for c in chunks]
        metadata = [c['metadata'] for c in chunks]
        count = await vs.add_documents(texts, metadata)
        print(f"✓ Added {count} chunks")

asyncio.run(process())