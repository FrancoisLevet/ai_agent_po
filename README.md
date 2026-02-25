# PO Agent — From Feedback to Product Decisions

Technical test réalisé dans le cadre du processus de recrutement THIGA.

Assistant Product owner basé sur l’IA permettant de transformer des feedbacks utilisateurs en insights actionnables, priorisation produit et user stories prêtes à implémenter.

---

## Problématique

Les équipes produit reçoivent en continu des feedbacks utilisateurs (emails, tickets, commentaires).  
Les analyser, identifier les priorités et formuler des actions concrètes est chronophage.

Cet assistant automatise ce processus pour aider le Product Owner à :

- comprendre les problèmes utilisateurs
- détecter les patterns récurrents
- prioriser les actions
- préparer les prochaines itérations produit

---

## Fonctionnalités

### Analyse des feedbacks
- extraction des demandes et problèmes
- détection des patterns récurrents
- identification du niveau de frustration
- synthèse globale

### Priorisation produit
- scoring RICE
- classification MoSCoW
- justification des priorités

### Génération de User Stories
- format prêt pour backlog produit
- critères d’acceptation
- estimation de complexité

---

## Workflow produit automatisé

1. Analyse des feedbacks utilisateurs  
2. Identification des problèmes et fonctionnalités clés  
3. Priorisation basée sur impact et urgence  
4. Génération des prochaines actions produit  

---

## Interface utilisateur

Application Streamlit simple et orientée décision :

1. Coller les feedbacks utilisateurs  
2. Obtenir une synthèse des problèmes  
3. Visualiser les priorités produit  
4. Générer les user stories prioritaires  

L’interface a été volontairement simplifiée pour favoriser une prise de décision rapide.

---

## Architecture

L’application repose sur une approche modulaire basée sur des tools spécialisés :

- `feedback` → analyse et structuration des feedbacks  
- `priority` → scoring et priorisation produit  
- `stories` → génération de user stories  

Chaque tool produit un JSON structuré garantissant robustesse et chaînage fiable.

L’orchestration est déterministe afin d’assurer une UX claire et prévisible.

---

## Architecture compatible agent

L’application repose sur des tools modulaires pouvant être orchestrés par un agent LLM.

Un orchestrateur agent est également implémenté dans le dépôt et peut piloter automatiquement l’analyse des feedbacks, la priorisation et la génération de user stories.

L’interface actuelle orchestre le workflow de manière déterministe afin de garantir la fiabilité, tout en permettant une évolution vers des workflows autonomes et conversationnels.

## Choix techniques

- LLM + tools spécialisés pour modularité et maintenabilité  
- Sorties JSON strictes pour fiabilité et interopérabilité  
- Streamlit pour prototypage rapide et UX accessible  
- RICE et MoSCoW comme standards reconnus en product management  

---

## Logique de priorisation

L’assistant priorise automatiquement :

- les bugs critiques et bloquants
- les problèmes récurrents
- les fonctionnalités à fort impact utilisateur

Les user stories sont générées pour les priorités les plus critiques.

---

## Améliorations possibles

- regroupement automatique des fonctionnalités similaires  
- intégration avec Jira ou Linear  
- apprentissage sur données réelles  
- analyse continue des feedbacks  

---

## Lancer l’application

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
---

## Auteur

François Levet  
Technical test – THIGA