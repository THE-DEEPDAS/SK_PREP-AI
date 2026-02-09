import asyncio
from scrape_daily_news import scrape_pib_news
import sys
sys.path.append('..')

from app.services.vector_service import VectorService

async def daily_update():
    """Run daily to update current affairs"""
    
    print("Running daily update...")
    
    # 1. Scrape today's news
    articles = scrape_pib_news()
    
    # 2. Add to vector database
    if articles:
        vector_service = VectorService()
        await vector_service.initialize()
        
        texts = [a['title'] for a in articles]
        metadata = [{
            'type': 'current_affairs',
            'date': a['date'],
            'source': a['source'],
            'url': a['url']
        } for a in articles]
        
        count = await vector_service.add_documents(texts, metadata)
        print(f"✓ Added {count} articles to knowledge base")
    
    print("✓ Daily update complete!")

if __name__ == "__main__":
    asyncio.run(daily_update())