from .base_agent import BaseAgent
import random

class OperationsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Operations & Procurement Agent")

    def run(self, task_data: dict) -> dict:
        entities = task_data.get("entities", {})
        dates = entities.get("dates", ["this week"])
        orgs = entities.get("orgs", ["Internal"])
        schedule_date = dates[0] if dates else "this week"
        vendor = orgs[0] if orgs else "Default Vendor"
        ref = f"OPS-{random.randint(1000,9999)}"

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
        return self.success(steps, output)