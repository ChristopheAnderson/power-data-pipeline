# -*- coding: utf-8 -*-
"""
Projet 4 - PySpark & Hive SQL Distributed Pipeline (Pandas Simulation)
Aggregates high-frequency 15-minute smart meter consumption across 321 clients.

NOTE: This module simulates PySpark behavior using pandas for compatibility
with Python 3.14+. PySpark officially supports Python 3.8–3.12 only.
To use real PySpark, set up a separate Python 3.10/3.11 virtual environment.
"""
import pandas as pd
import numpy as np
import os
import datetime


def run_spark_pipeline(data_file_path=None):
    """
    Simulates a PySpark/Hive SQL distributed pipeline using pandas.
    Performs the same aggregations (avg, max, group by hour) as the Spark version.
    """
    print("Initialisation du pipeline distribué (simulation PySpark via pandas)...")

    # --- Load or generate data ---
    if not data_file_path or not os.path.exists(data_file_path):
        print("Génération d'un échantillon distribué (1 000 lignes × 15 min)...")
        base_time = datetime.datetime(2024, 1, 1, 0, 0)
        records = []
        for i in range(1000):
            t = base_time + datetime.timedelta(minutes=15 * i)
            records.append({
                "timestamp": t,
                "client_1": round(1.2 + (i % 10) * 0.5, 4),
                "client_2": round(2.1 + (i % 7) * 0.3, 4),
                "client_3": round(0.8 + (i % 5) * 0.2, 4),
            })
        df = pd.DataFrame(records)
    else:
        df = pd.read_csv(data_file_path, sep=";", header=0)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        for col in ["client_1", "client_2", "client_3"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Hive SQL equivalent: DATE_TRUNC('hour', ...) ---
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["heure_mesure"] = df["timestamp"].dt.floor("h")  # equivalent to DATE_TRUNC('hour')

    # --- GROUP BY heure_mesure (equivalent to Hive SQL aggregation) ---
    print("Exécution de l'agrégation Hive SQL (simulation pandas)...")
    result_df = (
        df.groupby("heure_mesure")
        .agg(
            charge_moyenne_client1_kw=("client_1", "mean"),
            charge_pointe_client1_kw=("client_1", "max"),
            charge_moyenne_client2_kw=("client_2", "mean"),
        )
        .round(3)
        .reset_index()
        .sort_values("heure_mesure", ascending=False)
    )

    print(result_df.head(15).to_string(index=False))
    print(f"\n[OK] Pipeline execute avec succes -- {len(result_df)} lignes agregees.")

    return result_df


if __name__ == "__main__":
    res = run_spark_pipeline()
    print("[OK] PySpark Pipeline (pandas simulation) executed successfully.")
