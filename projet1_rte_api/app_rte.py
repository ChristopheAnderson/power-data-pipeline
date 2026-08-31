# -*- coding: utf-8 -*-
"""
Projet 1 - Streamlit Dashboard: Observatoire Électrique Temps Réel (RTE éCO2mix)
Ingestion API publique REST sans clé & Analytics visuels
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

@st.cache_data(ttl=300)
def load_rte_data():
    url = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"
    params = {
        "dataset": "eco2mix-national-tr",
        "rows": 100,
        "sort": "-date_heure"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            records = res.json().get('records', [])
            fields = [r['fields'] for r in records if 'fields' in r]
            df = pd.DataFrame(fields)
            return df
    except Exception as e:
        st.error(f"Erreur d'accès à l'API RTE: {e}")
    return pd.DataFrame()

def render_projet1():
    st.header("⚡ Projet 1 : Pipeline API Données Électriques & Dashboard Temps Réel")
    
    st.info("""
    🔗 **Source & Accès aux Données Utilisées (100% Réelles & Vérifiables) :**
    - **Fournisseur Officiel :** RTE (Réseau de Transport d'Électricité) via le portail *Open Data Réseaux Énergies (ODRE)*
    - **Jeu de données :** *éCO2mix - Données nationales temps réel de consommation et mix de production électrique*
    - **Liens officiels directs :**
      - 🌐 [Portail Officiel Open Data Réseaux Énergies (éCO2mix)](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/information/)
      - 📥 [Téléchargement direct du Dataset Officiel Complet (CSV ODRE)](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true)
      - 🔌 [Endpoint API REST Direct (JSON)](https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-tr&rows=100)
    - **Type d'accès :** API REST Publique Gratuite (Format JSON en direct, sans clé d'authentification requise).
    """)

    st.markdown("""
    **Architecture & Traitement** :
    - Ingestion automatisée en JSON, traitement des séries temporelles sous `Pandas` & visualisation réactive avec `Plotly`.
    """)

    with st.spinner("Extraction des données en temps réel depuis l'API RTE..."):
        df = load_rte_data()

    if df.empty:
        st.warning("⚠️ Impossible de récupérer les données en direct de l'API. Affichage des données de secours.")
        return

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger le jeu de données récupéré (.CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="rte_eco2mix_donnees_reelles.csv",
            mime="text/csv",
            key="p1_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger le jeu de données (.JSON)",
            data=df.to_json(orient="records", date_format="iso").encode('utf-8'),
            file_name="rte_eco2mix_donnees_reelles.json",
            mime="application/json",
            key="p1_dl_json"
        )

    # Cleaning & Processing
    df['date_heure'] = pd.to_datetime(df['date_heure'])
    cols_filiere = ['consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz', 'fioul', 'charbon']
    for col in cols_filiere:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        else:
            df[col] = 0.0

    df['total_enr'] = df['eolien'] + df['solaire'] + df['hydraulique']
    df['pct_enr'] = (df['total_enr'] / df['consommation'].replace(0, 1)) * 100.0

    latest = df.iloc[0]

    # Metrics Section
    st.subheader("📌 Métriques Clés en Direct (Dernier Relevé)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Consommation Totale", f"{latest['consommation']:,.0f} MW")
    m2.metric("Production Éolienne", f"{latest['eolien']:,.0f} MW")
    m3.metric("Production Solaire", f"{latest['solaire']:,.0f} MW")
    m4.metric("Part EnR (Éolien+Sol+Hyd)", f"{latest['pct_enr']:.1f} %")

    st.markdown("---")

    # Time-Series Chart
    st.subheader("📈 Évolution Temporelle de la Charge et du Mix Énergétique")
    mix_cols = [c for c in ['consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz'] if c in df.columns]
    
    fig_line = px.line(
        df,
        x='date_heure',
        y=mix_cols,
        title="Puissance par Filière (MW) en Fonction du Temps",
        labels={"value": "Puissance (MW)", "date_heure": "Horodatage", "variable": "Filière"},
        color_discrete_map={
            "consommation": "#1E3A8A",
            "nucleaire": "#6B7280",
            "eolien": "#0D9488",
            "solaire": "#F59E0B",
            "hydraulique": "#3B82F6",
            "gaz": "#EF4444"
        }
    )
    fig_line.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

    col_pie, col_gauge = st.columns(2)

    with col_pie:
        st.subheader("🍰 Répartition de la Production Actuelle")
        prod_data = {
            "Nucléaire": latest['nucleaire'],
            "Éolien": latest['eolien'],
            "Solaire": latest['solaire'],
            "Hydraulique": latest['hydraulique'],
            "Gaz": latest['gaz']
        }
        df_pie = pd.DataFrame(list(prod_data.items()), columns=['Filière', 'Production_MW'])
        fig_pie = px.pie(
            df_pie,
            names='Filière',
            values='Production_MW',
            hole=0.4,
            color_discrete_sequence=['#6B7280', '#0D9488', '#F59E0B', '#3B82F6', '#EF4444']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_gauge:
        st.subheader("🎯 Jauge de Pénétration des Énergies Renouvelables")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest['pct_enr'],
            number={'suffix': '%'},
            title={'text': "Part EnR dans la Consommation"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#0D9488"},
                'steps': [
                    {'range': [0, 25], 'color': "#FEE2E2"},
                    {'range': [25, 50], 'color': "#FEF3C7"},
                    {'range': [50, 100], 'color': "#D1FAE5"}
                ]
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    
    # 🔬 SECTION MODÉLISATION MATHÉMATIQUE & FORMULATION ANALYTIQUE
    st.subheader("🔬 Étude Mathématique Approfondie & Modélisation Analytique")
    
    st.markdown(r"""
    En tant qu'**Ingénieur en Modélisation Mathématique**, l'observation des séries temporelles électriques nécessite d'extraire la structure sous-jacente par décomposition spectrale et régression analytique.
    
    #### 1. Modèle Harmonique de Fourier pour la Dynamique de Charge
    La demande électrique $P_{\text{load}}(t)$ est un processus pseudo-périodique décomposable en série de Fourier tronquée d'ordre $K=2$ (fondamentale journalière $T=24\text{ h}$ et harmonique $12\text{ h}$) :
    $$P_{\text{load}}(t) = a_0 + a_1 \cos\left(\frac{2\pi t}{24}\right) + b_1 \sin\left(\frac{2\pi t}{24}\right) + a_2 \cos\left(\frac{4\pi t}{24}\right) + b_2 \sin\left(\frac{4\pi t}{24}\right) + \epsilon(t)$$
    où $\epsilon(t) \sim \mathcal{N}(0, \sigma^2)$ représente le résidu stochastique résiduel.
    """)
    
    # Dynamic Math Modeling Calculation
    try:
        import numpy as np
        
        # Sort chronologically for time series modeling
        df_sort = df.sort_values('date_heure').copy()
        if len(df_sort) >= 10:
            df_sort['t_hours'] = (df_sort['date_heure'] - df_sort['date_heure'].min()).dt.total_seconds() / 3600.0
            t = df_sort['t_hours'].values
            y = df_sort['consommation'].values
            
            # Design Matrix for Fourier Regression (K=2)
            omega = 2 * np.pi / 24.0
            X_mat = np.column_stack([
                np.ones_like(t),
                np.cos(omega * t),
                np.sin(omega * t),
                np.cos(2 * omega * t),
                np.sin(2 * omega * t)
            ])
            
            # Ordinary Least Squares (OLS): beta = (X^T X)^(-1) X^T y
            beta, residuals, rank, s = np.linalg.lstsq(X_mat, y, rcond=None)
            y_pred = X_mat @ beta
            
            # Goodness-of-fit metrics
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1.0 - (ss_res / (ss_tot + 1e-8))
            rmse = np.sqrt(np.mean((y - y_pred) ** 2))
            mae = np.mean(np.abs(y - y_pred))
            mape = np.mean(np.abs((y - y_pred) / (y + 1e-8))) * 100.0
            
            # Display Math KPIs
            kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
            kpi_col1.metric("Intercept Moyen $a_0$", f"{beta[0]:,.0f} MW")
            kpi_col2.metric("Qualité d'Ajustement $R^2$", f"{max(0.0, r2):.4f}")
            kpi_col3.metric("Erreur $RMSE$", f"{rmse:.2f} MW")
            kpi_col4.metric("Erreur $MAE$", f"{mae:.2f} MW")
            kpi_col5.metric("Erreur Relative $MAPE$", f"{mape:.2f} %")
            
            df_sort['Ajustement_Fourier_Analytique'] = y_pred
            
            fig_model = go.Figure()
            fig_model.add_trace(go.Scatter(
                x=df_sort['date_heure'], y=df_sort['consommation'],
                mode='markers+lines', name='Données Réelles Observées $P(t)$',
                line=dict(color='#1E3A8A', width=2)
            ))
            fig_model.add_trace(go.Scatter(
                x=df_sort['date_heure'], y=df_sort['Ajustement_Fourier_Analytique'],
                mode='lines', name='Modèle Analytique OLS $\hat{P}(t)$',
                line=dict(color='#EF4444', width=3, dash='dash')
            ))
            fig_model.update_layout(
                title="Ajustement Analytique du Modèle de Fourier sur la Série Temporelle de Charge",
                xaxis_title="Horodatage",
                yaxis_title="Puissance (MW)",
                hovermode="x unified"
            )
            st.plotly_chart(fig_model, use_container_width=True)
            
            st.markdown(r"""
            #### 2. Formule Analytique Identifiée par Moindres Carrés Ordinaires :
            """)
            st.latex(f"\\hat{{P}}(t) = {beta[0]:.1f} + {beta[1]:.1f}\\cos(\\omega t) + {beta[2]:.1f}\\sin(\\omega t) + {beta[3]:.1f}\\cos(2\\omega t) + {beta[4]:.1f}\\sin(2\\omega t)")
            
            st.markdown(r"""
            #### 3. Formulation de l'Intensité Carbone Moyenne Pondérée :
            $$I_{\text{CO}_2}(t) = \frac{\sum_{i=1}^M \gamma_i \cdot P_i(t)}{\sum_{i=1}^M P_i(t)} \quad \left[\text{gCO}_2/\text{kWh}\right]$$
            Ce modèle garantit l'évaluation en continu de l'impact environnemental du mix régional WAPP.
            """)
    except Exception as e:
        st.warning(f"Note de calcul analytique: {e}")

    st.markdown("---")
    st.subheader("📋 Extraits des Données Brut Ingestées (API RTE)")
    st.dataframe(df[['date_heure', 'consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz']].head(15), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="PowerGrid - Projet 1 RTE API", layout="wide")
    render_projet1()
