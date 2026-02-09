import asyncio
import sys
sys.path.append('..')

from app.services.pdf_processor import PDFProcessor
from app.services.vector_service import VectorService
from pathlib import Path

async def process_and_load():
    print("Processing real UPSC data...")
    print("="*60)
    
    vector_service = VectorService()
    await vector_service.initialize()
    
    pdf_processor = PDFProcessor()
    
    # Process all NCERT PDFs
    ncert_dir = Path("data/pdfs/ncert")
    
    if not ncert_dir.exists():
        print("✗ NCERT directory not found!")
        print(f"  Create: {ncert_dir}")
        return
    
    total_chunks = 0
    
    for pdf_file in ncert_dir.glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")
        
        try:
            # Extract and chunk
            chunks = await pdf_processor.process_pdf(
                str(pdf_file), 
                pdf_file.name
            )
            
            # Prepare for vector DB
            texts = [c['text'] for c in chunks]
            metadata = [c['metadata'] for c in chunks]
            
            # Add to vector database
            count = await vector_service.add_documents(texts, metadata)
            
            print(f"  ✓ Added {count} chunks")
            total_chunks += count
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*60)
    print(f"✓ Successfully processed {total_chunks} chunks!")
    print("✓ Your chatbot now has REAL UPSC study material!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(process_and_load())