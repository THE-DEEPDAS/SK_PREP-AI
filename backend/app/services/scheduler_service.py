
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from typing import List, Dict
import asyncio

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.exam_calendar = self._load_exam_calendar()
        
    def _load_exam_calendar(self) -> List[Dict]:
        """Load UPSC exam calendar"""
        return [
            {
                "name": "UPSC Prelims 2025",
                "date": datetime(2025, 5, 26),
                "type": "prelims",
                "notify_before": [180, 90, 60, 30, 15, 7, 3, 1]  # days
            },
            {
                "name": "UPSC Mains 2025",
                "date": datetime(2025, 9, 15),
                "type": "mains",
                "notify_before": [180, 90, 60, 30, 15, 7, 3, 1]
            },
            {
                "name": "UPSC Interview 2025",
                "date": datetime(2026, 2, 1),
                "type": "interview",
                "notify_before": [90, 60, 30, 15, 7, 3, 1]
            }
        ]
    
    async def start(self):
        """Start the scheduler"""
        # Daily notifications check
        self.scheduler.add_job(
            self.send_daily_quote,
            'cron',
            hour=7,
            minute=0
        )
        
        # Weekly progress summary
        self.scheduler.add_job(
            self.send_weekly_summary,
            'cron',
            day_of_week='sun',
            hour=20,
            minute=0
        )
        
        # Exam notifications
        self.scheduler.add_job(
            self.check_exam_notifications,
            'interval',
            hours=24
        )
        
        # Current affairs update
        self.scheduler.add_job(
            self.fetch_daily_news,
            'cron',
            hour=9,
            minute=0
        )
        
        self.scheduler.start()
        print("✓ Scheduler started")
    
    async def send_daily_quote(self):
        """Send motivational quote every morning"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal. - Winston Churchill",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
        ]
        
        import random
        quote = random.choice(quotes)
        
        # Store in database or send notification
        await self._send_notification(
            title="Daily Motivation",
            message=quote,
            priority="low"
        )
    
    async def send_weekly_summary(self):
        """Send weekly progress summary"""
        # Fetch user progress from database
        summary = {
            "hours_studied": 45.5,
            "questions_solved": 250,
            "tests_completed": 3,
            "accuracy": 82.5
        }
        
        message = f"""
        📊 Weekly Summary:
        - Study Hours: {summary['hours_studied']}
        - Questions Solved: {summary['questions_solved']}
        - Tests Completed: {summary['tests_completed']}
        - Accuracy: {summary['accuracy']}%
        
        Keep up the great work! 💪
        """
        
        await self._send_notification(
            title="Weekly Progress Report",
            message=message,
            priority="medium"
        )
    
    async def check_exam_notifications(self):
        """Check for upcoming exams and send notifications"""
        today = datetime.now().date()
        
        for exam in self.exam_calendar:
            exam_date = exam["date"].date()
            days_until_exam = (exam_date - today).days
            
            if days_until_exam in exam["notify_before"]:
                message = self._generate_exam_message(exam, days_until_exam)
                
                await self._send_notification(
                    title=f"Exam Alert: {exam['name']}",
                    message=message,
                    priority="high" if days_until_exam <= 30 else "medium"
                )
    
    def _generate_exam_message(self, exam: Dict, days_left: int) -> str:
        """Generate exam notification message"""
        if days_left == 1:
            return f"🚨 {exam['name']} is TOMORROW! Final revision time!"
        elif days_left <= 7:
            return f"⏰ {exam['name']} is in {days_left} days. Time to intensify preparation!"
        elif days_left <= 30:
            return f"📅 {exam['name']} is in {days_left} days. Focus on weak areas."
        elif days_left <= 90:
            return f"📚 {exam['name']} is in {days_left} days. Start comprehensive revision."
        else:
            return f"📖 {exam['name']} is in {days_left} days. Begin your preparation."
    
    async def fetch_daily_news(self):
        """Fetch and process daily current affairs"""
        from app.services.news_scraper import NewsScraper
        
        scraper = NewsScraper()
        articles = await scraper.fetch_daily_news()
        
        # Store in vector database for chat context
        from app.services.vector_service import VectorService
        vector_service = VectorService()
        
        for article in articles:
            await vector_service.add_documents(
                texts=[article["title"]],
                metadata=[{
                    "source": article["source"],
                    "date": article["date"],
                    "category": "current_affairs",
                    "type": "news"
                }]
            )
        
        await self._send_notification(
            title="Current Affairs Updated",
            message=f"📰 {len(articles)} new articles added to your knowledge base",
            priority="low"
        )
    
    async def _send_notification(self, title: str, message: str, priority: str):
        """Send notification to user"""
        notification = {
            "id": f"notif_{datetime.now().timestamp()}",
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        # Store in Redis or PostgreSQL
        # For now, just log
        print(f"📬 Notification: {title} - {message[:50]}...")


# ============================================
# File: app/routers/notifications.py
# ============================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
            # Echo back or process
            await websocket.send_json({
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
