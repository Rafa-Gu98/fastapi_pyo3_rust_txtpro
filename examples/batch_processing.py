"""
Batch Processing Example
Demonstrates how to process multiple files or large datasets
"""
import requests
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

API_BASE = "http://localhost:8000"

async def process_text_async(session, text, operation):
    """Asynchronously process a single text"""
    endpoint_map = {
        "count_words": "/count-words",
        "extract_emails": "/extract-emails", 
        "clean_text": "/clean-text"
    }
    
    url = f"{API_BASE}{endpoint_map[operation]}"
    payload = {"text": text, "operation": operation}
    
    async with session.post(url, json=payload) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"error": f"HTTP {response.status}"}

async def batch_process_async(texts, operation="count_words"):
    """Asynchronously batch process multiple texts"""
    async with aiohttp.ClientSession() as session:
        tasks = [process_text_async(session, text, operation) for text in texts]
        results = await asyncio.gather(*tasks)
        return results

def batch_process_sync(texts, operation="count_words"):
    """Synchronous batch processing (for comparison)"""
    endpoint_map = {
        "count_words": "/count-words",
        "extract_emails": "/extract-emails",
        "clean_text": "/clean-text"
    }
    
    url = f"{API_BASE}{endpoint_map[operation]}"
    results = []
    
    for text in texts:
        response = requests.post(url, json={"text": text, "operation": operation})
        if response.status_code == 200:
            results.append(response.json())
        else:
            results.append({"error": f"HTTP {response.status_code}"})
    
    return results

def demo_batch_processing():
    """Batch processing demonstration"""
    
    # Prepare test data
    sample_texts = [
        "Hello world! Contact: user1@example.com",
        "Python and Rust integration test. Email: dev@company.org", 
        "Performance testing with multiple emails: test@demo.com, info@sample.net",
        "Text processing benchmark. Reach us at: support@fastapi.com",
        "Final test document with contact: admin@textprocessor.io"
    ]
    
    print("=== Batch Processing Performance Comparison ===")
    
    # Synchronous processing
    print("\nSynchronous processing...")
    start_time = time.time()
    sync_results = batch_process_sync(sample_texts, "count_words")
    sync_time = time.time() - start_time
    print(f"Synchronous processing time: {sync_time:.2f}s")
    
    # Asynchronous processing
    print("\nAsynchronous processing...")
    start_time = time.time()
    async_results = asyncio.run(batch_process_async(sample_texts, "count_words"))
    async_time = time.time() - start_time
    print(f"Asynchronous processing time: {async_time:.2f}s")
    
    print(f"\nPerformance improvement: {sync_time/async_time:.2f}x")
    
    # Display result summary
    print("\n=== Processing Result Summary ===")
    total_words = sum(result.get('total_words', 0) for result in async_results)
    total_processing_time = sum(result.get('processing_time_ms', 0) for result in async_results)
    
    print(f"Total documents: {len(sample_texts)}")
    print(f"Total words: {total_words}")
    print(f"Total Rust processing time: {total_processing_time:.2f}ms")
    print(f"Average processing time per document: {total_processing_time/len(sample_texts):.2f}ms")

if __name__ == "__main__":
    demo_batch_processing()