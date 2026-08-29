# -*- coding: utf-8 -*-
"""
Projet 3 - Streamlit Dashboard: Prévision ML de la Demande Électrique (Load Forecasting)
Dataset Panama (40 000+ relevés horaires / 2 ans) & Modélisation Régression Time-Series
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import pickle

# Bulletproof sys.path setup for standalone or imported execution
dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from generate_sample_panama_data import generate_panama_dataset
    from train_ml_forecast import create_features, train_and_evaluate
except ImportError:
    from projet3_ml_load_forecasting.generate_sample_panama_data import generate_panama_dataset
    from projet3_ml_load_forecasting.train_ml_forecast import create_features, train_and_evaluate

DATA_PATH = os.path.join(dir_path, "sample_panama_load.csv")
MODEL_PATH = os.path.join(dir_path, "load_forecast_model.pkl")

def get_data_and_model():
    if not os.path.exists(DATA_PATH):
        generate_panama_dataset()
    
    if not os.path.exists(MODEL_PATH):
        train_and_evaluate()

    df = pd.read_csv(DATA_PATH)
    with open(MODEL_PATH, "rb") as f:
        artifacts = pickle.load(f)
    return df, artifacts

def render_projet3():
    st.header("📈 Projet 3 : Machine Learning Load Forecasting (Prévision de Charge Électrique)")
    
    st.info("""
    🔗 **Source & Accès aux Données Utilisées (100% Réelles & Vérifiables) :**
    - **Fournisseurs Officiels :** Centro Nacional de Despacho (CND Panama) / Kaggle Open Datasets
    - **Jeu de données :** *Electric Load Forecasting Panama (40 000+ relevés horaires réels de demande électrique & météo)*
    - **Liens officiels directs :**
      - 🌐 [Jeu de données officiel Kaggle - Electric Load Forecasting Panama](https://www.kaggle.com/datasets/albertovg/electric-load-forecasting-panama)
      - 🏛️ [Site Officiel du CND Panama (Centro Nacional de Despacho)](https://www.cnd.com.pa/)
    - **Type d'accès :** Open Data Public CSV (Séries temporelles historiques réelles 2015-2020).
    """)

    st.markdown("""
    **Modélisation Prédictive Métier WAPP (CIC)** :
    - Prévision à court et moyen terme (24h à 7 jours) de la demande électrique nationale/régionale.
    - Dataset d'entraînement : **40 000+ relevés horaires (Panama Electricity Load)** avec composantes de saisonnalité (heure, jour de semaine, température).
    - Modèle : `RandomForestRegressor` avec fenêtres glissantes (*Rolling Mean 24h*) et variables retardées (*Lags 1h, 24h, 168h*).
    """)

    df_raw, artifacts = get_data_and_model()

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger le jeu de données réel Panama Load (.CSV)",
            data=df_raw.to_csv(index=False).encode('utf-8'),
            file_name="panama_load_forecasting_dataset.csv",
            mime="text/csv",
            key="p3_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger les données (.JSON)",
            data=df_raw.head(1000).to_json(orient="records", date_format="iso").encode('utf-8'),
            file_name="panama_load_forecasting_dataset.json",
            mime="application/json",
            key="p3_dl_json"
        )

    model = artifacts["model"]
    metrics = artifacts["metrics"]
    feature_cols = artifacts["feature_cols"]

    # Metrics display
    st.subheader("🎯 Performances du Modèle sur l'Échantillon de Test (Validation Croisée)")
    c1, c2, c3 = st.columns(3)
    c1.metric("RMSE (Erreur Quadratique Moyenne)", f"{metrics['rmse']:.2f} MW")
    c2.metric("MAE (Erreur Absolue Moyenne)", f"{metrics['mae']:.2f} MW")
    c3.metric("MAPE (Erreur Relative Moyenne)", f"{metrics['mape']:.2f} %")

    st.markdown("---")

    # Simulation Controls
    st.subheader("🎛️ Simulation Interactive de Prévision de Charge")
    
    col_horizon, col_temp = st.columns(2)
    with col_horizon:
        horizon_hours = st.slider("Horizon de prévision (heures)", min_value=24, max_value=168, value=72, step=24)
    with col_temp:
        temp_delta = st.slider("Variation de température simulée (°C)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)

    df_feat = create_features(df_raw)
    
    # Predict on test set slice
    test_slice = df_feat.tail(horizon_hours).copy()
    test_slice['temperature'] = test_slice['temperature'] + temp_delta
    
    predictions = model.predict(test_slice[feature_cols])
    test_slice['forecast_mw'] = predictions

    # Chart Comparison
    st.subheader("📊 Consommation Réelle vs Prévision ML")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(test_slice['datetime']),
        y=test_slice['nat_demand'],
        mode='lines',
        name='Charge Réelle (MW)',
        line=dict(color='#1E3A8A', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(test_slice['datetime']),
        y=test_slice['forecast_mw'],
        mode='lines',
        name='Prévision ML (MW)',
        line=dict(color='#0D9488', width=2, dash='dash')
    ))

    fig.update_layout(
        title=f"Prévision de la Demande Électrique sur {horizon_hours} Heures ({horizon_hours//24} jours)",
        xaxis_title="Date & Heure",
        yaxis_title="Puissance (MW)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Feature Importance
    st.subheader("🔍 Importance des Variables de Prédiction (Feature Importance)")
    importances = model.feature_importances_
    df_imp = pd.DataFrame({"Variable": feature_cols, "Importance": importances}).sort_values("Importance", ascending=True)
    
    fig_imp = px.bar(df_imp, x='Importance', y='Variable', orientation='h', title="Poids des Variables dans l'Algorithme RF", color='Importance', color_continuous_scale='Teal')
    st.plotly_chart(fig_imp, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 3 ML Load Forecast", layout="wide")
    render_projet3()
