from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv(dotenv_path="app/.env")






# Routers
from app.routers import (
    chat, pdf, mock, analytics, news, scheduler,
    notifications, syllabus, pyq, scraper_api, interview
)
from app.routers import current_affairs



# Services
from app.services.scheduler_service import SchedulerService
from app.services.vector_service import VectorService

# FastAPI instance
app = FastAPI(title="UPSC AI Chatbot")
print(">>> current_affairs router REGISTERED")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(pyq.router, prefix="/api/pyq", tags=["pyq"])
app.include_router(scraper_api.router, prefix="/api/scraper", tags=["scraper"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["pdf"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(interview.router, prefix="/api/mock/interview", tags=["interview"])
app.include_router(current_affairs.router, prefix="/api", tags=["current_affairs"])


print("✅ current_affairs router registered")

# Services
scheduler_service = None
vector_service = VectorService()

@app.on_event("startup")
async def startup():
    global scheduler_service
    await vector_service.initialize()
    scheduler_service = SchedulerService()
    await scheduler_service.start()
    print("✓ All services started")

@app.on_event("shutdown")
async def shutdown():
    if scheduler_service and scheduler_service.scheduler:
        scheduler_service.scheduler.shutdown()
    print("✓ Services stopped")

@app.get("/")
async def root():
    return {"message": "UPSC AI Chatbot API", "version": "1.0.0"}
@app.get("/test")
def test():
    return {"ok": True}

