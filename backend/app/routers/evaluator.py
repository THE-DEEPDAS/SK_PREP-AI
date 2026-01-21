
# ============================================
# BACKEND: Mains Answer Evaluator API
# File: backend/app/routers/answer_evaluator.py
# ============================================

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
import base64
from app.services.keyword_services import extract_keywords, keyword_score


router = APIRouter()

class AnswerEvaluation(BaseModel):
    overall_score: float  # Out of 10
    content_score: float
    structure_score: float
    language_score: float
    keyword_coverage: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    model_answer: str
    detailed_feedback: str

class EvaluateRequest(BaseModel):
    question: Optional[str] = None
    answer_text: Optional[str] = None
    difficulty: str = "hard"  # easy or hard

@router.post("/evaluate-text", response_model=AnswerEvaluation)
async def evaluate_text_answer(request: EvaluateRequest):
    """Evaluate text answer"""
    
    try:
        # Use OpenAI or Mistral to evaluate
        prompt = f"""You are a UPSC Mains answer evaluator. Evaluate this answer critically.

Question: {request.question or 'General Mains Answer'}

Student's Answer:
{request.answer_text}

Evaluation Criteria:
1. Content Quality (0-10): Depth, accuracy, relevance
2. Structure (0-10): Introduction, body, conclusion
3. Language (0-10): Grammar, clarity, expression
4. Keyword Coverage (0-10): Important terms and concepts

Provide evaluation in this JSON format:
{{
    "overall_score": float (0-10),
    "content_score": float (0-10),
    "structure_score": float (0-10),
    "language_score": float (0-10),
    "keyword_coverage": float (0-10),
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
    "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
    "model_answer": "An ideal answer would be...",
    "detailed_feedback": "Detailed paragraph explaining the evaluation"
}}

Be {'very strict and critical' if request.difficulty == 'hard' else 'moderate and encouraging'} in your evaluation.
"""

        # Call LLM (using OpenAI or Ollama)
        if os.getenv("USE_OPENAI", "false").lower() == "true":
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            result_text = response.choices[0].message.content
        else:
            # Use Ollama/Mistral
            import requests
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "upsc-mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            result_text = ollama_response.json().get('response', '')
        
        # Parse JSON response
        import json
        import re
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            evaluation = json.loads(json_match.group())
            return AnswerEvaluation(**evaluation)
        else:
            # Fallback evaluation
            return AnswerEvaluation(
                overall_score=7.0,
                content_score=7.0,
                structure_score=7.0,
                language_score=7.0,
                keyword_coverage=6.5,
                strengths=["Good attempt", "Clear writing"],
                weaknesses=["Could be more detailed"],
                suggestions=["Add more examples", "Improve conclusion"],
                model_answer="An ideal answer would cover...",
                detailed_feedback="Your answer shows understanding but needs improvement in depth."
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate-image", response_model=AnswerEvaluation)
async def evaluate_image_answer(
    answer_images: List[UploadFile] = File(...),
    question: Optional[str] = Form(None),
    difficulty: str = Form("hard")
):
    """Evaluate answer from uploaded images (OCR + Evaluation)"""
    
    try:
        # Step 1: OCR to extract text from images
        from PIL import Image
        import pytesseract
        import io
        
        extracted_text = ""
        
        for image_file in answer_images:
            # Read image
            image_data = await image_file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # OCR
            text = pytesseract.image_to_string(image, lang='eng')
            extracted_text += text + "\n\n"
        
        # Step 2: Evaluate the extracted text
        request = EvaluateRequest(
            question=question,
            answer_text=extracted_text,
            difficulty=difficulty
        )
        
        return await evaluate_text_answer(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

@router.post("/compare-answers")
async def compare_multiple_answers(
    answers: List[str],
    question: str
):
    """Compare multiple answers to the same question"""
    
    evaluations = []
    
    for idx, answer in enumerate(answers):
        request = EvaluateRequest(
            question=question,
            answer_text=answer,
            difficulty="hard"
        )
        evaluation = await evaluate_text_answer(request)
        evaluations.append({
            "answer_number": idx + 1,
            "evaluation": evaluation
        })
    
    # Rank by score
    evaluations.sort(key=lambda x: x["evaluation"].overall_score, reverse=True)
     keywords = extract_keywords(req.question)
    
    coverage = keyword_score(req.user_answer, keywords)
    
    return {
        "total_answers": len(answers),
        "evaluations": evaluations,
        "best_answer": evaluations[0] if evaluations else None
    }
   
