"""Tests for utilities."""

import pytest
from app.utils.ids import (
    generate_id,
    generate_ticket_id,
    generate_task_id,
    generate_request_id,
    generate_lead_id,
    generate_ops_id,
)


class TestIDGeneration:
    """Test secure ID generation."""

    def test_generate_id_with_prefix(self):
        """Test ID generation with prefix."""
        id_val = generate_id("TEST")
        assert id_val.startswith("TEST-")
        assert len(id_val) > len("TEST-")

    def test_generate_id_without_prefix(self):
        """Test ID generation without prefix."""
        id_val = generate_id()
        assert "-" not in id_val
        assert len(id_val) > 0

    def test_generate_id_uniqueness(self):
        """Test that IDs are unique."""
        ids = [generate_id("ID") for _ in range(100)]
        assert len(set(ids)) == 100  # All unique

    def test_generate_ticket_id(self):
        """Test ticket ID generation."""
        ticket_id = generate_ticket_id()
        assert ticket_id.startswith("TKT-")
        assert len(ticket_id.split("-")[1]) >= 8  # Sufficient entropy

    def test_generate_task_id(self):
        """Test task ID generation."""
        task_id = generate_task_id()
        assert task_id.startswith("TSK-")

    def test_generate_request_id(self):
        """Test request ID generation."""
        req_id = generate_request_id()
        assert req_id.startswith("REQ-")

    def test_generate_lead_id(self):
        """Test lead ID generation."""
        lead_id = generate_lead_id()
        assert lead_id.startswith("LEAD-")

    def test_generate_ops_id(self):
        """Test operations ID generation."""
        ops_id = generate_ops_id()
        assert ops_id.startswith("OPS-")

    def test_id_security_collisions_unlikely(self):
        """Test that collision probability is extremely low."""
        ids = [generate_ticket_id() for _ in range(1000)]
        assert len(set(ids)) == 1000  # No collisions in 1000 attempts
