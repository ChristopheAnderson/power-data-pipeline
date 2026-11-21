# -*- coding: utf-8 -*-
"""
Projet 15 - Telecom Unstructured NLP & Mobile Money Fraud Detection Engine
Mining de données textuelles (SAV Call Center) & Détection d'anomalies de transactions financières
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def generate_telecom_unstructured_tickets(n_tickets=800, random_state=42):
    """
    Génère un corpus représentatif de tickets de réclamations clients non structurés (en français)
    dans le contexte des télécommunications et des services financiers mobiles en Afrique de l'Ouest.
    """
    np.random.seed(random_state)
    
    templates = [
        # Catégorie 1: Réseau & Débit
        ("Connexion 4G très lente et coupures fréquentes depuis ce matin à {loc}.", "Réseau & Débit", -0.7, "Élevée"),
        ("Impossible de charger les vidéos, le débit internet est quasi nul à {loc}.", "Réseau & Débit", -0.8, "Moyenne"),
        ("Perte totale de signal réseau sur mon téléphone depuis hier soir vers {loc}.", "Réseau & Débit", -0.9, "Critique"),
        ("Le réseau 4G bascule sans cesse en 2G Edge, navigation impossible.", "Réseau & Débit", -0.6, "Moyenne"),
        
        # Catégorie 2: Forfaits & Facturation
        ("Mon forfait data mensuel a été épuisé en deux jours sans utilisation intensive.", "Facturation & Forfaits", -0.7, "Moyenne"),
        ("Crédit principal déduit alors que j'avais activé un pass nuit illimité.", "Facturation & Forfaits", -0.8, "Élevée"),
        ("Échec d'activation du bundle data après débit du solde principal de 2000 FCFA.", "Facturation & Forfaits", -0.9, "Élevée"),
        ("Facturation abusive de SMS promotionnels non sollicités sur ma ligne.", "Facturation & Forfaits", -0.5, "Faible"),
        
        # Catégorie 3: Mobile Money & Fraude
        ("Débit suspect de {amount} FCFA sur mon compte Mobile Money sans mon code secret !", "Mobile Money & Fraude", -1.0, "Critique"),
        ("Tentative de retrait non autorisée signalée par SMS chez un agent à {loc}.", "Mobile Money & Fraude", -0.95, "Critique"),
        ("Transfert MoMo validé mais le destinataire n'a jamais reçu les fonds après 4 heures.", "Mobile Money & Fraude", -0.75, "Élevée"),
        ("Ma carte SIM a été désactivée sans ma demande, suspicion de SIM swap frauduleux.", "Mobile Money & Fraude", -1.0, "Critique"),
        
        # Catégorie 4: Qualité Vocale & Service Client
        ("Appels vocaux hachés et coupures automatiques après 30 secondes de communication.", "Voix & Service Client", -0.6, "Moyenne"),
        ("Service client injoignable après 25 minutes d'attente au standard 111.", "Voix & Service Client", -0.7, "Faible"),
        ("Bonne assistance reçue hier en agence mais le problème persiste sur la ligne.", "Voix & Service Client", 0.2, "Faible"),
        ("Service rapide en agence de {loc}, merci pour la réactivation de la ligne.", "Voix & Service Client", 0.8, "Faible")
    ]
    
    locations = ["Cotonou (Cadjehoun)", "Cotonou (Akpakpa)", "Abomey-Calavi", "Porto-Novo", "Parakou", "Bohicon", "Ouidah"]
    
    tickets = []
    for i in range(1, n_tickets + 1):
        tmpl, category, sentiment_base, urgency_base = templates[np.random.choice(len(templates))]
        loc = np.random.choice(locations)
        amount = np.random.choice([5000, 15000, 25000, 50000, 100000])
        
        text = tmpl.format(loc=loc, amount=amount)
        sentiment = np.round(sentiment_base + np.random.uniform(-0.15, 0.15), 2)
        sentiment = np.clip(sentiment, -1.0, 1.0)
        
        # Urgence
        urgency = urgency_base
        if sentiment < -0.85 and urgency != "Critique":
            urgency = "Élevée"
            
        tickets.append({
            'ticket_id': f"TCK-2026-{i:05d}",
            'date': pd.Timestamp('2026-11-01') + pd.Timedelta(days=np.random.randint(0, 21), hours=np.random.randint(0, 24)),
            'raw_text': text,
            'category': category,
            'sentiment_score': sentiment,
            'urgency_level': urgency,
            'channel': np.random.choice(["App Mobile", "Call Center (Voix)", "SMS Réclamation", "Twitter / X", "WhatsApp Support"], p=[0.35, 0.25, 0.15, 0.15, 0.10]),
            'location': loc
        })
        
    df_tickets = pd.DataFrame(tickets).sort_values('date', ascending=False)
    return df_tickets

def perform_topic_modeling(df_tickets, n_topics=4):
    """
    Extraction de sujets (Topic Modeling) non supervisé par NMF et TF-IDF.
    """
    french_stop_words = [
        "de", "la", "le", "et", "les", "des", "en", "un", "une", "du", "sur", "mon", "ma",
        "mes", "ce", "cette", "ces", "pour", "dans", "par", "au", "aux", "avec", "sans",
        "depuis", "hier", "matin", "soir", "mais", "vers", "hier", "apres", "vers"
    ]
    
    tfidf = TfidfVectorizer(max_features=500, stop_words=french_stop_words, ngram_range=(1, 2))
    tfidf_matrix = tfidf.fit_transform(df_tickets['raw_text'])
    
    nmf = NMF(n_components=n_topics, random_state=42, max_iter=200)
    nmf_matrix = nmf.fit_transform(tfidf_matrix)
    
    feature_names = tfidf.get_feature_names_out()
    topics = {}
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-7:-1]]
        topics[f"Topic {topic_idx + 1}"] = top_words
        
    return topics, nmf_matrix

def generate_mobile_money_transactions(n_transactions=1500, random_state=42):
    """
    Génère un flux de transactions Mobile Money (MoMo / Flooz) avec marqueurs de fraude complexes.
    """
    np.random.seed(random_state)
    
    txn_ids = [f"TXN-MM-229-{i:07d}" for i in range(1, n_transactions + 1)]
    user_ids = [f"USR-{np.random.randint(1000, 3500)}" for _ in range(n_transactions)]
    agent_ids = [f"AGT-COT-{np.random.randint(10, 80):03d}" for _ in range(n_transactions)]
    
    # Heure de la transaction (0 à 23h)
    hour_probs = np.array([
        0.01, 0.01, 0.01, 0.01, 0.01, 0.02, # 0h-5h (creux)
        0.04, 0.06, 0.08, 0.09, 0.08, 0.07, # 6h-11h
        0.06, 0.06, 0.07, 0.08, 0.09, 0.08, # 12h-17h
        0.07, 0.05, 0.03, 0.01, 0.01, 0.00  # 18h-23h
    ], dtype=float)
    hour_probs = hour_probs / hour_probs.sum()
    
    hour_of_day = np.random.choice(range(24), size=n_transactions, p=hour_probs)
    
    # Montant en FCFA
    amount_xof = np.random.lognormal(mean=9.5, sigma=1.2, size=n_transactions) # ~25 000 FCFA médian
    amount_xof = np.round(np.clip(amount_xof, 500, 1500000), -2)
    
    # Distance inhabituelle de l'antenne BTS par rapport à la zone habituelle (en km)
    distance_from_usual_bts_km = np.random.exponential(scale=3.5, size=n_transactions)
    distance_from_usual_bts_km = np.round(np.clip(distance_from_usual_bts_km, 0.1, 120), 1)
    
    # Tentatives de code PIN échouées avant validation
    failed_pin_attempts = np.random.choice([0, 1, 2, 3], size=n_transactions, p=[0.88, 0.08, 0.03, 0.01])
    
    # Remplacement de carte SIM (SIM Swap) dans les 48h précédentes (1 = Oui, 0 = Non)
    sim_swap_within_48h = np.random.choice([0, 1], size=n_transactions, p=[0.97, 0.03])
    
    # Ratio retrait / dépôt moyen sur les 7 derniers jours
    withdrawal_to_deposit_ratio = np.random.uniform(0.1, 2.5, size=n_transactions)
    
    # Injection de motifs de fraude réels :
    # Si SIM swap + heure nocturne + montant élevé -> forte anomalie
    is_injected_fraud = (
        (sim_swap_within_48h == 1) & (amount_xof > 200000)
    ) | (
        (hour_of_day < 5) & (amount_xof > 350000) & (failed_pin_attempts >= 2)
    ) | (
        (distance_from_usual_bts_km > 60) & (amount_xof > 500000)
    )
    
    df_txn = pd.DataFrame({
        'transaction_id': txn_ids,
        'user_id': user_ids,
        'agent_id': agent_ids,
        'hour_of_day': hour_of_day,
        'amount_xof': amount_xof,
        'distance_from_usual_bts_km': distance_from_usual_bts_km,
        'failed_pin_attempts': failed_pin_attempts,
        'sim_swap_within_48h': sim_swap_within_48h,
        'withdrawal_ratio': np.round(withdrawal_to_deposit_ratio, 2),
        'ground_truth_fraud': is_injected_fraud.astype(int)
    })
    
    return df_txn

def train_fraud_detection_model(df_txn):
    """
    Modèle de Data Mining non-supervisé (Isolation Forest) pour détecter les transactions atypiques.
    """
    feature_cols = [
        'hour_of_day', 'amount_xof', 'distance_from_usual_bts_km',
        'failed_pin_attempts', 'sim_swap_within_48h', 'withdrawal_ratio'
    ]
    X = df_txn[feature_cols]
    
    # Isolation Forest avec contamination estimée à 3.5%
    iso_forest = IsolationForest(n_estimators=120, contamination=0.035, random_state=42)
    preds = iso_forest.fit_predict(X)
    scores = iso_forest.decision_function(X)
    
    df_res = df_txn.copy()
    df_res['anomaly_flag'] = np.where(preds == -1, 1, 0)
    df_res['anomaly_score'] = -scores # Plus le score est élevé, plus c'est anormal
    
    # Classification de sévérité
    def get_severity(row):
        if row['anomaly_flag'] == 0:
            return "Normal"
        if row['anomaly_score'] > 0.12 or row['sim_swap_within_48h'] == 1:
            return "Critique"
        return "Élevé"
        
    df_res['severity'] = df_res.apply(get_severity, axis=1)
    return df_res, iso_forest
