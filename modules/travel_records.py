# modules/travel_records.py

import streamlit as st
import pandas as pd
from datetime import date
from db import get_connection

def render():
    """
    Module Travel Records
    - 📥 Enregistrer le retour et le coût final d’une mission
    - 📋 Consulter l’historique des retours
    """
    st.header("🗄️ Travel Records")

    conn = get_connection()
    cursor = conn.cursor()

    tab_record, tab_view = st.tabs(["📥 Record Travel", "📋 View Records"])

    # --- Enregistrement d’un retour de mission ---
    with tab_record:
        st.subheader("Record Travel Return")
        with st.form("record_form"):
            auth_id             = st.number_input(
                "Travel Authorization ID", min_value=1, step=1,
                help="ID de la TA créée dans l’onglet Travel Authorization"
            )
            final_fare          = st.number_input(
                "Final Fare (€)", min_value=0.0, format="%.2f"
            )
            actual_return_date  = st.date_input(
                "Actual Return Date", date.today()
            )
            submitted = st.form_submit_button("Submit Record")
            if submitted:
                cursor.execute(
                    """
                    INSERT INTO travel_records
                        (authorization_id, final_fare, actual_return_date)
                    VALUES (?, ?, ?)
                    """,
                    (
                        auth_id,
                        final_fare,
                        actual_return_date.isoformat()
                    )
                )
                conn.commit()
                st.success("✅ Travel record saved.")

    # --- Consultation des retours de mission ---
    with tab_view:
        st.subheader("All Travel Records")
        df = pd.read_sql(
            "SELECT * FROM travel_records ORDER BY actual_return_date DESC", conn
        )
        if df.empty:
            st.info("No travel records yet.")
        else:
            # Format des dates pour l’affichage
            df["actual_return_date"] = pd.to_datetime(df["actual_return_date"]).dt.date
            st.dataframe(df, use_container_width=True)
