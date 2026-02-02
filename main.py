"""
AI-Generated Voice Detection API
A simple FastAPI application for detecting AI-generated vs human voice
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="API for detecting AI-generated vs human voice",
    version="1.0.0"
)

# ============================================================================
# REQUEST MODEL (Pydantic for validation)
# ============================================================================

class VoiceRequest(BaseModel):
    """Request model for voice prediction"""
    language: str = Field(
        ..., 
        description="Language of the audio",
        min_length=1
    )
    audioFormat: str = Field(
        ..., 
        description="Format of the audio (mp3, wav, etc.)",
        min_length=1
    )
    audioBase64: str = Field(
        ..., 
        description="Base64 encoded audio data",
        min_length=1
    )


# ============================================================================
# RESPONSE MODEL
# ============================================================================

class VoiceResponse(BaseModel):
    """Response model for voice prediction"""
    status: Literal["success", "error"]
    prediction: Literal["human", "AI-generated"]
    confidence: float
    language: str
    note: str


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "AI Voice Detection API"
    }


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AI Voice Detection API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# ============================================================================
# MAIN PREDICTION ENDPOINT
# ============================================================================

@app.post("/predict", response_model=VoiceResponse)
async def predict_voice(data: VoiceRequest):
    """
    Predict whether audio is human or AI-generated.
    
    - **language**: Language of the audio
    - **audioFormat**: Format of the audio (mp3, wav, etc.)
    - **audioBase64**: Base64 encoded audio data (required)
    
    Returns prediction with confidence score.
    """
    
    # Validate audioBase64 is present and not empty
    if not data.audioBase64 or not data.audioBase64.strip():
        raise HTTPException(
            status_code=400,
            detail="audioBase64 is required and cannot be empty"
        )
    
    # Dummy ML logic - replace with real model later
    # For now, return a consistent dummy response based on input length
    is_ai_generated = len(data.audioBase64) % 2 == 0
    prediction_type = "AI-generated" if is_ai_generated else "human"
    confidence_score = 0.85 if is_ai_generated else 0.82
    
    return VoiceResponse(
        status="success",
        prediction=prediction_type,
        confidence=confidence_score,
        language=data.language,
        note="Endpoint validated successfully"
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "status": "error",
        "detail": exc.detail
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    return {
        "status": "error",
        "detail": "An unexpected error occurred"
    }



# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
