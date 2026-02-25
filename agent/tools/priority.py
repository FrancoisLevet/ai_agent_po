from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from agent.llm import llm
from agent.utils.json_utils import parse_json_loose, to_json
load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant Product Owner expert en priorisation.
Tu travailles pour une startup SaaS de gestion de projet.

Tu reçois une liste de features au format JSON.

Réponds STRICTEMENT avec un JSON valide (pas de markdown, pas de texte autour).
Pour chaque feature, applique MoSCoW et calcule un score RICE.

Règles métier importantes:
- Si type == "bug", MoSCoW = Must par défaut.
- Si un bug est bloquant, final_priority = Haute.

RICE (échelles recommandées) :
- reach : 1 à 10
- impact : 0.25, 0.5, 1, 2, 3
- confidence : 0.0 à 1.0
- effort : 1, 2, 3, 5, 8, 13
- score = reach * impact * confidence / effort

Schéma attendu:

{
  "frameworks": ["MoSCoW", "RICE"],
  "items": [
    {
      "title": "...",
      "moscow": "Must|Should|Could|Wont",
      "rice": {
        "reach": 0,
        "impact": 0,
        "confidence": 0,
        "effort": 0,
        "score": 0
      },
      "final_priority": "Haute|Moyenne|Basse",
      "justification": "..."
    }
  ]
}

Entrée attendue (exemple):
{
  "features": [
    {"title": "Export PDF", "type": "feature_request", "mentions": 2, "context": "..."}
  ]
}
"""

@tool
def prioritize_features(features: str) -> str:
    """Priorise une liste de features (JSON) via MoSCoW et RICE."""
    input_data = parse_json_loose(features)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=to_json(input_data))
    ]

    response = llm.invoke(messages)
    output_data = parse_json_loose(response.content)
    return to_json(output_data)

