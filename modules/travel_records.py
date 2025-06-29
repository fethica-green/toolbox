import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("🗄️ Travel Records")

    # Utilisez la BDD quand vous serez prêts
    # conn = init_db()
    # df = pd.read_sql("SELECT * FROM records ORDER BY date DESC", conn)

    # Pour l’instant, données fictives
    df = pd.DataFrame([
        {"ID": 1, "Voyageur": "Alice Dupont",    "Destination": "NYC", "Date": "2025-01-15", "Statut": "Approuvé"},
        {"ID": 2, "Voyageur": "Bob Martin",      "Destination": "PAR", "Date": "2025-02-03", "Statut": "Vérifié"},
        {"ID": 3, "Voyageur": "Charlie Laurent", "Destination": "TOK", "Date": "2025-03-20", "Statut": "En attente"},
        {"ID": 4, "Voyageur": "Dana Smith",      "Destination": "BRU", "Date": "2025-04-05", "Statut": "Approuvé"},
    ])

    st.dataframe(df)
