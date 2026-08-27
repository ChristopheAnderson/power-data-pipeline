# -*- coding: utf-8 -*-
"""
Projet 3 - Machine Learning Trainer: Load Forecasting Model
Feature Engineering & Random Forest / Ridge Time-Series Regression
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import pickle

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_panama_load.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "load_forecast_model.pkl")

def create_features(df):
    """
    Creates temporal and lag features for short-term load forecasting.
    """
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['dayofyear'] = df['datetime'].dt.dayofyear
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)

    # Lags & Rolling Statistics
    df['lag_1h'] = df['nat_demand'].shift(1)
    df['lag_24h'] = df['nat_demand'].shift(24)
    df['lag_168h'] = df['nat_demand'].shift(168) # 1 week ago
    df['rolling_avg_24h'] = df['nat_demand'].shift(1).rolling(window=24).mean()

    return df.dropna()

def train_and_evaluate():
    if not os.path.exists(DATA_PATH):
        print("Generating Panama dataset first...")
        from generate_sample_panama_data import generate_panama_dataset
        generate_panama_dataset()

    df = pd.read_csv(DATA_PATH)
    df_feat = create_features(df)

    feature_cols = ['hour', 'dayofweek', 'month', 'dayofyear', 'is_weekend', 'temperature', 'lag_1h', 'lag_24h', 'lag_168h', 'rolling_avg_24h']
    target_col = 'nat_demand'

    # Split Train (80%) / Test (20%) chronologically
    train_size = int(len(df_feat) * 0.8)
    train_df = df_feat.iloc[:train_size]
    test_df = df_feat.iloc[train_size:]

    X_train, y_train = train_df[feature_cols], train_df[target_col]
    X_test, y_test = test_df[feature_cols], test_df[target_col]

    model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100.0

    print("--- PERFORMANCE DU MODÈLE DE PRÉVISION DE CHARGE ---")
    print(f"RMSE (Root Mean Squared Error) : {rmse:.2f} MW")
    print(f"MAE  (Mean Absolute Error)     : {mae:.2f} MW")
    print(f"MAPE (Mean Abs. Pct Error)     : {mape:.2f} %")

    # Save model and metadata
    artifacts = {
        "model": model,
        "feature_cols": feature_cols,
        "metrics": {"rmse": rmse, "mae": mae, "mape": mape}
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifacts, f)

    print(f"✅ Model saved: {MODEL_PATH}")
    return artifacts

if __name__ == "__main__":
    train_and_evaluate()
