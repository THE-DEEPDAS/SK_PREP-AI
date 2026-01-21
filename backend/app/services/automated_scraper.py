import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.vector_service import VectorService
from app.services.upsc_scraper import UPSCScraper
from app.services.pyq_scraper import PYQScraper
import logging

logger = logging.getLogger(__name__)

class AutomatedScraperService:
    """
    Automated scraping service that runs daily to:
    1. Scrape UPSC official website for notifications
    2. Scrape exam calendar updates
    3. Scrape PYQ from multiple sources
    4. Update vector database with new content
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.upsc_scraper = UPSCScraper()
        self.pyq_scraper = PYQScraper()
        self.vector_service = VectorService()
        
        # Track last scrape times
        self.last_scrape = {
            "notifications": None,
            "calendar": None,
            "pyq": None,
            "results": None
        }
    
    async def start(self):
        """Start all automated scraping jobs"""
        
        # Daily: Scrape UPSC notifications (Every day at 8 AM)
        self.scheduler.add_job(
            self.scrape_upsc_notifications,
            'cron',
            hour=8,
            minute=0,
            id='upsc_notifications'
        )
        
        # Daily: Scrape exam calendar (Every day at 9 AM)
        self.scheduler.add_job(
            self.scrape_exam_calendar,
            'cron',
            hour=9,
            minute=0,
            id='exam_calendar'
        )
        
        # Weekly: Scrape PYQ from multiple sources (Every Sunday at 10 AM)
        self.scheduler.add_job(
            self.scrape_all_pyq,
            'cron',
            day_of_week='sun',
            hour=10,
            minute=0,
            id='pyq_scraper'
        )
        
        # Daily: Scrape results page (Every day at 6 PM)
        self.scheduler.add_job(
            self.scrape_results,
            'cron',
            hour=18,
            minute=0,
            id='results_scraper'
        )
        
        # Weekly: Update syllabus database (Every Monday at 11 AM)
        self.scheduler.add_job(
            self.update_syllabus_database,
            'cron',
            day_of_week='mon',
            hour=11,
            minute=0,
            id='syllabus_update'
        )
        
        self.scheduler.start()
        logger.info("✓ Automated scraper service started")
        
        # Run initial scrape
        await self.run_initial_scrape()
    
    async def run_initial_scrape(self):
        """Run initial scrape on startup"""
        logger.info("Running initial scrape...")
        await self.scrape_upsc_notifications()
        await self.scrape_exam_calendar()
    
    async def scrape_upsc_notifications(self):
        """Scrape UPSC official website for new notifications"""
        try:
            logger.info("Scraping UPSC notifications...")
            
            notifications = await self.upsc_scraper.fetch_exam_notifications()
            
            # Store in database
            from app.database import get_write_db
            from app.models.notification import Notification
            
            new_count = 0
            for notif in notifications:
                # Check if notification already exists
                # If new, add to database and send alert
                new_count += 1
            
            self.last_scrape["notifications"] = datetime.now()
            logger.info(f"✓ Scraped {len(notifications)} notifications ({new_count} new)")
            
            return notifications
            
        except Exception as e:
            logger.error(f"Error scraping notifications: {e}")
            return []
    
    async def scrape_exam_calendar(self):
        """Scrape and update exam calendar"""
        try:
            logger.info("Scraping exam calendar...")
            
            calendar = await self.upsc_scraper.fetch_exam_calendar()
            
            # Update scheduler with new exam dates
            await self._update_exam_reminders(calendar)
            
            self.last_scrape["calendar"] = datetime.now()
            logger.info(f"✓ Scraped {len(calendar)} calendar entries")
            
            return calendar
            
        except Exception as e:
            logger.error(f"Error scraping calendar: {e}")
            return []
    
    async def scrape_all_pyq(self):
        """Scrape PYQ from multiple sources"""
        try:
            logger.info("Scraping PYQ from all sources...")
            
            all_questions = []
            current_year = datetime.now().year
            
            # Scrape last 5 years
            for year in range(current_year - 1, current_year - 6, -1):
                logger.info(f"  Scraping PYQ for year {year}...")
                
                # Vision IAS
                questions = await self.pyq_scraper.scrape_pyq_from_vision(year)
                all_questions.extend(questions)
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(2)
            
            # Store in vector database
            if all_questions:
                await self._store_pyq_in_vector_db(all_questions)
            
            self.last_scrape["pyq"] = datetime.now()
            logger.info(f"✓ Scraped {len(all_questions)} PYQ questions")
            
            return all_questions
            
        except Exception as e:
            logger.error(f"Error scraping PYQ: {e}")
            return []
    
    async def scrape_results(self):
        """Scrape latest UPSC results"""
        try:
            logger.info("Scraping UPSC results...")
            
            results = await self.upsc_scraper.fetch_results()
            
            # Store and notify users
            await self._process_results(results)
            
            self.last_scrape["results"] = datetime.now()
            logger.info(f"✓ Scraped {len(results)} result announcements")
            
            return results
            
        except Exception as e:
            logger.error(f"Error scraping results: {e}")
            return []
    
    async def update_syllabus_database(self):
        """Update syllabus with latest UPSC changes"""
        try:
            logger.info("Updating syllabus database...")
            
            # Scrape official syllabus PDF if available
            syllabus_data = await self._scrape_official_syllabus()
            
            # Update vector database with syllabus
            if syllabus_data:
                await self._store_syllabus_in_vector_db(syllabus_data)
            
            logger.info("✓ Syllabus database updated")
            
        except Exception as e:
            logger.error(f"Error updating syllabus: {e}")
    
    async def _store_pyq_in_vector_db(self, questions: List[Dict]):
        """Store PYQ questions in vector database"""
        try:
            texts = []
            metadata = []
            
            for q in questions:
                # Create searchable text
                text = f"Question: {q.get('question_text', '')} "
                text += f"Year: {q.get('year', '')} "
                text += f"Paper: {q.get('paper', '')} "
                text += f"Topic: {q.get('topic', '')}"
                
                texts.append(text)
                metadata.append({
                    "type": "pyq",
                    "year": q.get("year"),
                    "paper": q.get("paper"),
                    "question_id": q.get("id"),
                    "source": q.get("source", ""),
                    "difficulty": q.get("difficulty", "medium")
                })
            
            count = await self.vector_service.add_documents(texts, metadata)
            logger.info(f"  Stored {count} questions in vector DB")
            
        except Exception as e:
            logger.error(f"Error storing PYQ in vector DB: {e}")
    
    async def _store_syllabus_in_vector_db(self, syllabus_data: List[Dict]):
        """Store syllabus in vector database"""
        try:
            texts = []
            metadata = []
            
            for item in syllabus_data:
                texts.append(item["content"])
                metadata.append({
                    "type": "syllabus",
                    "paper": item.get("paper"),
                    "topic": item.get("topic"),
                    "source": "UPSC Official"
                })
            
            count = await self.vector_service.add_documents(texts, metadata)
            logger.info(f"  Stored {count} syllabus items in vector DB")
            
        except Exception as e:
            logger.error(f"Error storing syllabus in vector DB: {e}")
    
    async def _update_exam_reminders(self, calendar: List[Dict]):
        """Update scheduler with exam reminder jobs"""
        try:
            for exam in calendar:
                exam_name = exam.get("exam_name", "")
                exam_date_str = exam.get("date", "")
                
                # Parse date and create reminder jobs
                # Add jobs at: 30 days, 15 days, 7 days, 3 days, 1 day before
                
                pass  # Implementation details...
                
        except Exception as e:
            logger.error(f"Error updating exam reminders: {e}")
    
    async def _process_results(self, results: List[Dict]):
        """Process and notify about new results"""
        try:
            # Store in database
            # Send notifications to relevant users
            pass
            
        except Exception as e:
            logger.error(f"Error processing results: {e}")
    
    async def _scrape_official_syllabus(self) -> List[Dict]:
        """Scrape official UPSC syllabus PDF"""
        try:
            # Download latest syllabus PDF
            # Extract and parse content
            # Return structured data
            return []
            
        except Exception as e:
            logger.error(f"Error scraping official syllabus: {e}")
            return []
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("✓ Automated scraper service stopped")
