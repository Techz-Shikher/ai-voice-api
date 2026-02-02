# AI Voice Detection API

A FastAPI application for detecting AI-generated vs human voice.

## Quick Start

### Local Development

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Access the API:**
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Test the Endpoint

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Please analyze this voice sample",
    "audio_url": "https://example.com/sample.mp3"
  }'
```

## API Endpoints

### POST /predict
Predict whether audio is human or AI-generated.

**Request:**
```json
{
  "message": "string (required)",
  "audio_url": "string (required, must be HTTP/HTTPS URL)"
}
```

**Response:**
```json
{
  "status": "success",
  "prediction": "human or AI-generated",
  "confidence": 0.85,
  "language": "English",
  "note": "Additional information"
}
```

### GET /health
Health check endpoint.

### GET /
Root endpoint with API info.

## Deployment on Render

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Create new Web Service
4. Set Runtime to Python 3.11
5. Set Start Command to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

## Project Structure

```
ai-voice-api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Technologies

- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.11+**

## Next Steps

Replace dummy ML logic in the `/predict` endpoint with:
1. Audio downloading from URL
2. Audio preprocessing
3. Real ML model inference
4. Actual predictions

## License

MIT
