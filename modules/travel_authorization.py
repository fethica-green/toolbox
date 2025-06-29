# modules/travel_authorization.py

import os
import sqlite3
import zipfile
from io import BytesIO
from datetime import date, datetime, time as dt_time

import streamlit as st
import pandas as pd
from fpdf import FPDF

from db import init_db
from utils import to_excel

SIG_DIR = "assets/signatures"

def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        params = dict(st.query_params)
        params["reload"] = [str(int(datetime.now().timestamp()))]
        st.query_params = params

def get_initials(fullname: str) -> str:
    parts = fullname.split()
    if len(parts) < 2:
        return fullname[:3].upper()
    return (parts[0][0] + parts[-1][:2]).upper()

def next_sequence(conn: sqlite3.Connection, initials: str, year: str) -> str:
    cur = conn.cursor()
    pattern = f"TA-{initials}-{year}-%"
    cur.execute("SELECT code FROM travel_authorizations WHERE code LIKE ? ORDER BY code DESC LIMIT 1", (pattern,))
    row = cur.fetchone()
    if not row:
        return "001"
    last = int(row[0].rsplit("-", 1)[-1])
    return f"{last+1:03d}"

class TA_PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=False, margin=10)
        self.set_margins(left=10, top=20, right=10)

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Travel Authorization", ln=True, align="C")
        self.ln(5)

    def add_section(self, label: str, user: str, ts: str, sig_path: str):
        self.set_font("Arial", size=12)
        text = f"{label} by {user} on {ts}"
        self.cell(0, 8, text, ln=True)
        # draw signature at fixed right margin
        sig_w = 25
        x_img = self.w - self.r_margin - sig_w
        y_img = self.get_y() - 8
        if sig_path and os.path.exists(sig_path):
            try:
                self.image(sig_path, x=x_img, y=y_img, w=sig_w)
            except RuntimeError:
                pass
        self.ln(12)

def create_pdf(record: dict) -> bytes:
    pdf = TA_PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # general info
    for field in ("code","user","destination","depart_date","return_date","project","fund"):
        pdf.cell(0, 8, f"{field.capitalize()}: {record[field]}", ln=True)
    pdf.ln(5)
    # sections
    pdf.add_section("Submitted", record.get("submitted_by",""), record.get("submitted_at",""), record.get("submitted_sig",""))
    if record.get("status") in ("Verified","Approved"):
        pdf.add_section("Verified", record.get("verified_by",""), record.get("verified_at",""), record.get("verified_sig",""))
    if record.get("status") == "Approved":
        pdf.add_section("Approved", record.get("approved_by",""), record.get("approved_at",""), record.get("approved_sig",""))
    return pdf.output(dest="S").encode("latin1")

