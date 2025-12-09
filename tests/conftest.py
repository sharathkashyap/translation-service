import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.config import get_settings


@pytest.fixture(scope="session")
def settings():
    """Get settings"""
    return get_settings()


@pytest.fixture(scope="function")
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def test_data():
    """Test data fixtures"""
    return {
        "english": "Hello, how are you?",
        "spanish": "Hola, ¿cómo estás?",
        "french": "Bonjour, comment allez-vous?",
        "german": "Hallo, wie geht es dir?",
    }
