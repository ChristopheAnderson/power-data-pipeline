# -*- coding: utf-8 -*-
"""
ETL Background Script - RTE éCO2mix Real-Time Data Fetcher
Extracts live electrical mix data from RTE Open Data API and stores in SQLite.

Architecture ETL :
  [RTE Open Data API] → (requests HTTP GET) → [JSON] → (Pandas) → [Nettoyage] → (SQLite) → [rte_power_data.db]

Corrections appliquées (bonnes pratiques production) :
  1. Logging explicite des erreurs d'insertion (abandon du 'except: pass' silencieux).
  2. Validation obligatoire de date_heure avant insertion (évite les clés primaires vides).
  3. Utilisation de datetime UTC pour fetched_at (robustesse multi-fuseaux horaires).
"""
import requests
import pandas as pd
import sqlite3
import datetime
import os
import logging

# --- Configuration du Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# --- Chemin de la base SQLite (dans le même dossier que le script) ---
DB_PATH = os.path.join(os.path.dirname(__file__), "rte_power_data.db")


def init_db():
    """
    Initialise la base SQLite et crée la table rte_records si elle n'existe pas.

    Schéma :
        date_heure      TEXT PRIMARY KEY  → Horodatage unique de la mesure (ISO 8601)
        consommation    REAL              → Puissance consommée nationale (MW)
        nucleaire       REAL              → Production nucléaire (MW)
        eolien          REAL              → Production éolienne (MW)
        solaire         REAL              → Production solaire photovoltaïque (MW)
        hydraulique     REAL              → Production hydraulique (MW)
        gaz             REAL              → Production gaz naturel (MW)
        fioul           REAL              → Production fioul (MW)
        charbon         REAL              → Production charbon (MW)
        taux_co2        REAL              → Intensité carbone du mix (gCO2/kWh)
        fetched_at      TEXT              → Horodatage UTC de l'ingestion ETL
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rte_records (
            date_heure TEXT PRIMARY KEY,
            consommation REAL,
            nucleaire REAL,
            eolien REAL,
            solaire REAL,
            hydraulique REAL,
            gaz REAL,
            fioul REAL,
            charbon REAL,
            taux_co2 REAL,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info(f"Base SQLite initialisée : {DB_PATH}")


def fetch_rte_api(rows=100):
    """
    Extrait les télémesures temps réel depuis l'API Open Data Réseaux Énergies (ODRE).

    Paramètres :
        rows (int) : Nombre d'enregistrements à récupérer (par défaut 100).

    Retourne :
        pd.DataFrame : DataFrame contenant les relevés du mix électrique national.
                       Retourne un DataFrame vide en cas d'erreur réseau.
    """
    url = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"
    params = {
        "dataset": "eco2mix-national-tr",
        "rows": rows,
        "sort": "-date_heure"   # Tri antéchronologique : données les plus récentes en premier
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            records = res.json().get('records', [])
            fields = [r['fields'] for r in records if 'fields' in r]
            df = pd.DataFrame(fields)
            logger.info(f"API RTE : {len(df)} enregistrements extraits.")
            return df
        else:
            logger.warning(f"API RTE a retourné le code HTTP {res.status_code}.")
    except Exception as e:
        logger.error(f"Erreur réseau lors de l'appel à l'API RTE : {e}")
    return pd.DataFrame()


def save_to_db(df):
    """
    Transforme et charge le DataFrame dans la base SQLite (étapes T et L de l'ETL).

    Transformations appliquées :
        - Colonnes manquantes imputées à 0.0.
        - Conversion forcée en type numérique (pd.to_numeric).
        - Remplacement des NaN résiduels par 0.0.
        - Validation obligatoire de date_heure (clé primaire non vide).
        - INSERT OR IGNORE pour garantir l'idempotence du pipeline.

    Paramètres :
        df (pd.DataFrame) : DataFrame issu de fetch_rte_api().

    Retourne :
        int : Nombre de nouveaux enregistrements effectivement insérés.
    """
    if df.empty:
        logger.warning("DataFrame vide reçu. Aucune insertion effectuée.")
        return 0

    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Colonnes numériques attendues ---
    cols = ['consommation', 'nucleaire', 'eolien', 'solaire',
            'hydraulique', 'gaz', 'fioul', 'charbon', 'taux_co2']

    for c in cols:
        if c not in df.columns:
            df[c] = 0.0
        else:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

    # CORRECTION 3 : Utilisation de datetime UTC pour la traçabilité des fuseaux horaires
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    inserted = 0

    for idx, row in df.iterrows():

        # CORRECTION 2 : Validation obligatoire de date_heure avant insertion
        date_heure = row.get('date_heure')
        if not date_heure or str(date_heure).strip() == '':
            logger.warning(f"Ligne {idx} ignorée : date_heure absente ou vide.")
            continue

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO rte_records 
                (date_heure, consommation, nucleaire, eolien, solaire, hydraulique, gaz, fioul, charbon, taux_co2, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(date_heure),
                float(row.get('consommation', 0.0)),
                float(row.get('nucleaire', 0.0)),
                float(row.get('eolien', 0.0)),
                float(row.get('solaire', 0.0)),
                float(row.get('hydraulique', 0.0)),
                float(row.get('gaz', 0.0)),
                float(row.get('fioul', 0.0)),
                float(row.get('charbon', 0.0)),
                float(row.get('taux_co2', 0.0)),
                now_utc
            ))
            inserted += cursor.rowcount

        # CORRECTION 1 : Logging explicite des erreurs (abandon du 'except: pass' silencieux)
        except Exception as err:
            logger.error(f"Erreur d'insertion pour date_heure={date_heure} : {err}")

    conn.commit()
    conn.close()
    logger.info(f"{inserted} nouveaux enregistrements insérés dans {DB_PATH}.")
    return inserted


if __name__ == "__main__":
    logger.info("=== Démarrage du pipeline ETL RTE éCO2mix ===")
    data = fetch_rte_api(rows=50)
    count = save_to_db(data)
    logger.info(f"=== Pipeline terminé. {count} nouveaux relevés stockés dans SQLite ({DB_PATH}). ===")
