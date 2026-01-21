from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.llm_service import LLMService
from app.services.pyq_service import get_filtered_pyqs
from app.services.current_affairs_service import filter_current_affairs
import random
from app.services.pyq_service import clean_text




router = APIRouter()


# ---------------- REQUEST MODELS ----------------

class MockTestRequest(BaseModel):
    exam_type: str                 # prelims / mains
    paper_type: str                # prelims / gs1 / gs2 etc
    num_questions: int = 10
    difficulty: str = "medium"     # easy / medium / hard
    question_source: str = "mock"  # mock / pyq / mixed
    include_current_affairs: bool = False


class SubmitRequest(BaseModel):
    answers: Dict[str, str] 
    

# question_id -> selected option


# ---------------- RESPONSE MODELS ----------------

class Question(BaseModel):
    id: str
    question: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    marks: int
    topic: str
    difficulty: str


class MockTestResponse(BaseModel):
    test_id: str
    questions: List[Question]
    duration_minutes: int


# ==========================================================
# ================= MOCK TEST GENERATOR ====================
# ==========================================================

@router.post("/generate", response_model=MockTestResponse)
async def generate_mock_test(request: MockTestRequest):

    try:
        llm_service = LLMService()
        questions = []

        exam_type = request.exam_type.lower()
        paper_type = request.paper_type.lower()

        difficulty = request.difficulty.lower()

        print("MOCK REQUEST RECEIVED:", request)

        # ---------------- CURRENT AFFAIRS ----------------

        current_context = []
        if request.include_current_affairs:
            news = filter_current_affairs(
                exam_type=request.exam_type,
                paper_type=request.paper_type,
                limit=10
            )
            current_context = [{"text": n} for n in news]

        # ---------------- PYQ MODE ----------------

        if request.question_source == "pyq":

            pyq_questions = get_filtered_pyqs(
                exam_type=request.exam_type,
                paper_type=request.paper_type,
                limit=request.num_questions
            )

            for q in pyq_questions:

                is_prelims = "prelim" in exam_type



                questions.append({
                    "id": f"pyq_{q['question_number']}",
                    "question": clean_text(q["question_text"]),
                    "options": [clean_text(opt) for opt in q.get("options", [])] if is_prelims else None,
                    "correct_answer": q.get("answer") if is_prelims else None,
                    "explanation": "Previous Year Question",
                    "marks": 2 if is_prelims else 10,
                    "topic": paper_type,
                    "difficulty": "medium"
                })


        # ---------------- MOCK MODE ----------------

        elif request.question_source == "mock":

            for _ in range(request.num_questions):

                is_prelims = "prelim" in exam_type


                q = await llm_service.generate_mock_question(
                    topic=paper_type,
                    difficulty=difficulty,
                    question_type="mcq" if is_prelims else "descriptive",
                    current_affairs=current_context
                )
                if is_prelims and not q.get("options"):
                    continue
                questions.append({
                    "id": f"mock_{random.randint(10000,99999)}",
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["answer"],
                    "explanation": q.get("explanation", ""),
                    "marks": 2,
                    "topic": paper_type,
                    "difficulty": difficulty
                })
                
                

                # MAINS
            else:

                questions.append({
                    "id": f"mock_{random.randint(10000,99999)}",
                    "question": q["question"],
                    "options": None,
                    "correct_answer": None,
                    "explanation": None,
                    "marks": 10,
                    "topic": paper_type,
                    "difficulty": difficulty
                })

        # ---------------- MIXED MODE ----------------

        else:

            pyq_count = request.num_questions // 2
            mock_count = request.num_questions - pyq_count

            is_prelims = "prelim" in exam_type


            pyqs = get_filtered_pyqs(
                request.exam_type,
                request.paper_type,
                pyq_count
            )

            # PYQ QUESTIONS
            for q in pyqs:

                questions.append({
                    "id": f"pyq_{q['question_number']}",
                    "question": clean_text(q["question"]),
                    "options": [clean_text(opt) for opt in q.get("options", [])] if is_prelims else None,
                    "correct_answer": q.get("answer") if is_prelims else None,
                    "explanation": "Previous Year Question",
                    "marks": 2 if is_prelims else 10,
                    "topic": paper_type,
                    "difficulty": "medium"
                })

            # MOCK QUESTIONS
            for _ in range(mock_count):

                q = await llm_service.generate_mock_question(
                    topic=paper_type,
                    difficulty=difficulty,
                    question_type="mcq" if is_prelims else "descriptive",
                    current_affairs=current_context
                )

                if is_prelims:

                    questions.append({
                        "id": f"mock_{random.randint(10000,99999)}",
                        "question": q["question"],
                        "options": q["options"],
                        "correct_answer": q["answer"],
                        "explanation": q.get("explanation", ""),
                        "marks": 2,
                        "topic": paper_type,
                        "difficulty": difficulty
                    })

                else:

                    questions.append({
                        "id": f"mock_{random.randint(10000,99999)}",
                        "question": q["question"],
                        "options": None,
                        "correct_answer": None,
                        "explanation": None,
                        "marks": 10,
                        "topic": paper_type,
                        "difficulty": difficulty
                    })

        # ---------------- RESPONSE ----------------

        return MockTestResponse(
            test_id=f"test_{random.randint(1000,9999)}",
            questions=questions,
            duration_minutes=request.num_questions * (2 if exam_type == "prelims" else 10)
        )

    except Exception as e:
        print("MOCK ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# ================= TEST SUBMISSION API ====================
# ==========================================================
print("SUBMIT API HIT")

@router.post("/submit/{test_id}")
async def submit_mock_test(
    test_id: str,
    payload: SubmitRequest,
    
):

    try:

        results = []
        score = 0
        total = len(payload.answers)

        for qid, user_ans in payload.answers.items():

            is_correct = random.choice([True, False])

            if is_correct:
                score += 1

            results.append({
                "question_id": qid,
                "user_answer": user_ans,
                "correct": is_correct
            })

        # ---------- UPDATE DASHBOARD STATS ----------


        return {
            "test_id": test_id,
            "score": score,
            "total": total,
            "details": results
        }

    except Exception as e:
        print("SUBMIT ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
