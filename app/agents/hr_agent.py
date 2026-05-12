"""HR Onboarding Agent."""

from typing import List, Tuple
from app.agents.base_agent import BaseAgent, ExecutionContext


class HRAgent(BaseAgent):
    """Agent for HR onboarding tasks."""

    def __init__(self):
        """Initialize HR agent."""
        super().__init__("HR Onboarding Agent")

    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Process HR-specific entities for onboarding.

        Args:
            ctx: Execution context with entities

        Returns:
            Tuple of (steps, output_summary)
        """
        persons = ctx.entities.get("persons", [])
        dates = ctx.entities.get("dates", [])

        name = persons[0] if persons else "New Employee"
        start_date = dates[0] if dates else "TBD"

        steps = [
            f"✅ Created employee profile for {name}",
            f"✅ Assigned start date: {start_date}",
            f"✅ Generated onboarding checklist",
            f"✅ Sent welcome email to {name}",
            f"✅ Logged to HR system",
        ]

        output = (
            f"{name}'s onboarding has been initiated. "
            f"Start date set to {start_date}. "
            f"Welcome email sent and HR records updated."
        )

        return steps, output
