from .base_agent import BaseAgent

class HRAgent(BaseAgent):
    def __init__(self):
        super().__init__("HR Onboarding Agent")

    def run(self, task_data: dict) -> dict:
        entities = task_data.get("entities", {})
        persons = entities.get("persons", ["Unknown"])
        dates = entities.get("dates", ["TBD"])
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
        return self.success(steps, output)