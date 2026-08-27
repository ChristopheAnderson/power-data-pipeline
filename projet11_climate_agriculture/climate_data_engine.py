# -*- coding: utf-8 -*-
"""
Projet 11 - Ingestion RÉELLE API Open-Meteo (Précipitations, Température, Vent — Bénin / CEDEAO)
API confirmée: https://archive-api.open-meteo.com ✅ 200 OK - Aucune clé requise
"""
import requests
import pandas as pd
import numpy as np

OPENMETEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Stations climatiques stratégiques du Bénin et de la zone CEDEAO
STATIONS_BENIN = [
    {"ville": "Cotonou", "lat": 6.37, "lon": 2.35, "pays": "Bénin"},
    {"ville": "Porto-Novo", "lat": 6.49, "lon": 2.61, "pays": "Bénin"},
    {"ville": "Parakou", "lat": 9.35, "lon": 2.62, "pays": "Bénin"},
    {"ville": "Natitingou", "lat": 10.30, "lon": 1.38, "pays": "Bénin"},
    {"ville": "Lomé", "lat": 6.13, "lon": 1.22, "pays": "Togo"},
    {"ville": "Accra", "lat": 5.55, "lon": -0.20, "pays": "Ghana"},
    {"ville": "Ouagadougou", "lat": 12.37, "lon": -1.52, "pays": "Burkina Faso"},
    {"ville": "Niamey", "lat": 13.51, "lon": 2.11, "pays": "Niger"},
]

def fetch_openmeteo_annual(ville_info, start_year=2010, end_year=2023):
    """
    Ingestion des données climatiques réelles via Open-Meteo Archive API.
    Retourne les séries journalières de précipitations, température et vent.
    """
    params = {
        "latitude": ville_info["lat"],
        "longitude": ville_info["lon"],
        "start_date": f"{start_year}-01-01",
        "end_date": f"{end_year}-12-31",
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,windspeed_10m_max",
        "timezone": "Africa/Abidjan"
    }
    try:
        resp = requests.get(OPENMETEO_ARCHIVE_URL, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            daily = data.get("daily", {})
            df = pd.DataFrame({
                "date": pd.to_datetime(daily.get("time", [])),
                "precipitation_mm": daily.get("precipitation_sum", []),
                "temp_max_c": daily.get("temperature_2m_max", []),
                "temp_min_c": daily.get("temperature_2m_min", []),
                "vent_max_kmh": daily.get("windspeed_10m_max", []),
            })
            df["ville"] = ville_info["ville"]
            df["pays"] = ville_info["pays"]
            df["annee"] = df["date"].dt.year
            df["mois"] = df["date"].dt.month
            return df
        else:
            print(f"  Erreur HTTP {resp.status_code} pour {ville_info['ville']}")
            return pd.DataFrame()
    except Exception as e:
        print(f"  Exception pour {ville_info['ville']}: {e}")
        return pd.DataFrame()

def fetch_all_stations_climate(start_year=2015, end_year=2023):
    """
    Ingestion multi-stations des données climatiques réelles.
    """
    all_dfs = []
    for station in STATIONS_BENIN:
        print(f"  -> Ingestion {station['ville']} ({station['pays']})...")
        df = fetch_openmeteo_annual(station, start_year, end_year)
        if not df.empty:
            all_dfs.append(df)

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()

if __name__ == "__main__":
    print("Test API Open-Meteo Archive (Données Réelles)...")
    df = fetch_openmeteo_annual(STATIONS_BENIN[0], 2020, 2023)
    print(f"Lignes reçues pour Cotonou: {len(df)}")
    print(df.head())
    print(f"Précipitation annuelle moy Cotonou: {df.groupby('annee')['precipitation_mm'].sum().mean():.0f} mm")
