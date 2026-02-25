import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from agent.tools.feedback import analyze_feedback
from agent.tools.priority import prioritize_features
from agent.tools.stories import generate_stories
from agent.llm import llm_agent

load_dotenv()

ORCHESTRATOR_SYSTEM = SystemMessage(content="""
Tu es un agent Product Owner. Tu dois TOUJOURS travailler en 4 étapes en utilisant les tools :

1) Appelle analyze_feedback avec les feedbacks bruts.
   - Résultat: JSON (string). Parse-le mentalement.
   - Récupère global_summary.top_features (liste de features).

2) Construit un JSON d'entrée pour prioritize_features au format :
   {"features": [{"title": "...", "type": "...", "mentions": <int>, "context": "..."}]}

3) Appelle prioritize_features avec ce JSON.
   - Résultat: JSON avec items[]. Chaque item a moscow, rice.score, final_priority, justification.
   - Trie mentalement les items par final_priority (Haute > Moyenne > Basse) puis par rice.score décroissant.

4) Prends les 3 premières features (priorité Haute si possible) et appelle generate_stories avec :
   {"features": [{"title": "...", "moscow": "...", "final_priority": "..."}]}

Règles de sortie :
- Pour les réponses finales à l'utilisateur: retourne un JSON strict, avec les clés:
  {
    "feedback_analysis": <json de analyze_feedback>,
    "prioritization": <json de prioritize_features>,
    "stories": <json de generate_stories>
  }
- AUCUN texte hors JSON. Pas de markdown.
""")

tools = [analyze_feedback, prioritize_features, generate_stories]

agent = create_agent(llm_agent, tools, system_message=ORCHESTRATOR_SYSTEM).with_config(recursion_limit=10)

