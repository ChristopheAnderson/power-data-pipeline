# -*- coding: utf-8 -*-
"""
PORTAIL MULTI-PROJETS DATA ENGINEERING & ANALYTICS (13 Projets — Énergie + Multi-Secteurs + Afrique)
Candidat : Christophe WAVOEKE (Ingénieur Bac+5 Modélisation Mathématique & Informatique)
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
    page_title="Data Portfolio 13 Projets - Christophe WAVOEKE",
    page_icon="⚡", layout="wide", initial_sidebar_state="expanded"
)

st.sidebar.image("https://img.icons8.com/color/96/lightning-bolt.png", width=60)
st.sidebar.title("⚡ Portfolio 13 Projets")
st.sidebar.markdown("**Christophe WAVOEKE**  \nIngénieur Bac+5 Modélisation & Data")
st.sidebar.markdown("---")
st.sidebar.caption("🔵 Projets Énergie & Réseau")
st.sidebar.caption("🟢 Projets Multi-Secteurs")
st.sidebar.caption("🟡 Projets Afrique Réelle (APIs)")

PAGES = {
    "🏠 Accueil & Profil Candidat": None,
    # --- ÉNERGIE ---
    "⚡ P1 : Pipeline API RTE (Temps Réel)": render_projet1,
    "🛡️ P2 : Qualité & Données WAPP (CEDEAO)": render_projet2,
    "📈 P3 : Prévision ML (Load Forecasting)": render_projet3,
    "🐘 P4 : Big Data PySpark & Hive SQL": render_projet4,
    "🌍 P5 : Satellite Géospatiale (NASA POWER)": render_projet5,
    "📡 P6 : Streaming Temps Réel PMU/SCADA": render_projet6,
    "📊 P7 : Marché Nodal WAPP (LMP $/MWh)": render_projet7,
    # --- MULTI-SECTEURS ---
    "🔬 P8 : IoT & Capteurs Électroniques (FFT)": render_projet8,
    "💳 P9 : FinTech & Credit Risk Scoring": render_projet9,
    "🚚 P10 : Smart Logistics & Supply Chain": render_projet10,
    # --- AFRIQUE RÉELLE (APIS) ---
    "🌧️ P11 : Climat Réel (Open-Meteo API — Bénin)": render_projet11,
    "🏥 P12 : Santé & Démographie (WHO GHO + World Bank)": render_projet12,
    "📊 P13 : Économie & Développement (World Bank API)": render_projet13,
}

menu = st.sidebar.radio("Navigation :", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("✉️ christophewavoeke18@gmail.com  \n📞 +229 01 66 81 83 76  \n🌐 [Portfolio](https://christopher-portofolio.vercel.app/)  \n🐱 [GitHub](https://github.com/christopher-wavoeke/wapp-power-data-pipeline)")

if menu == "🏠 Accueil & Profil Candidat":
    st.title("⚡ Portfolio Data — 13 Projets : Énergie, Multi-Secteurs & Afrique")
    st.subheader("Christophe WAVOEKE | Ingénieur Bac+5 ENSGMM — Major de Promotion 2023")

    st.markdown("""
    Ce portail démontre **13 projets d'ingénierie de données** réels et fonctionnels,
    couvrant les secteurs **Énergie** (WAPP), **Big Data**, **IoT / Électronique**,
    **FinTech**, **Logistique** et les **réalités sociales et économiques de l'Afrique de l'Ouest**.
    """)

    categories = {
        "⚡ ÉNERGIE & RÉSEAU (P1–P7)": [
            "P1 · API RTE éCO2mix Temps Réel",
            "P2 · Gouvernance & Qualité des Données GRT WAPP",
            "P3 · ML Load Forecasting (Panama 40k relevés, RMSE 43 MW)",
            "P4 · Big Data PySpark 3.5 & Hive SQL (321 compteurs × 3 ans)",
            "P5 · Ingestion Satellite NASA POWER & Géostatistique BME/Krigeage",
            "P6 · Streaming SCADA/PMU 50 Hz (PySpark Structured Streaming)",
            "P7 · Economic Dispatch & Prix Marginaux Nodiaux LMP ($/MWh)",
        ],
        "🌐 MULTI-SECTEURS (P8–P10)": [
            "P8 · Industrial IoT : Traitement de Signal FFT & Durée de Vie Restante (RUL)",
            "P9 · FinTech : Credit Risk Scoring & Détection de Risque de Défaut Bancaire",
            "P10 · Logistique : Traces GPS Flotte & Optimisation CO2 des Tournées",
        ],
        "🌍 AFRIQUE RÉELLE — APIs Gratuites (P11–P13)": [
            "P11 · Précipitations & Risques Climatiques (Open-Meteo Archive API — Bénin)",
            "P12 · Paludisme, Santé & Démographie (WHO GHO API + World Bank API)",
            "P13 · PIB, Pauvreté, Chômage & Développement Durable (World Bank API)",
        ]
    }

    for cat, items in categories.items():
        with st.expander(cat, expanded=True):
            for item in items:
                st.markdown(f"- {item}")

    st.success("👈 Naviguez dans le menu latéral pour explorer les 13 projets en détail avec des données réelles !")
else:
    fn = PAGES[menu]
    if fn:
        fn()
