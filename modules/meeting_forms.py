# modules/meeting_forms.py

import streamlit as st
import pandas as pd
from datetime import date
from db import get_connection

def render():
    """
    Module Meeting Forms
    - ➕ Create a new meeting form
    - 📋 View submitted meeting forms
    """
    st.header("📅 Meeting Forms")

    conn = get_connection()
    cursor = conn.cursor()

    tab_new, tab_view = st.tabs(["➕ New Form", "📋 View Forms"])

    with tab_new:
        st.subheader("Create New Meeting Form")
        with st.form("meeting_form"):
            organizer    = st.text_input("Organizer", st.session_state.get("user", ""))
            subject      = st.text_input("Subject")
            meeting_date = st.date_input("Meeting Date", date.today())
            location     = st.text_input("Location")
            attendees    = st.text_area("Attendees (comma-separated)")
            submitted    = st.form_submit_button("Submit Form")
            if submitted:
                cursor.execute(
                    """
                    INSERT INTO meeting_forms
                        (organizer, subject, meeting_date, location, attendees)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        organizer,
                        subject,
                        meeting_date.isoformat(),
                        location,
                        attendees
                    )
                )
                conn.commit()
                st.success("✅ Meeting form submitted.")

    with tab_view:
        st.subheader("All Meeting Forms")
        df = pd.read_sql("SELECT * FROM meeting_forms ORDER BY meeting_date DESC", conn)
        if df.empty:
            st.info("No meeting forms available.")
        else:
            # Convert meeting_date to date
            df["meeting_date"] = pd.to_datetime(df["meeting_date"]).dt.date
            # Show as interactive table
            st.dataframe(df, use_container_width=True)
