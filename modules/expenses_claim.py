import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("🧾 Expenses Claim")

    # A décommenter pour vraie BDD
    # conn = init_db()
    # df = pd.read_sql("SELECT * FROM expenses_claim", conn)

    # Exemple fictif
    df = pd.DataFrame([
        {"ID": 101, "Voyageur": "Alice Dupont",   "Montant": "250.00 CHF", "Date soumission": "2025-01-20"},
        {"ID": 102, "Voyageur": "Bob Martin",     "Montant": "180.50 CHF", "Date soumission": "2025-02-10"},
        {"ID": 103, "Voyageur": "Charlie Laurent","Montant": "320.75 CHF", "Date soumission": "2025-03-12"},
    ])

    st.dataframe(df)
