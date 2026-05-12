"""Tests for ML router."""

import pytest
from app.ml.router import route_task
from app.schemas import RouterResult


class TestRouteTask:
    """Test ML routing."""

    def test_route_hr_task(self):
        """Test routing HR intent."""
        result = route_task("Onboard new employee John")
        assert isinstance(result, RouterResult)
        assert result.routed_to == "hr_agent"
        assert result.confidence > 0

    def test_route_finance_task(self):
        """Test routing Finance intent."""
        result = route_task("Reconcile invoices for last month")
        assert result.routed_to == "finance_agent"

    def test_route_returns_all_scores(self):
        """Test that all agent scores are returned."""
        result = route_task("Onboard new employee")
        assert len(result.all_scores) == 5  # 5 agents
        assert all(0 <= v <= 1 for v in result.all_scores.values())

    def test_route_confidence_is_valid(self):
        """Test that confidence is valid probability."""
        result = route_task("Onboard new employee")
        assert 0 <= result.confidence <= 1

    def test_invalid_input_raises(self):
        """Test that invalid input raises error."""
        with pytest.raises(Exception):
            route_task("")
