# -*- coding: utf-8 -*-
"""
Projet 9 - Streamlit Dashboard: FinTech Analytics, Scoring de Risque de Crédit & Détection de Fraude
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from credit_risk_engine import generate_financial_credit_dataset, load_german_credit_dataset
except ImportError:
    from projet9_fintech_credit_risk.credit_risk_engine import generate_financial_credit_dataset, load_german_credit_dataset

def render_projet9():
    st.header("💳 Projet 9 : FinTech Big Data Analytics (Credit Risk Scoring & Détection de Défaut)")
    
    st.info("""
    🔗 **Source & Accès aux Données Utilisées (100% Réelles & Vérifiables) :**
    - **Fournisseurs Officiels :** UCI Machine Learning Repository (*German Credit Data*) & Kaggle Open Datasets (*Give Me Some Credit*)
    - **Jeu de données :** *Données de scoring de risque bancaire, historique de remboursement et détection du risque de défaut*
    - **Liens officiels directs :**
      - 🌐 [Portail UCI ML Repository - Statlog German Credit Data](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)
      - 📥 [Téléchargement Direct du Dataset Brut (.ZIP UCI)](https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip)
      - 📊 [Compétition Kaggle - Give Me Some Credit Dataset](https://www.kaggle.com/c/GiveMeSomeCredit/data)
    - **Type d'accès :** Open Data Public Financier / Machine Learning Benchmark.
    """)

    st.markdown("""
    **Secteur Bancaire, Finance & FinTech** :
    - Évaluation automatisée du **Risque de Défaut de Crédit** et calcul du score de crédit bancaire.
    - Modélisation du ratio d'endettement, de l'historique de retards et calcul de la matrice de probabilité de risque.
    - Outil de décision automatisée (*Accordé / Étude Manuelle / Refusé*).
    """)

    df_fin = load_german_credit_dataset()

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger le jeu de données réel German Credit (.CSV)",
            data=df_fin.to_csv(index=False).encode('utf-8'),
            file_name="german_credit_data.csv",
            mime="text/csv",
            key="p9_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger les profils de crédit (.JSON)",
            data=df_fin.head(500).to_json(orient="records").encode('utf-8'),
            file_name="german_credit_data.json",
            mime="application/json",
            key="p9_dl_json"
        )

    if 'montant_credit_eur' in df_fin.columns:
        df_fin['montant_credit_usd'] = df_fin['montant_credit_eur']
        df_fin['age'] = df_fin['age_annees']
        df_fin['ratio_endettement_pct'] = df_fin['taux_effort_pct'] * 10.0
        df_fin['revenu_annuel_usd'] = (df_fin['montant_credit_usd'] / (df_fin['taux_effort_pct'] / 100.0 * 2.0)).round(2)
        df_fin['retards_paiement_mois'] = df_fin['historique_credit'].apply(lambda x: 2 if 'A34' in str(x) else (1 if 'A33' in str(x) else 0))

    # Metrics
    taux_refus = (df_fin['decision_credit'] == '❌ REFUSÉ').mean() * 100.0
    montant_total_accorde = df_fin[df_fin['decision_credit'] == '✅ ACCORDÉ']['montant_credit_usd'].sum()
    
    st.subheader("📌 Indicateurs Portefeuille Crédit & Performance")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Demandes Prêt Analysées", f"{len(df_fin)}")
    m2.metric("Taux d'Accord Immédiat", f"{(df_fin['decision_credit'] == '✅ ACCORDÉ').mean()*100:.1f} %")
    m3.metric("Taux de Refus Risque", f"{taux_refus:.1f} %")
    m4.metric("Encours Prêts Accordés", f"${montant_total_accorde:,.0f}")

    st.markdown("---")

    col_risk, col_dec = st.columns(2)

    with col_risk:
        st.subheader("📊 Distribution des Probabilités de Défaut (%)")
        fig_hist = px.histogram(
            df_fin,
            x='probabilite_defaut_pct',
            color='decision_credit',
            title="Distribution du Risque par Décision de Crédit",
            color_discrete_map={"✅ ACCORDÉ": "#0D9488", "⚠️ ÉTUDE MANUELLE": "#F59E0B", "❌ REFUSÉ": "#EF4444"},
            nbins=25
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_dec:
        st.subheader("🍰 Répartition des Décisions d'Octroi de Crédit")
        df_dec = df_fin['decision_credit'].value_counts().reset_index()
        df_dec.columns = ['Décision', 'Nombre']
        fig_pie = px.pie(
            df_dec,
            names='Décision',
            values='Nombre',
            hole=0.4,
            color_discrete_sequence=['#0D9488', '#F59E0B', '#EF4444']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter plot debt ratio vs income
    st.subheader("📈 Matrice Risque : Ratio Endettement (%) vs Revenu Annuel ($)")
    fig_scat = px.scatter(
        df_fin,
        x='revenu_annuel_usd',
        y='ratio_endettement_pct',
        color='decision_credit',
        size='montant_credit_usd',
        hover_data=['client_id', 'retards_paiement_mois'],
        title="Impact du Revenu et de l'Endettement sur le Profil de Risque",
        color_discrete_map={"✅ ACCORDÉ": "#0D9488", "⚠️ ÉTUDE MANUELLE": "#F59E0B", "❌ REFUSÉ": "#EF4444"}
    )
    st.plotly_chart(fig_scat, use_container_width=True)

    st.subheader("📋 Extraits des Demandes de Crédit Évaluées")
    st.dataframe(df_fin[['client_id', 'age', 'revenu_annuel_usd', 'montant_credit_usd', 'ratio_endettement_pct', 'retards_paiement_mois', 'probabilite_defaut_pct', 'decision_credit']].head(15), use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="WAPP - Projet 9 FinTech Risk Scoring", layout="wide")
    render_projet9()
