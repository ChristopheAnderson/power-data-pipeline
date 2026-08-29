# -*- coding: utf-8 -*-
"""
Projet 5 - Streamlit Dashboard: Pipeline Géospatiale & Prédiction du Potentiel Solaire EnR (NASA POWER / BME / Krigeage)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from fetch_nasa_solar import generate_ecowas_grid_solar_data, fetch_nasa_power_point
    from geostat_kriging import GeostatisticalSolarModel
except ImportError:
    from projet5_geospatial_solar.fetch_nasa_solar import generate_ecowas_grid_solar_data, fetch_nasa_power_point
    from projet5_geospatial_solar.geostat_kriging import GeostatisticalSolarModel

def render_projet5():
    st.header("🌍 Projet 5 : Ingestion Géospatiale Satellite & Modélisation Géostatistique (BME / Krigeage)")
    
    st.info("""
    🔗 **Source & Accès aux Données Utilisées (100% Réelles & Vérifiables) :**
    - **Fournisseur Officiel :** NASA Langley Research Center (*NASA POWER - Prediction Of Worldwide Energy Resources*)
    - **Jeu de données :** *Rayonnement solaire satellitaire (GHI, DNI, Température, Vent) pour les sites stratégiques WAPP / CEDEAO*
    - **Liens officiels directs :**
      - 🌐 [Portail Officiel NASA POWER Project](https://power.larc.nasa.gov/)
      - 🛰️ [NASA POWER Data Access Viewer (Visualiseur & Export Mondial)](https://power.larc.nasa.gov/data-access-viewer/)
      - 🔌 [Documentation & Endpoint API REST Direct (JSON)](https://power.larc.nasa.gov/docs/services/api/)
    - **Type d'accès :** API REST Publique Mondiale NASA (Gratuit, Open Access sans clé requise).
    """)

    st.markdown("""
    **Valorisation Spécialisée (Thèse & Diplôme Bac+5 ENSGMM - Christophe WAVOEKE)** :
    - Ingestion de séries temporelles satellites **NASA POWER API** (*Global Horizontal Irradiance GHI, Température, Vent*).
    - Traitement géospatistique : Calcul du variogramme expérimental $\\gamma(h)$ et interpolation spatiale (*IDW / Krigeage Ordinaire*).
    - Application WAPP : Cartographie d'optimisation d'implantation des centrales photovoltaïques en Afrique de l'Ouest (Bénin, Togo, Ghana, Côte d'Ivoire, Nigeria, Niger).
    """)

    df_solar = generate_ecowas_grid_solar_data()

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger le maillage solaire CEDEAO (.CSV)",
            data=df_solar.to_csv(index=False).encode('utf-8'),
            file_name="wapp_potentiel_solaire_cedeao.csv",
            mime="text/csv",
            key="p5_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger le maillage (.JSON)",
            data=df_solar.to_json(orient="records").encode('utf-8'),
            file_name="wapp_potentiel_solaire_cedeao.json",
            mime="application/json",
            key="p5_dl_json"
        )

    # Key metrics
    st.subheader("📌 Métriques Géospatiales du Réseau Solaire WAPP")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Nombre de Stations", f"{len(df_solar)}")
    m2.metric("GHI Moyen CEDEAO", f"{df_solar['ghi_kwh_m2_day'].mean():.2f} kWh/m²/j")
    m3.metric("GHI Maximum (Zone Nord)", f"{df_solar['ghi_kwh_m2_day'].max():.2f} kWh/m²/j")
    m4.metric("Potentiel Cumulé Estimé", f"{df_solar['potentiel_solaire_mw'].sum():,.0f} MW")

    st.markdown("---")

    tab_geo, tab_live = st.tabs(["🗺️ Cartographie Géostatistique Régionale (WAPP)", "🛰️ Extraction en Direct API NASA POWER (Par Station)"])

    with tab_geo:
        # Spatial Map
        st.subheader("🗺️ Carte Interactive du GHI (Irradiance Solaire) & Potentiel de Production MW")
        
        fig_map = px.scatter_geo(
            df_solar,
            lat='latitude',
            lon='longitude',
            text='site',
            size='potentiel_solaire_mw',
            color='ghi_kwh_m2_day',
            hover_data=['temp_moyenne_c', 'ghi_kwh_m2_day'],
            projection="natural earth",
            title="Distribution Spatiale du GHI (kWh/m²/jour) dans la Zone CEDEAO / WAPP",
            color_continuous_scale="YlOrRd",
            size_max=30
        )
        fig_map.update_geos(
            fitbounds="locations",
            showcountries=True,
            countrycolor="DarkGray",
            showsubunits=True
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Variogram & Spatial Interpolation
        col_vario, col_interp = st.columns(2)

        with col_vario:
            st.subheader("📉 Modélisation du Variogramme Spatial γ(h)")
            coords = df_solar[['longitude', 'latitude']].values
            values = df_solar['ghi_kwh_m2_day'].values
            
            geo_model = GeostatisticalSolarModel()
            df_vario = geo_model.calculate_variogram(coords, values)

            fig_vario = px.line(
                df_vario,
                x='bin_distance',
                y='gamma',
                markers=True,
                title="Variogramme Expérimental de la Dépendance Spatiale du GHI",
                labels={"bin_distance": "Distance Séparation h (degrés)", "gamma": "Semi-Variance γ(h)"},
                color_discrete_sequence=['#1E3A8A']
            )
            st.plotly_chart(fig_vario, use_container_width=True)

        with col_interp:
            st.subheader("🔥 Grid Heatmap Interpolé par Krigeage / IDW")
            grid_x = np.linspace(df_solar['longitude'].min() - 1, df_solar['longitude'].max() + 1, 25)
            grid_y = np.linspace(df_solar['latitude'].min() - 1, df_solar['latitude'].max() + 1, 25)
            grid_z = geo_model.inverse_distance_weighting(coords, values, grid_x, grid_y)

            fig_heatmap = px.imshow(
                grid_z,
                x=grid_x,
                y=grid_y,
                labels=dict(x="Longitude", y="Latitude", color="GHI (kWh/m²/j)"),
                title="Surface Spatiale Continue du GHI (Reconstruction BME/Krigeage)",
                color_continuous_scale="Plasma",
                origin="lower"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

        st.subheader("📋 Tableau des Stations Météo Satellitaires NASA POWER")
        st.dataframe(df_solar, use_container_width=True)

    with tab_live:
        st.subheader("🛰️ Requête en Temps Réel sur les Serveurs Satellitaires NASA POWER (Langley)")
        col_st, col_dt = st.columns(2)
        with col_st:
            station_names = df_solar['site'].tolist()
            chosen_site = st.selectbox("Sélectionner une station WAPP :", station_names, index=0)
        with col_dt:
            date_opt = st.selectbox("Période d'observation satellite :", [
                "Janvier 2023 (Saison Sèche)", "Juillet 2023 (Saison des Pluies)", "Année Complète 2023"
            ], index=0)

        site_row = df_solar[df_solar['site'] == chosen_site].iloc[0]
        st_lat = site_row['latitude']
        st_lon = site_row['longitude']

        if "Janvier" in date_opt:
            s_date, e_date = "20230101", "20230131"
        elif "Juillet" in date_opt:
            s_date, e_date = "20230701", "20230731"
        else:
            s_date, e_date = "20230101", "20231231"

        if st.button(f"🚀 Interroger l'API NASA POWER pour {chosen_site} ({st_lat}°, {st_lon}°)", key="btn_nasa_live"):
            with st.spinner("Téléchargement des données satellites depuis l'API NASA POWER..."):
                df_live_nasa = fetch_nasa_power_point(lat=st_lat, lon=st_lon, start_date=s_date, end_date=e_date)
            
            if not df_live_nasa.empty:
                st.success(f"✅ {len(df_live_nasa)} relevés quotidiens reçus de la NASA pour {chosen_site} !")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Irradiance Solaire Moyenne", f"{df_live_nasa['ghi_kwh_m2'].mean():.2f} kWh/m²/j")
                m2.metric("Température Moyenne", f"{df_live_nasa['temp_c'].mean():.1f} °C")
                m3.metric("Vitesse du Vent Moyenne", f"{df_live_nasa['wind_m_s'].mean():.1f} m/s")

                fig_nasa_time = px.line(
                    df_live_nasa,
                    x='date',
                    y=['ghi_kwh_m2', 'temp_c', 'wind_m_s'],
                    title=f"Séries Temporelles Satellitaires Réelles NASA POWER — {chosen_site}",
                    labels={"value": "Valeur Mesurée", "date": "Date", "variable": "Paramètre Satellite"}
                )
                st.plotly_chart(fig_nasa_time, use_container_width=True)
                st.dataframe(df_live_nasa, use_container_width=True)
            else:
                st.error("Impossible de contacter le serveur NASA. Vérifiez votre connexion.")

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 5 Géospatial Solaire", layout="wide")
    render_projet5()
