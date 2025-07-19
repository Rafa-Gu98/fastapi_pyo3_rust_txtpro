import pytest
import text_processor_rust
from collections import Counter

class TestRustExtension:
    """Direct testing of Rust extension module"""
    
    def test_count_words_basic(self, sample_text):
        """Test basic word counting functionality"""
        result = text_processor_rust.count_words(sample_text)
        
        assert isinstance(result, dict)
        assert "hello" in result
        assert "world" in result
        assert result["hello"] == 3
        assert result["world"] == 3
    
    def test_count_words_empty(self):
        """Test empty text processing"""  # Modified
        result = text_processor_rust.count_words("")
        assert result == {}
    
    def test_count_words_case_insensitive(self):
        """Test case insensitivity"""  # Modified
        text = "Hello HELLO hello"
        result = text_processor_rust.count_words(text)
        assert result["hello"] == 3
    
    def test_extract_emails_basic(self, sample_text):
        """Test basic email extraction"""  # Modified
        emails = text_processor_rust.extract_emails(sample_text)
        
        assert isinstance(emails, list)
        assert "john@example.com" in emails
        assert "alice@test.org" in emails
        assert len(emails) == 2
    
    def test_extract_emails_empty(self):
        """Test text without emails"""  # Modified
        emails = text_processor_rust.extract_emails("No emails here!")
        assert emails == []
    
    def test_extract_emails_multiple_formats(self):
        """Test various email formats"""  # Modified
        text = """
        Standard: user@domain.com
        Subdomain: test@mail.example.org
        Numbers: user123@test456.co.uk
        Dots and dashes: first.last@sub-domain.example.com
        Invalid: @invalid.com, user@, incomplete
        """
        emails = text_processor_rust.extract_emails(text)
        
        valid_emails = [
            "user@domain.com",
            "test@mail.example.org", 
            "user123@test456.co.uk",
            "first.last@sub-domain.example.com"
        ]
        
        for email in valid_emails:
            assert email in emails
        
        assert "@invalid.com" not in emails
    
    def test_clean_text_basic(self, sample_text):
        """Test basic text cleaning"""  # Modified
        cleaned = text_processor_rust.clean_text(sample_text)
        
        assert isinstance(cleaned, str)
        assert "@#$%^&*()" not in cleaned
        assert "hello" in cleaned.lower()
    
    def test_clean_text_preserves_punctuation(self):
        """Test preserving specified punctuation"""  # Modified
        text = "Hello, world! How are you? Fine."
        cleaned = text_processor_rust.clean_text(text)
        
        assert "," in cleaned
        assert "!" in cleaned
        assert "?" in cleaned
        assert "." in cleaned
    
    def test_clean_text_removes_special_chars(self):
        """Test removing special characters"""  # Modified
        text = "Hello@#$%world^&*()test"
        cleaned = text_processor_rust.clean_text(text)
        
        for char in "@#$%^&*()":
            assert char not in cleaned

class TestRustExtensionPerformance:
    """Performance testing for Rust extension"""
    
    def test_large_text_processing(self, large_text):
        """Test large text processing capability"""
        import time
        
        start_time = time.time()
        result = text_processor_rust.count_words(large_text)
        processing_time = time.time() - start_time
        
        assert isinstance(result, dict)
        assert len(result) > 0
        # Should complete within reasonable time
        assert processing_time < 5.0  # Complete within 5 seconds
    
    def test_memory_efficiency(self):
        """Test memory usage efficiency"""  # Modified
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process large text
        large_text = "word " * 100000
        text_processor_rust.count_words(large_text)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024