
from fastapi import APIRouter, BackgroundTasks
from app.services.upsc_scraper import UPSCScraper
from app.services.pyq_scraper import PYQScraper
from app.services.vector_service import VectorService

router = APIRouter()

@router.post("/scrape/notifications")
async def scrape_notifications(background_tasks: BackgroundTasks):
    """Scrape latest UPSC notifications"""
    
    scraper = UPSCScraper()
    notifications = await scraper.fetch_exam_notifications()
    
    return {
        "status": "success",
        "notifications_found": len(notifications),
        "data": notifications
    }


@router.post("/scrape/calendar")
async def scrape_exam_calendar():
    """Scrape UPSC exam calendar"""
    
    scraper = UPSCScraper()
    calendar = await scraper.fetch_exam_calendar()
    
    return {
        "status": "success",
        "exams_found": len(calendar),
        "calendar": calendar
    }


@router.post("/scrape/pyq/{year}")
async def scrape_pyq_for_year(year: int, background_tasks: BackgroundTasks):
    """Scrape PYQ for a specific year"""
    
    scraper = PYQScraper()
    questions = await scraper.scrape_pyq_from_vision(year)
    
    # Store in vector database in background
    async def store_in_vector_db():
        vector_service = VectorService()
        
        texts = [q["question_text"] for q in questions]
        metadata = [
            {
                "year": q["year"],
                "paper": q.get("paper", "Unknown"),
                "type": "pyq",
                "source": q.get("source", "")
            }
            for q in questions
        ]
        
        await vector_service.add_documents(texts, metadata)
    
    background_tasks.add_task(store_in_vector_db)
    
    return {
        "status": "success",
        "year": year,
        "questions_scraped": len(questions),
        "message": "Questions are being stored in vector database"
    }
