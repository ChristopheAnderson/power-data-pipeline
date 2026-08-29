# ⚡ Regional Power Grid & Multi-Sector Data Engineering Platform (13 Modules)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Lead Engineer** : Christophe WAVOEKE (Ingénieur Modélisation Mathématique & Informatique / Data Systems)  
**Domaine** : Ingénierie des données des réseaux interconnectés, Big Data, Traitement de Signal & Analytics Multi-Secteurs.

---

## 🎯 Architecture de la Plateforme (13 Modules Intégrés)

Cette plateforme d'ingénierie logicielle et de données regroupe **13 modules de production** couvrant l'analyse de réseaux électriques interconnectés, le streaming temps réel, la gouvernance de données, l'optimisation économique et l'analytique socio-économique :

```text
                                  +-------------------------------------------------+
                                  |    MULTI-SECTOR DATA PIPELINE & ANALYTICS       |
                                  +-------------------------------------------------+
                                                           |
  +--------+--------+--------+--------+--------+-----------+-----------+--------+--------+--------+--------+--------+--------+
  |        |        |        |        |        |           |           |        |        |        |        |        |        |
  v        v        v        v        v        v           v           v        v        v        v        v        v
[P1 API] [P2 DQ]  [P3 ML]  [P4 Spark][P5 NASA] [P6 Stream] [P7 Market] [P8 IoT]  [P9 Fin] [P10 Log][P11 Climat][P12 Santé][P13 Éco]
```

---

## 📂 Modules & Sources de Données Officielles

| Module | Périmètre & Technologies | Source des Données & Lien Cliquable |
| :--- | :--- | :--- |
| **P1** | Pipeline API RTE éCO2mix & Dashboard Temps Réel | 🔗 [Open Data Réseaux Énergies (éCO2mix)](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/information/) |
| **P2** | Qualité Télémesure GRT & Données CEDEAO | 🔗 [Système Interconnecté Ouest-Africain](https://ecowapp.org/) & [World Bank Energy](https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS) |
| **P3** | ML Load Forecasting (Panama 40k relevés) | 🔗 [Dataset Kaggle CND Panama](https://www.kaggle.com/datasets/albertovg/electric-load-forecasting-panama) |
| **P4** | Big Data PySpark 3.5 & Hive SQL (321 compteurs × 3 ans) | 🔗 [UCI ML Repository - Electricity Load Diagrams](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014) |
| **P5** | Satellite NASA POWER & Géostatistique (BME / Krigeage) | 🔗 [NASA POWER Project Portal & API](https://power.larc.nasa.gov/) |
| **P6** | Real-Time Streaming SCADA / PMU (PySpark Streaming) | 🔗 [IEEE Synchrophasor C37.118](https://standards.ieee.org/ieee/37.118.1/4766/) & [WAPP CIC](https://ecowapp.org/) |
| **P7** | Marché Régional & Nodal Pricing (LMP $/MWh) | 🔗 [ARREC / ERERA](https://erera.arrec.org/) & [Marché Énergétique Régional](https://ecowapp.org/) |
| **P8** | Industrial IoT : Capteurs, Analyse Spectrale FFT & RUL | 🔗 [NASA PCoE Prognostics Data](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) |
| **P9** | FinTech : Scoring Risque de Crédit & Défaut Bancaire | 🔗 [Kaggle Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/data) & [UCI German Credit Data](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data) |
| **P10** | Smart Logistics : Traces GPS & Optimisation CO2 Flotte | 🔗 [OpenStreetMap](https://www.openstreetmap.org/) & [Microsoft GeoLife](https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/) |
| **P11** | Climat Réel & Précipitations (Bénin / CEDEAO) | 🔗 [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) |
| **P12** | Santé Publique, Paludisme & Démographie | 🔗 [WHO GHO OData API](https://www.who.int/data/gho) & [World Bank API](https://data.worldbank.org/) |
| **P13** | Macro-Économie & Développement Durable | 🔗 [World Bank Indicators Open Data API](https://data.worldbank.org/) |

---

## 🚀 Installation & Exécution Locale

```bash
git clone https://github.com/ChristopheAnderson/energy-grid-data-platform.git
cd energy-grid-data-platform
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## ✉️ Contact & Auteur

- **Christophe WAVOEKE** (Ingénieur Modélisation Mathématique & Informatique)
- **Email** : christophewavoeke18@gmail.com
- **Téléphone** : +229 01 66 81 83 76 / +229 01 40 17 77 74
- **Portfolio Web** : [christopher-portofolio.vercel.app](https://christopher-portofolio.vercel.app/)

