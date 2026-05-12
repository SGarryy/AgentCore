"""Sales & Lead Routing Agent."""

import random
from typing import List, Tuple
from app.agents.base_agent import BaseAgent, ExecutionContext
from app.utils.ids import generate_lead_id


class SalesAgent(BaseAgent):
    """Agent for sales and lead routing."""

    def __init__(self):
        """Initialize Sales agent."""
        super().__init__("Sales & Lead Routing Agent")

    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Process sales lead routing.

        Args:
            ctx: Execution context with entities

        Returns:
            Tuple of (steps, output_summary)
        """
        orgs = ctx.entities.get("orgs", [])
        sector = orgs[0] if orgs else "General"

        # Simulate lead generation
        leads = random.randint(3, 10)
        top_lead = generate_lead_id()

        steps = [
            f"✅ Scanned lead database for sector: {sector}",
            f"✅ Scored {leads} potential leads",
            f"✅ Top lead identified: {top_lead}",
            f"✅ Routed leads to sales team",
            f"✅ CRM updated with new prospects",
        ]

        output = (
            f"Found {leads} qualified leads in {sector} sector. "
            f"Top prospect: {top_lead}. "
            f"All leads routed to sales team and CRM updated."
        )

        return steps, output
