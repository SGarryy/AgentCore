"""Finance Reconciliation Agent."""

import random
from typing import List, Tuple
from app.agents.base_agent import BaseAgent, ExecutionContext
from app.constants import DEFAULT_DUPLICATES_RANGE


class FinanceAgent(BaseAgent):
    """Agent for finance reconciliation tasks."""

    def __init__(self):
        """Initialize Finance agent."""
        super().__init__("Finance Reconciliation Agent")

    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Process finance reconciliation task.

        Args:
            ctx: Execution context with entities

        Returns:
            Tuple of (steps, output_summary)
        """
        dates = ctx.entities.get("dates", [])
        period = dates[0] if dates else "last month"

        # Simulate finding duplicates
        duplicates = random.randint(*DEFAULT_DUPLICATES_RANGE)
        total = random.randint(20, 100)

        steps = [
            f"✅ Scanned {total} invoices for period: {period}",
            f"✅ Found {duplicates} duplicate entries",
            f"✅ Flagged duplicates for review",
            f"✅ Generated reconciliation report",
            f"✅ Logged findings to finance system",
        ]

        output = (
            f"Reconciliation complete for {period}. "
            f"Scanned {total} invoices, found {duplicates} duplicates. "
            f"Report generated and flagged for review."
        )

        return steps, output
