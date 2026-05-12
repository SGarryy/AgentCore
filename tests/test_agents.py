"""Tests for agent module."""

import pytest
from app.agents.hr_agent import HRAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.it_agent import ITAgent
from app.agents.sales_agent import SalesAgent
from app.agents.operations_agent import OperationsAgent
from app.agents.base_agent import ExecutionContext


@pytest.fixture
def sample_context():
    """Sample execution context."""
    return ExecutionContext(
        entities={
            "persons": ["John"],
            "dates": ["2026-05-20"],
            "orgs": ["Engineering"],
            "misc": []
        },
        raw_text="Onboard new employee John",
        priority="high"
    )


class TestHRAgent:
    """Test HR Onboarding Agent."""

    def test_hr_agent_init(self):
        """Test HR agent initialization."""
        agent = HRAgent()
        assert agent.name == "HR Onboarding Agent"

    def test_hr_agent_process_entities(self, sample_context):
        """Test HR agent processes entities."""
        agent = HRAgent()
        steps, output = agent.process_entities(sample_context)

        assert len(steps) > 0
        assert "John" in output
        assert "2026-05-20" in output

    def test_hr_agent_handles_missing_data(self):
        """Test HR agent handles missing entities."""
        agent = HRAgent()
        ctx = ExecutionContext(
            entities={"persons": [], "dates": [], "orgs": [], "misc": []},
            raw_text="Onboard someone",
            priority="medium"
        )
        steps, output = agent.process_entities(ctx)

        assert len(steps) > 0
        assert "New Employee" in output  # Should use default


class TestFinanceAgent:
    """Test Finance Reconciliation Agent."""

    def test_finance_agent_init(self):
        """Test Finance agent initialization."""
        agent = FinanceAgent()
        assert agent.name == "Finance Reconciliation Agent"

    def test_finance_agent_process_entities(self, sample_context):
        """Test Finance agent processes entities."""
        agent = FinanceAgent()
        steps, output = agent.process_entities(sample_context)

        assert len(steps) > 0
        assert "invoice" in output.lower()


class TestITAgent:
    """Test IT Support Agent."""

    def test_it_agent_init(self):
        """Test IT agent initialization."""
        agent = ITAgent()
        assert agent.name == "IT Support & Triage Agent"

    def test_it_agent_generates_ticket_id(self, sample_context):
        """Test IT agent generates secure ticket IDs."""
        agent = ITAgent()
        steps, output = agent.process_entities(sample_context)

        # Should have TKT- prefix for ticket ID
        assert any("TKT-" in step for step in steps)
        assert len(steps) > 0


class TestSalesAgent:
    """Test Sales Agent."""

    def test_sales_agent_init(self):
        """Test Sales agent initialization."""
        agent = SalesAgent()
        assert agent.name == "Sales & Lead Routing Agent"

    def test_sales_agent_generates_lead_id(self, sample_context):
        """Test Sales agent generates lead IDs."""
        agent = SalesAgent()
        steps, output = agent.process_entities(sample_context)

        # Should have LEAD- prefix
        assert any("LEAD-" in step for step in steps)


class TestOperationsAgent:
    """Test Operations Agent."""

    def test_operations_agent_init(self):
        """Test Operations agent initialization."""
        agent = OperationsAgent()
        assert agent.name == "Operations & Procurement Agent"

    def test_operations_agent_generates_ops_id(self, sample_context):
        """Test Operations agent generates ops IDs."""
        agent = OperationsAgent()
        steps, output = agent.process_entities(sample_context)

        # Should have OPS- prefix
        assert any("OPS-" in step for step in steps)