def render():
    st.header("📝 Travel Authorization")

    os.makedirs(SIG_DIR, exist_ok=True)
    conn = init_db()
    cursor = conn.cursor()
    role = st.session_state.get("role","")
    user = st.session_state.get("user","")

    # prompt signature upload
    sig_path = os.path.join(SIG_DIR, f"{user}.png")
    if role in ("Logistics","AdminHR","Manager","ProjectAdmin") and not os.path.exists(sig_path):
        st.warning("Please upload your signature (PNG) for inclusion in PDFs:")
        uploaded = st.file_uploader("Signature file", type=["png"], key="sig_up")
        if uploaded:
            with open(sig_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("Signature saved.")

    tab_new, tab_view = st.tabs(["➕ New TA","📋 Manage TAs"])

    created = None
    # New TA
    with tab_new:
        if role == "Logistics":
            st.subheader("Create Travel Authorization")
            with st.form("ta_form"):
                fullname = st.text_input("Traveler Full Name")
                dest = st.text_input("Destination")
                dep_d = st.date_input("Departure Date", date.today())
                dep_t = st.time_input("Departure Time", dt_time(8,0))
                ret_d = st.date_input("Return Date", date.today())
                ret_t = st.time_input("Return Time", dt_time(18,0))
                proj = st.text_input("Project Code")
                fund = st.text_input("Fund Code")
                if st.form_submit_button("Submit TA"):
                    initials = get_initials(fullname)
                    year = datetime.now().strftime("%y")
                    seq = next_sequence(conn, initials, year)
                    code = f"TA-{initials}-{year}-{seq}"
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sub_sig = sig_path if os.path.exists(sig_path) else ""
                    cursor.execute("""
                        INSERT INTO travel_authorizations
                        (code,user,destination,depart_date,return_date,project,fund,
                         status,submitted_by,submitted_at,submitted_sig)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        code, fullname, dest,
                        datetime.combine(dep_d,dep_t).isoformat(),
                        datetime.combine(ret_d,ret_t).isoformat(),
                        proj, fund,
                        "Pending Verification",
                        user, ts, sub_sig
                    ))
                    conn.commit()
                    st.success(f"✅ Created {code}")
                    created = {
                        "code": code, "user": fullname, "destination": dest,
                        "depart_date": dep_d, "return_date": ret_d,
                        "project": proj, "fund": fund,
                        "status": "Pending Verification",
                        "submitted_by": user, "submitted_at": ts, "submitted_sig": sub_sig,
                        "verified_by":"", "verified_at":"", "verified_sig":"",
                        "approved_by":"", "approved_at":"", "approved_sig":""
                    }
        else:
            st.info("Only Logistics Coordinators can create TAs.")

    # download created PDF
    if created:
        pdf_bytes = create_pdf(created)
        st.download_button(
            "📄 Download Submitted TA PDF",
            data=pdf_bytes,
            file_name=f"{created['code']}_submitted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            key=f"dl_{created['code']}_submitted"
        )

    # Manage workflow
    with tab_view:
        st.subheader("Manage Travel Authorizations")
        df = pd.read_sql("SELECT * FROM travel_authorizations ORDER BY depart_date DESC", conn)
        if df.empty:
            st.info("No travel authorizations found.")
            return

        for _, row in df.iterrows():
            st.markdown(f"**{row['code']}** — Status: **{row['status']}**")
            c1, c2, c3 = st.columns([1,1,1])

            # Verify
            if role == "AdminHR" and row["status"] == "Pending Verification":
                if c1.button("✅ Verify", key=f"v_{row['id']}"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ver_sig = sig_path if os.path.exists(sig_path) else ""
                    cursor.execute("""
                        UPDATE travel_authorizations
                        SET status=?, verified_by=?, verified_at=?, verified_sig=?
                        WHERE id=?
                    """, ("Verified", user, ts, ver_sig, row["id"]))
                    conn.commit()
                    st.success("Verified.")
                    safe_rerun()

            # Approve
            if role in ("Manager","ProjectAdmin") and row["status"] == "Verified":
                if c2.button("🆗 Approve", key=f"a_{row['id']}"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    apr_sig = sig_path if os.path.exists(sig_path) else ""
                    cursor.execute("""
                        UPDATE travel_authorizations
                        SET status=?, approved_by=?, approved_at=?, approved_sig=?
                        WHERE id=?
                    """, ("Approved", user, ts, apr_sig, row["id"]))
                    conn.commit()
                    st.success("Approved.")
                    safe_rerun()

            # Download PDF (all statuses)
            data = row.to_dict()
            for k in ("submitted_by","submitted_at","submitted_sig",
                      "verified_by","verified_at","verified_sig",
                      "approved_by","approved_at","approved_sig"):
                data.setdefault(k, "")
            pdf_bytes = create_pdf(data)
            c3.download_button(
                "📄 Download TA PDF",
                data=pdf_bytes,
                file_name=f"{row['code']}_{row['status'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key=f"dl_{row['id']}_{row['status']}"
            )

            st.markdown("---")
