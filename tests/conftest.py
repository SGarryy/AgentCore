"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import TaskRequest


@pytest.fixture
def client(monkeypatch):
    """FastAPI test client."""
    async def fake_check_ollama():
        return True

    monkeypatch.setattr("app.main.check_ollama", fake_check_ollama)
    monkeypatch.setattr("app.main.generate_response", lambda agent_result, user_input: agent_result.output)
    return TestClient(app)


@pytest.fixture
def sample_task():
    """Sample task request."""
    return TaskRequest(text="Onboard new employee John to engineering")


@pytest.fixture
def sample_tasks():
    """Multiple sample tasks for different agents."""
    return {
        "hr": TaskRequest(text="Hire a new developer for backend team"),
        "finance": TaskRequest(text="Reconcile last month invoices and flag duplicates"),
        "it": TaskRequest(text="Fix the authentication error on dashboard"),
        "sales": TaskRequest(text="Generate leads from retail sector"),
        "operations": TaskRequest(text="Schedule meeting for all teams"),
    }
