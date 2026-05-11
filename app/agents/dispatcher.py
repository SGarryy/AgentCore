from .hr_agent import HRAgent
from .finance_agent import FinanceAgent
from .it_agent import ITAgent
from .sales_agent import SalesAgent
from .operations_agent import OperationsAgent

AGENT_MAP = {
    "hr_agent": HRAgent,
    "finance_agent": FinanceAgent,
    "it_agent": ITAgent,
    "sales_agent": SalesAgent,
    "operations_agent": OperationsAgent,
}

def dispatch(intent: str, task_data: dict) -> dict:
    agent_class = AGENT_MAP.get(intent)
    if not agent_class:
        return {
            "agent": "Unknown",
            "status": "failed",
            "steps": [],
            "output": f"No agent found for intent: {intent}",
            "timestamp": ""
        }
    agent = agent_class()
    return agent.run(task_data)