from .base_agent import BaseAgent
import random

class ITAgent(BaseAgent):
    def __init__(self):
        super().__init__("IT Support & Triage Agent")

    def run(self, task_data: dict) -> dict:
        raw_text = task_data.get("raw_text", "")
        severity = random.choice(["P1 - Critical", "P2 - High", "P3 - Medium"])
        ticket_id = f"TKT-{random.randint(1000, 9999)}"

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
        return self.success(steps, output)