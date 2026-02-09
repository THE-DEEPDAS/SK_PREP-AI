
import asyncio
import sys
sys.path.append('..')

from app.services.vector_service import VectorService
from pathlib import Path
import json

class RealDataLoader:
    """Load all real data into vector database"""
    
    def __init__(self):
        self.vector_service = VectorService()
    
    async def load_syllabus(self):
        """Load official syllabus"""
        
        print("Loading syllabus into vector DB...")
        
        syllabus_file = Path("data/official/syllabus_structured.json")
        
        if syllabus_file.exists():
            data = json.loads(syllabus_file.read_text())
            
            texts = []
            metadata = []
            
            for paper_code, paper_data in data['papers'].items():
                text = f"{paper_code}: {paper_data['name']}"
                
                texts.append(text)
                metadata.append({
                    'type': 'syllabus',
                    'paper': paper_code,
                    'source': 'UPSC Official'
                })
            
            count = await self.vector_service.add_documents(texts, metadata)
            print(f"✓ Loaded {count} syllabus items")
        else:
            print("✗ Syllabus file not found")
    
  
        
        
        from app.services.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        
        total = 0
        
        for pdf_file in pdf_dir.glob("*.pdf"):
            print(f"  Processing: {pdf_file.name}")
            
            chunks = await processor.process_pdf(str(pdf_file), pdf_file.name)
            
            texts = [c['text'] for c in chunks]
            metadata = [c['metadata'] for c in chunks]
            
            count = await self.vector_service.add_documents(texts, metadata)
            total += count
            print(f"    ✓ Added {count} chunks")
        
        print(f"✓ Total: {total} chunks from NCERT books")
    
    async def load_pyq(self):
        """Load PYQ questions"""
        
        print("Loading PYQ...")
        
        pyq_dir = Path("data/pyq")
        
        # Load extracted questions
        for json_file in pyq_dir.glob("*.json"):
            data = json.loads(json_file.read_text())
            
            texts = [q['question'] for q in data]
            metadata = [{
                'type': 'pyq',
                'year': q.get('year'),
                'paper': q.get('paper'),
                'source': 'UPSC Official'
            } for q in data]
            
            count = await self.vector_service.add_documents(texts, metadata)
            print(f"✓ Loaded {count} PYQ from {json_file.name}")
    
    async def load_current_affairs(self):
        """Load current affairs"""
        
        print("Loading current affairs...")
        
        affairs_dir = Path("data/current_affairs")
        
        for json_file in affairs_dir.glob("*.json"):
            data = json.loads(json_file.read_text())
            
            texts = [item['title'] for item in data]
            metadata = [{
                'type': 'current_affairs',
                'date': item.get('date'),
                'source': item.get('source'),
                'url': item.get('url')
            } for item in data]
            
            count = await self.vector_service.add_documents(texts, metadata)
            print(f"✓ Loaded {count} articles from {json_file.name}")
    
    async def load_all(self):
        """Load everything"""
        
        print("="* 60)
        print("LOADING ALL REAL DATA INTO VECTOR DATABASE")
        print("=" * 60)
        
        await self.vector_service.initialize()
        
       
        await self.load_pyq()
        await self.load_current_affairs()
        
        print("=" * 60)
        print("✓ ALL DATA LOADED SUCCESSFULLY!")
        print("=" * 60)
