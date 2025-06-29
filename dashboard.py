# modules/dashboard.py

import streamlit as st
import pandas as pd
from db import init_db  # Use init_db or get_connection alias


def render():
    st.header("📊 Dashboard Principal")

    # Connexion à la base (records doit exister via init_db())
    conn = init_db()
    cur = conn.cursor()

    # Comptage des actions
    cur.execute("SELECT COUNT(*) FROM records")
    total_actions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM travel_authorizations WHERE status = 'Pending Verification'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM travel_authorizations WHERE status = 'Verified'")
    verified = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM travel_authorizations WHERE status = 'Approved'")
    approved = cur.fetchone()[0]

    # Affichage des KPI
    cols = st.columns(4)
    cols[0].metric("Total Actions", total_actions)
    cols[1].metric("En attente", pending)
    cols[2].metric("Vérifiées", verified)
    cols[3].metric("Approuvées", approved)

    st.markdown("---")

    # Journal des actions
    st.subheader("Journal des actions")
    df = pd.read_sql("SELECT timestamp AS 'Date/Heure', user AS 'Utilisateur', action AS 'Action' FROM records ORDER BY id DESC", conn)
    st.dataframe(df)  # Use dataframe instead of experimental_data_editor
