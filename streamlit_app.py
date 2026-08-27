# -*- coding: utf-8 -*-
"""
PORTAIL MULTI-PROJETS DATA ENGINEERING, BIG DATA & ANALYTICS WAPP
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

st.set_page_config(
    page_title="WAPP Data Engineering Portfolio - Christophe WAVOEKE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/lightning-bolt.png", width=64)
st.sidebar.title("⚡ WAPP Portfolio Data")
st.sidebar.markdown("**Christophe WAVOEKE**  \nIngénieur Bac+5 Modélisation & Data")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Projets (7 Projets) :",
    [
        "🏠 Accueil & Profil Candidat",
        "⚡ Projet 1 : Pipeline API RTE (Temps Réel)",
        "🛡️ Projet 2 : Qualité & Données WAPP (CEDEAO)",
        "📈 Projet 3 : Prévision ML (Load Forecasting)",
        "🐘 Projet 4 : Big Data PySpark & Hive SQL",
        "🌍 Projet 5 : Ingestion Géospatiale Satellite (NASA POWER)",
        "⚡ Projet 6 : Streaming Temps Réel PMU (PySpark)",
        "📊 Projet 7 : Analytics Marché Nodal LMP (WAPP)"
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
    st.title("⚡ Portfolio d'Ingénierie de Données Énergétiques, Big Data & Analytics")
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
        ### 🎯 Portfolio de 7 Projets Avancés sur Données Énergétiques
        Ce portail rassemble **7 projets complexes d'ingénierie et d'analyse de données**, résolus sur des jeux de données ouverts 100% gratuits :

        1. **Projet 1 (API Ingestion)** : Ingestion automatisée temps réel de l'API RTE éCO2mix (JSON) & Dashboard réactif.
        2. **Projet 2 (Gouvernance & Qualité)** : Moteur d'audit de complétude % des GRT WAPP et données Banque Mondiale (CEDEAO).
        3. **Projet 3 (Machine Learning)** : Modèle de prévision de charge (*Load Forecasting*) sur 40 000+ relevés du Panama.
        4. **Projet 4 (Big Data PySpark)** : Traitement distribué sous **PySpark 3.x** & **Hive SQL** de millions de relevés 15-min.
        5. **Projet 5 (Géospatiale & Satellite)** : Ingestion **NASA POWER API** et interpolation par **Krigeage / BME** de l'irradiance solaire (GHI).
        6. **Projet 6 (Streaming Real-Time)** : Traitement de flux haute fréquence SCADA / PMU sous **PySpark Structured Streaming**.
        7. **Projet 7 (Marché & Pricing Nodal)** : Simulation de l'Economic Dispatch (OPF) et calcul des prix marginaux nodiaux ($/MWh).
        """)

    st.markdown("---")
    st.success("👈 Utilisez le menu dans la barre latérale pour explorer les 7 projets en détail !")

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
