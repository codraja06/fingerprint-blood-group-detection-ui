from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import prediction, users, settings as settings_api

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for BloodID Application",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": app.version}

app.include_router(users.router)
app.include_router(settings_api.router)
app.include_router(prediction.router)
