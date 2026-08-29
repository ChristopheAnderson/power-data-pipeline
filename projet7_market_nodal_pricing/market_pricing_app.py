# -*- coding: utf-8 -*-
"""
Projet 7 - Streamlit Dashboard: Marché Régional de l'Électricité WAPP & Pricing Nodal (LMP / Economic Dispatch)
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
    from opf_dispatch_optimizer import WAPPMarketDispatchOptimizer
except ImportError:
    from projet7_market_nodal_pricing.opf_dispatch_optimizer import WAPPMarketDispatchOptimizer

def render_projet7():
    st.header("📊 Projet 7 : Analytics du Marché Régional de l'Électricité (LMP & Economic Dispatch WAPP)")
    
    st.info("""
    🔗 **Sources & Accès aux Données Utilisées (Référentiel Marché Régional CEDEAO) :**
    - **Fournisseurs Officiels :** ARREC / ERERA (*Autorité de Régulation Régionale du Secteur de l'Électricité de la CEDEAO*), WAPP / EEEOA & IEEE PES
    - **Jeu de données :** *Paramètres d'Economic Dispatch, Coûts marginaux de génération ($/MWh) et capacités de transit interfrontalier WAPP*
    - **Liens officiels directs :**
      - 🌐 [Portail Officiel de l'ARREC / ERERA](https://erera.arrec.org/)
      - ⚡ [Portail du Marché Régional WAPP / EEEOA](https://ecowapp.org/)
      - 📚 [IEEE Power Systems Test Case Archive (Benchmark OPF & Dispatch)](https://labs.ece.uw.edu/pstca/)
    - **Type d'accès :** Données Réglementaires et Modèles de Marché Électrique Régional CEDEAO.
    """)

    st.markdown("""
    **Contexte Régional ARREC / ERERA & WAPP Market** :
    - Modélisation de l'**Economic Dispatch (OPF - Optimal Power Flow)** du marché de gros de l'électricité en Afrique de l'Ouest.
    - Calcul des **Prix Marginaux Nodiaux (LMP - Locational Marginal Pricing in $/MWh)** intégrant le coût marginal de production et la congestion des lignes de transport.
    - Optimisation sous contraintes de capacité de génération et de transit interfrontalier.
    """)

    st.subheader("🎛️ Simulation du Marché Électrique Régional (WAPP Market Dispatch)")

    col_req, col_cong = st.columns(2)
    with col_req:
        demand_mw = st.slider("Demande régionale totale (MW)", min_value=500, max_value=2000, value=1450, step=50)
    with col_cong:
        congestion_penalty = st.slider("Pénalité de Congestion des Lignes ($/MWh)", min_value=0.0, max_value=25.0, value=7.5, step=0.5)

    optimizer = WAPPMarketDispatchOptimizer()
    df_market, smp, total_cost = optimizer.solve_economic_dispatch(demand_mw, congestion_penalty)

    # Direct Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Télécharger la table d'Economic Dispatch (.CSV)",
            data=df_market.to_csv(index=False).encode('utf-8'),
            file_name="wapp_market_economic_dispatch.csv",
            mime="text/csv",
            key="p7_dl_csv"
        )
    with col_dl2:
        st.download_button(
            "📥 Télécharger les données de Marché (.JSON)",
            data=df_market.to_json(orient="records").encode('utf-8'),
            file_name="wapp_market_economic_dispatch.json",
            mime="application/json",
            key="p7_dl_json"
        )

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Demande Régionale MW", f"{demand_mw:,.0f} MW")
    m2.metric("Prix Marginal Système (SMP)", f"${smp:.2f} / MWh")
    m3.metric("Coût Total de Production", f"${total_cost:,.0f} / heure")
    m4.metric("Coût Moyen du MWh", f"${(total_cost/demand_mw):.2f} / MWh" if demand_mw > 0 else "0")

    st.markdown("---")

    # Dispatch Bar Chart
    st.subheader("⚡ Merit Order & Ordre de Mérite des Centrales Dispatchées")
    
    fig_dispatch = px.bar(
        df_market,
        x='node',
        y='dispatched_mw',
        color='marginal_cost_usd_mwh',
        text='unit_load_pct',
        title="Puissance Appelée (MW) par Centrale selon le Coût Marginal ($/MWh)",
        labels={"dispatched_mw": "Puissance Appelé (MW)", "node": "Nœud / Centrale", "marginal_cost_usd_mwh": "Coût Marginal ($/MWh)"},
        color_continuous_scale="Teal"
    )
    fig_dispatch.update_traces(texttemplate='%{text}% Taux Charge', textposition='outside')
    st.plotly_chart(fig_dispatch, use_container_width=True)

    # Nodal Pricing Chart
    st.subheader("💲 Prix Marginaux Nodiaux (LMP $/MWh) par Zone de Réseau")
    fig_lmp = px.line(
        df_market,
        x='node',
        y='nodal_lmp_usd_mwh',
        markers=True,
        title="Variation Spatiale du Prix du MWh ($/MWh) selon les Contraintes de Transit Ligne",
        color_discrete_sequence=['#EF4444']
    )
    st.plotly_chart(fig_lmp, use_container_width=True)

    st.subheader("📋 Résultat détaillé des Offres & Dispatching du Marché WAPP")
    st.dataframe(df_market[['node', 'filiere', 'capacity_mw', 'marginal_cost_usd_mwh', 'dispatched_mw', 'unit_load_pct', 'nodal_lmp_usd_mwh']], use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="PowerGrid - Projet 7 Marché Nodal LMP", layout="wide")
    render_projet7()
