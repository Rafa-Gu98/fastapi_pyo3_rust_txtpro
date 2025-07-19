"""
Basic Usage Example
Demonstrates how to call each endpoint of the API
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_basic_usage():
    """Basic functionality test"""
    
    # Sample text
    sample_text = """
    Welcome to our company! We provide excellent service.
    Contact us at: info@company.com or support@company.com
    Our team works hard to deliver quality results.
    Visit our website for more information.
    """
    
    # 1. Word frequency statistics
    print("=== Word Frequency Statistics ===")
    response = requests.post(f"{API_BASE}/count-words", 
                           json={"text": sample_text, "operation": "count_words"})
    if response.status_code == 200:
        data = response.json()
        print(f"Total words: {data['total_words']}")
        print(f"Unique words: {data['unique_words']}")
        print(f"Processing time: {data['processing_time_ms']}ms")
        print(f"Top words: {dict(list(data['word_count'].items())[:5])}")
    
    # 2. Email extraction
    print("\n=== Email Extraction ===")
    response = requests.post(f"{API_BASE}/extract-emails",
                           json={"text": sample_text, "operation": "extract_emails"})
    if response.status_code == 200:
        data = response.json()
        print(f"Found emails: {data['emails']}")
        print(f"Email count: {data['email_count']}")
    
    # 3. Text sanitization
    print("\n=== Text Sanitization ===")
    dirty_text = "Hello@#$%^&*() World!!! This is a test???"
    response = requests.post(f"{API_BASE}/clean-text",
                           json={"text": dirty_text, "operation": "clean_text"})
    if response.status_code == 200:
        data = response.json()
        print(f"Original text: {dirty_text}")
        print(f"Sanitized text: {data['cleaned_text']}")
        print(f"Length change: {data['original_length']} -> {data['cleaned_length']}")

if __name__ == "__main__":
    test_basic_usage()