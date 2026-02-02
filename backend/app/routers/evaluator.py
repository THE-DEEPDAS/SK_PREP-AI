from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os, json, re, requests, io

from PIL import Image, ImageFile
import pytesseract
import fitz

router = APIRouter(
    prefix="/api/evaluator",
    tags=["evaluator"]
)


# ================= REQUEST MODEL =================

class EvaluateRequest(BaseModel):
    question: Optional[str]
    answer_text: str
    difficulty: str
    paper: str
    marks: int


# ================= RESPONSE MODELS =================

class SectionScores(BaseModel):
    introduction: float
    body: float
    conclusion: float
    presentation: float


class AnswerEvaluation(BaseModel):
    final_score: float
    section_scores: SectionScores
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    detailed_feedback: str


# ================= OCR =================

async def extract_text(file: UploadFile):

    data = await file.read()
    content_type = file.content_type or ""

    extracted_text = ""

    # -------- PDF --------

    if content_type == "application/pdf":

        try:
            pdf = fitz.open(stream=data, filetype="pdf")
        except:
            raise HTTPException(400, "Invalid PDF")

        for page in pdf:
            extracted_text += page.get_text()

    # -------- IMAGE --------

    elif content_type.startswith("image"):

        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True

            image = Image.open(io.BytesIO(data))
            image = image.convert("RGB")

            # Resize large scans
            if image.width > 2000:
                ratio = 2000 / image.width
                image = image.resize((2000, int(image.height * ratio)))

            image = image.convert("L")

            # Improve contrast
            image = image.point(lambda x: 0 if x < 140 else 255)

            extracted_text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

        except Exception as e:
            print("OCR ERROR:", e)
            extracted_text = ""

    else:
        raise HTTPException(400, "Unsupported file type")

    return extracted_text


# ================= CORE EVALUATOR =================

async def evaluate_text_answer(request: EvaluateRequest):

    strictness = "very strict" if request.difficulty == "hard" else "moderate"

    prompt = f"""
You are a UPSC Mains examiner.

Paper: {request.paper}
Maximum Marks: {request.marks}

Question:
{request.question}

Student Answer:
{request.answer_text}

Evaluate strictly like real UPSC checking.

Return STRICT JSON ONLY:

{{
"final_score": float,
"section_scores": {{
    "introduction": float,
    "body": float,
    "conclusion": float,
    "presentation": float
}},
"strengths": [],
"weaknesses": [],
"suggestions": [],
"detailed_feedback": ""
}}

Rules:
- Section total must sum to final_score
- final_score must be <= {request.marks}
- Be {strictness}
"""

    try:

        # -------- LLM --------

        if os.getenv("USE_OPENAI") == "true":

            import openai

            res = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            result_text = res.choices[0].message.content

        else:

            res = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            result_text = res.json().get("response", "")

        # -------- JSON SAFE PARSE --------

        match = re.search(r"\{.*\}", result_text, re.DOTALL)

        if not match:
            print("LLM RAW RESPONSE:", result_text)

            # fallback safe response
            return AnswerEvaluation(
                final_score=0,
                section_scores={
                    "introduction": 0,
                    "body": 0,
                    "conclusion": 0,
                    "presentation": 0
                },
                strengths=["Answer detected"],
                weaknesses=["AI could not parse evaluation"],
                suggestions=["Retry evaluation"],
                detailed_feedback="Evaluation parsing failed"
            )

        data = json.loads(match.group())

        # Safety clamp
        data["final_score"] = min(float(data["final_score"]), request.marks)

        return AnswerEvaluation(**data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================= MAIN API =================

@router.post("/evaluate-upload", response_model=AnswerEvaluation)
async def evaluate_upload(
    files: List[UploadFile] = File(...),
    question: Optional[str] = Form(None),
    difficulty: str = Form("hard"),
    paper: str = Form(...),
    marks: str = Form(...)  # <-- FIX: accept as string
):

    # SAFE CAST
    try:
        marks = int(marks)
    except:
        raise HTTPException(400, "Invalid marks value")

    full_text = ""

    for file in files:
        text = await extract_text(file)
        full_text += text + "\n"

    # OCR fallback (DO NOT FAIL)
    if not full_text.strip():
        full_text = "Handwritten answer detected. Partial OCR extraction."

    request = EvaluateRequest(
        question=question,
        answer_text=full_text,
        difficulty=difficulty,
        paper=paper,
        marks=marks
    )

    result = await evaluate_text_answer(request)

    return result
