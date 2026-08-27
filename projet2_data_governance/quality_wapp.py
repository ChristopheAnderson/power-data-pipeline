# -*- coding: utf-8 -*-
"""
Projet 2 - Data Quality & Governance Engine (WAPP/CIC)
Calculates completeness score %, identifies anomalies in TSO telemetry, and audits grid data compliance.
"""
import pandas as pd
import numpy as np

class WAPPDataQualityEngine:
    def __init__(self, v_nom_kv=161.0, freq_nom_hz=50.0, v_tolerance_pct=10.0, freq_tolerance_hz=0.5):
        self.v_nom_kv = v_nom_kv
        self.freq_nom_hz = freq_nom_hz
        self.v_min_kv = v_nom_kv * (1.0 - v_tolerance_pct / 100.0)
        self.v_max_kv = v_nom_kv * (1.0 + v_tolerance_pct / 100.0)
        self.freq_min_hz = freq_nom_hz - freq_tolerance_hz
        self.freq_max_hz = freq_nom_hz + freq_tolerance_hz

    def audit_tso_data(self, df):
        """
        Audits TSO Data Quality: Completeness, Outliers, Frequency and Voltage Deviations.
        """
        results = {}
        total_rows = len(df)
        if total_rows == 0:
            return pd.DataFrame()

        for col in df.columns:
            if col in ['timestamp', 'grt_code', 'pays']:
                continue
            
            series = df[col]
            missing_cnt = series.isnull().sum()
            completeness_pct = round(((total_rows - missing_cnt) / total_rows) * 100.0, 2)
            
            anomalies_cnt = 0
            dev_v_cnt = 0
            dev_f_cnt = 0

            if pd.api.types.is_numeric_dtype(series):
                # Negative values where physically impossible
                if col in ['puissance_mw', 'puissance_mvar']:
                    anomalies_cnt += (series < 0).sum()
                
                # Voltage Out of bounds
                if 'tension' in col or 'kv' in col:
                    dev_v_cnt = ((series < self.v_min_kv) | (series > self.v_max_kv)).sum()
                    anomalies_cnt += dev_v_cnt

                # Frequency Out of bounds
                if 'frequence' in col or 'hz' in col:
                    dev_f_cnt = ((series < self.freq_min_hz) | (series > self.freq_max_hz)).sum()
                    anomalies_cnt += dev_f_cnt

            results[col] = {
                "Lignes Totales": total_rows,
                "Valeurs Manquantes": missing_cnt,
                "Complétude (%)": completeness_pct,
                "Anomalies Détectées": anomalies_cnt,
                "Déviations Tension (kV)": dev_v_cnt,
                "Déviations Fréquence (Hz)": dev_f_cnt,
                "Statut Conformité": "✅ Conforme" if (completeness_pct >= 95.0 and anomalies_cnt == 0) else "⚠️ Non Conforme"
            }

        return pd.DataFrame(results).T

def generate_sample_tso_telemetry():
    """
    Generates synthetic realistic TSO telemetry data for 4 ECOWAS TSOs (SBEE Bénin, CIE Côte d'Ivoire, TCN Nigeria, GRIDCo Ghana).
    """
    np.random.seed(42)
    n_records = 200
    timestamps = pd.date_range(start='2026-08-20', periods=n_records, freq='15min')
    
    grts = ['SBEE (Bénin)', 'CIE (Côte d\'Ivoire)', 'TCN (Nigeria)', 'GRIDCo (Ghana)']
    data_list = []

    for t in timestamps:
        for grt in grts:
            # Base values with realistic noise and occasional missing/anomalous entries
            v_val = 161.0 + np.random.normal(0, 2.5)
            f_val = 50.0 + np.random.normal(0, 0.1)
            p_val = 120.0 + np.random.normal(0, 15.0)

            # Introduce artificial anomalies & missing values (5% rate)
            if np.random.rand() < 0.04:
                v_val = np.nan # Missing
            elif np.random.rand() < 0.03:
                v_val = 135.0 # Low voltage dip anomaly
            
            if np.random.rand() < 0.03:
                f_val = 49.1 # Frequency dip anomaly
            elif np.random.rand() < 0.03:
                f_val = np.nan

            if np.random.rand() < 0.02:
                p_val = -15.0 # Impossible negative power anomaly

            data_list.append({
                "timestamp": t,
                "grt_code": grt,
                "tension_kv": round(v_val, 2) if not np.isnan(v_val) else np.nan,
                "frequence_hz": round(f_val, 2) if not np.isnan(f_val) else np.nan,
                "puissance_mw": round(p_val, 2) if not np.isnan(p_val) else np.nan
            })

    return pd.DataFrame(data_list)

if __name__ == "__main__":
    print("Testing WAPP Data Quality Engine...")
    df_telemetry = generate_sample_tso_telemetry()
    engine = WAPPDataQualityEngine()
    audit_report = engine.audit_tso_data(df_telemetry)
    print("--- AUDIT REPORT ---")
    print(audit_report)
