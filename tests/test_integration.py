import pytest
from fastapi.testclient import TestClient
import json
import tempfile
import os

class TestIntegration:
    """Integration testing"""
    
    def test_full_workflow(self, client):
        """Test complete workflow"""
        text = """
        Welcome to our company! 
        Contact us at: support@company.com or sales@company.com
        Our team includes: John, Alice, Bob, John, Alice
        Visit our website for more information.
        """
        
        # 1. Email extraction
        response = client.post("/extract-emails", 
                             json={"text": text, "operation": "extract_emails"})
        assert response.status_code == 200
        emails = response.json()["emails"]
        assert len(emails) == 2
        
        # 2. Word counting
        response = client.post("/count-words", 
                             json={"text": text, "operation": "count_words"})
        assert response.status_code == 200
        word_count = response.json()["word_count"]
        assert "john" in word_count
        assert word_count["john"] == 2
        
        # 3. Text cleaning
        response = client.post("/clean-text", 
                             json={"text": text, "operation": "clean_text"})
        assert response.status_code == 200
        cleaned = response.json()["cleaned_text"]
        assert "@" not in cleaned  # Special characters removed
    
    def test_api_consistency(self, client, sample_text):
        """Test API response consistency"""
        # Multiple calls should yield identical results
        responses = []
        for _ in range(3):
            response = client.post("/count-words", 
                                 json={"text": sample_text, "operation": "count_words"})
            responses.append(response.json())
        
        # Word count results should be identical
        for i in range(1, len(responses)):
            assert responses[0]["word_count"] == responses[i]["word_count"]
    
    def test_error_recovery(self, client):
        """Test error recovery capability"""
        # Send invalid request
        client.post("/count-words", json={"invalid": "data"})
        
        # Subsequent valid requests should still work
        response = client.post("/count-words", 
                             json={"text": "test", "operation": "count_words"})
        assert response.status_code == 200

class TestRealWorldScenarios:
    """Real-world scenario testing"""
    
    def test_multilingual_text(self, client):
        """Test multilingual text processing"""
        multilingual_text = """
        Hello world! 你好世界! Hola mundo!
        Email: contact@global.com
        More text with numbers: 123, 456, 789
        """
        
        response = client.post("/count-words", 
                             json={"text": multilingual_text, "operation": "count_words"})
        assert response.status_code == 200
        
        # Should handle characters from different languages
        data = response.json()
        assert data["total_words"] > 0
    
    def test_edge_cases(self, client):
        """Test edge cases"""
        edge_cases = [
            "",  # Empty string
            "   ",  # Only whitespace
            "\n\n\n",  # Only newlines
            "a",  # Single character
            "a@b",  # Invalid email format
            "word" * 1000,  # Very long word
        ]
        
        for text in edge_cases:
            response = client.post("/count-words", 
                                 json={"text": text, "operation": "count_words"})
            assert response.status_code == 200
            # Should return valid response structure
            data = response.json()
            assert "word_count" in data
            assert "total_words" in data

    def test_file_processing_simulation(self, client):
        """Simulate file processing scenario"""
        # Simulate processing a "file" with mixed content
        file_content = """
        Document Title: Annual Report 2024
        
        Executive Summary:
        This year has been remarkable for our company.
        
        Contact Information:
        - CEO: ceo@company.com
        - HR: hr@company.com  
        - Support: help@support.com
        
        Financial Data:
        Revenue increased by 25% this year.
        Profit margins improved significantly.
        
        Special characters and formatting:
        @#$%^&*() should be cleaned up.
        """
        
        # Process with different operations in batch
        operations = [
            ("count-words", "count_words"),
            ("extract-emails", "extract_emails"), 
            ("clean-text", "clean_text")
        ]
        
        results = {}
        for endpoint, operation in operations:
            response = client.post(f"/{endpoint}", 
                                 json={"text": file_content, "operation": operation})
            assert response.status_code == 200
            results[operation] = response.json()
        
        # Validate result sanity
        assert results["count_words"]["total_words"] > 20
        assert len(results["extract_emails"]["emails"]) == 3
        assert len(results["clean_text"]["cleaned_text"]) < len(file_content)