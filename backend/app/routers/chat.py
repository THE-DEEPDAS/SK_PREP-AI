from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
from app.config import settings


from app.services.llm_service import LLMService
from app.services.vector_service import VectorService

router = APIRouter()

vector_service = VectorService()
llm_service = LLMService()


class ChatRequest(BaseModel):
    message: str
    session_id: str
    use_gpt4: bool = False


class ChatResponse(BaseModel):
    response: str
    sources: List[dict]
    model_used: str

    class Config:
        # Allow field names that start with model_ to avoid warnings
        protected_namespaces = ()
@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    try:
        print("CHAT REQUEST RECEIVED")

        context = []   # vector disabled temporarily

        response = await llm_service.generate_response(
            request.message,
            context,
            request.use_gpt4
        )

        print("LLM RESPONSE GENERATED")

        return ChatResponse(
            response=response,
            sources=[],
            model_used="gpt-4" if request.use_gpt4 else "mistral-7b"
        )

    except Exception as e:
        print("CHAT ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


print("API KEY:", settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY)
print("PROVIDER:", settings.LLM_PROVIDER)
print("DEBUG CONFIG ----------------")
print("OPENROUTER_API_KEY =", settings.OPENROUTER_API_KEY)
print("OPENROUTER_MODEL =", getattr(settings, "OPENROUTER_MODEL", None))
print("LLM_PROVIDER =", settings.LLM_PROVIDER)
print("QDRANT_HOST =", settings.QDRANT_HOST)
print("REDIS_URL =", settings.REDIS_URL)
print("--------------------------------")
print("DEFAULT_MODEL =", getattr(settings, "DEFAULT_MODEL", None))
print("DATABASE_URL =", settings.DATABASE_URL)


