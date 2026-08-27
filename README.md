# ⚡ WAPP Power Data Pipeline & Analytics Portfolio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Candidat** : Christophe WAVOEKE (Ingénieur Bac+5 Modélisation Mathématique & Informatique)  
**Poste ciblé** : Ingénieur en Gestion et Analyse de Données des Systèmes Électriques — **West African Power Pool (WAPP / EEEOA)**  
**Institution** : Centre d'Information et de Coordination (CIC) — Division Coordination de l'Exploitation du Système (SOCD)

---

## 🎯 Aperçu du Portfolio

Ce dépôt contient la suite complète des **4 projets pratiques d'ingénierie et d'analyse de données électriques**, développés sur des sources Open Data 100% gratuites pour répondre aux exigences exactes du Terme de Référence (TDR) du WAPP :

```text
                                  +-------------------------------------------------+
                                  |     WAPP DATA PIPELINE & ANALYTICS PORTAL       |
                                  +-------------------------------------------------+
                                                           |
           +-----------------------+-----------------------+-----------------------+-----------------------+
           |                       |                       |                       |                       |
           v                       v                       v                       v                       v
+-----------------------+ +-----------------------+ +-----------------------+ +-----------------------+ +-----------------------+
|  Projet 1 : RTE API   | | Projet 2 : Quality DQ | |  Projet 3 : ML Load   | | Projet 4 : PySpark    | |   Streamlit Portal    |
| Ingestion & Dashboard | | Audit GRT & WB Data | | Forecasting (40k)   | | Big Data & Hive SQL   | |    Cloud Interactive  |
+-----------------------+ +-----------------------+ +-----------------------+ +-----------------------+ +-----------------------+
```

---

## 📂 Structure du Répertoire

```text
wapp-power-data-pipeline/
│
├── README.md                      <-- Documentation & Architecture
├── requirements.txt               <-- Dépendances Python pour le Cloud
├── .gitignore                     <-- Exclusion Git
├── streamlit_app.py               <-- Portail Multi-Projets Principal Streamlit
│
├── projet1_rte_api/
│   ├── fetch_data.py              <-- Script d'extraction ETL vers SQLite
│   └── app_rte.py                 <-- Dashboard Temps Réel API RTE éCO2mix
│
├── projet2_data_governance/
│   ├── quality_wapp.py            <-- Moteur de contrôle qualité GRT (Tension/Fréquence)
│   └── data_governance_app.py     <-- Dashboard Qualité & Données Banque Mondiale CEDEAO
│
├── projet3_ml_load_forecasting/
│   ├── generate_sample_panama_data.py <-- Générateur de séries temporelles (40 000+ relevés)
│   ├── train_ml_forecast.py       <-- Script d'entraînement Machine Learning (Random Forest)
│   └── ml_forecasting_app.py      <-- Interface de simulation des prévisions de charge
│
└── projet4_pyspark_bigdata/
    ├── docker-compose.yml         <-- Configuration Cluster Bitnami PySpark & Hive Metastore
    ├── spark_pipeline.py          <-- Pipeline d'agrégation distribuée PySpark & Hive SQL
    └── pyspark_app.py             <-- Visualisation & Benchmarks de performance Big Data
```

---

## ⚡ Description Détaillée des 4 Projets

### 1. Projet 1 — Pipeline API Données Électriques (RTE éCO2mix) & Dashboard
- **Source** : API Publique REST RTE éCO2mix (Open Data Réseaux Énergies - sans clé API).
- **Stack** : Python, Requests, Pandas, SQLite, Streamlit, Plotly.
- **Fonctionnalités** : Ingestion en temps réel des données de consommation et de production par filière (Solaire, Éolien, Hydraulique, Nucléaire, Gaz), calcul de la part EnR % et jauge réactive.

### 2. Projet 2 — Gouvernance, Qualité de Données & Analytics Afrique (WAPP / CEDEAO)
- **Source** : Données de télémesure GRT (Bénin SBEE, Côte d'Ivoire CIE, Nigeria TCN, Ghana GRIDCo) + World Bank Open Data.
- **Stack** : Python, Data Quality Metrics Engine, Plotly, Streamlit.
- **Fonctionnalités** : Audit de complétude %, détection d'anomalies de tension ($161\text{ kV} \pm 10\%$) et de fréquence ($50\text{ Hz} \pm 0.5\text{ Hz}$), cartographie d'accès à l'électricité et des pertes réseau en Afrique de l'Ouest.

### 3. Projet 3 — Machine Learning Load Forecasting (Panama - 40 000+ Relevés)
- **Source** : Kaggle Panama Electricity Load Dataset (2 ans d'historique horaire).
- **Stack** : Scikit-Learn, Pandas, Plotly, Streamlit.
- **Fonctionnalités** : Extraction de features temporelles et lags ($1\text{h}$, $24\text{h}$, $168\text{h}$), prévision de la pointe de charge avec métriques **RMSE** (43.03 MW), **MAE** (34.39 MW) et **MAPE** (3.22%).

### 4. Projet 4 — Mini Pipeline Big Data Distributed Processing (PySpark & Hive SQL)
- **Source** : UCI ML Repository - ElectricityLoadDiagrams (321 compteurs x 3 ans à 15-min).
- **Stack** : PySpark 3.5, Hive SQL, Docker Compose (`bitnami/spark`).
- **Fonctionnalités** : Traitement distribué multi-cœurs évitant les limites RAM de Pandas, requêtes Hive SQL d'agrégation de charge par heure et benchmark de performance.

---

## 🚀 Guide d'Exécution Locale

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/christopher-wavoeke/wapp-power-data-pipeline.git
   cd wapp-power-data-pipeline
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer le portail Streamlit** :
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 🌐 Déploiement sur Streamlit Community Cloud

1. Rendez-vous sur [share.streamlit.io](https://share.streamlit.io) et connectez-vous avec votre compte GitHub (**christopher-wavoeke** / `christophewavoeke18@gmail.com`).
2. Cliquez sur **"New App"**.
3. Sélectionnez le dépôt `wapp-power-data-pipeline`, la branche `main` et le fichier `streamlit_app.py`.
4. Cliquez sur **"Deploy"** !

---

## ✉️ Contact & Liens Professionnels

- **Candidat** : Christophe WAVOEKE
- **Email** : christophewavoeke18@gmail.com
- **Téléphone** : +229 01 66 81 83 76 / +229 01 40 17 77 74
- **Portfolio Web** : [christopher-portofolio.vercel.app](https://christopher-portofolio.vercel.app/)
