import pytest
from fastapi.testclient import TestClient
from fastapi import status

class TestAPIEndpoints:
    """API endpoint tests"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_health_endpoint(self, client):
        """Test health check"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "rust_extension" in data
    
    def test_count_words_endpoint(self, client, sample_text):
        """Test word frequency API"""
        payload = {"text": sample_text, "operation": "count_words"}
        response = client.post("/count-words", json=payload)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "word_count" in data
        assert "total_words" in data
        assert "unique_words" in data
        assert data["total_words"] > 0
    
    def test_extract_emails_endpoint(self, client, sample_text):
        """Test email extraction API"""
        payload = {"text": sample_text, "operation": "extract_emails"}
        response = client.post("/extract-emails", json=payload)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "emails" in data
        assert "email_count" in data
        assert len(data["emails"]) == data["email_count"]
    
    def test_clean_text_endpoint(self, client, sample_text):
        """Test text cleaning API"""
        payload = {"text": sample_text, "operation": "clean_text"}
        response = client.post("/clean-text", json=payload)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "cleaned_text" in data
        assert "original_length" in data
        assert "cleaned_length" in data

class TestAPIValidation:
    """API input validation tests"""
    
    def test_invalid_json(self, client):
        """Test invalid JSON"""
        invalid_content = b"invalid json"
        response = client.post("/count-words", content=invalid_content, headers={"Content-Type": "application/json"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_missing_fields(self, client):
        """Test missing fields"""
        response = client.post("/count-words", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_empty_text(self, client):
        """Test empty text processing"""
        payload = {"text": "", "operation": "count_words"}
        response = client.post("/count-words", json=payload)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_words"] == 0

class TestAPIErrors:
    """API error handling tests"""
    
    def test_large_payload(self, client):
        """Test large payload handling"""
        huge_text = "word " * 1000000  # 1M words
        payload = {"text": huge_text, "operation": "count_words"}
        
        response = client.post("/count-words", json=payload)
        # Should handle properly or return appropriate error
        assert response.status_code in [200, 413, 422]