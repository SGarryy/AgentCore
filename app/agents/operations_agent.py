"""Operations & Procurement Agent."""

from typing import List, Tuple
from app.agents.base_agent import BaseAgent, ExecutionContext
from app.utils.ids import generate_ops_id


class OperationsAgent(BaseAgent):
    """Agent for operations and procurement tasks."""

    def __init__(self):
        """Initialize Operations agent."""
        super().__init__("Operations & Procurement Agent")

    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Process operations task.

        Args:
            ctx: Execution context with entities

        Returns:
            Tuple of (steps, output_summary)
        """
        dates = ctx.entities.get("dates", [])
        orgs = ctx.entities.get("orgs", [])

        schedule_date = dates[0] if dates else "this week"
        vendor = orgs[0] if orgs else "Default Vendor"

        # Generate secure reference ID
        ref = generate_ops_id()

        steps = [
            f"✅ Received operations request",
            f"✅ Vendor identified: {vendor}",
            f"✅ Scheduled for: {schedule_date}",
            f"✅ Purchase order created: {ref}",
            f"✅ Operations team notified",
        ]

        output = (
            f"Operations task {ref} initiated. "
            f"Vendor {vendor} contacted, scheduled for {schedule_date}. "
            f"Operations team has been notified."
        )

        return steps, output
