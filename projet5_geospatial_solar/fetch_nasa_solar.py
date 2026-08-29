# -*- coding: utf-8 -*-
"""
Projet 5 - Ingestion API NASA POWER (GHI Solar Radiation, Température, Vent)
Données géospatiales ouvertes gratuites sans clé API.
"""
import requests
import pandas as pd
import numpy as np

def fetch_nasa_power_point(lat=6.37, lon=2.35, start_date="20230101", end_date="20230131"):
    """
    Interroge l'API NASA POWER pour un point géographique (Lat, Lon).
    Paramètres : ALLSKY_SFC_SW_DWN (Irradiance solaire kWh/m²/jour), T2M (Temp °C), WS10M (Vent m/s).
    """
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,T2M,WS10M&community=RE&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            params = data.get('properties', {}).get('parameter', {})
            ghi = params.get('ALLSKY_SFC_SW_DWN', {})
            temp = params.get('T2M', {})
            wind = params.get('WS10M', {})
            
            records = []
            for date_key in sorted(ghi.keys()):
                records.append({
                    "date": pd.to_datetime(date_key, format="%Y%m%d"),
                    "latitude": lat,
                    "longitude": lon,
                    "ghi_kwh_m2": ghi.get(date_key, 0.0),
                    "temp_c": temp.get(date_key, 0.0),
                    "wind_m_s": wind.get(date_key, 0.0)
                })
            return pd.DataFrame(records)
    except Exception as e:
        print(f"Erreur API NASA POWER: {e}")
    return pd.DataFrame()

def generate_ecowas_grid_solar_data():
    """
    Génère un maillage géospatial sur l'Afrique de l'Ouest (CEDEAO / Bénin) pour la modélisation spatiale.
    """
    np.random.seed(42)
    # Villes / Points stratégiques de la zone WAPP
    points = [
        {"nom": "Cotonou (Bénin)", "lat": 6.37, "lon": 2.35, "ghi_base": 5.4},
        {"nom": "Parakou (Bénin)", "lat": 9.35, "lon": 2.62, "ghi_base": 5.9},
        {"nom": "Natitingou (Bénin)", "lat": 10.30, "lon": 1.38, "ghi_base": 6.1},
        {"nom": "Lomé (Togo)", "lat": 6.13, "lon": 1.22, "ghi_base": 5.3},
        {"nom": "Abidjan (Côte d'Ivoire)", "lat": 5.35, "lon": -4.00, "ghi_base": 4.9},
        {"nom": "Korhogo (Côte d'Ivoire)", "lat": 9.45, "lon": -5.63, "ghi_base": 5.8},
        {"nom": "Accra (Ghana)", "lat": 5.55, "lon": -0.20, "ghi_base": 5.1},
        {"nom": "Tamale (Ghana)", "lat": 9.40, "lon": -0.84, "ghi_base": 6.0},
        {"nom": "Lagos (Nigeria)", "lat": 6.52, "lon": 3.37, "ghi_base": 5.0},
        {"nom": "Kano (Nigeria)", "lat": 12.00, "lon": 8.52, "ghi_base": 6.5},
        {"nom": "Niamey (Niger)", "lat": 13.51, "lon": 2.11, "ghi_base": 6.4},
        {"nom": "Ouagadougou (Burkina)", "lat": 12.37, "lon": -1.52, "ghi_base": 6.2}
    ]
    
    rows = []
    for p in points:
        ghi_val = p["ghi_base"] + np.random.normal(0, 0.2)
        temp_val = 26.0 + p["lat"] * 0.4 + np.random.normal(0, 0.5)
        potential_mw = round(ghi_val * 45.0, 1) # Potentiel de production solaire estimé (MW)
        rows.append({
            "site": p["nom"],
            "latitude": p["lat"],
            "longitude": p["lon"],
            "ghi_kwh_m2_day": round(ghi_val, 2),
            "temp_moyenne_c": round(temp_val, 1),
            "potentiel_solaire_mw": potential_mw
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Extraction test API NASA POWER...")
    df_nasa = fetch_nasa_power_point()
    print(f"Lignes récupérées: {len(df_nasa)}")
    print(generate_ecowas_grid_solar_data())
