import pytest
import time
import statistics
from app.services import TextProcessorService

class TestPerformanceComparison:
    """Performance comparison tests"""
    
    def pure_python_word_count(self, text):
        """Pure Python word count implementation (for comparison)"""
        import re
        from collections import Counter
        
        words = re.findall(r'\b\w+\b', text.lower())
        return dict(Counter(words))
    
    def test_rust_vs_python_performance(self, large_text):
        """Compare performance of Rust vs Python implementations"""
        # Run multiple times to get an average
        rust_times = []
        python_times = []

        # Warm-up 
        for _ in range(3):
            TextProcessorService.count_words(large_text)  # Rust
            self.pure_python_word_count(large_text)  # Python
        
        for _ in range(5):
            start = time.perf_counter()
            rust_result = TextProcessorService.count_words(large_text)
            rust_times.append(time.perf_counter() - start)
        
            start = time.perf_counter()
            python_result = self.pure_python_word_count(large_text)
            python_times.append(time.perf_counter() - start)
        
        rust_avg = statistics.mean(rust_times)
        python_avg = statistics.mean(python_times)
        
        print(f"\nPerformance Comparison:")
        print(f"Rust average: {rust_avg:.4f}s")
        print(f"Python average: {python_avg:.4f}s")
        print(f"Speedup: {python_avg/rust_avg:.2f}x")
        
        # Rust should be faster (or at least not significantly slower)
        assert rust_avg <= (python_avg * 1.5)  # Allow 50% margin of error
    
    def test_scaling_performance(self):
        """Test performance scaling"""
        sizes = [1000, 5000, 10000, 50000]
        times = []
        
        for size in sizes:
            text = "word " * size
            start = time.time()
            TextProcessorService.count_words(text)
            times.append(time.time() - start)
        
        # Performance growth should be linear, not exponential
        for i in range(1, len(times)):
            ratio = times[i] / times[i-1]
            size_ratio = sizes[i] / sizes[i-1]
            # Time increase ratio should be proportional to data size increase
            assert ratio <= size_ratio * 2  # Allow 2x growth factor

class TestConcurrentPerformance:
    """Concurrency performance tests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client, sample_text):
        """Test handling of concurrent requests"""
        import asyncio
        import aiohttp
        
        async def make_request():
            payload = {"text": sample_text, "operation": "count_words"}
            # For simplicity using sync client in test
            response = client.post("/count-words", json=payload)
            return response.status_code == 200
        
        # Simulate 10 concurrent requests
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(results)

class TestMemoryPerformance:
    """Memory performance tests"""
    
    def test_memory_usage_stability(self):
        """Test memory usage stability"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process multiple texts in sequence
        for _ in range(100):
            text = "test text " * 1000
            TextProcessorService.count_words(text)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be limited
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB