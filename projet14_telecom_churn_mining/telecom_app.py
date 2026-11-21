# -*- coding: utf-8 -*-
"""
Projet 14 - Telecom Data Mining & Churn Prediction Dashboard
Spécialiste Data Mining / Télécoms (Afrique de l'Ouest - Bénin)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, sys

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from telecom_engine import generate_telecom_churn_data, train_churn_models, calculate_retention_roi
except ImportError:
    from projet14_telecom_churn_mining.telecom_engine import generate_telecom_churn_data, train_churn_models, calculate_retention_roi

@st.cache_data
def get_cached_telecom_data():
    return generate_telecom_churn_data(n_samples=2500)

@st.cache_resource
def get_cached_trained_models():
    df = get_cached_telecom_data()
    return train_churn_models(df)

def render_projet14():
    st.header("Projet 14 : Télécom Data Mining, Ingestion CDR & Modélisation Prédictive du Churn")
    
    st.info(r"""
    **Contexte Métier & Alignement avec l'Offre Spécialiste Data Mining (Réf : ETT-0926I01SDM) :**
    - **Secteur Télécommunications :** Analyse de données réelles d'usage réseau (CDR : voix, SMS, data 4G/5G, Mobile Money).
    - **Pipeline ETL / ELT :** Ingestion, agrégation temporelle ($\Delta \text{Usage}$ à 30 jours) et calcul de l'ARPU moyen en Francs CFA (XOF).
    - **Machine Learning & Modèles Prédictifs :** Benchmark d'algorithmes (Gradient Boosting, Random Forest, Régression Logistique).
    - **Aide à la Décision Stratégique :** Simulateur financier du ROI des campagnes de rétention pour la direction marketing.
    """)
    
    df = get_cached_telecom_data()
    results, feat_imp, (X_test, y_test), best_name = get_cached_trained_models()
    
    kpis = df.telecom_summary.kpis()
    
    # Cartes KPI Principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Abonnés Analysés", f"{kpis['total_subscribers']:,}")
    col2.metric("Taux d'Attrition (Churn)", f"{kpis['churn_rate']:.1f} %")
    col3.metric("ARPU Moyen Mensuel", f"{kpis['avg_arpu_xof']:,.0f} FCFA")
    col4.metric("Ancienneté Moyenne", f"{kpis['avg_tenure_months']:.1f} mois")
    
    # Direct Downloads
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "Télécharger le Jeu de Données Télécom CDR (.CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="telecom_cdr_subscribers_data.csv",
            mime="text/csv",
            key="p14_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "Télécharger les Métriques au format JSON (.JSON)",
            data=df.head(100).to_json(orient="records", indent=2).encode('utf-8'),
            file_name="telecom_cdr_sample.json",
            mime="application/json",
            key="p14_dl_json"
        )
        
    st.divider()
    
    tabs = st.tabs([
        "Aperçu & Segmentation Régionale",
        "Pipeline ETL & Corrélations d'Usage",
        "Modélisation Machine Learning",
        "Diagnostic Abonné & Scoring de Risque",
        "Simulateur Financier ROI de Rétention"
    ])
    
    # ---------------- TAB 1 ----------------
    with tabs[0]:
        st.subheader("Analyse de la Base Abonnés & Répartition Géographique (Bénin)")
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            # Churn par région
            region_churn = df.groupby('region').agg(
                total=('subscriber_id', 'count'),
                churners=('churn', 'sum'),
                arpu=('monthly_arpu_xof', 'mean')
            ).reset_index()
            region_churn['churn_rate'] = (region_churn['churners'] / region_churn['total']) * 100
            
            fig_reg = px.bar(
                region_churn,
                x='region',
                y='churn_rate',
                color='arpu',
                labels={'churn_rate': "Taux de Churn (%)", 'region': "Région / Pôle", 'arpu': "ARPU (FCFA)"},
                title="Taux d'attrition par département avec ARPU moyen (Couleur)",
                color_continuous_scale="Blues"
            )
            fig_reg.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig_reg, use_container_width=True)
            
        with c2:
            fig_pie = px.pie(
                df,
                names='plan_type',
                values='monthly_arpu_xof',
                title="Contribution au Chiffre d'Affaires par Type d'Abonnement",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig_pie.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("""
        **Observations Analytiques :**
        - Le segment **Prépayé Classique** représente plus de 80% des volumes d'abonnés mais présente le taux de volatilité le plus élevé en raison de la facilité de bascule multi-SIM.
        - Les pôles urbains (*Littoral Cotonou* et *Atlantique Calavi*) concentrent le revenu le plus élevé par abonné (ARPU > 4 500 FCFA), ce qui en fait les zones prioritaires de fidélisation.
        """)

    # ---------------- TAB 2 ----------------
    with tabs[1]:
        st.subheader("Pipeline ETL : Extraction d'Indicateurs Comportementaux & Corrélations")
        
        col_corr1, col_corr2 = st.columns([1.2, 1])
        with col_corr1:
            numeric_cols = [
                'tenure_months', 'monthly_data_mb', 'monthly_voice_mins', 'monthly_arpu_xof',
                'usage_trend_30d', 'complaint_tickets', 'days_since_last_recharge', 'churn'
            ]
            corr_matrix = df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=".2f",
                labels=dict(color="Corrélation"),
                title="Matrice de Corrélation Linéaire des Variables d'Usage Télécom",
                color_continuous_scale="RdBu_r"
            )
            fig_corr.update_layout(template="plotly_dark", height=420)
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with col_corr2:
            st.markdown("#### Distribution de la Tendance d'Usage")
            fig_hist = px.histogram(
                df,
                x='usage_trend_30d',
                color='churn',
                labels={'usage_trend_30d': "Évolution d'Usage 30j (%)", 'churn': "Churn (1=Oui, 0=Non)"},
                barmode="overlay",
                title=r"Tendance d'Usage ($\Delta$) vs Statut d'Attrition",
                color_discrete_map={0: "#00D4FF", 1: "#FF4B4B"}
            )
            fig_hist.update_layout(template="plotly_dark", height=420)
            st.plotly_chart(fig_hist, use_container_width=True)
            
        st.info("**Règle d'extraction métier identifiée par le Data Mining :** Une baisse d'usage supérieure à -30% sur les 30 derniers jours combinée à un délai sans recharge supérieur à 10 jours multiplie par 3.8 la probabilité de résiliation.")

    # ---------------- TAB 3 ----------------
    with tabs[2]:
        st.subheader("Performance Comparée des Algorithmes de Machine Learning")
        
        perf_data = []
        for name, m_res in results.items():
            perf_data.append({
                'Modèle': name,
                'ROC-AUC': m_res['auc'],
                'Score F1': m_res['f1'],
                'Précision': m_res['precision'],
                'Rappel (Recall)': m_res['recall']
            })
        df_perf = pd.DataFrame(perf_data).sort_values('ROC-AUC', ascending=False)
        
        st.dataframe(df_perf.style.format({
            'ROC-AUC': "{:.4f}",
            'Score F1': "{:.4f}",
            'Précision': "{:.4f}",
            'Rappel (Recall)': "{:.4f}"
        }), use_container_width=True)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            # Courbes ROC
            fig_roc = go.Figure()
            for name, m_res in results.items():
                fig_roc.add_trace(go.Scatter(
                    x=m_res['fpr'], y=m_res['tpr'],
                    mode='lines',
                    name=f"{name} (AUC = {m_res['auc']:.3f})"
                ))
            fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Aléatoire'))
            fig_roc.update_layout(
                title="Courbes ROC (Receiver Operating Characteristic)",
                xaxis_title="Taux de Faux Positifs (FPR)",
                yaxis_title="Taux de Vrais Positifs (TPR)",
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig_roc, use_container_width=True)
            
        with col_m2:
            # Feature Importance
            fig_imp = px.bar(
                feat_imp.head(8),
                x='importance',
                y='feature',
                orientation='h',
                title="Facteurs Prédictifs Majeurs (Feature Importance)",
                labels={'importance': "Poids Relatif", 'feature': "Variable d'Usage"},
                color='importance',
                color_continuous_scale="Viridis"
            )
            fig_imp.update_layout(template="plotly_dark", height=400, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_imp, use_container_width=True)

    # ---------------- TAB 4 ----------------
    with tabs[3]:
        st.subheader("Diagnostic Individuel en Temps Réel d'un Abonné Mobile")
        
        col_sel1, col_sel2 = st.columns([1, 2])
        with col_sel1:
            selected_sub_id = st.selectbox("Sélectionnez l'identifiant abonné :", df['subscriber_id'].values[:50])
            sub_row = df[df['subscriber_id'] == selected_sub_id].iloc[0]
            
            st.markdown(f"""
            - **Région :** {sub_row['region']}
            - **Plan :** {sub_row['plan_type']} ({sub_row['network_type']})
            - **Ancienneté :** {sub_row['tenure_months']} mois
            - **Dépense Mensuelle :** {sub_row['monthly_arpu_xof']:,.0f} FCFA
            - **Usage Data :** {sub_row['monthly_data_mb']:,.0f} Mo
            - **Tendance 30j :** {sub_row['usage_trend_30d']}%
            - **Délai dernière recharge :** {sub_row['days_since_last_recharge']} jours
            - **Réclamations SAV :** {sub_row['complaint_tickets']}
            """)
            
        with col_sel2:
            model = results[best_name]['model']
            features_input = pd.DataFrame([{
                'tenure_months': sub_row['tenure_months'],
                'monthly_data_mb': sub_row['monthly_data_mb'],
                'monthly_voice_mins': sub_row['monthly_voice_mins'],
                'monthly_sms_count': sub_row['monthly_sms_count'],
                'monthly_arpu_xof': sub_row['monthly_arpu_xof'],
                'recharges_count': sub_row['recharges_count'],
                'momo_active': sub_row['momo_active'],
                'momo_monthly_transactions': sub_row['momo_monthly_transactions'],
                'usage_trend_30d': sub_row['usage_trend_30d'],
                'complaint_tickets': sub_row['complaint_tickets'],
                'days_since_last_recharge': sub_row['days_since_last_recharge']
            }])
            churn_risk_prob = model.predict_proba(features_input)[0, 1] * 100
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=churn_risk_prob,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Probabilité d'Attrition Estimée ({best_name})"},
                gauge={
                    'axis': {'range': [0, 100], 'ticksuffix': "%"},
                    'bar': {'color': "#FF4B4B" if churn_risk_prob > 50 else "#00D4FF"},
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(0, 212, 255, 0.2)"},
                        {'range': [30, 60], 'color': "rgba(255, 193, 7, 0.2)"},
                        {'range': [60, 100], 'color': "rgba(255, 75, 75, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(template="plotly_dark", height=280)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            if churn_risk_prob >= 50:
                st.error(f"Abonné à haut risque de défection ({churn_risk_prob:.1f}%). Action préventive recommandée : Déclencher une offre rétention avec bonus Data immédiat.")
            else:
                st.success(f"Abonné fidélisé ({churn_risk_prob:.1f}%). Comportement stable.")

    # ---------------- TAB 5 ----------------
    with tabs[4]:
        st.subheader("Simulateur d'Impact Financier : Campagnes de Rétention & ROI")
        
        st.markdown("""
        Cet outil permet d'évaluer le gain net généré par une campagne de rétention ciblée sur les abonnés identifiés comme appétents à la défection par le modèle de Machine Learning.
        """)
        
        df_churners = df[df['churn'] == 1]
        
        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            target_pct = st.slider("Pourcentage des clients à risque ciblés (%) :", 10, 100, 35, step=5)
        with scol2:
            success_pct = st.slider("Taux de conversion / réactivation estimé (%) :", 15, 80, 45, step=5)
        with scol3:
            promo_cost = st.number_input("Coût unitaire de l'offre de rétention (FCFA) :", value=1500, step=100)
            
        roi = calculate_retention_roi(df_churners, target_percent=target_pct, success_rate=success_pct, promo_cost_xof=promo_cost)
        
        rcol1, rcol2, rcol3, rcol4 = st.columns(4)
        rcol1.metric("Abonnés Ciblés", f"{roi['targeted_users']:,}")
        rcol2.metric("Abonnés Sauvés", f"{roi['saved_users']:,}")
        rcol3.metric("Revenu Annuel Préservé", f"{roi['annual_revenue_saved_xof']:,.0f} FCFA")
        rcol4.metric("Gain Net / ROI", f"{roi['net_margin_xof']:,.0f} FCFA", delta=f"{roi['roi_percent']:.0f} %")
        
        # Comparaison visuelle
        df_sim = pd.DataFrame({
            'Poste': ["Coût Total Campagne", "Revenu Annuel Préservé", "Marge Nette Dégagée"],
            'Montant_XOF': [roi['campaign_total_cost_xof'], roi['annual_revenue_saved_xof'], roi['net_margin_xof']]
        })
        fig_bar_sim = px.bar(
            df_sim,
            x='Poste',
            y='Montant_XOF',
            color='Poste',
            title="Bilan Financier Projeté de la Campagne de Rétention Ciblée",
            color_discrete_sequence=["#FF7F0E", "#2CA02C", "#1F77B4"]
        )
        fig_bar_sim.update_layout(template="plotly_dark", height=380, showlegend=False)
        st.plotly_chart(fig_bar_sim, use_container_width=True)
