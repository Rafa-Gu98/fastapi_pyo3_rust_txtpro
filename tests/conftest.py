import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)

@pytest.fixture
def sample_text():
    """Sample text fixture for testing"""
    return """
    Hello world! This is a test email: john@example.com
    Another email here: alice@test.org
    Some words: hello, world, test, hello, world
    Special characters: @#$%^&*()
    """

@pytest.fixture
def large_text():
    """Large text data fixture for performance testing"""
    base_text = "hello world test performance " * 10000
    emails = ["user{}@example.com ".format(i) for i in range(100)]
    return base_text + " ".join(emails)

@pytest.fixture
def event_loop():
    """Event loop fixture for async testing"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()