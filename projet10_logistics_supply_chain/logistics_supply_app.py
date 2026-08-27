# -*- coding: utf-8 -*-
"""
Projet 10 - Streamlit Dashboard: Smart Logistics, Trajectoires GPS & Optimisation Supply Chain
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
    from route_optimizer import generate_gps_fleet_trajectories, solve_tsp_route_optimization
except ImportError:
    from projet10_logistics_supply_chain.route_optimizer import generate_gps_fleet_trajectories, solve_tsp_route_optimization

def render_projet10():
    st.header("🚚 Projet 10 : Smart Logistics, Traces GPS & Optimisation d'Empreinte Carbone Supply Chain")
    st.markdown("""
    **Secteur Transport, Logistique & Mobilité Intelligente** :
    - Traitement des séries temporelles de **géolocalisation GPS de flottes de transport de marchandises**.
    - Algorithmes d'optimisation de tournée (*Travelling Salesperson Problem - TSP*) pour réduire les distances parcourues.
    - Évaluation de l'impact écologique : Réduction du carburant consommé et des émissions de $\\text{CO}_2$ (kg).
    """)

    df_gps = generate_gps_fleet_trajectories()
    df_opt = solve_tsp_route_optimization(df_gps)

    # Metrics
    total_dist = df_opt['distance_totale_km'].sum()
    total_fuel = df_opt['carburant_consomme_l'].sum()
    total_co2_saved = df_opt['economie_co2_kg'].sum()

    st.subheader("📌 Métriques Clés de la Flotte de Transport")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Véhicules Suivis", f"{len(df_opt)}")
    m2.metric("Distance Totale Parcourue", f"{total_dist:,.0f} km")
    m3.metric("Carburant Total Consommé", f"{total_fuel:,.0f} Litres")
    m4.metric("Économie CO2 Optimisée", f"{total_co2_saved:,.1f} kg CO2", delta="-15% Carburant")

    st.markdown("---")

    # GPS Map
    st.subheader("🗺️ Cartographie des Trajectoires GPS de la Flotte")
    fig_map = px.scatter_geo(
        df_gps,
        lat='latitude',
        lon='longitude',
        color='vehicule_id',
        hover_data=['timestamp', 'vitesse_kmh', 'consommation_carburant_l'],
        projection="natural earth",
        title="Traces GPS en Temps Réel des Camions de Livraison",
        size='vitesse_kmh',
        size_max=15
    )
    fig_map.update_geos(fitbounds="locations", showcountries=True, countrycolor="LightGray")
    st.plotly_chart(fig_map, use_container_width=True)

    col_fuel, col_co2 = st.columns(2)

    with col_fuel:
        st.subheader("⛽ Consommation de Carburant (Brut vs Optimisé)")
        fig_fuel = px.bar(
            df_opt,
            x='vehicule_id',
            y=['carburant_consomme_l', 'carburant_optimise_l'],
            barmode='group',
            title="Gain de Carburant (Litres) par Camion",
            labels={"value": "Carburant (L)", "vehicule_id": "Camion", "variable": "Scenario"},
            color_discrete_map={"carburant_consomme_l": "#EF4444", "carburant_optimise_l": "#0D9488"}
        )
        st.plotly_chart(fig_fuel, use_container_width=True)

    with col_co2:
        st.subheader("🌱 Réduction d'Émissions CO2 (kg) par Véhicule")
        fig_co2 = px.bar(
            df_opt,
            x='vehicule_id',
            y='economie_co2_kg',
            title="Économie d'Émissions de CO2 Réalisée (kg)",
            color='economie_co2_kg',
            color_continuous_scale="Teal"
        )
        st.plotly_chart(fig_co2, use_container_width=True)

    st.subheader("📋 Résumé de l'Optimisation de Tournée Supply Chain")
    st.dataframe(df_opt, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 10 Supply Chain Logistics", layout="wide")
    render_projet10()
