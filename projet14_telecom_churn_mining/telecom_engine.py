# -*- coding: utf-8 -*-
"""
Projet 14 - Telecom Data Mining & Churn Prediction Engine
Analyse d'usage CDR, Pipeline ETL, Modélisation Machine Learning & Simulateur Financier de Rétention
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix, roc_curve

try:
    @pd.api.extensions.register_dataframe_accessor("telecom_summary")
    class TelecomSummaryAccessor:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def kpis(self):
            total = len(self._obj)
            churn_rate = self._obj['churn'].mean() * 100
            avg_arpu = self._obj['monthly_arpu_xof'].mean()
            avg_tenure = self._obj['tenure_months'].mean()
            return {
                'total_subscribers': total,
                'churn_rate': churn_rate,
                'avg_arpu_xof': avg_arpu,
                'avg_tenure_months': avg_tenure
            }
except Exception:
    pass

def generate_telecom_churn_data(n_samples=2500, random_state=42):
    """
    Génère un jeu de données réaliste d'abonnés télécoms (Afrique de l'Ouest / Bénin).
    Prend en compte l'usage Voix, Data, SMS, Mobile Money et les réclamations.
    """
    np.random.seed(random_state)
    
    subscriber_ids = [f"BEN-229-9{i:06d}" for i in range(1, n_samples + 1)]
    regions = np.random.choice(
        ["Littoral (Cotonou)", "Atlantique (Calavi)", "Ouémé (Porto-Novo)", "Borgou (Parakou)", "Zou (Bohicon)", "Atacora (Natitingou)"],
        size=n_samples, p=[0.38, 0.22, 0.15, 0.12, 0.08, 0.05]
    )
    plan_types = np.random.choice(["Prépayé Classique", "Prépayé Hybride", "Postpayé Entreprise"], size=n_samples, p=[0.82, 0.13, 0.05])
    network_types = np.random.choice(["4G LTE", "3G+", "5G Ready"], size=n_samples, p=[0.68, 0.24, 0.08])
    
    tenure_months = np.random.exponential(scale=18, size=n_samples).astype(int) + 1
    tenure_months = np.clip(tenure_months, 1, 72)
    
    # Usage data mensuel (Mo) et voix (minutes)
    monthly_data_mb = np.random.lognormal(mean=8.2, sigma=1.1, size=n_samples) # ~3000 Mo moyen
    monthly_data_mb = np.round(np.clip(monthly_data_mb, 50, 45000), 1)
    
    monthly_voice_mins = np.random.normal(loc=140, scale=60, size=n_samples)
    monthly_voice_mins = np.round(np.clip(monthly_voice_mins, 5, 800), 1)
    
    monthly_sms_count = np.random.poisson(lam=25, size=n_samples)
    
    # ARPU mensuel en Francs CFA (XOF)
    base_arpu = (monthly_data_mb * 0.45) + (monthly_voice_mins * 12) + (monthly_sms_count * 5)
    monthly_arpu_xof = np.round(base_arpu * np.random.uniform(0.85, 1.25, size=n_samples), 0)
    monthly_arpu_xof = np.clip(monthly_arpu_xof, 500, 45000)
    
    # Nombre de recharges et canal de recharge
    recharges_count = np.random.poisson(lam=6, size=n_samples) + 1
    momo_active = np.random.choice([1, 0], size=n_samples, p=[0.74, 0.26])
    momo_monthly_transactions = np.where(momo_active == 1, np.random.poisson(lam=12, size=n_samples) + 1, 0)
    
    # Tendance d'usage sur les 30 derniers jours par rapport aux mois précédents (en %)
    # Valeurs négatives = baisse d'usage (signal d'attrition)
    usage_trend_30d = np.random.normal(loc=-2, scale=28, size=n_samples)
    usage_trend_30d = np.round(np.clip(usage_trend_30d, -95, 80), 1)
    
    # Réclamations service client au cours des 90 derniers jours
    complaint_tickets = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.65, 0.20, 0.09, 0.04, 0.02])
    
    # Délai depuis la dernière recharge (jours)
    days_since_last_recharge = np.random.exponential(scale=5, size=n_samples).astype(int)
    days_since_last_recharge = np.clip(days_since_last_recharge, 0, 45)
    
    # Génération réaliste du Churn (probabilité logistique)
    logit = (
        - 1.8
        + 0.035 * days_since_last_recharge
        - 0.028 * usage_trend_30d
        + 0.45 * complaint_tickets
        - 0.015 * tenure_months
        - 0.00003 * monthly_arpu_xof
        - 0.40 * momo_active
    )
    prob_churn = 1 / (1 + np.exp(-logit))
    churn = (np.random.rand(n_samples) < prob_churn).astype(int)
    
    df = pd.DataFrame({
        'subscriber_id': subscriber_ids,
        'region': regions,
        'plan_type': plan_types,
        'network_type': network_types,
        'tenure_months': tenure_months,
        'monthly_data_mb': monthly_data_mb,
        'monthly_voice_mins': monthly_voice_mins,
        'monthly_sms_count': monthly_sms_count,
        'monthly_arpu_xof': monthly_arpu_xof,
        'recharges_count': recharges_count,
        'momo_active': momo_active,
        'momo_monthly_transactions': momo_monthly_transactions,
        'usage_trend_30d': usage_trend_30d,
        'complaint_tickets': complaint_tickets,
        'days_since_last_recharge': days_since_last_recharge,
        'churn': churn
    })
    
    return df

def train_churn_models(df):
    """
    Entraîne et compare 3 algorithmes de Machine Learning pour prédire l'attrition.
    """
    feature_cols = [
        'tenure_months', 'monthly_data_mb', 'monthly_voice_mins', 'monthly_sms_count',
        'monthly_arpu_xof', 'recharges_count', 'momo_active', 'momo_monthly_transactions',
        'usage_trend_30d', 'complaint_tickets', 'days_since_last_recharge'
    ]
    
    X = df[feature_cols]
    y = df['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42),
        'Régression Logistique': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    }
    
    results = {}
    best_model = None
    best_auc = -1
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        
        results[name] = {
            'model': model,
            'auc': auc,
            'f1': f1,
            'precision': prec,
            'recall': rec,
            'confusion_matrix': cm,
            'fpr': fpr,
            'tpr': tpr
        }
        
        if auc > best_auc:
            best_auc = auc
            best_model = model
            best_name = name
            
    # Feature importances du meilleur modèle ensembliste (Gradient Boosting ou Random Forest)
    feat_imp = pd.DataFrame({
        'feature': feature_cols,
        'importance': results['Gradient Boosting']['model'].feature_importances_
    }).sort_values('importance', ascending=False)
    
    return results, feat_imp, (X_test, y_test), best_name

def calculate_retention_roi(df_churned, target_percent=25, success_rate=45, promo_cost_xof=1200):
    """
    Simulateur de retour sur investissement (ROI) financier pour une campagne de rétention ciblée.
    """
    total_churners = len(df_churned)
    targeted_users = int(total_churners * (target_percent / 100))
    avg_arpu = df_churned['monthly_arpu_xof'].mean()
    
    saved_users = int(targeted_users * (success_rate / 100))
    annual_revenue_saved_xof = saved_users * avg_arpu * 12
    campaign_total_cost_xof = targeted_users * promo_cost_xof
    net_margin_xof = annual_revenue_saved_xof - campaign_total_cost_xof
    roi_percent = (net_margin_xof / campaign_total_cost_xof * 100) if campaign_total_cost_xof > 0 else 0
    
    return {
        'total_churners': total_churners,
        'targeted_users': targeted_users,
        'saved_users': saved_users,
        'avg_arpu': avg_arpu,
        'annual_revenue_saved_xof': annual_revenue_saved_xof,
        'campaign_total_cost_xof': campaign_total_cost_xof,
        'net_margin_xof': net_margin_xof,
        'roi_percent': roi_percent
    }
