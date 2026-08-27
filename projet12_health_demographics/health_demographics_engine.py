# -*- coding: utf-8 -*-
"""
Projet 12 - Ingestion RÉELLE APIs WHO GHO + World Bank (Santé Publique & Démographie — Bénin / CEDEAO)
APIs confirmées 200 OK:
- WHO GHO: https://ghoapi.azureedge.net/api/
- World Bank: https://api.worldbank.org/v2/
"""
import requests
import pandas as pd
import numpy as np

WHO_GHO_BASE = "https://ghoapi.azureedge.net/api"
WB_BASE = "https://api.worldbank.org/v2"

CEDEAO_COUNTRIES = {
    "BEN": "Bénin", "GHA": "Ghana", "CIV": "Côte d'Ivoire",
    "NGA": "Nigeria", "NER": "Niger", "BFA": "Burkina Faso",
    "TGO": "Togo", "SEN": "Sénégal", "MLI": "Mali",
    "GIN": "Guinée", "SLE": "Sierra Leone", "LBR": "Libéria"
}

def fetch_who_malaria_incidence(country_code="BEN"):
    """
    Récupère l'incidence du paludisme (pour 1000 personnes à risque) depuis l'API WHO GHO.
    Indicateur: MALARIA_EST_INCIDENCE
    """
    url = f"{WHO_GHO_BASE}/MALARIA_EST_INCIDENCE?$filter=SpatialDim eq '{country_code}'&$orderby=TimeDim desc"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("value", [])
            if data:
                df = pd.DataFrame(data)
                df = df[['SpatialDim', 'TimeDim', 'NumericValue']].dropna()
                df.columns = ['pays_code', 'annee', 'incidence_paludisme_1000']
                df['pays'] = CEDEAO_COUNTRIES.get(country_code, country_code)
                return df.sort_values("annee")
    except Exception as e:
        print(f"WHO GHO Error ({country_code}): {e}")
    return pd.DataFrame()

def fetch_who_indicator_all_cedeao(indicator_code, label):
    """
    Ingestion d'un indicateur WHO GHO pour l'ensemble des pays CEDEAO.
    """
    all_dfs = []
    for code, name in CEDEAO_COUNTRIES.items():
        url = f"{WHO_GHO_BASE}/{indicator_code}?$filter=SpatialDim eq '{code}'"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get("value", [])
                if data:
                    df = pd.DataFrame(data)
                    if 'NumericValue' in df.columns and 'TimeDim' in df.columns:
                        df = df[['TimeDim', 'NumericValue']].dropna()
                        df.columns = ['annee', label]
                        df['pays'] = name
                        df['pays_code'] = code
                        all_dfs.append(df)
        except Exception:
            continue

    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

def fetch_world_bank_indicator(indicator_code, countries_str="BEN;GHA;CIV;NGA;NER;BFA;TGO;SEN", mrv=25):
    """
    Ingestion d'un indicateur de la Banque Mondiale pour les pays CEDEAO.
    Ex: NY.GDP.MKTP.CD (PIB), SP.POP.TOTL (Population), SI.POV.DDAY (Pauvreté)
    """
    url = f"{WB_BASE}/country/{countries_str}/indicator/{indicator_code}?format=json&mrv={mrv}&per_page=500"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            raw = resp.json()
            if len(raw) < 2 or not raw[1]:
                return pd.DataFrame()
            data = raw[1]
            records = []
            for item in data:
                if item.get("value") is not None:
                    records.append({
                        "pays": item.get("country", {}).get("value", ""),
                        "pays_code": item.get("countryiso3code", ""),
                        "annee": int(item.get("date", 0)),
                        "valeur": item.get("value")
                    })
            return pd.DataFrame(records).sort_values(["pays", "annee"])
    except Exception as e:
        print(f"World Bank Error ({indicator_code}): {e}")
    return pd.DataFrame()

if __name__ == "__main__":
    print("Test Paludisme WHO GHO - Bénin...")
    df_malaria = fetch_who_malaria_incidence("BEN")
    print(df_malaria.tail(5))

    print("\nTest PIB World Bank - CEDEAO...")
    df_gdp = fetch_world_bank_indicator("NY.GDP.MKTP.CD")
    print(df_gdp[df_gdp["pays_code"] == "BEN"].tail(5))
