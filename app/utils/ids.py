"""Secure ID generation utilities."""

import uuid
from app.constants import (
    TICKET_ID_PREFIX,
    TASK_ID_PREFIX,
    REQUEST_ID_PREFIX,
    LEAD_ID_PREFIX,
    OPS_ID_PREFIX,
)


def generate_id(prefix: str = "", use_short: bool = False) -> str:
    """
    Generate cryptographically secure ID.

    Args:
        prefix: Optional prefix for ID
        use_short: Use first 8 chars of UUID (shorter but less unique)

    Returns:
        Formatted ID string (e.g., "TKT-A7F2E9B3C1D4")
    """
    if use_short:
        id_part = uuid.uuid4().hex[:8].upper()
    else:
        id_part = uuid.uuid4().hex[:12].upper()

    if prefix:
        return f"{prefix}-{id_part}"
    return id_part


def generate_ticket_id() -> str:
    """Generate ticket ID (e.g., TKT-A7F2E9B3C1D4)."""
    return generate_id(TICKET_ID_PREFIX, use_short=False)


def generate_task_id() -> str:
    """Generate task ID (e.g., TSK-A7F2E9B3C1D4)."""
    return generate_id(TASK_ID_PREFIX, use_short=False)


def generate_request_id() -> str:
    """Generate request ID for tracking (e.g., REQ-A7F2E9B3C1D4)."""
    return generate_id(REQUEST_ID_PREFIX, use_short=True)


def generate_lead_id() -> str:
    """Generate lead ID (e.g., LEAD-A7F2E9B3C1D4)."""
    return generate_id(LEAD_ID_PREFIX, use_short=False)


def generate_ops_id() -> str:
    """Generate operations ID (e.g., OPS-A7F2E9B3C1D4)."""
    return generate_id(OPS_ID_PREFIX, use_short=False)
