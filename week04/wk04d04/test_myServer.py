"""
Test suite for FastAPI application.

Demonstrates testing best practices using pytest and FastAPI's TestClient.
Uses the custom logger module for test logging.
"""

import pytest
from fastapi.testclient import TestClient

from myServer import app
from myLogger import get_logger

# Set up test logger
logger = get_logger(__name__)


# Test client fixture
@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    logger.info("Creating test client")
    return TestClient(app)


class TestRootEndpoints:
    """Test suite for root and health endpoints."""
    
    def test_read_root(self, client):
        """Test the root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Welcome" in response.json()["message"]
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestItemEndpoints:
    """Test suite for item-related endpoints."""
    
    def test_read_item_valid(self, client):
        """Test reading an item with valid ID."""
        response = client.get("/api/v1/items/42")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 42
        assert "q" in data
    
    def test_read_item_with_query(self, client):
        """Test reading an item with query parameter."""
        response = client.get("/api/v1/items/42?q=search")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 42
        assert data["q"] == "search"
    
    def test_read_item_not_found(self, client):
        """Test reading a non-existent item."""
        response = client.get("/api/v1/items/9999")
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_read_item_invalid_id(self, client):
        """Test reading an item with invalid ID (negative)."""
        response = client.get("/api/v1/items/-1")
        assert response.status_code == 422  # Validation error


class TestUserItemEndpoints:
    """Test suite for user item endpoints."""
    
    def test_read_user_item_valid(self, client):
        """Test reading a user's item with valid IDs."""
        response = client.get("/api/v1/users/1/items/42")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 42
        assert data["owner_id"] == 1
    
    def test_read_user_item_with_short_description(self, client):
        """Test reading a user's item with short description."""
        response = client.get("/api/v1/users/1/items/42?short=true")
        assert response.status_code == 200
        data = response.json()
        assert data["description"] is not None
        assert "short" in data["description"].lower()
    
    def test_read_user_item_not_found(self, client):
        """Test reading a non-existent user item."""
        response = client.get("/api/v1/users/9999/items/9999")
        assert response.status_code == 404


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""
    
    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "FastAPI Boilerplate"


# Run tests with: pytest test_myServer.py -v
# Run with coverage: pytest test_myServer.py -v --cov=myServer
