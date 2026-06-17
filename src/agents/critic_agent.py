from __future__ import annotations

from src.agents._factory import create_agent
from src.agents.prompt_loader import load_prompt
from src.config import GEMINI_MODEL
from src.models.critic_output import CriticOutput


CRITIC_INSTRUCTION = load_prompt("critic.md")

critic_agent = create_agent(
    model=GEMINI_MODEL,
    name="critic_agent",
    description="Evaluates article quality with rubric scores and justifications",
    instruction=CRITIC_INSTRUCTION,
    output_schema=CriticOutput,
)
