# -*- coding: utf-8 -*-
"""
PORTAIL MULTI-PROJETS DATA ENGINEERING, BIG DATA & MULTI-SECTEUR ANALYTICS (10 PROJETS)
Candidat : Christophe WAVOEKE (Ingénieur Bac+5 Modélisation Mathématique & Informatique)
Poste : Ingénieur en Gestion et Analyse de Données des Systèmes Électriques (WAPP / EEEOA)
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from projet1_rte_api.app_rte import render_projet1
from projet2_data_governance.data_governance_app import render_projet2
from projet3_ml_load_forecasting.ml_forecasting_app import render_projet3
from projet4_pyspark_bigdata.pyspark_app import render_projet4
from projet5_geospatial_solar.geospatial_solar_app import render_projet5
from projet6_streaming_pyspark.streaming_app import render_projet6
from projet7_market_nodal_pricing.market_pricing_app import render_projet7
from projet8_iot_electronics_sensor.iot_electronics_app import render_projet8
from projet9_fintech_credit_risk.fintech_risk_app import render_projet9
from projet10_logistics_supply_chain.logistics_supply_app import render_projet10

st.set_page_config(
    page_title="WAPP Multi-Sector Data Portfolio - Christophe WAVOEKE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/lightning-bolt.png", width=64)
st.sidebar.title("⚡ Portfolio Data 10 Projets")
st.sidebar.markdown("**Christophe WAVOEKE**  \nIngénieur Bac+5 Modélisation & Data")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation (10 Projets Multi-Secteurs) :",
    [
        "🏠 Accueil & Profil Candidat",
        "⚡ Projet 1 : Pipeline API RTE (Temps Réel)",
        "🛡️ Projet 2 : Qualité & Données WAPP (CEDEAO)",
        "📈 Projet 3 : Prévision ML (Load Forecasting)",
        "🐘 Projet 4 : Big Data PySpark & Hive SQL",
        "🌍 Projet 5 : Ingestion Géospatiale Satellite (NASA POWER)",
        "⚡ Projet 6 : Streaming Temps Réel PMU (PySpark)",
        "📊 Projet 7 : Analytics Marché Nodal LMP (WAPP)",
        "🔬 Projet 8 : Industrial IoT & Capteurs Électroniques (FFT)",
        "💳 Projet 9 : FinTech Big Data & Credit Risk Scoring",
        "🚚 Projet 10 : Smart Logistics & Supply Chain GPS"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Contact & Liens** :
- ✉️ christophewavoeke18@gmail.com
- 📞 +229 01 66 81 83 76
- 🌐 [Portfolio Vercel](https://christopher-portofolio.vercel.app/)
- 🐱 [GitHub Repository](https://github.com/christopher-wavoeke/wapp-power-data-pipeline)
""")

if menu == "🏠 Accueil & Profil Candidat":
    st.title("⚡ Portfolio Multi-Secteurs : Ingénierie de Données, Big Data & Analytics (10 Projets)")
    st.subheader("Candidature pour le poste d'Ingénieur en Gestion et Analyse de Données — WAPP / EEEOA")

    col_profile, col_summary = st.columns([1, 2])

    with col_profile:
        st.markdown("""
        ### 👨‍💻 Christophe WAVOEKE
        **Ingénieur diplômé ENSGMM (Bac+5)**  
        *Major de Promotion 2023 | Prix Route de la Soie*

        - 📍 Cotonou / Abomey-Calavi, Bénin
        - 🎓 Modélisation Mathématique & Informatique
        - 💼 Responsable Formation & Développeur Full-Stack chez Modernetic Bénin
        - 🔬 Chercheur / Analyste Géostatistique sur 40 000+ données (URBioPSIB)
        - 👨‍🏫 Assistant Professeur à l'UNSTIM
        """)

    with col_summary:
        st.markdown("""
        ### 🎯 Portfolio de 10 Projets Avancés Résolus (Multi-Secteurs)
        Ce portail rassemble **10 projets complexes d'ingénierie et d'analyse de données**, couvrant l'énergie, l'électronique industrielle, la finance et la logistique :

        - **Secteur Énergie & Réseau** : API RTE Temps Réel, Audit Qualité GRT WAPP, ML Load Forecasting (Panama 40k), Big Data PySpark/Hive SQL (321 compteurs x 3 ans).
        - **Secteur Géospatiale & Satellite** : Ingestion **NASA POWER API** et interpolation par **Krigeage / BME** de l'irradiance solaire (GHI).
        - **Secteur Réseau Temps Réel & SCADA** : Flux de télémesure PMU (50 Hz) sous **PySpark Structured Streaming**.
        - **Secteur Économie de l'Énergie** : Economic Dispatch (OPF) et calcul des prix marginaux nodiaux (LMP $/MWh).
        - **Secteur IoT & Électronique** : Filtrage et analyse spectrale **FFT (Transformée de Fourier)** de capteurs de vibrations (1 kHz) et durée de vie utile (RUL).
        - **Secteur FinTech & Risk** : Moteur de **Credit Risk Scoring** bancaire et prédiction du risque de défaut.
        - **Secteur Logistique & Supply Chain** : Traitement de traces GPS de flottes de camions et optimisation d'itinéraires (réduction CO2).
        """)

    st.markdown("---")
    st.success("👈 Utilisez le menu dans la barre latérale pour explorer l'ensemble des 10 projets en détail !")

elif menu == "⚡ Projet 1 : Pipeline API RTE (Temps Réel)":
    render_projet1()

elif menu == "🛡️ Projet 2 : Qualité & Données WAPP (CEDEAO)":
    render_projet2()

elif menu == "📈 Projet 3 : Prévision ML (Load Forecasting)":
    render_projet3()

elif menu == "🐘 Projet 4 : Big Data PySpark & Hive SQL":
    render_projet4()

elif menu == "🌍 Projet 5 : Ingestion Géospatiale Satellite (NASA POWER)":
    render_projet5()

elif menu == "⚡ Projet 6 : Streaming Temps Réel PMU (PySpark)":
    render_projet6()

elif menu == "📊 Projet 7 : Analytics Marché Nodal LMP (WAPP)":
    render_projet7()

elif menu == "🔬 Projet 8 : Industrial IoT & Capteurs Électroniques (FFT)":
    render_projet8()

elif menu == "💳 Projet 9 : FinTech Big Data & Credit Risk Scoring":
    render_projet9()

elif menu == "🚚 Projet 10 : Smart Logistics & Supply Chain GPS":
    render_projet10()
