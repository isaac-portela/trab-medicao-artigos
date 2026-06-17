from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentSpec:
    name: str
    model: str
    description: str
    instruction: str
    output_schema: type[Any]


def create_agent(
    *,
    name: str,
    model: str,
    description: str,
    instruction: str,
    output_schema: type[Any],
) -> Any:
    try:
        from google.adk.agents import Agent

        return Agent(
            model=model,
            name=name,
            description=description,
            instruction=instruction,
            output_schema=output_schema,
        )
    except Exception:
        return AgentSpec(
            name=name,
            model=model,
            description=description,
            instruction=instruction,
            output_schema=output_schema,
        )


def get_agent_attr(agent: Any, attr: str) -> Any:
    return getattr(agent, attr)

