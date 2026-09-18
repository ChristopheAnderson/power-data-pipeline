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

# --- CSS DE GESTION DE LA BARRE LATÉRALE REPLIABLE ---
st.markdown("""
<style>
    /* Bouton de fermeture de la barre latérale toujours visible et stylisé */
    [data-testid="stSidebarCollapseButton"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        opacity: 1 !important;
        visibility: visible !important;
        background: rgba(0, 212, 255, 0.12) !important;
        color: #00D4FF !important;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 6px rgba(0, 212, 255, 0.25) !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #00D4FF !important;
        color: #0b1120 !important;
        border-color: #00D4FF !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stSidebarCollapseButton"] button::after {
        content: " Masquer";
        font-size: 11px;
        font-weight: 600;
        margin-left: 3px;
    }

    /* Bouton pour rouvrir la barre latérale repliée */
    [data-testid="stSidebarCollapsedControl"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        background: #0b1120 !important;
        color: #00D4FF !important;
        border: 1px solid #00D4FF !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 6px 12px !important;
        font-weight: 600 !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: #1e293b !important;
        color: #38bdf8 !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stSidebarCollapsedControl"] button::after {
        content: " Menu";
        font-size: 11px;
        font-weight: 600;
        margin-left: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- PHOTO DE PROFIL DANS LA BARRE LATÉRALE (RONDE & CENTRÉE) ---
PROFILE_PIC_PATH = None
for path in ["assets/profile.jpg", "assets/profile.png", "assets/profile.jpeg", "profile.jpg", "profile.png"]:
    if os.path.exists(os.path.join(os.path.dirname(__file__), path)):
        PROFILE_PIC_PATH = os.path.join(os.path.dirname(__file__), path)
        break

img_src = "https://raw.githubusercontent.com/ChristopheAnderson/energy-grid-data-platform/main/assets/profile.jpg"
if PROFILE_PIC_PATH:
    import base64
    with open(PROFILE_PIC_PATH, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    ext = PROFILE_PIC_PATH.split('.')[-1].lower()
    if ext == 'jpg':
        ext = 'jpeg'
    img_src = f"data:image/{ext};base64,{encoded}"

st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 15px;">
        <img src="{img_src}" style="width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 3px solid #00D4FF; box-shadow: 0 4px 12px rgba(0,212,255,0.25);" />
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("⚡ PowerGrid & Data Suite")
st.sidebar.markdown("**Christophe WAVOEKE**  \nIngénieur Modélisation & Data Systems")
st.sidebar.markdown("---")
st.sidebar.caption("🔵 Énergie & Réseaux Électriques")
st.sidebar.caption("🟢 Big Data & Multi-Secteurs")
st.sidebar.caption("🟡 Données & Indicateurs Régionaux")
st.sidebar.info("💡 **Affichage large :** Cliquez sur **« Masquer** en haut à droite pour replier ce menu et afficher les graphiques en pleine largeur.")

import streamlit.components.v1 as components

def render_cv():
    st.markdown("## 📄 Curriculum Vitæ Exécutif — Christophe WAVOEKE")
    st.markdown("**Ingénieur Modélisation Mathématique & Informatique | Data Systems & Big Data**")
    
    cv_dir = os.path.join(os.path.dirname(__file__), "assets")
    cv_pdf_path = os.path.join(cv_dir, "cv.pdf")
    cv_html_path = os.path.join(cv_dir, "cv.html")
    
    col1, col2, col3 = st.columns([1.5, 1.5, 3])
    with col1:
        if os.path.exists(cv_pdf_path):
            with open(cv_pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le CV (PDF Officiel 2 Pages)",
                    data=f.read(),
                    file_name="CV_Christophe_WAVOEKE_Data_Analyst_BI.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    with col2:
        if os.path.exists(cv_html_path):
            with open(cv_html_path, "r", encoding="utf-8") as f:
                html_data = f.read()
            st.download_button(
                label="🌐 Télécharger la Version HTML Standalone",
                data=html_data,
                file_name="CV_Christophe_WAVOEKE_Data_Analyst_BI.html",
                mime="text/html",
                use_container_width=True
            )
    with col3:
        st.info("💡 **Aperçu haute fidélité :** Le CV interactif complet est navigable ci-dessous avec tous les liens vers les démonstrateurs et dépôts GitHub.")

    if os.path.exists(cv_html_path):
        with open(cv_html_path, "r", encoding="utf-8") as f:
            raw_html = f.read()
        components.html(raw_html, height=1250, scrolling=True)
    else:
        st.error("Le fichier du CV HTML est introuvable dans le dossier assets.")

PAGES = {
    "🏠 Vue d'ensemble de la Plateforme": None,
    "📄 Curriculum Vitæ (CV Exécutif)": render_cv,
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

default_index = 0
try:
    page_param = st.query_params.get("page", "").lower()
    if page_param:
        for idx, p_name in enumerate(PAGES.keys()):
            if page_param in p_name.lower():
                default_index = idx
                break
except Exception:
    pass

menu = st.sidebar.radio("Navigation :", list(PAGES.keys()), index=default_index)
st.sidebar.markdown("---")
st.sidebar.info("✉️ christophewavoeke18@gmail.com  \n📞 +229 01 66 81 83 76  \n🌐 [Portfolio Web](https://christopher-portofolio.vercel.app/)  \n📊 [Démonstrateurs Data Analytics & BI](https://data-analytics-bi-portfolio-ek57rbdepycxrx94gjvdv8.streamlit.app/)  \n🐱 [GitHub Repository](https://github.com/ChristopheAnderson/power-data-pipeline)")

if menu == "🏠 Vue d'ensemble de la Plateforme":
    st.title("⚡ Power Grid & Multi-Sector Data Engineering Platform")
    st.subheader("Architecture de Traitement, Big Data, Streaming SCADA & Optimisation Énergétique")

    st.markdown("""
    Cette suite applicative intègre **13 pipelines de données et modules d'analyse avancée** en production,
    couvrant la **gestion des réseaux électriques interconnectés**, le **Big Data**, les **flux IoT / Télémétrie**,
    la **FinTech**, la **Logistique** et les **indicateurs socio-économiques régionaux**.
    """)

    st.info("📄 **Curriculum Vitæ Exécutif :** Consultez l'onglet **« 📄 Curriculum Vitæ (CV Exécutif) »** dans le menu latéral pour visualiser le profil complet en format interactif ou télécharger le PDF officiel 2 pages.")


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
