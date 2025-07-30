from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from .models import TextInput, WordCountResponse, EmailResponse, CleanTextResponse, SentimentInput, SentimentResponse
from .services import TextProcessorService, SentimentService
import logging
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Text Processor API",
    description="FastAPI application with Rust extensions for high-performance text processing",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

service = TextProcessorService()

@app.get("/")
async def root():
    return {
        "message": "Text Processor API with Rust Extensions",
        "endpoints": ["/count-words", "/extract-emails", "/clean-text"],
        "docs": "/docs"
    }

@app.post("/count-words", response_model=WordCountResponse)
async def count_words(input_data: TextInput):
    try:
        result = service.count_words(input_data.text)
        logger.info(f"Word count completed in {result['processing_time_ms']}ms")
        return WordCountResponse(**result)
    except Exception as e:
        logger.error(f"Error in count_words: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-emails", response_model=EmailResponse)
async def extract_emails(input_data: TextInput):
    try:
        result = service.extract_emails(input_data.text)
        logger.info(f"Email extraction completed in {result['processing_time_ms']}ms")
        return EmailResponse(**result)
    except Exception as e:
        logger.error(f"Error in extract_emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clean-text", response_model=CleanTextResponse)
async def clean_text(input_data: TextInput):
    try:
        result = service.clean_text(input_data.text)
        logger.info(f"Text cleaning completed in {result['processing_time_ms']}ms")
        return CleanTextResponse(**result)
    except Exception as e:
        logger.error(f"Error in clean_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "rust_extension": "loaded"}

@app.post(
    "/analyze-sentiment",
    response_model=SentimentResponse,
    summary="Analyze text sentiment",
    description="Analyze the sentiment of input text using high-performance Rust algorithms",
    tags=["Text Analysis"]
)
async def analyze_sentiment(input_data: SentimentInput):
    """
    Analyze sentiment of input text.
    
    Returns sentiment score, label, confidence, and identified emotional words.
    """
    try:
        result = SentimentService.analyze_sentiment(input_data.text)
        return SentimentResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )