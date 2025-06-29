# modules/dsa_declaration.py

import streamlit as st
import pandas as pd
from datetime import date, time, datetime
from io import BytesIO
from db import get_connection
from utils import to_excel
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def render():
    """
    Module de déclaration des DSA (Daily Subsistence Allowance).
    Permet de créer une nouvelle mission DSA et de consulter l'historique.
    """
    st.header("💼 DSA Declaration")
    with st.expander("❓ How to fill DSA Declaration"):
        st.write(
            "- Select country & city  ",
            "- Enter TA No., codes & budget  ",
            "- Fill departure/return date & time  ",
            "- Adjust lunch/dinner/full deductions  ",
            "- Upload justificatifs (billet d'avion, boarding pass…)  ",
            "- Save and review missions",
            sep="\n"
        )

    @st.cache_data
    def load_dsa_rates():
        df = pd.read_excel("Perdiem DSA 2025 par pays.xlsx",
                           sheet_name="Feuil1", skiprows=4)
        df = df[['Country','Area','Full DSA.1','Lunch only.1','Dinner only.1']] \
               .dropna(subset=['Country'])
        df.columns = ['Country','Area','Full_DSA','Lunch_Only','Dinner_Only']
        df['Country'] = df['Country'].str.strip()
        df['Area'] = df['Area'].str.strip()
        df['Area'] = df.apply(
            lambda r: f"Elsewhere ({r['Country']})"
                      if r['Area'].lower()=="elsewhere"
                      else r['Area'],
            axis=1
        )
        return df

    dsa_df = load_dsa_rates()  # Chargement des taux DSA :contentReference[oaicite:0]{index=0}

    # Initialisation du state
    for key, init in [
        ('missions', []),
        ('ded_lunch', 0),
        ('ded_dinner', 0),
        ('ded_full', 0),
        ('dsa_files', [])
    ]:
        if key not in st.session_state:
            st.session_state[key] = init

    tab_new, tab_view = st.tabs(["➕ Create Mission", "📋 View Missions"])

    with tab_new:
        # Saisie des infos de mission
        c1, c2, c3 = st.columns(3)
        name    = c1.text_input("Traveler's Name", key="dsa_nm")
        ta_no   = c2.text_input("TA No.",            key="dsa_tano")
        country = c3.selectbox("Country", sorted(dsa_df['Country']),
                               key="dsa_ct")
        city    = st.selectbox("City",
                               sorted(dsa_df[dsa_df['Country']==country]['Area']),
                               key="dsa_city")

        p1, p2, p3, p4 = st.columns(4)
        pj = p1.text_input("Project Code", key="dsa_pj")
        fd = p2.text_input("Fund Code",    key="dsa_fd")
        ac = p3.text_input("Activity Code",key="dsa_ac")
        bd = p4.text_input("Budget Line",  key="dsa_bd")

        dcol, rcol = st.columns(2)
        dep_d = dcol.date_input("Dep Date",   date.today(), key="dsa_dd")
        dep_t = dcol.time_input("Dep Time",   time(8,0),      key="dsa_dt")
        ret_d = rcol.date_input("Ret Date",   date.today(), key="dsa_rd")
        ret_t = rcol.time_input("Ret Time",   time(20,0),   key="dsa_rt")

        st.subheader("➖ Deductions")
        dl, dm, df_ = st.columns(3)
        with dl:
            st.write(f"Lunch deductions: {st.session_state.ded_lunch}")
            if st.button("+ Lunch", key="dsa_al"): st.session_state.ded_lunch += 1
            if st.button("– Lunch", key="dsa_sl") and st.session_state.ded_lunch > 0:
                st.session_state.ded_lunch -= 1
        with dm:
            st.write(f"Dinner deductions: {st.session_state.ded_dinner}")
            if st.button("+ Dinner", key="dsa_ad"): st.session_state.ded_dinner += 1
            if st.button("– Dinner", key="dsa_sd") and st.session_state.ded_dinner > 0:
                st.session_state.ded_dinner -= 1
        with df_:
            st.write(f"Full-day deductions: {st.session_state.ded_full}")
            if st.button("+ Full DSA", key="dsa_af"): st.session_state.ded_full += 1
            if st.button("– Full DSA", key="dsa_sf") and st.session_state.ded_full > 0:
                st.session_state.ded_full -= 1

        # Upload des justificatifs
        uploads = st.file_uploader("Upload justificatifs",
                                   type=['pdf','jpg','png'],
                                   accept_multiple_files=True,
                                   key="dsa_up")
        if uploads:
            for f in uploads:
                if f.name not in [x.name for x in st.session_state.dsa_files]:
                    st.session_state.dsa_files.append(f)

        # Sauvegarde de la mission DSA
        if st.button("✅ Save Mission", key="dsa_save"):
            # Calcul DSA
            rate = dsa_df[
                (dsa_df['Country']==country)&(dsa_df['Area']==city)
            ].iloc[0]
            full, lun, din = rate['Full_DSA'], rate['Lunch_Only'], rate['Dinner_Only']
            dt_dep = datetime.combine(dep_d, dep_t)
            dt_ret = datetime.combine(ret_d, ret_t)
            days   = (dt_ret.date() - dt_dep.date()).days + 1
            d_dep  = full if dep_t < time(10,0) else (din if dep_t <= time(14,0) else 0)
            d_ret  = full if ret_t > time(19,0) else (lun if ret_t >= time(13,0) else 0)
            mid    = max(0, days - 2)
            tot    = d_dep + d_ret + mid * full
            ded    = (st.session_state.ded_lunch * lun +
                      st.session_state.ded_dinner * din +
                      st.session_state.ded_full * full)
            final  = tot - ded

            st.session_state.missions.append({
                'Name': name, 'TA No.': ta_no,
                'Country': country, 'City': city,
                'Dep':     dt_dep, 'DSA Dep': d_dep,
                'Ret':     dt_ret, 'DSA Ret': d_ret,
                'Mid Days': mid,
                'Lunch Ded': st.session_state.ded_lunch,
                'Dinner Ded': st.session_state.ded_dinner,
                'Full Ded':   st.session_state.ded_full,
                'Total DSA':  final,
                'Attachments': len(st.session_state.dsa_files)
            })
            st.success("Mission DSA enregistrée.")  # :contentReference[oaicite:1]{index=1}

    with tab_view:
        st.subheader("All DSA Missions")
        if st.session_state.missions:
            df = pd.DataFrame(st.session_state.missions)
            for col in ['Name','Country']:
                flt = st.multiselect(f"Filter by {col}", df[col].unique(),
                                     key=f"dsa_flt_{col}")
                if flt:
                    df = df[df[col].isin(flt)]
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=True)
            AgGrid(df, gridOptions=gb.build(), update_mode=GridUpdateMode.MODEL_CHANGED)

            # Bouton de téléchargement Excel
            buf = BytesIO()
            buf.write(to_excel(df))
            st.download_button(
                "⬇️ Download Excel",
                buf.getvalue(),
                file_name="dsa_missions.xlsx",
                key="dsa_dl"
            )
        else:
            st.info("No missions.")  # :contentReference[oaicite:2]{index=2}
