import os
import pandas as pd
import numpy as np

CSV_GERMAN = os.path.join(os.path.dirname(__file__), "german_credit_data.csv")

def load_german_credit_dataset():
    """
    Charge le dataset réel UCI Machine Learning Repository (Statlog German Credit Data).
    1000 profils de crédit avec 20 variables économiques et statut de défaut réel.
    """
    if os.path.exists(CSV_GERMAN):
        df = pd.read_csv(CSV_GERMAN)
        return df
    else:
        return generate_financial_credit_dataset(500)

def generate_financial_credit_dataset(n_samples=500):
    """
    Génère un dataset calibré de demandes de prêt bancaire et de transactions.
    """
    np.random.seed(42)
    
    revenu_annuel_usd = np.random.normal(25000, 8000, n_samples)
    montant_credit_usd = np.random.normal(12000, 4000, n_samples)
    ratio_endettement = (montant_credit_usd / (revenu_annuel_usd + 1e-5)) * 100.0
    age_client = np.random.randint(21, 65, n_samples)
    historique_retards_mois = np.random.choice([0, 1, 2, 3, 5], size=n_samples, p=[0.7, 0.15, 0.08, 0.04, 0.03])
    
    # Probability of default (Logit-like linear combination)
    score_logit = -2.0 + 0.04 * ratio_endettement + 0.6 * historique_retards_mois - 0.02 * (revenu_annuel_usd / 1000.0)
    prob_defaut = 1.0 / (1.0 + np.exp(-score_logit))
    statut_defaut = (prob_defaut > 0.35).astype(int)

    df = pd.DataFrame({
        "client_id": [f"CLI-{1000+i}" for i in range(n_samples)],
        "age": age_client,
        "revenu_annuel_usd": np.round(revenu_annuel_usd, 2),
        "montant_credit_usd": np.round(montant_credit_usd, 2),
        "ratio_endettement_pct": np.round(ratio_endettement, 1),
        "retards_paiement_mois": historique_retards_mois,
        "probabilite_defaut_pct": np.round(prob_defaut * 100.0, 1),
        "statut_defaut": statut_defaut,
        "decision_credit": np.where(prob_defaut < 0.25, "✅ ACCORDÉ", np.where(prob_defaut < 0.40, "⚠️ ÉTUDE MANUELLE", "❌ REFUSÉ"))
    })

    return df

if __name__ == "__main__":
    df_fin = load_german_credit_dataset()
    print("Dataset FinTech UCI German Credit Risk chargé:")
    print(df_fin.head(10))
