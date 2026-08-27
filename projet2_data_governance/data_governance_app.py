# -*- coding: utf-8 -*-
"""
Projet 2 - Streamlit Dashboard: Gouvernance, Qualité de Données GRT & Données Banque Mondiale (CEDEAO/WAPP)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Bulletproof sys.path setup for standalone or imported execution
dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from quality_wapp import WAPPDataQualityEngine, generate_sample_tso_telemetry
except ImportError:
    from projet2_data_governance.quality_wapp import WAPPDataQualityEngine, generate_sample_tso_telemetry

def get_world_bank_ecowas_data():
    """
    Returns World Bank Open Data indicators for ECOWAS / WAPP Member States.
    """
    data = [
        {"Pays": "Bénin", "Code": "BEN", "Acces_Electricite_Pct": 45.6, "Pertes_Reseau_Pct": 18.2, "Capacite_MW": 350},
        {"Pays": "Côte d'Ivoire", "Code": "CIV", "Acces_Electricite_Pct": 71.1, "Pertes_Reseau_Pct": 14.5, "Capacite_MW": 2250},
        {"Pays": "Nigeria", "Code": "NGA", "Acces_Electricite_Pct": 55.4, "Pertes_Reseau_Pct": 22.0, "Capacite_MW": 13000},
        {"Pays": "Ghana", "Code": "GHA", "Acces_Electricite_Pct": 85.9, "Pertes_Reseau_Pct": 16.1, "Capacite_MW": 5000},
        {"Pays": "Togo", "Code": "TGO", "Acces_Electricite_Pct": 53.8, "Pertes_Reseau_Pct": 17.5, "Capacite_MW": 240},
        {"Pays": "Burkina Faso", "Code": "BFA", "Acces_Electricite_Pct": 21.0, "Pertes_Reseau_Pct": 19.8, "Capacite_MW": 410},
        {"Pays": "Sénégal", "Code": "SEN", "Acces_Electricite_Pct": 70.4, "Pertes_Reseau_Pct": 13.2, "Capacite_MW": 1550},
        {"Pays": "Niger", "Code": "NER", "Acces_Electricite_Pct": 19.3, "Pertes_Reseau_Pct": 24.1, "Capacite_MW": 280},
        {"Pays": "Mali", "Code": "MLI", "Acces_Electricite_Pct": 50.8, "Pertes_Reseau_Pct": 20.5, "Capacite_MW": 620}
    ]
    return pd.DataFrame(data)

def render_projet2():
    st.header("🛡️ Projet 2 : Contrôle Qualité, Gouvernance & Analytics Données Afrique (WAPP)")
    st.markdown("""
    **Périmètre Métier WAPP (Centre d'Information et de Coordination)** :
    - Audit automatisé des flux de télémesure envoyés par les Gestionnaires de Réseau de Transport (GRT) membres.
    - Évaluation des scores de complétude (%) et détection des déviations hors normes (Tension $161\\text{ kV} \\pm 10\\%$, Fréquence $50\\text{ Hz} \\pm 0.5\\text{ Hz}$).
    - Intégration des Open Data Banque Mondiale / CEDEAO (*Access to Electricity & Network Losses*).
    """)

    tab1, tab2 = st.tabs(["📊 Audit Qualité Télémesure GRT", "🌍 Indicateurs Énergétiques Banque Mondiale (CEDEAO)"])

    with tab1:
        st.subheader("1. Audit de Complétude et Détection d'Anomalies des GRT")
        df_telemetry = generate_sample_tso_telemetry()
        
        selected_grt = st.multiselect(
            "Filtrer par GRT (Gestionnaire de Réseau)",
            options=df_telemetry['grt_code'].unique().tolist(),
            default=df_telemetry['grt_code'].unique().tolist()
        )

        df_filtered = df_telemetry[df_telemetry['grt_code'].isin(selected_grt)]
        engine = WAPPDataQualityEngine()
        audit_df = engine.audit_tso_data(df_filtered)

        m1, m2, m3 = st.columns(3)
        total_obs = len(df_filtered)
        val_manquantes = df_filtered[['tension_kv', 'frequence_hz', 'puissance_mw']].isnull().sum().sum()
        completeness_global = ((total_obs * 3 - val_manquantes) / (total_obs * 3)) * 100.0 if total_obs > 0 else 0

        m1.metric("Observations Totales", f"{total_obs:,.0f}")
        m2.metric("Score Complétude Global", f"{completeness_global:.2f} %")
        m3.metric("Nombre de GRT Audités", f"{len(selected_grt)}")

        st.markdown("#### Table de Synthèse du Contrôle Qualité")
        st.dataframe(audit_df, use_container_width=True)

        st.subheader("2. Visualisation des Anomalies sur le Réseau (Tension & Fréquence)")
        fig_scatter = px.scatter(
            df_filtered,
            x='timestamp',
            y='tension_kv',
            color='grt_code',
            title="Variation de la Tension Réseau (kV) vs Seuil Nominal (161 kV ± 10%)",
            labels={"tension_kv": "Tension (kV)", "timestamp": "Horodatage", "grt_code": "GRT"}
        )
        fig_scatter.add_hline(y=161.0 * 1.1, line_dash="dash", line_color="red", annotation_text="+10% Max (177.1 kV)")
        fig_scatter.add_hline(y=161.0 * 0.9, line_dash="dash", line_color="red", annotation_text="-10% Min (144.9 kV)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        st.subheader("🌍 Indicateurs d'Accès à l'Électricité & Pertes Réseau (Banque Mondiale)")
        df_wb = get_world_bank_ecowas_data()

        fig_bar = px.bar(
            df_wb,
            x='Pays',
            y='Acces_Electricite_Pct',
            color='Pertes_Reseau_Pct',
            title="Taux d'Accès à l'Électricité (%) & Pertes de Transmission (%) en Afrique de l'Ouest",
            labels={"Acces_Electricite_Pct": "Accès Électricité (% Pop.)", "Pertes_Reseau_Pct": "Pertes Réseau (%)"},
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.dataframe(df_wb, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 2 Qualité & Données WAPP", layout="wide")
    render_projet2()
