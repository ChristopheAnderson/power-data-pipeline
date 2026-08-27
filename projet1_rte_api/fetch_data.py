# -*- coding: utf-8 -*-
"""
ETL Background Script - RTE éCO2mix Real-Time Data Fetcher
Extracts live electrical mix data from RTE Open Data API and stores in SQLite.
"""
import requests
import pandas as pd
import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "rte_power_data.db")

def init_db():
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

def fetch_rte_api(rows=100):
    url = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"
    params = {
        "dataset": "eco2mix-national-tr",
        "rows": rows,
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
        print(f"Error fetching RTE API: {e}")
    return pd.DataFrame()

def save_to_db(df):
    if df.empty:
        return 0
    
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cols = ['consommation', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz', 'fioul', 'charbon', 'taux_co2']
    for c in cols:
        if c not in df.columns:
            df[c] = 0.0
        else:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
            
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserted = 0
    
    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO rte_records 
                (date_heure, consommation, nucleaire, eolien, solaire, hydraulique, gaz, fioul, charbon, taux_co2, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row.get('date_heure', '')),
                float(row.get('consommation', 0.0)),
                float(row.get('nucleaire', 0.0)),
                float(row.get('eolien', 0.0)),
                float(row.get('solaire', 0.0)),
                float(row.get('hydraulique', 0.0)),
                float(row.get('gaz', 0.0)),
                float(row.get('fioul', 0.0)),
                float(row.get('charbon', 0.0)),
                float(row.get('taux_co2', 0.0)),
                now_str
            ))
            inserted += cursor.rowcount
        except Exception as err:
            pass

    conn.commit()
    conn.close()
    return inserted

if __name__ == "__main__":
    print("Executing RTE API Fetcher...")
    data = fetch_rte_api(rows=50)
    count = save_to_db(data)
    print(f"Extraction completed. {count} new records stored in SQLite ({DB_PATH}).")
