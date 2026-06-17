from __future__ import annotations

from src.agents._factory import create_agent
from src.agents.prompt_loader import load_prompt
from src.config import GEMINI_MODEL
from src.models.synthesis import SynthesisOutput


SYNTHESIZER_INSTRUCTION = load_prompt("synthesizer.md")

synthesizer_agent = create_agent(
    model=GEMINI_MODEL,
    name="synthesizer_agent",
    description="Analyzes thematic relationships across all classified articles",
    instruction=SYNTHESIZER_INSTRUCTION,
    output_schema=SynthesisOutput,
)
