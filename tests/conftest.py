import os
import sys
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
# Import your app
from git_day_practice.api import app

@pytest.fixture(scope="session")
def client() -> TestClient:
    """Create a TestClient instance for the entire test session."""
    # Set required environment variables
    os.environ.setdefault("API_KEY", "test-key")
    os.environ.setdefault("APP_NAME", "Test API")
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DEBUG", "false")
    
    return TestClient(app)

