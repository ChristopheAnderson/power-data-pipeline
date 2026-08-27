# ⚡ WAPP Power Data Pipeline, Big Data & Analytics Portfolio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Candidat** : Christophe WAVOEKE (Ingénieur Bac+5 Modélisation Mathématique & Informatique)  
**Poste ciblé** : Ingénieur en Gestion et Analyse de Données des Systèmes Électriques — **West African Power Pool (WAPP / EEEOA)**  
**Institution** : Centre d'Information et de Coordination (CIC) — Division Coordination de l'Exploitation du Système (SOCD)

---

## 🎯 Aperçu du Portfolio (7 Projets Avancés)

Ce dépôt contient la suite complète des **7 projets complexes d'ingénierie, de Big Data et d'analyse de données électriques**, développés sur des sources Open Data 100% gratuites pour répondre aux exigences du Terme de Référence (TDR) du WAPP :

```text
                                  +-------------------------------------------------+
                                  |     WAPP DATA PIPELINE & ANALYTICS PORTAL       |
                                  +-------------------------------------------------+
                                                           |
           +-------------------+-------------------+-------+-------+-------------------+-------------------+
           |                   |                   |               |                   |                   |
           v                   v                   v               v                   v                   v
+-------------------+ +-------------------+ +-------------------+ +-------------------+ +-------------------+ +-------------------+
| Projet 1 : RTE    | | Projet 2 : Quality| | Projet 3 : ML     | | Projet 4 : PySpark| | Projet 5 : NASA   | | Projet 6 : PMU    |
| API Ingestion     | | Audit GRT & WB    | | Load Forecasting  | | Big Data / Hive   | | Satellite & BME   | | Realtime Streaming|
+-------------------+ +-------------------+ +-------------------+ +-------------------+ +-------------------+ +-------------------+
```

---

## 📂 Structure du Répertoire

```text
wapp-power-data-pipeline/
│
├── README.md                      <-- Documentation & Architecture
├── requirements.txt               <-- Dépendances Python pour le Cloud
├── .gitignore                     <-- Exclusion Git
├── streamlit_app.py               <-- Portail Multi-Projets Principal (7 Projets)
│
├── projet1_rte_api/               <-- Ingestion API RTE éCO2mix (Données Temps Réel)
├── projet2_data_governance/       <-- Moteur Qualité GRT & Données Banque Mondiale (CEDEAO)
├── projet3_ml_load_forecasting/   <-- Machine Learning Prévision de Charge (Panama 40k)
├── projet4_pyspark_bigdata/       <-- Big Data PySpark 3.5 & Hive SQL (UCI 321 clients)
├── projet5_geospatial_solar/      <-- API NASA POWER Satellite & Géostatistique (BME/Krigeage)
├── projet6_streaming_pyspark/     <-- PySpark Structured Streaming & SCADA/PMU 50 Hz
└── projet7_market_nodal_pricing/  <-- Marché Régional WAPP & Nodal Marginal Pricing (LMP)
```

---

## ⚡ Description Détaillée des 7 Projets

### 1. Projet 1 — Pipeline API RTE éCO2mix & Dashboard Temps Réel
- Ingestion sans clé de l'API REST RTE (JSON). Stockage SQLite et visuels Plotly du mix électrique.

### 2. Projet 2 — Gouvernance, Qualité de Données & Analytics Afrique (WAPP / CEDEAO)
- Audit de complétude % des GRT (Bénin, Côte d'Ivoire, Nigeria, Ghana) et indicateurs Banque Mondiale.

### 3. Projet 3 — Machine Learning Load Forecasting (Panama - 40 000+ Relevés)
- Modélisation de la pointe de charge avec Random Forest (RMSE: 43.03 MW, MAE: 34.39 MW, MAPE: 3.22%).

### 4. Projet 4 — Mini Pipeline Big Data Distributed Processing (PySpark & Hive SQL)
- Traitement distribué sous **PySpark 3.5** et requêtes **Hive SQL** sur cluster Docker Bitnami.

### 5. Projet 5 — Ingestion Géospatiale Satellite (NASA POWER API) & Géostatistique
- Ingestion satellite GHI, variogramme expérimental $\gamma(h)$ et interpolation par **Krigeage/IDW** (Rapprochement direct avec la thèse d'ingénieur ENSGMM de Christophe WAVOEKE).

### 6. Projet 6 — Real-Time Streaming & SCADA/PMU (PySpark Structured Streaming)
- Traitement en streaming des signaux PMU (50 Hz), fenêtres glissantes et détection des chutes de fréquence (< 49.5 Hz).

### 7. Projet 7 — Marché Régional WAPP & Locational Marginal Pricing (LMP $/MWh)
- Optimisation de l'Economic Dispatch (OPF) du marché régional d'électricité CEDEAO et calcul des prix marginaux nodiaux.

---

## 🚀 Exécution Locale

```bash
git clone https://github.com/christopher-wavoeke/wapp-power-data-pipeline.git
cd wapp-power-data-pipeline
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

---

## ✉️ Contact & Links

- **Candidat** : Christophe WAVOEKE (Bac+5 Modélisation Mathématique & Informatique)
- **Email** : christophewavoeke18@gmail.com
- **Téléphone** : +229 01 66 81 83 76 / +229 01 40 17 77 74
- **Portfolio Web** : [christopher-portofolio.vercel.app](https://christopher-portofolio.vercel.app/)
