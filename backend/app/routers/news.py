from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from app.services.news_scraper import NewsScraper
from typing import Optional

router = APIRouter()

class NewsArticle(BaseModel):
    id: str
    title: str
    summary: str
    category: str
    source: str
    date: str
    url: Optional[str] = None
    importance: str  # high, medium, low

@router.get("/daily", response_model=List[NewsArticle])
async def get_daily_news():
    """Get today's current affairs"""
    
    try:
        scraper = NewsScraper()
        articles = await scraper.fetch_daily_news()
        
        # Transform to NewsArticle format
        news_list = []
        for idx, article in enumerate(articles):
            news_list.append(NewsArticle(
                id=f"news_{idx}",
                title=article.get("title", ""),
                summary=article.get("summary", ""),
                category=article.get("category", "General"),
                source=article.get("source", ""),
                date=article.get("date", datetime.now().strftime("%Y-%m-%d")),
                url=article.get("url"),
                importance=article.get("importance", "medium")
            ))
        
        return news_list
        
    except Exception as e:
        # Return mock data if service fails
        return [
            NewsArticle(
                id="1",
                title="New Education Policy Updates",
                summary="Government announces major changes to NEP 2020 implementation",
                category="Policy",
                source="PIB",
                date=datetime.now().strftime("%Y-%m-%d"),
                importance="high"
            ),
            NewsArticle(
                id="2",
                title="India-China Border Developments",
                summary="Latest updates on LAC disengagement talks",
                category="International Relations",
                source="The Hindu",
                date=datetime.now().strftime("%Y-%m-%d"),
                importance="high"
            ),
            NewsArticle(
                id="3",
                title="Budget 2025 Highlights",
                summary="Key allocations and policy announcements",
                category="Economy",
                source="Economic Times",
                date=datetime.now().strftime("%Y-%m-%d"),
                importance="high"
            )
        ]

@router.get("/weekly", response_model=List[NewsArticle])
async def get_weekly_compilation():
    """Get this week's important current affairs compilation"""
    
    # This would fetch and compile weekly important news
    # For now, return placeholder
    return await get_daily_news()

@router.get("/quiz")
async def get_current_affairs_quiz():
    """Generate quiz from recent current affairs"""
    
    return {
        "quiz_id": "ca_quiz_001",
        "questions": [
            {
                "question": "Which country recently hosted the G20 summit?",
                "options": ["India", "Brazil", "Japan", "Germany"],
                "correct": 0,
                "explanation": "India hosted G20 summit in 2023"
            }
        ]
    }
