# -*- coding: utf-8 -*-
"""
Projet 1 - Streamlit Dashboard: Observatoire Électrique Temps Réel (RTE éCO2mix)
Ingestion API publique REST sans clé & Analytics visuels
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def load_rte_data():
    url = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"
    params = {
        "dataset": "eco2mix-national-tr",
        "rows": 100,
        "sort": "-date_heure"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            records = res.json().get('records', [])
            fields = [r['fields'] for r in records if 'fields' in r]
            df = pd.DataFrame(fields)
            return df
    except Exception as e:
        st.error(f"Erreur d'accès à l'API RTE: {e}")
    return pd.DataFrame()

def render_projet1():
    st.header("⚡ Projet 1 : Pipeline API Données Électriques & Dashboard Temps Réel")
    st.markdown("""
    **Architecture & Source** :
    - API Publique RTE éCO2mix (*Open Data Réseaux Énergies*) - 100% Gratuite sans clé API.
    - Ingestion automatisée en JSON, traitement des séries temporelles sous `Pandas` & visualisation réactive avec `Plotly`.
    """)

    with st.spinner("Extraction des données en temps réel depuis l'API RTE..."):
        df = load_rte_data()

    if df.empty:
        st.warning("⚠️ Impossible de récupérer les données en direct. Affichage des données de secours.")
        return

    # Cleaning & Processing
    df['date_heure'] = pd.to_datetime(df['date_heure'])
    cols_filiere = ['consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz', 'fioul', 'charbon']
    for col in cols_filiere:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        else:
            df[col] = 0.0

    df['total_enr'] = df['eolien'] + df['solaire'] + df['hydraulique']
    df['pct_enr'] = (df['total_enr'] / df['consommation'].replace(0, 1)) * 100.0

    latest = df.iloc[0]

    # Metrics Section
    st.subheader("📌 Métriques Clés en Direct (Dernier Relevé)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Consommation Totale", f"{latest['consommation']:,.0f} MW")
    m2.metric("Production Éolienne", f"{latest['eolien']:,.0f} MW")
    m3.metric("Production Solaire", f"{latest['solaire']:,.0f} MW")
    m4.metric("Part EnR (Éolien+Sol+Hyd)", f"{latest['pct_enr']:.1f} %")

    st.markdown("---")

    # Time-Series Chart
    st.subheader("📈 Évolution Temporelle de la Charge et du Mix Énergétique")
    mix_cols = [c for c in ['consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz'] if c in df.columns]
    
    fig_line = px.line(
        df,
        x='date_heure',
        y=mix_cols,
        title="Puissance par Filière (MW) en Fonction du Temps",
        labels={"value": "Puissance (MW)", "date_heure": "Horodatage", "variable": "Filière"},
        color_discrete_map={
            "consommation": "#1E3A8A",
            "nucleaire": "#6B7280",
            "eolien": "#0D9488",
            "solaire": "#F59E0B",
            "hydraulique": "#3B82F6",
            "gaz": "#EF4444"
        }
    )
    fig_line.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

    col_pie, col_gauge = st.columns(2)

    with col_pie:
        st.subheader("🍰 Répartition de la Production Actuelle")
        prod_data = {
            "Nucléaire": latest['nucleaire'],
            "Éolien": latest['eolien'],
            "Solaire": latest['solaire'],
            "Hydraulique": latest['hydraulique'],
            "Gaz": latest['gaz']
        }
        df_pie = pd.DataFrame(list(prod_data.items()), columns=['Filière', 'Production_MW'])
        fig_pie = px.pie(
            df_pie,
            names='Filière',
            values='Production_MW',
            hole=0.4,
            color_discrete_sequence=['#6B7280', '#0D9488', '#F59E0B', '#3B82F6', '#EF4444']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_gauge:
        st.subheader("🎯 Jauge de Pénétration des Énergies Renouvelables")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest['pct_enr'],
            number={'suffix': '%'},
            title={'text': "Part EnR dans la Consommation"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#0D9488"},
                'steps': [
                    {'range': [0, 25], 'color': "#FEE2E2"},
                    {'range': [25, 50], 'color': "#FEF3C7"},
                    {'range': [50, 100], 'color': "#D1FAE5"}
                ]
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.subheader("📋 Extraits des Données Brut Ingestées (API RTE)")
    st.dataframe(df[['date_heure', 'consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz']].head(15), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 1 RTE API", layout="wide")
    render_projet1()
