from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class TextInput(BaseModel):
    text: str
    operation: str  # "count_words", "extract_emails", "clean_text"

class WordCountResponse(BaseModel):
    word_count: Dict[str, int]
    total_words: int
    unique_words: int

class EmailResponse(BaseModel):
    emails: List[str]
    email_count: int

class CleanTextResponse(BaseModel):
    cleaned_text: str
    original_length: int
    cleaned_length: int

class SentimentInput(BaseModel):
    text: str = Field(..., description="Text to analyze for sentiment", max_length=10000)

class SentimentResponse(BaseModel):
    score: float = Field(..., description="Sentiment score between -1.0 and 1.0")
    label: str = Field(..., description="Sentiment label: positive, negative, or neutral")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    word_count: int = Field(..., description="Number of words processed")
    positive_words: List[str] = Field(..., description="Identified positive words")
    negative_words: List[str] = Field(..., description="Identified negative words")
    language: str = Field(..., description="Detected language: en, zh, or mixed")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")