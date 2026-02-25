from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from agent.llm import llm
from agent.utils.json_utils import parse_json_loose, to_json
load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant Product Owner expert.
Tu travailles pour une startup SaaS de gestion de projet.

Tu reçois une liste de features au format JSON.
Génère des user stories structurées.

Réponds STRICTEMENT avec un JSON valide (pas de markdown, pas de texte autour).

Complexité : 1, 2, 3, 5, 8, 13

Schéma attendu:
{
  "stories": [
    {
      "feature_title": "...",
      "story_title": "...",
      "user_story": "En tant que ..., je veux ..., afin de ...",
      "acceptance_criteria": ["...","..."],
      "complexity_points": 0,
      "complexity_justification": "..."
    }
  ]
}

Entrée attendue (exemple):
{
  "features": [
    {"title": "Export PDF", "moscow": "Must", "final_priority": "Haute"}
  ]
}
"""

@tool
def generate_stories(features: str) -> str:
    """Génère des user stories à partir d'une liste de features (JSON)."""
    input_data = parse_json_loose(features)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=to_json(input_data))
    ]

    response = llm.invoke(messages)
    output_data = parse_json_loose(response.content)
    return to_json(output_data)

