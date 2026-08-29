# -*- coding: utf-8 -*-
"""
Projet 12 - Streamlit Dashboard: Santé Publique, Paludisme, Démographie & Indicateurs Sociaux (WHO GHO + World Bank APIs)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path: sys.path.insert(0, dir_path)
if parent_dir not in sys.path: sys.path.insert(0, parent_dir)

try:
    from health_demographics_engine import (fetch_who_malaria_incidence, fetch_who_indicator_all_cedeao,
                                            fetch_world_bank_indicator, CEDEAO_COUNTRIES)
except ImportError:
    from projet12_health_demographics.health_demographics_engine import (
        fetch_who_malaria_incidence, fetch_who_indicator_all_cedeao,
        fetch_world_bank_indicator, CEDEAO_COUNTRIES)

def render_projet12():
    st.header("🏥 Projet 12 : Santé Publique, Paludisme & Démographie (API WHO GHO + World Bank — Données Réelles)")
    
    st.info("""
    🔗 **Sources & Accès aux Données Utilisées (100% Réelles & Vérifiables) :**
    - **Fournisseurs Officiels :** Organisation Mondiale de la Santé (*WHO GHO API*) & Banque Mondiale (*World Bank Open Data*)
    - **Jeux de données & Liens directs :**
      - 🦟 *Incidence du paludisme, espérance de vie & mortalité* : [Portail WHO Global Health Observatory](https://www.who.int/data/gho) | [Documentation WHO GHO OData API](https://www.who.int/data/gho/info/gho-odata-api) | [🔌 Endpoint API WHO Malaria](https://ghoapi.azureedge.net/api/MALARIA002)
      - 👥 *Démographie, population totale et fécondité* : [Portail World Bank (SP.POP.TOTL)](https://data.worldbank.org/indicator/SP.POP.TOTL) | [📥 Téléchargement Direct CSV (World Bank)](https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv)
    - **Type d'accès :** APIs REST / OData Publiques 100% Gratuites sans clé API requise.
    """)

    st.markdown("""
    **Périmètre d'Analyse & Enjeux Métiers :**
    - Suivi de la charge épidémiologique du paludisme (cas pour 1 000 hab.) dans l'espace CEDEAO.
    - Analyse de la dynamique démographique et de l'accès aux soins de santé primaires.
    > *💡 Pertinence : ODD 3 (Bonne Santé) | PAG 2 Bénin (Santé) | CEDEAO Plan Santé 2021–2025.*
    """)

    tab1, tab2, tab3 = st.tabs(["🦟 Paludisme", "👥 Démographie & Population", "📈 Indicateurs Sociaux CEDEAO"])

    # === TAB 1: PALUDISME ===
    with tab1:
        st.subheader("🦟 Incidence du Paludisme au Bénin & en Afrique de l'Ouest (WHO GHO)")
        
        selected_countries = st.multiselect(
            "Sélectionner les pays à comparer",
            options=list(CEDEAO_COUNTRIES.keys()),
            default=["BEN", "GHA", "NGA", "NER"],
            format_func=lambda x: CEDEAO_COUNTRIES[x]
        )

        with st.spinner("Interrogation API WHO GHO (paludisme)..."):
            dfs_malaria = []
            for code in selected_countries:
                df_m = fetch_who_malaria_incidence(code)
                if not df_m.empty:
                    dfs_malaria.append(df_m)
        
        if dfs_malaria:
            df_malaria_all = pd.concat(dfs_malaria, ignore_index=True)
            df_malaria_all['annee'] = df_malaria_all['annee'].astype(int)
            df_malaria_all['incidence_paludisme_1000'] = pd.to_numeric(df_malaria_all['incidence_paludisme_1000'], errors='coerce')

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.download_button(
                    "📥 Télécharger les données réelles Paludisme WHO (.CSV)",
                    data=df_malaria_all.to_csv(index=False).encode('utf-8'),
                    file_name="who_malaria_incidence_cedeao.csv",
                    mime="text/csv",
                    key="p12_malaria_csv"
                )
            with col_m2:
                st.download_button(
                    "📥 Télécharger les données (.JSON)",
                    data=df_malaria_all.to_json(orient="records").encode('utf-8'),
                    file_name="who_malaria_incidence_cedeao.json",
                    mime="application/json",
                    key="p12_malaria_json"
                )

            # Metrics for Benin
            df_ben = df_malaria_all[df_malaria_all['pays_code'] == 'BEN']
            if not df_ben.empty:
                latest = df_ben.sort_values('annee').iloc[-1]
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Incidence Bénin (Dernière Année)", f"{latest['incidence_paludisme_1000']:.0f} / 1000")
                m2.metric("Année de Référence", f"{int(latest['annee'])}")
                m3.metric("Minimum Historique Bénin", f"{df_ben['incidence_paludisme_1000'].min():.0f}")
                m4.metric("Maximum Historique Bénin", f"{df_ben['incidence_paludisme_1000'].max():.0f}")

            fig_malaria = px.line(df_malaria_all, x='annee', y='incidence_paludisme_1000', color='pays',
                title="Évolution de l'Incidence du Paludisme (cas pour 1000 personnes à risque)",
                labels={"incidence_paludisme_1000": "Incidence Paludisme (/ 1000)", "annee": "Année"},
                markers=True)
            st.plotly_chart(fig_malaria, use_container_width=True)
        else:
            st.warning("Données paludisme non disponibles. Vérifiez votre connexion Internet.")

    # === TAB 2: DEMOGRAPHIE ===
    with tab2:
        st.subheader("👥 Population Totale & Croissance Démographique (World Bank API)")

        with st.spinner("Interrogation World Bank API (démographie)..."):
            df_pop = fetch_world_bank_indicator("SP.POP.TOTL")
            df_fert = fetch_world_bank_indicator("SP.DYN.TFRT.IN")
            df_life = fetch_world_bank_indicator("SP.DYN.LE00.IN")

        if not df_pop.empty:
            df_pop['valeur_m'] = df_pop['valeur'] / 1_000_000

            col_pop1, col_pop2 = st.columns(2)
            with col_pop1:
                st.download_button(
                    "📥 Télécharger les données Démographie CEDEAO (.CSV)",
                    data=df_pop.to_csv(index=False).encode('utf-8'),
                    file_name="world_bank_population_cedeao.csv",
                    mime="text/csv",
                    key="p12_pop_csv"
                )
            with col_pop2:
                st.download_button(
                    "📥 Télécharger les données (.JSON)",
                    data=df_pop.to_json(orient="records").encode('utf-8'),
                    file_name="world_bank_population_cedeao.json",
                    mime="application/json",
                    key="p12_pop_json"
                )
            
            df_benin_pop = df_pop[df_pop['pays_code'] == 'BEN'].sort_values('annee')
            if not df_benin_pop.empty:
                m1, m2, m3 = st.columns(3)
                latest_pop = df_benin_pop.iloc[-1]
                m1.metric("Population Bénin (Dernière)", f"{latest_pop['valeur_m']:.2f} Millions")
                m2.metric("Année", f"{int(latest_pop['annee'])}")
                pop_2000 = df_benin_pop[df_benin_pop['annee'] == 2000]['valeur_m']
                if not pop_2000.empty:
                    growth = ((latest_pop['valeur_m'] / pop_2000.values[0]) - 1) * 100
                    m3.metric("Croissance depuis 2000", f"+{growth:.0f} %")

            fig_pop = px.line(df_pop, x='annee', y='valeur_m', color='pays',
                title="Évolution de la Population (Millions d'habitants) — CEDEAO",
                labels={"valeur_m": "Population (Millions)", "annee": "Année"})
            st.plotly_chart(fig_pop, use_container_width=True)

        col_f, col_l = st.columns(2)
        if not df_fert.empty:
            with col_f:
                st.subheader("👶 Taux de Fécondité (Enfants/Femme)")
                fig_fert = px.line(df_fert, x='annee', y='valeur', color='pays',
                    title="Taux de Fécondité (Naissances par Femme)",
                    labels={"valeur": "Enfants / Femme", "annee": "Année"})
                st.plotly_chart(fig_fert, use_container_width=True)

        if not df_life.empty:
            with col_l:
                st.subheader("💚 Espérance de Vie (Années)")
                fig_life = px.line(df_life, x='annee', y='valeur', color='pays',
                    title="Espérance de Vie à la Naissance (Années)",
                    labels={"valeur": "Espérance de Vie (ans)", "annee": "Année"})
                st.plotly_chart(fig_life, use_container_width=True)

    # === TAB 3: INDICATEURS SOCIAUX ===
    with tab3:
        st.subheader("📈 Indicateurs Sociaux & Économiques (World Bank API — CEDEAO)")

        with st.spinner("Interrogation World Bank API (indicateurs sociaux)..."):
            df_poverty = fetch_world_bank_indicator("SI.POV.DDAY")
            df_access_elec = fetch_world_bank_indicator("EG.ELC.ACCS.ZS")
            df_unem = fetch_world_bank_indicator("SL.UEM.TOTL.ZS")

        if not df_poverty.empty:
            col_soc1, col_soc2 = st.columns(2)
            with col_soc1:
                st.download_button(
                    "📥 Télécharger les données Pauvreté CEDEAO (.CSV)",
                    data=df_poverty.to_csv(index=False).encode('utf-8'),
                    file_name="world_bank_pauvrete_cedeao.csv",
                    mime="text/csv",
                    key="p12_pov_csv"
                )
            with col_soc2:
                st.download_button(
                    "📥 Télécharger les données (.JSON)",
                    data=df_poverty.to_json(orient="records").encode('utf-8'),
                    file_name="world_bank_pauvrete_cedeao.json",
                    mime="application/json",
                    key="p12_pov_json"
                )

        col_pov, col_elec = st.columns(2)

        if not df_poverty.empty:
            with col_pov:
                st.subheader("💔 Taux de Pauvreté Extrême (<2.15$/jour)")
                fig_pov = px.bar(
                    df_poverty.sort_values("annee").groupby("pays").last().reset_index(),
                    x='pays', y='valeur', color='valeur', color_continuous_scale='Reds',
                    title="Taux de Pauvreté Extrême (%) — Dernière Donnée Disponible",
                    labels={"valeur": "Taux de Pauvreté (%)", "pays": "Pays"})
                st.plotly_chart(fig_pov, use_container_width=True)

        if not df_access_elec.empty:
            with col_elec:
                st.subheader("💡 Accès à l'Électricité (% Population)")
                fig_elec = px.bar(
                    df_access_elec.sort_values("annee").groupby("pays").last().reset_index(),
                    x='pays', y='valeur', color='valeur', color_continuous_scale='Teal',
                    title="Accès à l'Électricité (%) — Dernière Donnée Disponible",
                    labels={"valeur": "Accès Electricité (%)", "pays": "Pays"})
                st.plotly_chart(fig_elec, use_container_width=True)

        if not df_unem.empty:
            st.subheader("💼 Taux de Chômage (%)")
            fig_unem = px.line(df_unem, x='annee', y='valeur', color='pays',
                title="Évolution du Taux de Chômage (%) — CEDEAO",
                labels={"valeur": "Taux de Chômage (%)", "annee": "Année"})
            st.plotly_chart(fig_unem, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Projet 12 - Santé & Démographie Réelles", layout="wide")
    render_projet12()
