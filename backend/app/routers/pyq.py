from fastapi import APIRouter, Query
from pathlib import Path
import json
from typing import Optional

router = APIRouter()

@router.get("/questions")
async def get_pyq_questions(
    year: Optional[int] = None,
    paper: Optional[str] = None,
    exam_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 50
):
    """Get PYQ questions from processed data"""
    
    # Load processed questions
    pyq_file = Path("data/pyq/processed_pyq.json")
    
    if not pyq_file.exists():
        return {"error": "PYQ data not processed yet. Run process_pyq_folders.py"}
    
    questions = json.loads(pyq_file.read_text())
    
    # Apply filters
    if year:
        questions = [q for q in questions if q['year'] == year]
    if paper:
        questions = [q for q in questions if paper.lower() in q['paper_type'].lower()]
    if exam_type:
        questions = [q for q in questions if q['exam_type'] == exam_type.lower()]
    if difficulty:
        questions = [q for q in questions if q['difficulty'].lower() == difficulty.lower()]
    
    # Limit results
    return questions[:limit]

@router.get("/statistics")
async def get_pyq_statistics():
    """Get PYQ statistics"""
    
    stats_file = Path("data/pyq/pyq_statistics.json")
    
    if stats_file.exists():
        return json.loads(stats_file.read_text())
    else:
        return {"error": "Statistics not available"}