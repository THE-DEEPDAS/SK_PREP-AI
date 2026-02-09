import asyncio
from typing import List, Dict
import json
import re

from openai import OpenAI

from app.config import settings


class LLMService:

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        print(">>> ACTIVE LLM PROVIDER:", self.provider)

        self.local_llm = None
        self._openrouter_client = None
        self._openai_client = None

        if self.provider == "local":
            self._load_local_model()
        elif self.provider == "openrouter":
            self._openrouter_client = self._build_openrouter_client()
        elif self.provider == "openai":
            self._openai_client = self._build_openai_client()

    # ================= LOAD LOCAL MODEL =================

    def _load_local_model(self):
        print("Loading local GGUF model...")

        from llama_cpp import Llama

        self.local_llm = Llama(
            model_path=settings.LOCAL_MODEL_PATH,
            n_ctx=4096,
            n_threads=8,
            verbose=False,
        )

        print("✓ Local model loaded")

    # ================= PUBLIC CHAT API =================

    async def generate_response(
        self,
        query: str,
        context: List[Dict],
        max_tokens: int = 900,
    ) -> str:

        prompt = self._build_prompt(query, context)

        # Guard against incorrect parameter usage
        if isinstance(max_tokens, bool):
            max_tokens = 900

        return await asyncio.to_thread(
            self._generate_sync,
            prompt,
            max_tokens
        )

    # ================= CORE ROUTER =================

    def _generate_sync(self, prompt: str, max_tokens: int):

        if self.provider == "openrouter":
            return self._openrouter_generate(prompt, max_tokens)

        if self.provider == "openai":
            return self._openai_generate(prompt, max_tokens)

        if self.provider == "local":
            return self._local_generate(prompt, max_tokens)

        raise ValueError(f"Invalid LLM provider: {self.provider}")

    # ================= PROMPT BUILDER =================

    def _build_prompt(self, query: str, context: List[Dict]) -> str:

        context_text = "\n\n".join(c.get("text", "") for c in context)

        return f"""
You are an expert UPSC examiner.

Return ONLY valid JSON.
Do not include explanations outside JSON.

Context:
{context_text}

Task:
{query}
"""

    # ================= OPENROUTER =================

    def _build_openrouter_client(self) -> OpenAI:

        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set")

        return OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )

    def _openrouter_generate(self, prompt: str, max_tokens: int) -> str:

        client = self._openrouter_client or self._build_openrouter_client()

        res = client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )

        return res.choices[0].message.content.strip()

    # ================= LOCAL GGUF =================

    def _local_generate(self, prompt: str, max_tokens: int) -> str:

        output = self.local_llm(
            f"<s>[INST] {prompt} [/INST]",
            max_tokens=max_tokens,
            temperature=0.6,
            stop=["</s>"],
        )

        return output["choices"][0]["text"].strip()

    # ================= OPENAI =================

    def _build_openai_client(self) -> OpenAI:

        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        return OpenAI(api_key=settings.OPENAI_API_KEY)

    def _openai_generate(self, prompt: str, max_tokens: int) -> str:

        client = self._openai_client or self._build_openai_client()

        res = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )

        return res.choices[0].message.content.strip()

    # ====================================================
    # ================= JSON REPAIR ======================
    # ====================================================

    def _extract_json_block(self, text: str):

        match = re.search(r"\{[\s\S]*\}", text)

        if match:
            return match.group(0)

        cleaned = text.strip()

        if "question" in cleaned or "answer" in cleaned:

            if not cleaned.startswith("{"):
                cleaned = "{" + cleaned

            if not cleaned.endswith("}"):
                cleaned = cleaned + "}"

            return cleaned

        return None


    def _sanitize_json_text(self, text: str):

        # Fix smart quotes
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("’", "'")

        # Fix broken words like women"s → women's
        text = re.sub(r'(\w)"(\w)', r"\1'\2", text)

        return text


    # ====================================================
    # ================= FALLBACK =========================
    # ====================================================

    def _fallback(self, question_type):

        if question_type == "mcq":
            return {
                "question": "Question generation failed. Please retry.",
                "options": ["Retry A", "Retry B", "Retry C", "Retry D"],
                "answer": "A",
                "explanation": "Invalid model output"
            }

        return {
            "question": "Question generation failed. Please retry."
        }


    # ====================================================
    # ================ MOCK QUESTION ENGINE ===============
    # ====================================================

    async def generate_mock_question(
        self,
        topic: str,
        difficulty: str,
        question_type: str,
        current_affairs: List[Dict] = None
    ):

        difficulty_map = {
            "easy": "Basic conceptual",
            "medium": "UPSC analytical standard",
            "hard": "Tricky multi-dimensional"
        }

        difficulty_rule = difficulty_map.get(difficulty, "UPSC standard")

        # ================= PROMPTS =================

        if question_type == "mcq":

            prompt = f"""
Create ONE UPSC Prelims MCQ.

Topic: {topic}
Difficulty: {difficulty}
Rule: {difficulty_rule}

STRICT JSON:

{{
 "question": "Question text",
 "options": ["Option A","Option B","Option C","Option D"],
 "answer": "A",
 "explanation": "Short explanation"
}}

Rules:
Start with {{ and end with }}
No markdown
No extra text
"""

        else:

            prompt = f"""
Create ONE UPSC Mains descriptive question.

Topic: {topic}
Difficulty: {difficulty}

STRICT JSON:

{{
 "question": "Descriptive question"
}}

Rules:
Start with {{ and end with }}
No explanation
No answer
"""

        # ================= MODEL CALL + RETRY =================

        attempts = 3
        data = None

        for _ in range(attempts):

            raw = await self.generate_response(prompt, current_affairs or [])

            print("RAW MODEL OUTPUT:\n", raw)

            json_text = self._extract_json_block(raw)

            if not json_text:
                print("❌ JSON BLOCK NOT FOUND")
                continue

            json_text = self._sanitize_json_text(json_text)

            json_text = re.sub(r",\s*}", "}", json_text)
            json_text = re.sub(r",\s*]", "]", json_text)

            try:
                data = json.loads(json_text)
                break

            except Exception as e:
                print("❌ JSON PARSE FAILED:", e)
                print(json_text)

        if not data:
            return self._fallback(question_type)

        # ================= VALIDATION =================

        if question_type == "mcq":

            options = data.get("options")

            if not options or len(options) != 4:
                return self._fallback(question_type)

            return {
                "question": data.get("question", ""),
                "options": options,
                "answer": data.get("answer", "A"),
                "explanation": data.get("explanation", "")
            }

        else:

            return {
                "question": data.get("question", "Invalid question")
            }
