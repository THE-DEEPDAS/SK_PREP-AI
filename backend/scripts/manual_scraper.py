
import asyncio
from app.services.automated_scraper import AutomatedScraperService
from app.services.multi_source_scraper import MultiSourcePYQScraper

async def manual_scrape_all():
    """Manually trigger all scrapers"""
    
    scraper = AutomatedScraperService()
    
    print("🔍 Starting manual scrape...")
    print("\n1. Scraping UPSC notifications...")
    notifications = await scraper.scrape_upsc_notifications()
    print(f"   Found {len(notifications)} notifications")
    
    print("\n2. Scraping exam calendar...")
    calendar = await scraper.scrape_exam_calendar()
    print(f"   Found {len(calendar)} calendar entries")
    
    print("\n3. Scraping PYQ...")
    pyqs = await scraper.scrape_all_pyq()
    print(f"   Found {len(pyqs)} PYQ questions")
    
    print("\n4. Scraping results...")
    results = await scraper.scrape_results()
    print(f"   Found {len(results)} results")
    
    print("\n✅ Manual scrape completed!")

async def scrape_pyq_specific_year(year: int):
    """Scrape PYQ for a specific year from all sources"""
    
    scraper = MultiSourcePYQScraper()
    
    print(f"🔍 Scraping PYQ for year {year} from all sources...")
    questions = await scraper.scrape_all_sources(year)
    
    print(f"\n✅ Found {len(questions)} unique questions")
    
    # Save to file
    import json
    with open(f"pyq_{year}.json", "w") as f:
        json.dump(questions, f, indent=2)
    
    print(f"💾 Saved to pyq_{year}.json")

if __name__ == "__main__":
    # Run manual scrape
    asyncio.run(manual_scrape_all())
    