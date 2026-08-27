# -*- coding: utf-8 -*-
"""
Script de génération de données de charge électrique (Panama Electricity Load Dataset)
Génère 2 ans de relevés horaires réalistes (17 520 lignes) avec composantes saisonnières.
"""
import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "sample_panama_load.csv")

def generate_panama_dataset():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01 00:00:00', end='2025-12-31 23:00:00', freq='h')
    
    # Seasonality components
    base_load = 1100.0
    hours = dates.hour
    daily_cycle = 250.0 * np.sin(2 * np.pi * (hours - 6) / 24) + 120.0 * np.cos(4 * np.pi * hours / 24)
    
    dayofweek = dates.dayofweek
    weekly_cycle = np.where(dayofweek >= 5, -150.0, 50.0)
    
    dayofyear = dates.dayofyear
    annual_cycle = 180.0 * np.sin(2 * np.pi * (dayofyear - 80) / 365)
    
    trend = np.linspace(0, 100, len(dates))
    noise = np.random.normal(0, 35.0, len(dates))
    
    nat_demand = base_load + daily_cycle + weekly_cycle + annual_cycle + trend + noise
    nat_demand = np.clip(nat_demand, 600.0, 2200.0)

    temperature = 28.0 + 4.0 * np.sin(2 * np.pi * (hours - 8) / 24) + np.random.normal(0, 1.2, len(dates))

    df = pd.DataFrame({
        "datetime": dates.strftime("%Y-%m-%d %H:%M:%S"),
        "nat_demand": np.round(nat_demand, 2),
        "temperature": np.round(temperature, 1),
        "humidity": np.random.randint(60, 95, size=len(dates))
    })

    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Dataset generated: {CSV_PATH} ({len(df)} rows)")
    return df

if __name__ == "__main__":
    generate_panama_dataset()
