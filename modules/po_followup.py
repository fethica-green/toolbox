# modules/po_followup.py

import streamlit as st
import pandas as pd
from datetime import date
from db import get_connection

def render():
    """
    Module PO Follow-up
    - ➕ Create or update a Purchase Order
    - 📋 View & filter POs
    """
    st.header("🛒 PO Follow-up")

    conn = get_connection()
    cursor = conn.cursor()

    tab_new, tab_view = st.tabs(["➕ New / Update PO", "📋 View POs"])

    with tab_new:
        st.subheader("Create or Update PO")
        with st.form("po_form"):
            po_number    = st.text_input("PO Number")
            vendor       = st.text_input("Vendor")
            amount       = st.number_input("Amount", min_value=0.0, format="%.2f")
            status       = st.selectbox("Status", ["Open", "Pending", "Closed"])
            expected_date = st.date_input("Expected Delivery Date", date.today())
            submitted    = st.form_submit_button("Save PO")
            if submitted:
                # Check if PO exists
                cursor.execute(
                    "SELECT id FROM po_followup WHERE po_number = ?",
                    (po_number.strip(),)
                )
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        """
                        UPDATE po_followup
                        SET vendor = ?, amount = ?, status = ?, expected_date = ?
                        WHERE po_number = ?
                        """,
                        (vendor, amount, status, expected_date.isoformat(), po_number.strip())
                    )
                    st.success(f"✅ PO {po_number} mise à jour.")
                else:
                    cursor.execute(
                        """
                        INSERT INTO po_followup
                            (po_number, vendor, amount, status, expected_date)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (po_number.strip(), vendor, amount, status, expected_date.isoformat())
                    )
                    st.success(f"✅ PO {po_number} créée.")
                conn.commit()

    with tab_view:
        st.subheader("All Purchase Orders")
        df = pd.read_sql("SELECT * FROM po_followup ORDER BY expected_date DESC", conn)

        if df.empty:
            st.info("Aucune PO enregistrée.")
            return

        # Filtres interactifs
        cols = {
            "status": "Status",
            "vendor": "Vendor"
        }
        for col, label in cols.items():
            vals = df[col].unique().tolist()
            sel = st.multiselect(f"Filter by {label}", vals, default=vals, key=f"po_flt_{col}")
            df = df[df[col].isin(sel)]

        # Format expected_date
        df["expected_date"] = pd.to_datetime(df["expected_date"]).dt.date

        # Affichage
        st.dataframe(df, use_container_width=True)
