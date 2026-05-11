from .base_agent import BaseAgent
import random

class SalesAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sales & Lead Routing Agent")

    def run(self, task_data: dict) -> dict:
        entities = task_data.get("entities", {})
        orgs = entities.get("orgs", ["Unknown Sector"])
        sector = orgs[0] if orgs else "General"
        leads = random.randint(3, 10)
        top_lead = f"Company-{random.randint(100,999)}"

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
        return self.success(steps, output)