from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import users, chat, analytics
from app.db import get_db

app = FastAPI(
    title="NCD Health Chatbot API",
    description="A chatbot for Non-Communicable Disease health information",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

import os

frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
