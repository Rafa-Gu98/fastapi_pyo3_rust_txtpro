import pytest
from app.services import TextProcessorService
import time

class TestTextProcessorService:
    """Business logic layer testing"""
    
    def test_count_words_service(self, sample_text):
        """Test word frequency statistics service"""
        result = TextProcessorService.count_words(sample_text)
        
        assert "word_count" in result
        assert "total_words" in result
        assert "unique_words" in result
        assert "processing_time_ms" in result
        
        assert isinstance(result["word_count"], dict)
        assert isinstance(result["total_words"], int)
        assert isinstance(result["unique_words"], int)
        assert isinstance(result["processing_time_ms"], float)
        
        assert result["total_words"] > 0
        assert result["unique_words"] > 0
        assert result["processing_time_ms"] >= 0
    
    def test_extract_emails_service(self, sample_text):
        """Test email extraction service"""
        result = TextProcessorService.extract_emails(sample_text)
        
        assert "emails" in result
        assert "email_count" in result
        assert "processing_time_ms" in result
        
        assert isinstance(result["emails"], list)
        assert result["email_count"] == len(result["emails"])
        assert result["email_count"] >= 0
    
    def test_clean_text_service(self, sample_text):
        """Test text cleaning service"""
        result = TextProcessorService.clean_text(sample_text)
        
        assert "cleaned_text" in result
        assert "original_length" in result
        assert "cleaned_length" in result
        assert "processing_time_ms" in result
        
        assert isinstance(result["cleaned_text"], str)
        assert result["original_length"] == len(sample_text)
        assert result["cleaned_length"] == len(result["cleaned_text"])
    
    def test_service_error_handling(self):
        """Test service layer error handling"""
        # Test None input (if Rust extension doesn't handle it)
        try:
            TextProcessorService.count_words(None)
        except Exception as e:
            assert isinstance(e, (TypeError, AttributeError))

class TestServicePerformance:
    """Service layer performance testing"""
    
    def test_performance_tracking(self, large_text):
        """Test performance monitoring accuracy"""
        result = TextProcessorService.count_words(large_text)
        
        # Manual timing verification
        start_time = time.time()
        TextProcessorService.count_words(large_text)
        manual_time = (time.time() - start_time) * 1000
        
        # Service reported time should be reasonable
        assert result["processing_time_ms"] > 0
        # Allow for some margin of error
        assert abs(result["processing_time_ms"] - manual_time) < manual_time * 0.5