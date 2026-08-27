# -*- coding: utf-8 -*-
"""
PORTAIL MULTI-PROJETS DATA ENGINEERING & ANALYTICS WAPP
Candidat : Christophe WAVOEKE (Ingénieur Bac+5 Modélisation Mathématique & Informatique)
Poste : Ingénieur en Gestion et Analyse de Données des Systèmes Électriques (WAPP / EEEOA)
"""
import streamlit as st
import sys
import os

# Ensure subdirectories are importable
sys.path.append(os.path.dirname(__file__))

from projet1_rte_api.app_rte import render_projet1
from projet2_data_governance.data_governance_app import render_projet2
from projet3_ml_load_forecasting.ml_forecasting_app import render_projet3
from projet4_pyspark_bigdata.pyspark_app import render_projet4

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
    "Navigation Projets :",
    [
        "🏠 Accueil & Profil Candidat",
        "⚡ Projet 1 : Pipeline API RTE (Temps Réel)",
        "🛡️ Projet 2 : Qualité & Données WAPP (CEDEAO)",
        "📈 Projet 3 : Prévision ML (Load Forecasting)",
        "🐘 Projet 4 : Big Data PySpark & Hive SQL"
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
    st.title("⚡ Portfolio d'Ingénierie de Données Énergétiques & Analytics")
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
        ### 🎯 Alignement avec le Poste WAPP (Centre d'Information et de Coordination)
        Ce portail rassemble **4 projets pratiques d'ingénierie et d'analyse de données électriques**, développés sur des jeux de données ouverts 100% gratuits :

        1. **Projet 1 (API Ingestion)** : Pipeline automatisé interrogeant l'API RTE éCO2mix en temps réel avec restitution sous Streamlit.
        2. **Projet 2 (Gouvernance & Qualité)** : Engine d'audit des données télémesurées des GRT membres du WAPP et intégration des Open Data Banque Mondiale pour la zone CEDEAO.
        3. **Projet 3 (Machine Learning)** : Modèle de prévision de la demande électrique (*Load Forecasting*) sur 40 000+ relevés du Panama avec évaluation RMSE/MAE.
        4. **Projet 4 (Big Data)** : Traitement distribué sous **PySpark** & **Hive SQL** de données de comptage 15-min (UCI Data) sur cluster Docker.
        """)

    st.markdown("---")
    st.success("👈 Utilisez le menu dans la barre latérale pour explorer chaque projet en détail !")

elif menu == "⚡ Projet 1 : Pipeline API RTE (Temps Réel)":
    render_projet1()

elif menu == "🛡️ Projet 2 : Qualité & Données WAPP (CEDEAO)":
    render_projet2()

elif menu == "📈 Projet 3 : Prévision ML (Load Forecasting)":
    render_projet3()

elif menu == "🐘 Projet 4 : Big Data PySpark & Hive SQL":
    render_projet4()
