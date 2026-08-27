# -*- coding: utf-8 -*-
"""
Projet 8 - Moteur de Traitement de Signal & Maintenance Prédictive Électronique
Fast Fourier Transform (FFT), Analyse Spectrale & Durée de Vie Utile Restante (RUL).
"""
import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq

def generate_sensor_vibration_signal(sampling_rate=1000, duration_sec=2.0, anomaly_level=0.0):
    """
    Génère un signal temporel de capteur de vibration (accéléromètre 1 kHz) avec composantes harmoniques.
    """
    t = np.linspace(0, duration_sec, int(sampling_rate * duration_sec), endpoint=False)
    
    # Fundamental frequencies (50 Hz grid fundamental + 120 Hz motor rotation)
    f_grid = 50.0
    f_motor = 120.0
    
    signal = 2.5 * np.sin(2 * np.pi * f_grid * t) + 1.2 * np.sin(2 * np.pi * f_motor * t)
    
    # Add defect harmonic frequency (350 Hz bearing fault) if anomaly present
    if anomaly_level > 0:
        f_fault = 350.0
        signal += (anomaly_level * 3.5) * np.sin(2 * np.pi * f_fault * t)

    # Add Gaussian thermal noise
    noise = np.random.normal(0, 0.4, len(t))
    signal += noise

    return t, signal

def compute_fft_spectrum(time_array, signal_array, sampling_rate=1000):
    """
    Calcule la Transformée de Fourier Rapide (FFT) pour obtenir le spectre d'amplitude.
    """
    N = len(signal_array)
    yf = fft(signal_array)
    xf = fftfreq(N, 1.0 / sampling_rate)[:N // 2]
    amplitude = 2.0 / N * np.abs(yf[0:N // 2])

    df_spectrum = pd.DataFrame({
        "frequence_hz": np.round(xf, 1),
        "amplitude": np.round(amplitude, 4)
    })

    # Peak harmonic detection
    peak_freq = df_spectrum.iloc[df_spectrum["amplitude"].idxmax()]["frequence_hz"]

    return df_spectrum, peak_freq

if __name__ == "__main__":
    print("Testing IoT Signal Processing Engine...")
    t, s = generate_sensor_vibration_signal(anomaly_level=0.5)
    df_spec, peak = compute_fft_spectrum(t, s)
    print(f"Signal généré: {len(t)} points. Fréquence Pic: {peak} Hz")
    print(df_spec.head(10))
