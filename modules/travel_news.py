# modules/travel_news.py

import streamlit as st
import pandas as pd
from datetime import date
from db import get_connection

def render():
    """
    Module Travel News
    - ➕ Ajouter une actualité voyage
    - 📋 Consulter les actualités enregistrées
    """
    st.header("📰 Travel News")

    conn = get_connection()
    cursor = conn.cursor()

    tab_new, tab_view = st.tabs(["➕ Add News", "📋 View News"])

    with tab_new:
        st.subheader("Add Travel News")
        with st.form("news_form"):
            title = st.text_input("Title")
            url = st.text_input("URL")
            published_date = st.date_input("Published Date", date.today())
            snippet = st.text_area("Snippet / Summary")
            submitted = st.form_submit_button("Submit News")
            if submitted:
                cursor.execute(
                    """
                    INSERT INTO travel_news
                        (title, url, published_date, snippet)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        title.strip(),
                        url.strip(),
                        published_date.isoformat(),
                        snippet.strip()
                    )
                )
                conn.commit()
                st.success("✅ News item added.")

    with tab_view:
        st.subheader("All Travel News")
        df = pd.read_sql("SELECT * FROM travel_news ORDER BY published_date DESC", conn)
        if df.empty:
            st.info("No travel news available.")
        else:
            # Format published_date for display
            df["published_date"] = pd.to_datetime(df["published_date"]).dt.date
            # Display as interactive table
            st.dataframe(df, use_container_width=True)
