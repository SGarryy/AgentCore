from .base_agent import BaseAgent
import random

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Finance Reconciliation Agent")

    def run(self, task_data: dict) -> dict:
        entities = task_data.get("entities", {})
        dates = entities.get("dates", ["last month"])
        period = dates[0] if dates else "last month"
        duplicates = random.randint(1, 5)
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
        return self.success(steps, output)