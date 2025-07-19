"""
Performance Demonstration Script
Comparing processing performance under different text sizes
"""
import requests
import time
import matplotlib.pyplot as plt

API_BASE = "http://localhost:8000"

def generate_test_text(word_count):
    """Generate test text with specified word count"""
    words = ["hello", "world", "test", "performance", "benchmark", "speed"]
    emails = ["user@example.com", "test@demo.org", "info@company.com"]
    
    text_parts = []
    for i in range(word_count // 10):
        text_parts.extend(words)
        if i % 50 == 0:  # Add an email every 50 word groups
            text_parts.append(emails[i % len(emails)])
    
    return " ".join(text_parts)

def benchmark_api():
    """API performance benchmarking"""
    word_counts = [100, 500, 1000, 5000, 10000, 50000]
    processing_times = []
    
    print("Starting performance benchmark...")
    
    for count in word_counts:
        print(f"\nTesting {count} words...")
        test_text = generate_test_text(count)
        
        # Test word frequency statistics
        start_time = time.time()
        response = requests.post(f"{API_BASE}/count-words",
                               json={"text": test_text, "operation": "count_words"})
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            rust_time = data['processing_time_ms']
            print(f"  Total time: {total_time*1000:.2f}ms")
            print(f"  Rust processing: {rust_time:.2f}ms")
            print(f"  Network + serialization: {(total_time*1000 - rust_time):.2f}ms")
            processing_times.append(rust_time)
        else:
            print(f"  Error: {response.status_code}")
            processing_times.append(0)
    
    # Plot performance chart
    plt.figure(figsize=(10, 6))
    plt.plot(word_counts, processing_times, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Word Count')
    plt.ylabel('Processing Time (ms)')
    plt.title('Rust Extension Performance Test')
    plt.grid(True, alpha=0.3)
    plt.savefig('performance_benchmark.png', dpi=300, bbox_inches='tight')
    print(f"\nPerformance chart saved as 'performance_benchmark.png'")

if __name__ == "__main__":
    benchmark_api()