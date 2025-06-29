import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("📰 Travel News")

    # En production :
    # conn = init_db()
    # df = pd.read_sql("SELECT * FROM travel_news ORDER BY date DESC", conn)

    # Exemple fictif
    df = pd.DataFrame([
        {"Date": "2025-06-01", "Titre": "Nouvelle liaison GVA-LIS", "Source": "Airline News"},
        {"Date": "2025-06-10", "Titre": "Changements de visa Chine", "Source": "Gov Travel"},
        {"Date": "2025-06-20", "Titre": "Grève SNCF prévue",        "Source": "Local News"},
    ])

    st.dataframe(df)
