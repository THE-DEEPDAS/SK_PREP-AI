from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
import random

router = APIRouter()

class ProgressStats(BaseModel):
    topics_covered: int
    tests_attempted: int
    average_score: float
    study_hours: float
    weak_areas: List[str]
    strong_areas: List[str]

class DailyProgress(BaseModel):
    date: str
    hours_studied: float
    questions_solved: int
    accuracy: float

@router.get("/progress/{user_id}", response_model=ProgressStats)
async def get_progress(user_id: str):
    """Get user progress statistics"""
    # Fetch from PostgreSQL
    return ProgressStats(
        topics_covered=45,
        tests_attempted=12,
        average_score=68.5,
        study_hours=120.5,
        weak_areas=["Modern History", "Economy - GDP"],
        strong_areas=["Ancient History", "Geography"]
    )

@router.get("/daily/{user_id}")
async def get_daily_progress(user_id: str, days: int = 30):
    """Get daily progress for charts"""
    progress = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d")
        progress.append(DailyProgress(
            date=date,
            hours_studied=random.uniform(2, 8),
            questions_solved=random.randint(10, 50),
            accuracy=random.uniform(60, 90)
        ))
    return progress
