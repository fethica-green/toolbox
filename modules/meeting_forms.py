import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("📅 Meeting Forms")

    # En production, décommentez :
    # conn = init_db()
    # df = pd.read_sql("SELECT * FROM meeting_forms", conn)

    # Prototype avec données fictives
    df = pd.DataFrame([
        {"ID": 201, "Sujet": "Réunion Projet A",    "Date": "2025-02-14", "Participants": 5},
        {"ID": 202, "Sujet": "Atelier Sécurité",      "Date": "2025-03-01", "Participants": 12},
        {"ID": 203, "Sujet": "Briefing Budgets",      "Date": "2025-04-10", "Participants": 8},
    ])

    st.table(df)
