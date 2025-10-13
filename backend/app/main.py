from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .config import settings
from .database import engine, Base
from .routers import upload, parse, run, compose, download, analyze, tasks, assignments, basic_auth

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="LabMate AI API",
    description="Automated lab assignment processing platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.SCREENSHOT_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/screenshots", StaticFiles(directory=settings.SCREENSHOT_DIR), name="screenshots")
app.mount("/reports", StaticFiles(directory=settings.REPORT_DIR), name="reports")

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(parse.router, prefix="/api", tags=["parse"])
app.include_router(run.router, prefix="/api", tags=["run"])
app.include_router(compose.router, prefix="/api", tags=["compose"])
app.include_router(download.router, prefix="/api", tags=["download"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["assignments"])
app.include_router(basic_auth.router, prefix="/api/basic-auth", tags=["basic-auth"])


@app.get("/")
async def root():
    return {"message": "LabMate AI API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy", "service": "LabMate AI API", "version": "1.0.0"}

@app.get("/api/test-patterns")
async def test_patterns():
    """Test endpoint to verify question pattern matching"""
    import re
    from .services.composer_service import ComposerService
    
    composer = ComposerService()
    test_texts = [
        "1.Write a Python program to demonstrate the use of iterator and generator functions.",
        "2.Write a Python program to calculate sum of first 5 natural numbers using recursion.",
        "B. Questions/Programs:",
        "Question 1: Write a program",
        "Task 2: Demonstrate recursion"
    ]
    
    results = {}
    for text in test_texts:
        pattern_match = composer._find_question_pattern(text)
        results[text] = {
            "matched": pattern_match is not None,
            "task_number": pattern_match
        }
    
    return {"pattern_tests": results}
