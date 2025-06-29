import streamlit as st
import pandas as pd
from db import init_db

def render():
    st.header("🛒 PO Follow-up")

    # Pour production :
    # conn = init_db()
    # df = pd.read_sql("SELECT * FROM po_followup", conn)

    # Prototype :
    df = pd.DataFrame([
        {"PO #": "PO-2025-001", "Fournisseur": "ACME SA",        "Montant": "1 200 CHF", "Statut": "Approuvé"},
        {"PO #": "PO-2025-002", "Fournisseur": "LogiTrans SARL", "Montant": "3 500 CHF", "Statut": "En attente"},
        {"PO #": "PO-2025-003", "Fournisseur": "EventCo Ltd",   "Montant": "2 750 CHF", "Statut": "Vérifié"},
    ])

    st.table(df)
