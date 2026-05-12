"""Task dispatcher to route tasks to appropriate agents."""

import logging
from typing import Dict, Type
from app.agents.base_agent import BaseAgent
from app.agents.hr_agent import HRAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.it_agent import ITAgent
from app.agents.sales_agent import SalesAgent
from app.agents.operations_agent import OperationsAgent
from app.schemas import AgentResult
from datetime import datetime

logger = logging.getLogger(__name__)

# Agent mapping
AGENT_MAP: Dict[str, Type[BaseAgent]] = {
    "hr_agent": HRAgent,
    "finance_agent": FinanceAgent,
    "it_agent": ITAgent,
    "sales_agent": SalesAgent,
    "operations_agent": OperationsAgent,
}


def dispatch(intent: str, task_data: dict) -> AgentResult:
    """
    Dispatch task to appropriate agent.

    Args:
        intent: Detected intent from NLP
        task_data: Task data with entities and metadata

    Returns:
        AgentResult from the dispatched agent

    Raises:
        ValueError: If intent is not recognized
    """
    agent_class = AGENT_MAP.get(intent)
    if not agent_class:
        error_msg = f"No agent found for intent: {intent}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        logger.info(f"Dispatching to {agent_class.__name__} for intent: {intent}")
        agent = agent_class()
        return agent.run(task_data)
    except Exception as e:
        logger.error(f"Agent dispatch failed: {e}", exc_info=True)
        raise
