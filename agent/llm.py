import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Pour les outils — petit modèle, économe en tokens
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Pour l'agent — grand modèle, meilleur tool calling
llm_agent = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)