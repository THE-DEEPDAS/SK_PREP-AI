from fastapi import APIRouter, UploadFile, File
import fitz
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/evaluate/essay")
async def evaluate_essay(file: UploadFile = File(...)):

    pdf = fitz.open(stream=await file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    llm = LLMService()

    prompt = f"""
You are a senior UPSC Essay paper examiner.

Evaluate the essay STRICTLY as per UPSC Essay Paper standards.

Evaluation Criteria (Follow ALL):

1. Introduction Quality
- Hook (quote/data/anecdote usage)
- Context setting
- Clear thesis statement

2. Structure & Organization
- Logical flow of ideas
- Clear paragraph transitions
- Balanced coverage of dimensions
- Proper conclusion with way forward

3. Content Depth
- Multi-dimensional analysis (social, political, economic, ethical, historical)
- Conceptual clarity
- Factual accuracy

4. Examples & Case Studies
- Use of relevant examples
- Contemporary relevance
- Data/committee reports if used

5. Coherence & Flow
- Smooth continuity
- No abrupt topic jumps
- Argument linkage

6. Language & Expression
- Grammar and vocabulary
- Clarity of expression
- Academic tone
- Avoidance of informal language

7. Relevance to Topic
- Stays within essay theme
- No deviation
- No repetition

8. Critical Thinking
- Balanced viewpoints
- Analytical depth
- Original insights (if present)

9. Presentation (Simulated)
- Use of headings/subheadings
- Logical structuring
- Readability

Marking Rules:
- Maximum marks: 250
- Deduct marks for vague content, repetition, poor structure
- Do NOT be lenient
- Simulate real UPSC examiner strictness

Essay Content:
{text}

Return STRICT JSON ONLY:

{{
 "score": "marks out of 250",
 "introduction_feedback": "",
 "structure_feedback": "",
 "content_feedback": "",
 "language_feedback": "",
 "strengths": [
   "point1",
   "point2"
 ],
 "improvements": [
   "point1",
   "point2"
 ],
 "overall_verdict": "Excellent / Good / Average / Poor",
 "rank_category_prediction": "Top 100 / Top 500 / Interview Level / Needs Improvement"
}}

Rules:
- Do NOT add explanations outside JSON
- Do NOT add markdown
- Keep feedback concise and exam-focused
"""


    result = await llm.generate_response(prompt, [])

    return result
