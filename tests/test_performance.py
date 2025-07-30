import pytest
import time
import statistics
from app.services import TextProcessorService, SentimentService

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


class TestSentimentPerformance:
    
    def test_english_sentiment_performance(self):
        """测试英文情感分析性能"""
        # 大文本测试 - 英文
        large_text = "This is an amazing product with excellent quality! " * 200  # 约2000词
        
        start_time = time.time()
        result = SentimentService.analyze_sentiment(large_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # 性能断言：处理2000词应该在50ms内完成
        assert processing_time < 0.05
        assert result['processing_time_ms'] < 50
        assert result['word_count'] > 1000
        assert result['language'] == 'en'
    
    def test_chinese_sentiment_performance(self):
        """测试中文情感分析性能"""
        # 大文本测试 - 中文
        large_text = "这是一个非常棒的产品，质量很好，我很喜欢！" * 200  # 约2000字符
        
        start_time = time.time()
        result = SentimentService.analyze_sentiment(large_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # 中文分词可能稍慢，但至少应在80ms内
        assert processing_time < 0.08
        assert result['processing_time_ms'] < 80
        assert result['word_count'] > 200
        assert result['language'] == 'zh'
    
    def test_mixed_language_performance(self):
        """测试混合语言性能"""
        mixed_text = "这个 product 很好，quality 是 excellent！" * 100
        
        start_time = time.time()
        result = SentimentService.analyze_sentiment(mixed_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert processing_time < 0.05
        assert result['language'] == 'mixed'
    
    def test_parallel_processing_performance(self):
        """测试并行处理性能"""
        import concurrent.futures
        
        test_texts = [
            "This is amazing! I love it.",
            "这个产品很棒，我很喜欢。",
            "Terrible quality, very disappointed.",
            "质量太差了，很失望。",
            "Not bad, could be better.",
        ] * 20  # 100个文本
        
        start_time = time.time()
        
        # 并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(SentimentService.analyze_sentiment, test_texts))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 100个文本并行处理应该在1秒内完成
        assert total_time < 1.0
        assert len(results) == 100
    
    @pytest.mark.benchmark
    def test_sentiment_benchmark_english(self, benchmark):
        """英文情感分析基准测试"""
        text = "This is a great product with excellent features and amazing quality!"
        
        result = benchmark(SentimentService.analyze_sentiment, text)
        assert result['label'] == 'positive'
        assert result['language'] == 'en'
    
    @pytest.mark.benchmark
    def test_sentiment_benchmark_chinese(self, benchmark):
        """中文情感分析基准测试"""
        text = "这是一个很棒的产品，功能很好，质量也很优秀！"
        
        result = benchmark(SentimentService.analyze_sentiment, text)
        assert result['label'] == 'positive'
        assert result['language'] == 'zh'