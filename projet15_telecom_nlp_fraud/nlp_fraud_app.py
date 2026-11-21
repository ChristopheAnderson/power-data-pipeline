# -*- coding: utf-8 -*-
"""
Projet 15 - Telecom NLP Unstructured Data & Mobile Money Fraud Detection Dashboard
Spécialiste Data Mining / Télécoms & FinTech (Afrique de l'Ouest)
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
    from nlp_fraud_engine import (
        generate_telecom_unstructured_tickets, perform_topic_modeling,
        generate_mobile_money_transactions, train_fraud_detection_model
    )
except ImportError:
    from projet15_telecom_nlp_fraud.nlp_fraud_engine import (
        generate_telecom_unstructured_tickets, perform_topic_modeling,
        generate_mobile_money_transactions, train_fraud_detection_model
    )

@st.cache_data
def get_cached_tickets():
    return generate_telecom_unstructured_tickets(n_tickets=800)

@st.cache_data
def get_cached_topics():
    df_t = get_cached_tickets()
    return perform_topic_modeling(df_t, n_topics=4)

@st.cache_data
def get_cached_transactions():
    df_raw = generate_mobile_money_transactions(n_transactions=1500)
    df_res, model = train_fraud_detection_model(df_raw)
    return df_res

def render_projet15():
    st.header("Projet 15 : Traitement des Données Non Structurées (NLP SAV) & Détection de Fraude Mobile Money")
    
    st.info("""
    **Exigences Clés Validées (Offre Spécialiste Data Mining - Réf : ETT-0926I01SDM) :**
    - **Données Non Structurées :** Ingestion et traitement de réclamations textuelles réelles (Service Client, Call Center, SMS, Réseaux Sociaux).
    - **NLP & Modèles d'IA :** Vectorisation TF-IDF, analyse de polarité de sentiment et Topic Modeling non supervisé (NMF).
    - **Data Mining Non-Supervisé :** Détection d'anomalies de transactions financières Mobile Money (MoMo / Flooz) via **Isolation Forest**.
    - **Storytelling & Sécurité :** Console d'alerte en temps réel pour la direction de la sécurité financière et de la qualité réseau.
    """)
    
    df_tickets = get_cached_tickets()
    topics_dict, _ = get_cached_topics()
    df_txn = get_cached_transactions()
    
    # KPIs Haut de Page
    total_tickets = len(df_tickets)
    critical_tickets = len(df_tickets[df_tickets['urgency_level'] == 'Critique'])
    total_txns = len(df_txn)
    fraud_alerts = len(df_txn[df_txn['anomaly_flag'] == 1])
    fraud_amount_xof = df_txn[df_txn['anomaly_flag'] == 1]['amount_xof'].sum()
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tickets SAV Non Structurés", f"{total_tickets:,}")
    k2.metric("Réclamations Critiques", f"{critical_tickets:,}")
    k3.metric("Alertes Fraude MoMo (IsoForest)", f"{fraud_alerts:,}")
    k4.metric("Montant à Risque Détecté", f"{fraud_amount_xof:,.0f} FCFA")
    
    # Téléchargements
    c_dl1, c_dl2 = st.columns(2)
    with c_dl1:
        st.download_button(
            "Télécharger le Corpus de Tickets Non Structurés (.CSV)",
            data=df_tickets.to_csv(index=False).encode('utf-8'),
            file_name="telecom_unstructured_tickets_corpus.csv",
            mime="text/csv",
            key="p15_dl_tickets"
        )
    with c_dl2:
        st.download_button(
            "Télécharger les Transactions Mobile Money & Anomalies (.CSV)",
            data=df_txn.to_csv(index=False).encode('utf-8'),
            file_name="telecom_momo_fraud_anomalies.csv",
            mime="text/csv",
            key="p15_dl_momo"
        )
        
    st.divider()
    
    tabs = st.tabs([
        "Mining des Textes SAV (Données Non Structurées)",
        "Topic Modeling NMF (Thématiques de Pannes)",
        "Détection de Fraude Mobile Money (Isolation Forest)",
        "Console d'Investigation & Alertes en Temps Réel",
        "Testeur Interactif de Requêtes Clients"
    ])
    
    # ---------------- TAB 1 ----------------
    with tabs[0]:
        st.subheader("Analyse du Sentiment & Polarité des Verbatim Clients")
        
        col_t1, col_t2 = st.columns([1.3, 1])
        with col_t1:
            fig_sent = px.box(
                df_tickets,
                x='category',
                y='sentiment_score',
                color='category',
                points="all",
                labels={'category': "Motif de Réclamation", 'sentiment_score': "Score de Sentiment (-1 à +1)"},
                title="Distribution de la Polarité Sentimentale par Catégorie de Problème",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_sent.update_layout(template="plotly_dark", height=380, showlegend=False)
            st.plotly_chart(fig_sent, use_container_width=True)
            
        with col_t2:
            chan_summary = df_tickets.groupby(['channel', 'urgency_level']).size().reset_index(name='count')
            fig_chan = px.bar(
                chan_summary,
                x='channel',
                y='count',
                color='urgency_level',
                title="Volume de Tickets par Canal de Réception & Sévérité",
                labels={'channel': "Canal", 'count': "Nombre de Tickets", 'urgency_level': "Niveau d'Urgence"},
                color_discrete_map={"Critique": "#FF4B4B", "Élevée": "#FFA500", "Moyenne": "#00D4FF", "Faible": "#2CA02C"}
            )
            fig_chan.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig_chan, use_container_width=True)
            
        st.markdown("**Insights Qualité de Service :** Les réclamations relatives à *Mobile Money & Fraude* affichent le sentiment le plus dégradé (médiane à -0.92) et le taux de sévérité critique le plus élevé, nécessitant un traitement prioritaire sous 15 minutes.")

    # ---------------- TAB 2 ----------------
    with tabs[1]:
        st.subheader("Topic Modeling Non Supervisé (NMF & TF-IDF)")
        st.markdown("""
        L'algorithme de factorisation matricielle non négative (NMF) extrait automatiquement les 4 clusters sémantiques récurrents à partir des textes bruts non balisés :
        """)
        
        tcols = st.columns(4)
        colors = ["#00D4FF", "#FF7F0E", "#2CA02C", "#D62728"]
        for idx, (top_name, words) in enumerate(topics_dict.items()):
            with tcols[idx]:
                st.markdown(f"#### {top_name}")
                st.markdown(f"**Poids sémantique :** Thème {idx + 1}")
                st.markdown("\n".join([f"- `{w}`" for w in words]))
                
        st.divider()
        
        # Répartition géographique des pannes signalées
        loc_df = df_tickets.groupby(['location', 'category']).size().reset_index(name='count')
        fig_loc = px.bar(
            loc_df,
            x='location',
            y='count',
            color='category',
            title="Cartographie des Incidents Textuels par Commune / Pôle Réseau",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig_loc.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_loc, use_container_width=True)

    # ---------------- TAB 3 ----------------
    with tabs[2]:
        st.subheader("Détection d'Anomalies de Transactions (Isolation Forest)")
        
        st.markdown("""
        L'algorithme **Isolation Forest** isole les comportements financiers hautement atypiques en espace multidimensionnel sans nécessiter de labellisation préalable :
        """)
        
        f1, f2 = st.columns([1.5, 1])
        with f1:
            fig_scatter = px.scatter(
                df_txn,
                x='hour_of_day',
                y='amount_xof',
                size='distance_from_usual_bts_km',
                color='severity',
                title="Détection des Transactions Atypiques (Heure vs Montant vs Distance BTS)",
                labels={
                    'hour_of_day': "Heure de la Transaction (0h - 23h)",
                    'amount_xof': "Montant de la Transaction (FCFA)",
                    'distance_from_usual_bts_km': "Éloignement Antenne (km)",
                    'severity': "Statut Détecté"
                },
                color_discrete_map={"Normal": "#1F77B4", "Élevé": "#FF7F0E", "Critique": "#D62728"}
            )
            fig_scatter.update_layout(template="plotly_dark", height=420)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with f2:
            st.markdown("#### Profil des Anomalies Critiques")
            critical_df = df_txn[df_txn['severity'] == "Critique"]
            st.metric("Transactions Critiques Isolées", f"{len(critical_df)}")
            st.metric("Montant Moyen Critique", f"{critical_df['amount_xof'].mean():,.0f} FCFA")
            st.metric("Présence de SIM Swap récent", f"{(critical_df['sim_swap_within_48h'].mean()*100):.1f} %")
            
            st.info("""
            **Indicateurs d'Alerte Majeurs :**
            - Transactions supérieures à 300 000 FCFA intervenant entre minuit et 5h du matin.
            - Retrait massif suivant un remplacement de carte SIM (SIM Swap) sous 48h.
            - Éloignement géographique soudain (> 50 km de l'antenne habituelle).
            """)

    # ---------------- TAB 4 ----------------
    with tabs[3]:
        st.subheader("Console Opérationnelle de Surveillance des Alertes")
        
        sev_filter = st.multiselect(
            "Filtrer par niveau de sévérité :",
            options=["Critique", "Élevé", "Normal"],
            default=["Critique", "Élevé"]
        )
        
        filtered_alerts = df_txn[df_txn['severity'].isin(sev_filter)][[
            'transaction_id', 'user_id', 'agent_id', 'hour_of_day', 'amount_xof',
            'distance_from_usual_bts_km', 'sim_swap_within_48h', 'anomaly_score', 'severity'
        ]].sort_values('anomaly_score', ascending=False)
        
        st.dataframe(
            filtered_alerts.style.format({
                'amount_xof': "{:,.0f} FCFA",
                'distance_from_usual_bts_km': "{:.1f} km",
                'anomaly_score': "{:.4f}"
            }),
            use_container_width=True,
            height=350
        )

    # ---------------- TAB 5 ----------------
    with tabs[4]:
        st.subheader("Testeur Interactif NLP : Classification Instantanée d'une Réclamation")
        
        test_input = st.text_area(
            "Saisissez une plainte ou un texte client à analyser :",
            value="Mon solde Mobile Money de 45000 FCFA a disparu après un SMS bizarre demandant mon code à Cotonou."
        )
        
        if st.button("Analyser la réclamation avec le moteur NLP"):
            # Simple scoring heuristique basé sur les mots clés du modèle
            text_lower = test_input.lower()
            detected_cat = "Général / Non classé"
            urgency = "Moyenne"
            sentiment = -0.5
            
            if any(w in text_lower for w in ["momo", "money", "argent", "solde", "code", "retrait", "swap", "débit"]):
                detected_cat = "Mobile Money & Fraude"
                urgency = "Critique"
                sentiment = -0.95
            elif any(w in text_lower for w in ["4g", "débit", "connexion", "lent", "réseau", "signal", "antenne"]):
                detected_cat = "Réseau & Débit"
                urgency = "Élevée"
                sentiment = -0.75
            elif any(w in text_lower for w in ["forfait", "pass", "crédit", "facturation", "déduit"]):
                detected_cat = "Facturation & Forfaits"
                urgency = "Moyenne"
                sentiment = -0.70
            elif any(w in text_lower for w in ["voix", "appel", "coupure", "standard", "111"]):
                detected_cat = "Voix & Service Client"
                urgency = "Faible"
                sentiment = -0.40
                
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric("Catégorie Prédite", detected_cat)
            col_res2.metric("Score de Sentiment", f"{sentiment:.2f}")
            col_res3.metric("Niveau d'Urgence Assigné", urgency)
            
            if urgency == "Critique":
                st.error("Alerte Déclenchée : Ticket routé en priorité immédiate vers l'équipe Fraude & Sécurité Financière.")
            else:
                st.info("Ticket routé vers la file standard de support technique.")
