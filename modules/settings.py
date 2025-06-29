# modules/settings.py

import os
import uuid
import streamlit as st

SIG_DIR = "assets/signatures"

def render():
    st.header("⚙️ User Configuration")

    user = st.session_state.get("user", "")
    if not user:
        st.warning("Vous devez être connecté pour accéder à la configuration.")
        return

    # --- Signature management ---
    st.subheader("🔏 Signature Management")
    user_sig = os.path.join(SIG_DIR, f"{user}.png")
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists(user_sig):
            st.image(user_sig, width=100, caption="Votre signature enregistrée")
            if st.button("🗑️ Supprimer la signature"):
                os.remove(user_sig)
                st.success("Signature supprimée.")
        else:
            st.info("Aucune signature enregistrée.")
    with col2:
        uploaded = st.file_uploader("Uploader une signature (PNG)", type=["png"], key="settings_sig_up")
        keep = st.checkbox("💾 Conserver pour les sessions futures", key="settings_keep_sig")
        if uploaded and keep:
            os.makedirs(SIG_DIR, exist_ok=True)
            with open(user_sig, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("Signature enregistrée définitivement.")

    st.markdown("---")

    # --- Creative Top 10 To-Do List ---
    st.subheader("📝 Top 10 To-Do List")

    # Initialisation
    if "todos" not in st.session_state:
        st.session_state.todos = []

    # Ajout de tâche
    new_task = st.text_input("Nouvelle tâche", key="new_task_input")
    add_col, _ = st.columns([1, 9])
    if add_col.button("➕ Ajouter"):
        if not new_task:
            st.error("Veuillez saisir une description de tâche.")
        elif len(st.session_state.todos) >= 10:
            st.warning("Vous avez déjà 10 tâches. Supprimez-en une pour en ajouter.")
        else:
            st.session_state.todos.append({
                "id": str(uuid.uuid4()),
                "task": new_task,
                "done": False
            })
            # on relance pour réinitialiser le text_input
            st.experimental_rerun()

    # Affichage de la progression
    total = len(st.session_state.todos)
    if total > 0:
        done_count = sum(t["done"] for t in st.session_state.todos)
        st.markdown(f"**Progression : {done_count} / {total} terminées**")
        st.progress(done_count / total)

    # Liste des tâches en cartes
    to_remove = None
    for idx, todo in enumerate(st.session_state.todos):
        st.markdown(
            "<div style='background:#f0f4f8; padding:10px; border-radius:8px; margin-bottom:6px;'>",
            unsafe_allow_html=True
        )
        c_task, c_done, c_del = st.columns([8, 1, 1])
        # Édition de la description
        new_desc = c_task.text_input(
            "", value=todo["task"], key=f"task_{todo['id']}"
        )
        st.session_state.todos[idx]["task"] = new_desc

        # Checkbox Terminé
        done_val = c_done.checkbox(
            "", value=todo["done"], key=f"done_{todo['id']}"
        )
        st.session_state.todos[idx]["done"] = done_val

        # Bouton Supprimer
        if c_del.button("🗑️", key=f"del_{todo['id']}"):
            to_remove = idx

        st.markdown("</div>", unsafe_allow_html=True)

    # Suppression si demandé
    if to_remove is not None:
        st.session_state.todos.pop(to_remove)
        st.experimental_rerun()
