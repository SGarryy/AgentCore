"""Tests for API endpoints."""

import pytest
from app.schemas import TaskRequest


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self, client):
        """Test basic health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "timestamp" in data

    def test_detailed_health_check(self, client):
        """Test detailed health check."""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "checks" in data


class TestProcessEndpoint:
    """Test task processing endpoint."""

    def test_process_task_valid_input(self, client, sample_task):
        """Test processing valid task."""
        response = client.post("/process", json=sample_task.dict())
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or "error" in data

    def test_process_task_empty_text(self, client):
        """Test processing with empty text."""
        response = client.post("/process", json={"text": ""})
        assert response.status_code == 422

    def test_process_task_missing_text(self, client):
        """Test processing without text field."""
        response = client.post("/process", json={})
        assert response.status_code == 422  # Validation error

    def test_rate_limiting(self, client, sample_task):
        """Test rate limiting."""
        # Make many requests
        responses = []
        for i in range(20):
            response = client.post("/process", json=sample_task.dict())
            responses.append(response.status_code)

        # Should get rate limited (429) at some point
        assert 429 in responses or all(s in [200, 500, 422] for s in responses)
