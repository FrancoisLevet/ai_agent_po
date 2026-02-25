from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from agent.llm import llm
from agent.utils.json_utils import parse_json_loose, to_json
load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant Product Owner expert en analyse de feedback client
pour une startup SaaS de gestion de projet.

Tu reçois des feedbacks bruts (emails, tickets, commentaires).
Ta tâche : analyser et extraire des informations actionnables.
Regroupe les demandes similaires sous une même fonctionnalité.
Réponds STRICTEMENT avec un JSON valide (pas de markdown, pas de texte autour).
Schéma attendu:

{
  "individual": [
    {
      "id": "Feedback 1",
      "features": [{"title": "...", "type": "feature_request|bug|ux|performance", "evidence": "..."}],
      "problems": ["..."],
      "frustration": "Faible|Moyenne|Haute",
      "suggested_priority": "Haute|Moyenne|Basse"
    }
  ],
  "global_summary": {
    "patterns": ["..."],
    "top_features": [{"title": "...", "mentions": 0}],
    "recurring_problems": ["..."],
    "overall_priority": "Haute|Moyenne|Basse"
  }
}
"""

@tool
def analyze_feedback(feedback: str) -> str:
    """Analyse du feedback client brut et extrait les demandes de features,
    les problèmes identifiés et propose une priorité."""
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Feedback à analyser :\n{feedback}")
    ]
    
    response = llm.invoke(messages)
    data = parse_json_loose(response.content)
    return to_json(data)


