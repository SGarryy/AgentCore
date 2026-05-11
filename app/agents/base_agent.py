from datetime import datetime

class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def run(self, task_data: dict) -> dict:
        raise NotImplementedError("Each agent must implement run()")

    def success(self, steps: list, output: str) -> dict:
        return {
            "agent": self.name,
            "status": "success",
            "steps": steps,
            "output": output,
            "timestamp": datetime.now().isoformat()
        }

    def failure(self, reason: str) -> dict:
        return {
            "agent": self.name,
            "status": "failed",
            "steps": [],
            "output": reason,
            "timestamp": datetime.now().isoformat()
        }