from __future__ import annotations

import json

from src.agents._factory import create_agent
from src.agents.prompt_loader import load_prompt
from src.config import GEMINI_MODEL, TOPICOS_EMENTA, UNIDADES
from src.models.classification import ClassificationOutput


CLASSIFIER_INSTRUCTION = load_prompt("classifier.md").format(
    unidades=json.dumps(sorted(UNIDADES), ensure_ascii=False, indent=2),
    topicos_ementa=json.dumps(TOPICOS_EMENTA, ensure_ascii=False, indent=2),
)

classifier_agent = create_agent(
    model=GEMINI_MODEL,
    name="classifier_agent",
    description="Classifies article metadata from super-summary",
    instruction=CLASSIFIER_INSTRUCTION,
    output_schema=ClassificationOutput,
)
