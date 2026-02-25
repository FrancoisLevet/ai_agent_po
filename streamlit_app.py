import sys
import os
import streamlit as st
from dotenv import load_dotenv
import json
# Assure l'import depuis la racine du projet (ai_agent_po/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

from agent.tools.feedback import analyze_feedback
from agent.tools.priority import prioritize_features
from agent.tools.stories import generate_stories
st.set_page_config(page_title="PO Agent – Feedback to Insights", page_icon="🤖", layout="wide")
st.title("🤖 PO Agent – Feedback → Insights actionnables")
st.caption("Colle des feedbacks clients, obtiens une synthèse PO + des recommandations concrètes.")


st.markdown("---")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("1) Feedbacks bruts")
    feedbacks = st.text_area(
        "Colle ici emails, tickets, commentaires…",
        height=260,
        placeholder=(
            "Feedback 1 (email) : ...\n\n"
            "Feedback 2 (ticket) : ...\n\n"
            "Feedback 3 (in-app) : ..."
        ),
    )

    run = st.button("🔎 Analyser & proposer des actions", type="primary", use_container_width=True)


st.markdown("---")
def try_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None

def build_features_payload_from_feedback(feedback_analysis_json: dict, limit: int):
    top = (feedback_analysis_json.get("global_summary") or {}).get("top_features") or []
    feats = []
    for item in top[:limit]:
        title = (item or {}).get("title")
        if not title:
            continue
        feats.append({
            "title": title,
            "mentions": int((item or {}).get("mentions", 1))
        })
    return {"features": feats}


def list_text_to_features_json(text: str):
    feats = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # enlève "1. " / "- " / "• "
        if "." in line[:4]:
            line = line.split(".", 1)[1].strip()
        line = line.lstrip("-• ").strip()
        if line:
            feats.append({"title": line})
    return {"features": feats}

