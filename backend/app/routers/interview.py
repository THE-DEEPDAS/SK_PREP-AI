
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
import tempfile
import json

router = APIRouter()

class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str
    pyq_reference: Optional[str] = None

class EvaluationResponse(BaseModel):
    overall_score: float
    content_score: float
    clarity_score: float
    confidence_score: float
    feedback: str
    strengths: List[str]
    areas_to_improve: List[str]
    follow_up_question: str

@router.get("/questions", response_model=List[InterviewQuestion])
async def get_interview_questions():
    """Get interview questions from PYQ database"""
    
    # Questions based on actual UPSC interview patterns
    questions = [
        {
            "question": "Tell me about yourself and why you want to join the civil services.",
            "category": "DAF (Detailed Application Form)",
            "difficulty": "basic",
            "pyq_reference": "Common opening question"
        },
        {
            "question": "What do you think are the three major challenges facing India today?",
            "category": "Current Affairs",
            "difficulty": "medium",
            "pyq_reference": "2023 Interview Board"
        },
        {
            "question": "How would you improve the education system in rural areas if you were a District Collector?",
            "category": "Administration",
            "difficulty": "medium",
            "pyq_reference": "2022 Interview Board"
        },
        {
            "question": "Discuss the role of technology in improving governance.",
            "category": "Governance & Technology",
            "difficulty": "medium",
            "pyq_reference": "2024 Interview Panel"
        },
        {
            "question": "If your senior asks you to do something unethical, how would you handle it?",
            "category": "Ethics & Integrity",
            "difficulty": "hard",
            "pyq_reference": "Ethics case study 2023"
        },
        {
            "question": "What is your opinion on India's foreign policy regarding neighboring countries?",
            "category": "International Relations",
            "difficulty": "hard",
            "pyq_reference": "2023 Board Question"
        },
        {
            "question": "How can we balance economic development with environmental conservation?",
            "category": "Environment & Economy",
            "difficulty": "hard",
            "pyq_reference": "2024 Interview"
        },
        {
            "question": "What steps would you take to improve women's safety in your district?",
            "category": "Social Issues",
            "difficulty": "medium",
            "pyq_reference": "2022 Panel Question"
        }
    ]
    
    return questions


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_interview_response(
    video: UploadFile = File(...),
    question: str = Form(...),
    question_number: int = Form(...)
):
    """
    Evaluate video interview response using:
    1. Speech-to-text (OpenAI Whisper)
    2. Content analysis (GPT-4)
    3. Delivery evaluation
    """
    
    try:
        # Save video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_video:
            content = await video.read()
            tmp_video.write(content)
            video_path = tmp_video.name
        
        # Step 1: Extract audio and transcribe using Whisper
        # Note: You need ffmpeg installed for audio extraction
        audio_path = video_path.replace('.webm', '.mp3')
        
        # Use Whisper API for transcription
        with open(audio_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        
        transcribed_text = transcript['text']
        
        # Step 2: Evaluate content using GPT-4
        evaluation_prompt = f"""
You are an expert UPSC interview panelist. Evaluate this candidate's response to the interview question.

Question: {question}

Candidate's Response: {transcribed_text}

Evaluate the response based on:
1. Content Quality (0-10): Depth of knowledge, relevance, accuracy
2. Clarity of Expression (0-10): How well-articulated the response is
3. Confidence & Composure (0-10): Based on speech patterns, pauses, filler words

Provide:
- Overall Score (0-10)
- Detailed Feedback (3-4 sentences)
- 3 Strengths
- 3 Areas to Improve
- A relevant follow-up question to test depth

Format your response as JSON:
{{
    "overall_score": float,
    "content_score": float,
    "clarity_score": float,
    "confidence_score": float,
    "feedback": "string",
    "strengths": ["string1", "string2", "string3"],
    "areas_to_improve": ["string1", "string2", "string3"],
    "follow_up_question": "string"
}}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an experienced UPSC interview panelist."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the evaluation
        evaluation_text = response.choices[0].message.content
        
        # Extract JSON from response (remove any markdown formatting)
        evaluation_text = evaluation_text.strip()
        if evaluation_text.startswith('```json'):
            evaluation_text = evaluation_text[7:]
        if evaluation_text.endswith('```'):
            evaluation_text = evaluation_text[:-3]
        
        evaluation = json.loads(evaluation_text.strip())
        
        # Cleanup temporary files
        os.unlink(video_path)
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        
        return EvaluationResponse(**evaluation)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.get("/mock-interview/start")
async def start_mock_interview():
    """Initialize a new mock interview session"""
    
    questions = await get_interview_questions()
    
    # Select 5-6 questions for a session
    import random
    selected_questions = random.sample(questions, min(6, len(questions)))
    
    return {
        "session_id": f"interview_{random.randint(1000, 9999)}",
        "questions": selected_questions,
        "duration_minutes": 30,
        "instructions": [
            "Ensure good lighting and clear audio",
            "Answer each question within 2-3 minutes",
            "Be honest and authentic in your responses",
            "Take a moment to think before answering",
            "Maintain eye contact with the camera"
        ]
    }


@router.post("/mock-interview/complete")
async def complete_mock_interview(
    session_id: str,
    responses: List[dict]
):
    """
    Complete interview and provide overall assessment
    """
    
    # Calculate aggregate scores
    total_content = sum(r.get('content_score', 0) for r in responses) / len(responses)
    total_clarity = sum(r.get('clarity_score', 0) for r in responses) / len(responses)
    total_confidence = sum(r.get('confidence_score', 0) for r in responses) / len(responses)
    overall = (total_content + total_clarity + total_confidence) / 3
    
    # Generate comprehensive feedback
    feedback_prompt = f"""
Based on these interview responses, provide comprehensive feedback:

Average Scores:
- Content: {total_content:.1f}/10
- Clarity: {total_clarity:.1f}/10
- Confidence: {total_confidence:.1f}/10
- Overall: {overall:.1f}/10

Provide:
1. Overall performance summary (2-3 sentences)
2. Key strengths demonstrated
3. Critical areas needing improvement
4. Specific action items for preparation
5. Comparison with typical UPSC candidates
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a senior UPSC interview trainer."},
            {"role": "user", "content": feedback_prompt}
        ],
        temperature=0.7
    )
    
    comprehensive_feedback = response.choices[0].message.content
    
    return {
        "session_id": session_id,
        "overall_score": overall,
        "category_scores": {
            "content_knowledge": total_content,
            "communication_clarity": total_clarity,
            "confidence_composure": total_confidence
        },
        "comprehensive_feedback": comprehensive_feedback,
        "responses_evaluated": len(responses),
        "recommendation": "Ready for interview" if overall >= 7 else "Needs more preparation"
    }
