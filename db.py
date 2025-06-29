# db.py

import sqlite3

_conn = None

def init_db(db_path: str = "data.db") -> sqlite3.Connection:
    """
    Initialise (ou réutilise) la connexion SQLite
    et crée les tables de base si nécessaire.
    """
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        _conn.row_factory = sqlite3.Row
        cur = _conn.cursor()

        # Table 'records'
        cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                action TEXT,
                timestamp TEXT
            )
        """)

        # Table 'travel_authorizations'
        cur.execute("""
            CREATE TABLE IF NOT EXISTS travel_authorizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                user TEXT,
                destination TEXT,
                depart_date TEXT,
                return_date TEXT,
                project TEXT,
                fund TEXT,
                status TEXT,
                submitted_by TEXT,
                submitted_at TEXT,
                submitted_sig TEXT,
                verified_by TEXT,
                verified_at TEXT,
                verified_sig TEXT,
                approved_by TEXT,
                approved_at TEXT,
                approved_sig TEXT
            )
        """)

        _conn.commit()

    return _conn

# Alias pour compatibilité avec les modules existants
get_connection = init_db


# app.py

import os
import streamlit as st
from auth import login, has_access
import dashboard

from modules.travel_authorization import render as render_travel_authorization
from modules.dsa_declaration     import render as render_dsa_declaration
from modules.expenses_claim      import render as render_expenses_claim
from modules.travel_records      import render as render_travel_records
from modules.po_followup         import render as render_po_followup
from modules.meeting_forms       import render as render_meeting_forms
from modules.hd_log              import render as render_hd_log
from modules.travel_news         import render as render_travel_news
from modules.settings            import render as render_settings

CSS_PATH = "assets/style.css"


def load_css(path: str = CSS_PATH):
    if os.path.exists(path):
        with open(path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS introuvable : {path}")


def app_logout():
    """Vide session_state et relance l'app."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()


def main():
    # Configuration Streamlit
    st.set_page_config(
        page_title="🛫 HD Team Log Toolbox 🧰",
        layout="wide",
    )

    # Inject CSS
    load_css()

    # --- Header always visible ---
    col1, col2, col3 = st.columns([1,4,1])
    with col1:
        st.image("assets/hd_logo.png", width=80)
    with col2:
        st.markdown(
            "<h1 style='text-align:center; font-size:2.5rem;'>🛫 HD Team Log Toolbox 🧰</h1>",
            unsafe_allow_html=True
        )

    # --- Authentication sidebar ---
    login()
    if "user" not in st.session_state:
        return

    # --- Logout button ---
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state['user']}**")
        if st.button("🔒 Logout", key="btn_logout"):  
            app_logout()

    # --- Build tabs ---
    labels, renderers = [], []
    if has_access("dashboard"):
        labels.append("📊 Dashboard");           renderers.append(dashboard.render)
    if has_access("ta"):
        labels.append("📝 Travel Authorization"); renderers.append(render_travel_authorization)
    if has_access("dsa"):
        labels.append("💼 DSA Declaration");     renderers.append(render_dsa_declaration)
    if has_access("expenses"):
        labels.append("🧾 Expenses Claim");       renderers.append(render_expenses_claim)
    if has_access("records"):
        labels.append("🗄️ Travel Records");      renderers.append(render_travel_records)
    if has_access("po"):
        labels.append("🛒 PO Follow-up");         renderers.append(render_po_followup)
    if has_access("meeting"):
        labels.append("📅 Meeting Forms");       renderers.append(render_meeting_forms)
    if has_access("hdlog"):
        labels.append("📖 HD Log Handbook");     renderers.append(render_hd_log)
    if has_access("news"):
        labels.append("📰 Travel News");         renderers.append(render_travel_news)
    labels.append("⚙️ Settings");            renderers.append(render_settings)

    if not labels:
        st.error("Vous n'avez accès à aucun module.")
        return

    tabs = st.tabs(labels)
    for tab, fn in zip(tabs, renderers):
        with tab:
            st.markdown('<div class="module-content">', unsafe_allow_html=True)
            fn()
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