# ---------- RUN ----------
if run:
    if not feedbacks.strip():
        st.warning("Colle des feedbacks avant de lancer l’analyse.")
        st.stop()

    # 1) ANALYSE FEEDBACK
    with st.spinner("Analyse des feedbacks…"):
        feedback_analysis_str = analyze_feedback.invoke({"feedback": feedbacks})

    feedback_data = try_parse_json(feedback_analysis_str)
    if feedback_data is None:
        st.error("La sortie de analyze_feedback n'est pas un JSON valide. Affichage brut ci-dessous.")
        st.code(feedback_analysis_str, language="text")
        st.stop()

    # 2) FEATURES PAYLOAD (depuis top_features)
    features_payload = build_features_payload_from_feedback(feedback_data, 8)

    # 3) PRIORISATION
    prioritization_data = None
    prioritization_str = None
    with st.spinner("Proposition de priorisation…"):
        prioritization_str = prioritize_features.invoke(
            {"features": json.dumps(features_payload, ensure_ascii=False)}
        )
    prioritization_data = try_parse_json(prioritization_str)


    # ---------- DISPLAY (PROPRE) ----------
    st.subheader("📌 Résultats")

    # A) Synthèse PO
    st.markdown("### 🧾 Synthèse PO")
    gs = feedback_data.get("global_summary", {}) or {}
    patterns = gs.get("patterns", []) or []
    recurring = gs.get("recurring_problems", []) or []
    overall = gs.get("overall_priority")

    n_patterns = len(patterns)
    n_recurring = len(recurring)
    n_feedbacks = len(feedback_data.get("individual", []) or [])
    n_features = len(gs.get("top_features", []) or [])

    st.markdown(
        f"""
    <div style="padding: 12px 14px; border-radius: 12px; border: 2px solid rgba(49,51,63,0.2);">
    <div style="font-size: 1.5rem; margin-bottom: 6px;">
        <b>Lecture rapide :</b> {n_feedbacks} feedbacks analysés · {n_features} features candidates · {n_patterns} patterns · {n_recurring} problèmes récurrents
    </div>
    <div style="font-size: 1.55rem;">
        <b>Priorité globale :</b> <span style="padding: 3px 10px; border-radius: 999px; border: 1px solid rgba(49,51,63,0.25);">{overall}</span>
    </div>
    </div>
    """,
        unsafe_allow_html=True
    )

    # B) Top features (table)
    st.markdown("### 🧩 Top features (extraites)")
    top_features = gs.get("top_features", []) or []
    if top_features:
        st.dataframe(top_features, use_container_width=True)
    else:
        st.info("Aucune feature extraite dans global_summary.top_features.")

    # C) Détail par feedback (lisible)
    st.markdown("### 🗂️ Détail par feedback")
    for item in feedback_data.get("individual", []) or []:
        with st.expander(f"{item.get('id', 'Feedback')} — Frustration: {item.get('frustration', '—')} / Priorité: {item.get('suggested_priority', '—')}", expanded=False):
            feats = item.get("features", []) or []
            probs = item.get("problems", []) or []
            if feats:
                st.markdown("**Features mentionnées**")
                st.dataframe(feats, use_container_width=True)
            if probs:
                st.markdown("**Problèmes**")
                for pr in probs:
                    st.write(f"- {pr}")
            ev = None
            if feats and isinstance(feats[0], dict):
                ev = feats[0].get("evidence")
            if ev:
                st.markdown(f"**Evidence**: {ev}")

    # D) Priorisation (table propre)
    st.markdown("### 🎯 Priorisation (table)")
    if prioritization_data and isinstance(prioritization_data, dict):
        items = prioritization_data.get("items", []) or []
        if items:
            table = []
            for it in items:
                rice = it.get("rice") or {}
                table.append({
                    "title": it.get("title"),
                    "moscow": it.get("moscow"),
                    "final_priority": it.get("final_priority"),
                    "rice_score": rice.get("score"),
                    "reach": rice.get("reach"),
                    "impact": rice.get("impact"),
                    "confidence": rice.get("confidence"),
                    "effort": rice.get("effort"),
                })
            st.dataframe(table, use_container_width=True)
        else:
            st.info("Pas d'items dans la priorisation.")
    elif prioritization_str:
        st.warning("La priorisation n'est pas un JSON valide — affichage brut.")
        st.code(prioritization_str, language="text")
    else:
        st.info("Aucune priorisation disponible.")

    # 4) STORIES 
    stories_str = None

    def pick_features_for_stories(prioritization_data: dict) -> list[str]:
        """Sélectionne les features à transformer en stories."""
        items = prioritization_data.get("items", []) or []

        high = [it for it in items if it.get("final_priority") == "Haute"]
        if high:
            return [it.get("title") for it in high if it.get("title")]

        # fallback : top 2 par score RICE
        def rice_score(it):
            rice = it.get("rice") or {}
            return rice.get("score") or 0

        items_sorted = sorted(items, key=rice_score, reverse=True)
        return [it.get("title") for it in items_sorted[:2] if it.get("title")]

    if prioritization_data and isinstance(prioritization_data, dict):
        selected_titles = pick_features_for_stories(prioritization_data)

        if selected_titles:
            # Format texte attendu par ton tool actuel (liste numérotée)
            features_for_stories_text = "\n".join([f"{i+1}. {t}" for i, t in enumerate(selected_titles)])


            with st.spinner("Génération des user stories…"):
                stories_payload = {"features": [{"title": t} for t in selected_titles]}


                stories_str = generate_stories.invoke(
                    {"features": json.dumps(stories_payload, ensure_ascii=False)}
                )

    # E) User stories (affichage)
    st.markdown("### 📝 User stories (prioritaires)")

    stories_data = try_parse_json(stories_str) if stories_str else None

    if stories_data and isinstance(stories_data, dict):
        stories = stories_data.get("stories", []) or []
        if not stories:
            st.info("Aucune story générée.")
        else:
            for s in stories:
                title = s.get("story_title") or s.get("feature_title") or "User Story"
                with st.expander(title, expanded=False):
                    st.markdown(f"**Feature :** {s.get('feature_title', '—')}")
                    st.markdown(f"**User story :** {s.get('user_story', '—')}")
                    st.markdown(f"**Complexité :** {s.get('complexity_points', '—')}")
                    crit = s.get("acceptance_criteria", []) or []
                    if crit:
                        st.markdown("**Critères d’acceptation :**")
                        for c in crit:
                            st.write(f"- {c}")
                    just = s.get("complexity_justification")
                    if just:
                        st.markdown(f"**Justification complexité :** {just}")

    elif stories_str:
        st.warning("Les stories ne sont pas un JSON valide — affichage brut.")
        st.code(stories_str, language="text")
    else:
        st.info("Pas de stories générées (aucune feature sélectionnée).")



