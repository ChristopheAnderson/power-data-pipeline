# -*- coding: utf-8 -*-
"""
Projet 6 - Streamlit Dashboard: Streaming Temps Réel & Détection d'Anomalies SCADA / PMU (Control Room WAPP)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from pmu_stream_simulator import generate_pmu_streaming_batch
except ImportError:
    from projet6_streaming_pyspark.pmu_stream_simulator import generate_pmu_streaming_batch

def render_projet6():
    st.header("⚡ Projet 6 : Real-Time Streaming & Détection d'Anomalies PMU / SCADA (PySpark Structured Streaming)")
    st.markdown("""
    **Architecture SCADA / Control Room WAPP (CIC)** :
    - Traitement en streaming temps réel des unités de mesure de phaseur (**PMU / Phasor Measurement Unit** à 50 Hz).
    - Moteur **PySpark Structured Streaming** avec fenêtres glissantes (*Sliding Windows 5-sec & Watermarking*).
    - Détection instantanée des chutes de fréquence ($\text{Fréquence} < 49.5\text{ Hz}$) et des creux de tension ($\text{Tension} < 300\text{ kV}$).
    """)

    st.subheader("🖥️ Panneau de Contrôle Réseau Temps Réel (WAPP Dispatching Center)")

    df_pmu = generate_pmu_streaming_batch(150)
    df_pmu['timestamp_dt'] = pd.to_datetime(df_pmu['timestamp'])

    # Critical Alerts Count
    critical_df = df_pmu[df_pmu['status'] == 'CRITICAL_TRIP']
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Débit Streaming PMU", "100 msgs/sec")
    m2.metric("Fréquence Moyenne Réseau", f"{df_pmu['frequence_hz'].mean():.3f} Hz")
    m3.metric("Tension Moyenne Réseau", f"{df_pmu['tension_kv'].mean():.1f} kV")
    m4.metric("Alertes Critiques Détectées", f"{len(critical_df)}", delta_color="inverse")

    if len(critical_df) > 0:
        st.error(f"🚨 ALERTE CIC WAPP : {len(critical_df)} anomalies de stabilité réseau détectées sur le flux streaming !")

    # Frequency Stream Plot
    st.subheader("📉 Flux Temps Réel de la Fréquence Réseau (Hz) par Substation")
    fig_freq = px.line(
        df_pmu,
        x='timestamp_dt',
        y='frequence_hz',
        color='substation',
        title="Variation Télémesurée de la Fréquence (Seuil Critique: < 49.5 Hz)",
        labels={"frequence_hz": "Fréquence (Hz)", "timestamp_dt": "Horodatage Temps Réel"}
    )
    fig_freq.add_hline(y=49.5, line_dash="dash", line_color="red", annotation_text="Seuil de Délestage Rapide (49.5 Hz)")
    fig_freq.add_hline(y=50.5, line_dash="dash", line_color="orange", annotation_text="Seuil Surfréquence (50.5 Hz)")
    st.plotly_chart(fig_freq, use_container_width=True)

    # Voltage Stream Plot
    st.subheader("⚡ Flux Temps Réel de la Tension (kV) & Angle de Phase (°)")
    col_v, col_p = st.columns(2)

    with col_v:
        fig_volt = px.scatter(
            df_pmu,
            x='timestamp_dt',
            y='tension_kv',
            color='status',
            color_discrete_map={"NORMAL": "#0D9488", "CRITICAL_TRIP": "#EF4444"},
            title="Tension des Lignes d'Interconnexion (kV)"
        )
        st.plotly_chart(fig_volt, use_container_width=True)

    with col_p:
        fig_phase = px.line(
            df_pmu,
            x='timestamp_dt',
            y='angle_phase_deg',
            color='substation',
            title="Angle de Phase (°)"
        )
        st.plotly_chart(fig_phase, use_container_width=True)

    st.subheader("📋 Tampon de Streaming PySpark (Derniers 15 Relevés PMU Ingestés)")
    st.dataframe(df_pmu[['timestamp', 'substation', 'frequence_hz', 'tension_kv', 'angle_phase_deg', 'status']].head(15), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 6 Streaming PMU", layout="wide")
    render_projet6()
