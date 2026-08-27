# -*- coding: utf-8 -*-
"""
Projet 11 - Streamlit Dashboard: Clima Réel, Précipitations & Risques Climatiques (Open-Meteo API)
Données 100% réelles, sans clé API.
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
    from climate_data_engine import fetch_openmeteo_annual, fetch_all_stations_climate, STATIONS_BENIN
except ImportError:
    from projet11_climate_agriculture.climate_data_engine import fetch_openmeteo_annual, fetch_all_stations_climate, STATIONS_BENIN

def render_projet11():
    st.header("🌧️ Projet 11 : Données Climatiques Réelles (Open-Meteo API) — Précipitations, Sécheresses & Inondations (Bénin / CEDEAO)")
    st.markdown("""
    **Source : [Open-Meteo Archive API](https://open-meteo.com/en/docs/historical-weather-api) ✅ — 100% Gratuit, sans clé API**
    - Séries journalières réelles de **précipitations (mm), température (°C) et vent (km/h)** pour Cotonou, Parakou, Natitingou et les capitales CEDEAO.
    - Analyse des **saisons bimodales des pluies** au Bénin (2 saisons annuelles) et des événements extrêmes (inondations > 50 mm/jour).
    > *💡 Pertinence : ODD 13 – Action Climatique | Agenda 2063 UA | PAG 2 Bénin (Agriculture & Alimentation).*
    """)

    col_ctrl, col_yr = st.columns(2)
    with col_ctrl:
        selected_city = st.selectbox(
            "Choisir une ville / station météo :",
            options=[s["ville"] for s in STATIONS_BENIN],
            index=0
        )
    with col_yr:
        year_range = st.slider("Période d'analyse", min_value=2010, max_value=2023, value=(2015, 2023))

    station_info = next(s for s in STATIONS_BENIN if s["ville"] == selected_city)

    with st.spinner(f"Ingestion API Open-Meteo pour {selected_city} ({year_range[0]}–{year_range[1]})..."):
        df = fetch_openmeteo_annual(station_info, year_range[0], year_range[1])

    if df.empty:
        st.error("Erreur lors de la récupération des données. Vérifiez votre connexion Internet.")
        return

    df_annual = df.groupby("annee").agg(
        precip_totale_mm=("precipitation_mm", "sum"),
        temp_max_moy_c=("temp_max_c", "mean"),
        jours_extremes=("precipitation_mm", lambda x: (x >= 50).sum())
    ).reset_index()

    df_monthly = df.groupby("mois").agg(
        precip_moy_mm=("precipitation_mm", "mean"),
        temp_moy_c=("temp_max_c", "mean")
    ).reset_index()
    mois_noms = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]
    df_monthly["nom_mois"] = df_monthly["mois"].apply(lambda x: mois_noms[x-1])

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Précipitations Totales/An (Moy.)", f"{df_annual['precip_totale_mm'].mean():,.0f} mm")
    m2.metric("Temp. Max Moyenne", f"{df_annual['temp_max_moy_c'].mean():.1f} °C")
    m3.metric("Jours d'Inondation (>50mm)", f"{df_annual['jours_extremes'].sum()} jours")
    m4.metric("Année la plus humide", f"{df_annual.loc[df_annual['precip_totale_mm'].idxmax(), 'annee']}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 Précipitations Annuelles Réelles — {selected_city}")
        fig_bar = px.bar(df_annual, x='annee', y='precip_totale_mm',
            color='precip_totale_mm', color_continuous_scale='Blues',
            title=f"Cumul Annuel de Précipitations (mm) — {selected_city}",
            labels={"precip_totale_mm": "Précipitations (mm)", "annee": "Année"})
        fig_bar.add_hline(y=df_annual['precip_totale_mm'].mean(), line_dash="dash", line_color="red",
            annotation_text="Moyenne")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("📅 Cycle Saisonnier Bimodal (Mois)")
        fig_season = px.bar(df_monthly, x='nom_mois', y='precip_moy_mm',
            color='precip_moy_mm', color_continuous_scale='Teal',
            title=f"Profil Mensuel Moyen des Précipitations (mm) — {selected_city}",
            labels={"precip_moy_mm": "Précipitations (mm/mois)", "nom_mois": "Mois"})
        st.plotly_chart(fig_season, use_container_width=True)

    st.subheader("🌡️ Évolution de la Température Maximale Annuelle (Tendance de Réchauffement)")
    fig_temp = px.line(df_annual, x='annee', y='temp_max_moy_c', markers=True,
        title=f"Tendance de la Température Maximale Annuelle — {selected_city}",
        color_discrete_sequence=['#EF4444'],
        labels={"temp_max_moy_c": "Temp. Max Moy (°C)", "annee": "Année"})
    fig_temp.add_traces(px.scatter(df_annual, x='annee', y='temp_max_moy_c',
        trendline='ols').data[1])
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("🚨 Jours d'Événements Extrêmes (Précipitations ≥ 50 mm/jour = Risque Inondation)")
    fig_ext = px.bar(df_annual, x='annee', y='jours_extremes',
        color='jours_extremes', color_continuous_scale='OrRd',
        title=f"Nombre de Jours à Risque d'Inondation (≥50mm) — {selected_city}",
        labels={"jours_extremes": "Jours Extrêmes", "annee": "Année"})
    st.plotly_chart(fig_ext, use_container_width=True)

    with st.expander("📋 Voir les données journalières brutes (Open-Meteo)"):
        st.dataframe(df[['date','ville','precipitation_mm','temp_max_c','temp_min_c','vent_max_kmh']].tail(30), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Projet 11 - Climat Réel Bénin / CEDEAO", layout="wide")
    render_projet11()
