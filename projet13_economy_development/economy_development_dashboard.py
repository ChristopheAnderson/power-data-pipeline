# -*- coding: utf-8 -*-
"""
Projet 13 - Streamlit Dashboard: Tableau de Bord Macro-Économique & Développement Durable
(PIB, PIB/Hab, Inflation, Chômage, Déchets, Urbanisation — World Bank API Réelle)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests, os, sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path: sys.path.insert(0, dir_path)
if parent_dir not in sys.path: sys.path.insert(0, parent_dir)

WB_BASE = "https://api.worldbank.org/v2"
CEDEAO_ISO = "BEN;GHA;CIV;NGA;NER;BFA;TGO;SEN;MLI;GIN"

INDICATORS = {
    "NY.GDP.MKTP.CD": "PIB Total (USD)",
    "NY.GDP.PCAP.CD": "PIB / Habitant (USD)",
    "FP.CPI.TOTL.ZG": "Inflation (%)",
    "SL.UEM.TOTL.ZS": "Chômage (%)",
    "SI.POV.DDAY": "Pauvreté <2.15$/j (%)",
    "EN.URB.MCTY.TL.ZS": "Population Urbaine (%)",
    "EG.ELC.ACCS.ZS": "Accès Électricité (%)",
    "IT.NET.USER.ZS": "Utilisateurs Internet (%)",
    "SE.ADT.LITR.ZS": "Alphabétisation (%)"
}

@st.cache_data(ttl=3600)
def fetch_wb(indicator_code, countries=CEDEAO_ISO, mrv=25):
    url = f"{WB_BASE}/country/{countries}/indicator/{indicator_code}?format=json&mrv={mrv}&per_page=500"
    try:
        resp = requests.get(url, timeout=12)
        if resp.status_code == 200:
            raw = resp.json()
            if len(raw) >= 2 and raw[1]:
                records = [{"pays": i.get("country", {}).get("value"), "pays_code": i.get("countryiso3code"),
                            "annee": int(i.get("date", 0)), "valeur": i.get("value")}
                           for i in raw[1] if i.get("value") is not None]
                return pd.DataFrame(records).sort_values(["pays", "annee"])
    except Exception as e:
        st.error(f"Erreur API: {e}")
    return pd.DataFrame()

def render_projet13():
    st.header("📊 Projet 13 : Macro-Économie & Développement Durable (World Bank API Réelle — CEDEAO / Bénin)")
    st.markdown("""
    **Source : [World Bank Open Data API](https://data.worldbank.org) ✅ — 100% Gratuit, sans clé**
    - **PIB, PIB/Habitant, Inflation, Chômage, Pauvreté, Urbanisation, Électricité, Internet, Alphabétisation.**
    - Tableau de bord multi-indicateurs comparatif entre les **12 pays de la CEDEAO**.
    > *💡 Enjeux : ODD 1 (Pauvreté), ODD 8 (Travail Décent), ODD 10 (Inégalités) | Agenda 2063 UA | PAG 2 Bénin.*
    """)

    tab1, tab2, tab3 = st.tabs(["💰 PIB & Économie", "💼 Emploi & Pauvreté", "🌐 Indicateurs de Société"])

    # === TAB 1: PIB ===
    with tab1:
        st.subheader("💰 Produit Intérieur Brut — Bénin & CEDEAO")
        with st.spinner("Chargement données PIB (World Bank)..."):
            df_gdp = fetch_wb("NY.GDP.MKTP.CD")
            df_gdppc = fetch_wb("NY.GDP.PCAP.CD")

        if not df_gdp.empty:
            df_gdp_b = df_gdp[df_gdp['pays_code'] == 'BEN'].sort_values('annee')
            if not df_gdp_b.empty:
                latest = df_gdp_b.iloc[-1]
                oldest = df_gdp_b.iloc[0]
                m1, m2, m3 = st.columns(3)
                m1.metric("PIB Bénin (Dernière Année)", f"${latest['valeur']/1e9:.2f} Milliards USD", f"({int(latest['annee'])})")
                m2.metric("PIB Bénin Début Période", f"${oldest['valeur']/1e9:.2f} Milliards", f"({int(oldest['annee'])})")
                growth = ((latest['valeur'] / oldest['valeur']) ** (1/(latest['annee'] - oldest['annee'])) - 1) * 100
                m3.metric("Croissance Annuelle Moy.", f"+{growth:.1f} % / an")

            df_gdp['valeur_mrd'] = df_gdp['valeur'] / 1e9
            fig_gdp = px.line(df_gdp, x='annee', y='valeur_mrd', color='pays',
                title="Évolution du PIB (Milliards USD) — Pays CEDEAO",
                labels={"valeur_mrd": "PIB (Milliards $)", "annee": "Année"})
            st.plotly_chart(fig_gdp, use_container_width=True)

        if not df_gdppc.empty:
            latest_gdppc = df_gdppc.sort_values("annee").groupby("pays").last().reset_index()
            fig_pc = px.bar(latest_gdppc.sort_values("valeur", ascending=False), x='pays', y='valeur',
                color='valeur', color_continuous_scale='Viridis',
                title="PIB par Habitant (USD) — Comparaison CEDEAO (Dernière Année Disponible)",
                labels={"valeur": "PIB / Habitant ($)", "pays": "Pays"})
            st.plotly_chart(fig_pc, use_container_width=True)

    # === TAB 2: EMPLOI & PAUVRETÉ ===
    with tab2:
        st.subheader("💼 Chômage, Pauvreté Extrême & Inflation")
        with st.spinner("Chargement données emploi & pauvreté (World Bank)..."):
            df_unem = fetch_wb("SL.UEM.TOTL.ZS")
            df_pov = fetch_wb("SI.POV.DDAY")
            df_inf = fetch_wb("FP.CPI.TOTL.ZG")

        col_u, col_p = st.columns(2)

        if not df_unem.empty:
            with col_u:
                fig_unem = px.line(df_unem, x='annee', y='valeur', color='pays',
                    title="Taux de Chômage (%) — CEDEAO",
                    labels={"valeur": "Chômage (%)", "annee": "Année"})
                st.plotly_chart(fig_unem, use_container_width=True)

        if not df_pov.empty:
            with col_p:
                latest_pov = df_pov.sort_values("annee").groupby("pays").last().reset_index()
                fig_pov = px.bar(latest_pov.sort_values("valeur", ascending=False),
                    x='pays', y='valeur', color='valeur', color_continuous_scale='Reds',
                    title="Taux de Pauvreté Extrême <2.15$/j (%) — Dernière Donnée",
                    labels={"valeur": "Pauvreté (%)", "pays": "Pays"})
                st.plotly_chart(fig_pov, use_container_width=True)

        if not df_inf.empty:
            df_inf_ben = df_inf[df_inf['pays_code'] == 'BEN']
            if not df_inf_ben.empty:
                fig_inf = px.area(df_inf_ben, x='annee', y='valeur', color_discrete_sequence=['#EF4444'],
                    title="Inflation Annuelle au Bénin (%)",
                    labels={"valeur": "Inflation (%)", "annee": "Année"})
                fig_inf.add_hline(y=3, line_dash="dash", line_color="orange", annotation_text="Cible UEMOA (3%)")
                st.plotly_chart(fig_inf, use_container_width=True)

    # === TAB 3: SOCIÉTÉ ===
    with tab3:
        st.subheader("🌐 Électricité, Internet & Alphabétisation — CEDEAO")
        with st.spinner("Chargement indicateurs de société (World Bank)..."):
            df_elec = fetch_wb("EG.ELC.ACCS.ZS")
            df_net = fetch_wb("IT.NET.USER.ZS")
            df_lit = fetch_wb("SE.ADT.LITR.ZS")

        col_e, col_n = st.columns(2)
        if not df_elec.empty:
            with col_e:
                df_elec_ben = df_elec[df_elec['pays_code'] == 'BEN']
                fig_elec = px.area(df_elec_ben, x='annee', y='valeur', color_discrete_sequence=['#1E3A8A'],
                    title="Accès à l'Électricité au Bénin (% population)",
                    labels={"valeur": "Accès Electricité (%)", "annee": "Année"})
                st.plotly_chart(fig_elec, use_container_width=True)

        if not df_net.empty:
            with col_n:
                latest_net = df_net.sort_values("annee").groupby("pays").last().reset_index()
                fig_net = px.bar(latest_net.sort_values("valeur", ascending=False),
                    x='pays', y='valeur', color='valeur', color_continuous_scale='Teal',
                    title="Utilisateurs Internet (% pop.) — CEDEAO (Dernière Année)",
                    labels={"valeur": "Utilisateurs Internet (%)", "pays": "Pays"})
                st.plotly_chart(fig_net, use_container_width=True)

        if not df_lit.empty:
            latest_lit = df_lit.sort_values("annee").groupby("pays").last().reset_index()
            fig_lit = px.bar(latest_lit.sort_values("valeur", ascending=False),
                x='pays', y='valeur', color='valeur', color_continuous_scale='Greens',
                title="Taux d'Alphabétisation des Adultes (%) — CEDEAO",
                labels={"valeur": "Alphabétisation (%)", "pays": "Pays"})
            st.plotly_chart(fig_lit, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Projet 13 - Économie & Développement CEDEAO", layout="wide")
    render_projet13()
