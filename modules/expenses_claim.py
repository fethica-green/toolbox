# modules/expenses_claim.py

import os
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from db import get_connection
from utils import to_excel

def render():
    """
    Module de dépôt et suivi des notes de frais.
    - 🆕 Saisie d’une nouvelle dépense
    - 📋 Consultation & export des dépenses existantes
    """
    st.header("🧾 Expenses Claim")
    conn = get_connection()
    cursor = conn.cursor()

    # Onglets : création vs consultation
    tab_new, tab_view = st.tabs(["➕ New Claim", "📋 View Claims"])

    # --- Création d'une nouvelle note de frais ---
    with tab_new:
        st.subheader("Create New Expense Claim")
        with st.form("expense_form"):
            declaration_id = st.number_input(
                "DSA Declaration ID", min_value=1, step=1, help="Référence à l'ID de la déclaration DSA"
            )
            expense_date = st.date_input(
                "Expense Date", date.today()
            )
            category = st.selectbox(
                "Category", ["Transport", "Accommodation", "Meal", "Miscellaneous"]
            )
            amount = st.number_input(
                "Amount", min_value=0.0, format="%.2f"
            )
            receipt = st.file_uploader(
                "Upload Receipt (PDF, JPG, PNG)", type=["pdf", "jpg", "png"]
            )
            submitted = st.form_submit_button("Submit Claim")

            if submitted:
                # Sauvegarde du justificatif
                receipt_path = None
                if receipt:
                    os.makedirs("receipts", exist_ok=True)
                    filename = f"{declaration_id}_{expense_date}_{receipt.name}"
                    receipt_path = os.path.join("receipts", filename)
                    with open(receipt_path, "wb") as f:
                        f.write(receipt.getbuffer())

                # Insertion en base
                cursor.execute(
                    """
                    INSERT INTO expenses
                        (declaration_id, expense_date, category, amount, receipt_path)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        declaration_id,
                        expense_date.isoformat(),
                        category,
                        amount,
                        receipt_path,
                    )
                )
                conn.commit()
                st.success("✅ Expense claim submitted.")

    # --- Consultation des notes de frais ---
    with tab_view:
        st.subheader("All Expense Claims")
        df = pd.read_sql("SELECT * FROM expenses", conn)

        if df.empty:
            st.info("No expense claims available.")
            return

        # Filtres
        cols_to_filter = ["declaration_id", "category"]
        for col in cols_to_filter:
            vals = df[col].unique().tolist()
            sel = st.multiselect(f"Filter by {col}", vals, default=vals, key=f"exp_flt_{col}")
            df = df[df[col].isin(sel)]

        # Affichage interactif
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=False)
        AgGrid(
            df,
            gridOptions=gb.build(),
            height=300,
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.NO_UPDATE,
        )

        # Export Excel
        buf = BytesIO()
        buf.write(to_excel(df))
        st.download_button(
            "⬇️ Download as Excel",
            buf.getvalue(),
            file_name="expenses_claims.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
