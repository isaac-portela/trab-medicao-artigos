from __future__ import annotations

from src.agents._factory import create_agent
from src.agents.prompt_loader import load_prompt
from src.config import DEEPSEEK_MODEL
from src.models.super_summary import SuperSummary


READER_INSTRUCTION = load_prompt("reader.md")

reader_agent = create_agent(
    model=DEEPSEEK_MODEL,
    name="reader_agent",
    description="Extracts structured super-summary from PDF text",
    instruction=READER_INSTRUCTION,
    output_schema=SuperSummary,
)
