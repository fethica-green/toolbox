import streamlit as st
from config import CREDENTIALS, ACCESS

def login():
    """
    Affiche le formulaire de connexion et gère la session utilisateur.
    Met à jour st.session_state.user et st.session_state.role en cas de succès.
    """
    if "user" not in st.session_state:
        st.session_state.user = None
        st.session_state.role = None

    # Si pas encore connecté, on affiche le formulaire
    if not st.session_state.user:
        with st.form("login_form"):
            user_input = st.text_input("🔑 Identifiant")
            pwd_input  = st.text_input("🔒 Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter")
            if submitted:
                cred = CREDENTIALS.get(user_input.upper())
                if cred and cred["pwd"] == pwd_input:
                    # Connexion réussie
                    st.session_state.user = user_input.upper()
                    st.session_state.role = cred["role"]
                    st.success(f"Connecté·e en tant que « {st.session_state.role} »")
                else:
                    st.error("⚠️ Identifiant ou mot de passe invalide")
        # On stoppe l'exécution tant que l'utilisateur n'est pas connecté
        st.stop()

def has_access(module_key: str) -> bool:
    """
    Vérifie si le rôle courant a le droit d'accéder au module identifié par module_key.
    Ex : module_key = "dashboard", "ta", "expenses", etc.
    """
    role = st.session_state.get("role")
    if not role:
        return False
    return module_key in ACCESS.get(role, [])
