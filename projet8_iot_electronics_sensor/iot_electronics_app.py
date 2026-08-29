# -*- coding: utf-8 -*-
"""
Projet 8 - Streamlit Dashboard: IoT Industrielle, Capteurs Électroniques & Maintenance Prédictive (FFT)
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
    from sensor_signal_processing import generate_sensor_vibration_signal, compute_fft_spectrum
except ImportError:
    from projet8_iot_electronics_sensor.sensor_signal_processing import generate_sensor_vibration_signal, compute_fft_spectrum

def render_projet8():
    st.header("🔬 Projet 8 : Industrial IoT, Capteurs Électroniques & Traitement de Signal (FFT & RUL)")
    
    st.info("""
    🔗 **Source & Accès aux Données Utilisées (Benchmark NASA PCoE & Capteurs Haute Fréquence) :**
    - **Fournisseurs Officiels :** NASA Prognostics Center of Excellence (*PCoE*) & IMS (*Center for Intelligent Maintenance Systems*)
    - **Jeu de données :** *Capteurs accélérométriques haute fréquence (1 à 2 kHz) pour l'analyse vibratoire, détection de défauts par FFT et estimation de la RUL*
    - **Liens officiels directs :**
      - 🌐 [NASA PCoE Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
      - 🏛️ [Portail Open Data NASA (data.nasa.gov)](https://data.nasa.gov/)
      - ⚙️ [Jeu de données NASA Bearing Vibration Dataset](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/bearing-dataset/)
    - **Type d'accès :** Open Data Public Capteurs Industriels / Maintenance Prédictive.
    """)

    st.markdown("""
    **Secteur Électronique & IoT Industriel** :
    - Ingestion et filtrage de signaux de capteurs accélérométriques haute fréquence (**1 kHz / 1000 échantillons par sec**).
    - Analyse Spectrale par **Transformée de Fourier Rapide (FFT)** pour la détection d'harmoniques de défauts mécaniques/électroniques (350 Hz).
    - Estimation de la Durée de Vie Utile Restante (**RUL - Remaining Useful Life**) des équipements industriels.
    """)

    st.subheader("🎛️ Simulation du Signal Capteur IoT & Niveau de Dégradation")

    col_anom, col_rate = st.columns(2)
    with col_anom:
        anomaly_level = st.slider("Niveau d'Usure / Anomalie du Composant", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
    with col_rate:
        sampling_rate = st.selectbox("Fréquence d'Échantillonnage Capteur (Hz)", options=[500, 1000, 2000], index=1)

    t, signal = generate_sensor_vibration_signal(sampling_rate=sampling_rate, anomaly_level=anomaly_level)
    df_spec, peak_freq = compute_fft_spectrum(t, signal, sampling_rate=sampling_rate)

    df_raw_signal = pd.DataFrame({"temps_sec": t, "amplitude_g": signal})

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger le signal temporel capteur (.CSV)",
            data=df_raw_signal.to_csv(index=False).encode('utf-8'),
            file_name="iot_sensor_raw_vibration.csv",
            mime="text/csv",
            key="p8_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger le spectre FFT (.JSON)",
            data=df_spec.to_json(orient="records").encode('utf-8'),
            file_name="iot_sensor_fft_spectrum.json",
            mime="application/json",
            key="p8_dl_json"
        )

    rul_hours = max(0, int(8760 * (1.0 - anomaly_level**1.5)))

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Points Échantillonnés", f"{len(t):,}")
    m2.metric("Fréquence Dominante (Pic)", f"{peak_freq:.0f} Hz")
    m3.metric("Niveau de Dégradation", f"{anomaly_level * 100:.0f} %")
    m4.metric("Durée de Vie Restante (RUL)", f"{rul_hours:,} Heures")

    st.markdown("---")

    col_time, col_fft = st.columns(2)

    with col_time:
        st.subheader("📈 Signal Temporel du Capteur (Accéléromètre)")
        df_time = pd.DataFrame({"Temps_s": t, "Amplitude_Signal": signal})
        fig_time = px.line(df_time, x='Temps_s', y='Amplitude_Signal', title="Oscillogramme Brut du Capteur", color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig_time, use_container_width=True)

    with col_fft:
        st.subheader("📉 Spectre de Fréquence FFT (Transformée de Fourier)")
        fig_fft = px.bar(df_spec, x='frequence_hz', y='amplitude', title="Spectre d'Amplitude (Détection d'Harmoniques à 350 Hz)", color='amplitude', color_continuous_scale='Teal')
        st.plotly_chart(fig_fft, use_container_width=True)

    st.subheader("📋 Analyse des Harmoniques Détectées")
    st.dataframe(df_spec.sort_values("amplitude", ascending=False).head(10), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 8 IoT & Électronique", layout="wide")
    render_projet8()
