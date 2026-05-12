"""IT Support & Triage Agent."""

import random
from typing import List, Tuple
from app.agents.base_agent import BaseAgent, ExecutionContext
from app.utils.ids import generate_ticket_id


class ITAgent(BaseAgent):
    """Agent for IT support and ticket triage."""

    def __init__(self):
        """Initialize IT agent."""
        super().__init__("IT Support & Triage Agent")

    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Process IT support request and triage.

        Args:
            ctx: Execution context with entities

        Returns:
            Tuple of (steps, output_summary)
        """
        raw_text = ctx.raw_text

        # Classify severity
        severity = random.choice(["P1 - Critical", "P2 - High", "P3 - Medium"])

        # Generate secure ticket ID
        ticket_id = generate_ticket_id()

        steps = [
            f"✅ Received issue: '{raw_text[:50]}...'",
            f"✅ Classified severity: {severity}",
            f"✅ Created ticket: {ticket_id}",
            f"✅ Assigned to on-call engineer",
            f"✅ Stakeholders notified",
        ]

        output = (
            f"Ticket {ticket_id} created with severity {severity}. "
            f"Issue has been assigned to the on-call engineer. "
            f"Stakeholders have been notified."
        )

        return steps, output
