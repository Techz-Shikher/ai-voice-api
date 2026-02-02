"""
AI-Generated Voice Detection Endpoint Tester
A FastAPI application for testing voice detection predictions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from contextlib import asynccontextmanager
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="API for detecting AI-generated vs human voice",
    version="1.0.0"
)


# ============================================================================
# LIFESPAN CONTEXT MANAGER (Startup and Shutdown events)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    # Startup
    print("🚀 AI Voice Detection API is starting...")
    yield
    # Shutdown
    print("🛑 AI Voice Detection API is shutting down...")


# Reinitialize app with lifespan
app = FastAPI(
    title="AI Voice Detection API",
    description="API for detecting AI-generated vs human voice",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================================
# REQUEST & RESPONSE MODELS (Pydantic for validation)
# ============================================================================

class PredictionRequest(BaseModel):
    """Request model for voice detection prediction"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Please analyze this voice sample",
                "audio_url": "https://example.com/sample.mp3"
            }
        }
    )
    
    message: str = Field(
        ..., 
        description="Description or context about the audio",
        min_length=1,
        max_length=500
    )
    audio_url: str = Field(
        ..., 
        description="Public URL to the MP3 audio file",
        min_length=5
    )


class PredictionResponse(BaseModel):
    """Response model for voice detection prediction"""
    status: Literal["success", "error"] = Field(
        ..., 
        description="Status of the prediction"
    )
    prediction: Literal["human", "AI-generated"] = Field(
        ..., 
        description="Whether the voice is human or AI-generated"
    )
    confidence: float = Field(
        ..., 
        description="Confidence score between 0 and 1",
        ge=0.0,
        le=1.0
    )
    language: str = Field(
        ..., 
        description="Detected language of the audio"
    )
    note: str = Field(
        ..., 
        description="Additional information or explanation"
    )


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns a simple status message.
    """
    return {
        "status": "healthy",
        "service": "AI Voice Detection API"
    }


# ============================================================================
# MAIN PREDICTION ENDPOINT
# ============================================================================

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict whether audio is human or AI-generated.
    
    - **message**: Description or context about the audio
    - **audio_url**: Public URL to the MP3 audio file (required)
    
    Returns prediction with confidence score and metadata.
    """
    
    # Validate audio_url is present (Pydantic handles this, but explicit check for clarity)
    if not request.audio_url or not request.audio_url.strip():
        raise HTTPException(
            status_code=400,
            detail="audio_url is required and cannot be empty"
        )
    
    # Validate URL format (basic check)
    if not request.audio_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="audio_url must be a valid HTTP/HTTPS URL"
        )
    
    # ========================================================================
    # DUMMY ML LOGIC (Replace with real ML model later)
    # ========================================================================
    # For now, we return a dummy response based on audio_url characteristics
    # In production, this would involve:
    # 1. Downloading the audio from audio_url
    # 2. Preprocessing the audio
    # 3. Running through a trained ML model
    # 4. Returning actual predictions
    
    # Dummy logic: check URL length for demo purposes
    is_ai_generated = len(request.audio_url) % 2 == 0
    prediction_type = "AI-generated" if is_ai_generated else "human"
    confidence_score = 0.75 if is_ai_generated else 0.82
    
    # Create response
    response = PredictionResponse(
        status="success",
        prediction=prediction_type,
        confidence=confidence_score,
        language="English",
        note="This is a dummy prediction. Real ML model not yet implemented."
    )
    
    return response


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Generic exception handler for unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "An unexpected error occurred"
        }
    )




# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API documentation link"""
    return {
        "message": "Welcome to AI Voice Detection API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    # Run with uvicorn
    # Host 0.0.0.0 makes it accessible from outside (needed for Render)
    # Port defaults to 8000, but can be overridden by PORT environment variable
    import os
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Set to True only for development
    )
