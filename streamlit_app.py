# -*- coding: utf-8 -*-
"""
PLATEFORME D'INGÉNIERIE DE DONNÉES & ANALYTICS RÉSEAUX ÉNERGÉTIQUES (13 Modules)
Lead Engineer : Christophe WAVOEKE (Ingénieur Modélisation Mathématique & Informatique / Data Systems)
"""
import streamlit as st
import sys, os
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
from projet11_climate_agriculture.climate_dashboard import render_projet11
from projet12_health_demographics.health_demographics_dashboard import render_projet12
from projet13_economy_development.economy_development_dashboard import render_projet13

st.set_page_config(
    page_title="Power Grid & Multi-Sector Data Engineering Platform",
    page_icon="⚡", layout="wide", initial_sidebar_state="expanded"
)

# --- PHOTO DE PROFIL DANS LA BARRE LATÉRALE ---
PROFILE_PIC_PATH = None
for path in ["assets/profile.jpg", "assets/profile.png", "assets/profile.jpeg", "profile.jpg", "profile.png"]:
    if os.path.exists(os.path.join(os.path.dirname(__file__), path)):
        PROFILE_PIC_PATH = os.path.join(os.path.dirname(__file__), path)
        break

if PROFILE_PIC_PATH:
    st.sidebar.image(PROFILE_PIC_PATH, width=120)
else:
    # URL de photo de profil par défaut ou avatar
    st.sidebar.image("https://raw.githubusercontent.com/ChristopheAnderson/energy-grid-data-platform/main/assets/profile.jpg", width=120, fallback="https://img.icons8.com/color/96/user-female-circle.png")

st.sidebar.title("⚡ PowerGrid & Data Suite")
st.sidebar.markdown("**Christophe WAVOEKE**  \nIngénieur Modélisation & Data Systems")
st.sidebar.markdown("---")
st.sidebar.caption("🔵 Énergie & Réseaux Électriques")
st.sidebar.caption("🟢 Big Data & Multi-Secteurs")
st.sidebar.caption("🟡 Données & Indicateurs Régionaux")

PAGES = {
    "🏠 Vue d'ensemble de la Plateforme": None,
    # --- ÉNERGIE ---
    "⚡ P1 : Pipeline API RTE (Temps Réel)": render_projet1,
    "🛡️ P2 : Qualité & Gouvernance Données Énergie": render_projet2,
    "📈 P3 : Prévision ML (Load Forecasting)": render_projet3,
    "🐘 P4 : Big Data PySpark & Hive SQL": render_projet4,
    "🌍 P5 : Satellite Géospatiale (NASA POWER)": render_projet5,
    "📡 P6 : Streaming Temps Réel PMU/SCADA": render_projet6,
    "📊 P7 : Marché Nodal & Dispatch Économique": render_projet7,
    # --- MULTI-SECTEURS ---
    "🔬 P8 : IoT & Capteurs Électroniques (FFT)": render_projet8,
    "💳 P9 : FinTech & Credit Risk Scoring": render_projet9,
    "🚚 P10 : Smart Logistics & Supply Chain": render_projet10,
    # --- AFRIQUE RÉELLE (APIS) ---
    "🌧️ P11 : Climat & Précipitations (Open-Meteo API)": render_projet11,
    "🏥 P12 : Santé & Démographie (WHO GHO + World Bank)": render_projet12,
    "📊 P13 : Économie & Développement (World Bank API)": render_projet13,
}

menu = st.sidebar.radio("Navigation :", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("✉️ christophewavoeke18@gmail.com  \n📞 +229 01 66 81 83 76  \n🌐 [Portfolio](https://christopher-portofolio.vercel.app/)  \n🐱 [GitHub Repository](https://github.com/ChristopheAnderson/energy-grid-data-platform)")

if menu == "🏠 Vue d'ensemble de la Plateforme":
    st.title("⚡ Power Grid & Multi-Sector Data Engineering Platform")
    st.subheader("Architecture de Traitement, Big Data, Streaming SCADA & Optimisation Énergétique")

    st.markdown("""
    Cette suite applicative intègre **13 pipelines de données et modules d'analyse avancée** en production,
    couvrant la **gestion des réseaux électriques interconnectés**, le **Big Data**, les **flux IoT / Télémétrie**,
    la **FinTech**, la **Logistique** et les **indicateurs socio-économiques régionaux**.
    """)

    categories = {
        "⚡ ÉNERGIE & RÉSEAU (P1–P7)": [
            "**P1** · API RTE éCO2mix Temps Réel — 🔗 [Données Open Data Réseaux Énergies (ODRE)](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/information/) | 📥 *Téléchargeable en direct (.CSV / .JSON) sur la sous-page*",
            "**P2** · Gouvernance & Qualité des Données GRT WAPP — 🔗 [Portail WAPP](https://ecowapp.org/) & [Banque Mondiale Énergie](https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P3** · ML Load Forecasting (Panama 40k relevés) — 🔗 [Dataset Kaggle CND Panama](https://www.kaggle.com/datasets/albertovg/electric-load-forecasting-panama) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P4** · Big Data PySpark 3.5 & Hive SQL (321 compteurs × 3 ans) — 🔗 [UCI ML Repository Dataset](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P5** · Ingestion Satellite NASA POWER & Géostatistique BME — 🔗 [Portail & API NASA POWER](https://power.larc.nasa.gov/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P6** · Streaming SCADA/PMU 50 Hz (PySpark Structured Streaming) — 🔗 [Standard IEEE C37.118](https://standards.ieee.org/ieee/37.118.1/4766/) & [WAPP CIC](https://ecowapp.org/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P7** · Economic Dispatch & Prix Marginaux Nodiaux LMP ($/MWh) — 🔗 [ARREC / ERERA](https://erera.arrec.org/) & [Marché WAPP](https://ecowapp.org/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
        ],
        "🌐 MULTI-SECTEURS (P8–P10)": [
            "**P8** · Industrial IoT : Traitement de Signal FFT & RUL — 🔗 [NASA PCoE Prognostics Data](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P9** · FinTech : Credit Risk Scoring & Détection de Défaut — 🔗 [UCI German Credit Data](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data) & [Kaggle Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/data) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P10** · Smart Logistics : Traces GPS & Optimisation CO2 — 🔗 [OpenStreetMap](https://www.openstreetmap.org/) & [Microsoft Research GeoLife](https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
        ],
        "🌍 AFRIQUE RÉELLE — APIs Gratuites (P11–P13)": [
            "**P11** · Climat Réel (Précipitations Bénin / CEDEAO) — 🔗 [API Open-Meteo Historical Weather](https://open-meteo.com/en/docs/historical-weather-api) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P12** · Paludisme, Santé & Démographie — 🔗 [API WHO GHO](https://www.who.int/data/gho) & [API World Bank](https://data.worldbank.org/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
            "**P13** · Macro-Économie & Développement Durable — 🔗 [API World Bank Open Data](https://data.worldbank.org/) | 📥 *Téléchargeable en direct (.CSV / .JSON)*",
        ]
    }

    for cat, items in categories.items():
        with st.expander(cat, expanded=True):
            for item in items:
                st.markdown(f"- {item}")

    st.success("👈 Naviguez dans le menu latéral : chaque sous-page contient des boutons de téléchargement direct (.CSV / .JSON) et des liens vers les portails officiels !")
else:
    fn = PAGES[menu]
    if fn:
        fn()
