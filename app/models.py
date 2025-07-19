from pydantic import BaseModel
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