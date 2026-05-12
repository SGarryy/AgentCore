"""Base agent class with common workflow logic."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple
from app.schemas import AgentResult


logger = logging.getLogger(__name__)


@dataclass
class ExecutionContext:
    """Context for agent execution."""

    entities: dict
    raw_text: str
    priority: str


class BaseAgent(ABC):
    """Base agent with common workflow logic and error handling."""

    def __init__(self, name: str):
        """
        Initialize base agent.

        Args:
            name: Agent name (e.g., "HR Onboarding Agent")
        """
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def process_entities(self, ctx: ExecutionContext) -> Tuple[List[str], str]:
        """
        Implement agent-specific logic.

        Args:
            ctx: Execution context with entities and task data

        Returns:
            Tuple of (steps_completed, output_summary)

        Raises:
            ValueError: If entities are invalid
            Exception: If processing fails
        """
        pass

    def run(self, task_data: dict) -> AgentResult:
        """
        Execute agent workflow.

        This is the common workflow that all agents follow.
        Override process_entities() for agent-specific logic.

        Args:
            task_data: Dictionary with:
                - raw_text: Original user input
                - intent: Detected intent
                - entities: Extracted entities
                - priority: Task priority

        Returns:
            AgentResult with execution status, steps, and output
        """
        ctx = ExecutionContext(
            entities=task_data.get("entities", {}),
            raw_text=task_data.get("raw_text", ""),
            priority=task_data.get("priority", "medium")
        )

        try:
            self.logger.info(f"Executing {self.name} for: {ctx.raw_text[:50]}")
            steps, output = self.process_entities(ctx)
            return self.success(steps, output)
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}", exc_info=True)
            return self.failure(str(e))

    def success(self, steps: List[str], output: str) -> AgentResult:
        """
        Return success result.

        Args:
            steps: List of completed workflow steps
            output: Summary of execution output

        Returns:
            AgentResult marked as successful
        """
        result = AgentResult(
            agent=self.name,
            status="success",
            steps=steps,
            output=output,
            timestamp=datetime.now().isoformat()
        )
        self.logger.info(f"Agent succeeded: {len(steps)} steps completed")
        return result

    def failure(self, reason: str) -> AgentResult:
        """
        Return failure result.

        Args:
            reason: Reason for failure

        Returns:
            AgentResult marked as failed
        """
        result = AgentResult(
            agent=self.name,
            status="failed",
            steps=[],
            output=reason,
            timestamp=datetime.now().isoformat()
        )
        self.logger.warning(f"Agent failed: {reason}")
        return result
