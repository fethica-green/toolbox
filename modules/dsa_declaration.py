import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("💼 DSA Declaration")

    # Exemple de connexion (à décommenter pour vraie BDD)
    # conn = init_db()

    # Données fictives pour prototypage
    df = pd.DataFrame({
        "Date": ["2025-01-15", "2025-02-03", "2025-03-20"],
        "Voyageur": ["Alice Dupont", "Bob Martin", "Charlie Laurent"],
        "DSA (CHF/jour)": [75, 80, 75],
        "Nombre de jours": [3, 2, 4],
    })
    df["Total (CHF)"] = df["DSA (CHF/jour)"] * df["Nombre de jours"]

    st.table(df.style.format({"Total (CHF)": "{:.2f}"}))
