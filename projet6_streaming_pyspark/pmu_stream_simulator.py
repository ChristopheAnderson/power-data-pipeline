# -*- coding: utf-8 -*-
"""
Projet 6 - Simulateur d'Événements Telemetry PMU / SCADA Haute Fréquence (50 Hz / 100ms)
Génère des flux de données en streaming pour la détection de pannes sur le réseau WAPP.
"""
import pandas as pd
import numpy as np
import datetime

def generate_pmu_streaming_batch(batch_size=100):
    """
    Génère un lot de télémesures PMU (Phasor Measurement Unit) haute fréquence avec timestamps.
    """
    np.random.seed()
    now = datetime.datetime.now()
    timestamps = [now - datetime.timedelta(milliseconds=100 * i) for i in range(batch_size)]
    timestamps.reverse()

    substations = [
        "Substation Sakété (Bénin)",
        "Substation Ikeja West (Nigeria)",
        "Substation Akosombo (Ghana)",
        "Substation Taabo (Côte d'Ivoire)"
    ]

    records = []
    for t in timestamps:
        sub = np.random.choice(substations)
        
        # Nominal frequency 50.0 Hz with occasional frequency trip anomaly
        freq = 50.0 + np.random.normal(0, 0.08)
        if np.random.rand() < 0.05:
            freq = 49.2 # Critical frequency drop anomaly

        # Nominal voltage 330 kV with occasional sag
        volt = 330.0 + np.random.normal(0, 4.0)
        if np.random.rand() < 0.04:
            volt = 295.0 # Voltage sag anomaly

        # Phase angle (degrees)
        phase_angle = np.random.normal(0, 15.0)

        records.append({
            "timestamp": t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "substation": sub,
            "frequence_hz": round(freq, 3),
            "tension_kv": round(volt, 2),
            "angle_phase_deg": round(phase_angle, 2),
            "status": "CRITICAL_TRIP" if (freq < 49.5 or volt < 300.0) else "NORMAL"
        })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df_stream = generate_pmu_streaming_batch(20)
    print("Lot Streaming PMU généré:")
    print(df_stream.head(10))
