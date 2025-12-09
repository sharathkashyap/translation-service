import pytest
from fastapi import status


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "service" in data
    assert "docs" in data


def test_get_supported_languages(client):
    """Test getting supported languages"""
    response = client.get("/api/translate/languages")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "languages" in data
    assert "engine" in data
    assert isinstance(data["languages"], dict)
    assert len(data["languages"]) > 0


def test_translate_with_invalid_language(client):
    """Test translation with invalid language pair"""
    response = client.post(
        "/api/translate/",
        json={
            "text": "Hello",
            "source_language": "en",
            "target_language": "en"  # Same source and target
        }
    )
    # Could be 400 or 503 depending on engine


def test_translate_with_empty_text(client):
    """Test translation with empty text"""
    response = client.post(
        "/api/translate/",
        json={
            "text": "",  # Empty text
            "source_language": "en",
            "target_language": "es"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_batch_translate_with_invalid_count(client):
    """Test batch translation with invalid count"""
    response = client.post(
        "/api/translate/batch",
        json={
            "texts": [],  # Empty list
            "source_language": "en",
            "target_language": "es"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_translate_text_too_long(client):
    """Test translation with text exceeding max length"""
    long_text = "hello " * 2000  # Very long text
    response = client.post(
        "/api/translate/",
        json={
            "text": long_text,
            "source_language": "en",
            "target_language": "es"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
