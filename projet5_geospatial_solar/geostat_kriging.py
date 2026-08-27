# -*- coding: utf-8 -*-
"""
Projet 5 - Modélisation Géostatistique (Krigeage / IDW & Interpolation Spatiale)
Rapprochement direct avec la thèse d'ingénieur ENSGMM de Christophe WAVOEKE (HASM, BME, Krigeage).
"""
import pandas as pd
import numpy as np

class GeostatisticalSolarModel:
    def __init__(self, power_p=2.0):
        self.power_p = power_p

    def inverse_distance_weighting(self, known_coords, known_values, grid_x, grid_y):
        """
        Interpolation spatiale par Inverse Distance Weighting (IDW) sur la grille (grid_x, grid_y).
        """
        interpolated_grid = np.zeros((len(grid_y), len(grid_x)))

        for i, y in enumerate(grid_y):
            for j, x in enumerate(grid_x):
                distances = np.sqrt((known_coords[:, 0] - x)**2 + (known_coords[:, 1] - y)**2)
                
                # Check for exact location match
                exact_match = np.where(distances == 0)[0]
                if len(exact_match) > 0:
                    interpolated_grid[i, j] = known_values[exact_match[0]]
                else:
                    weights = 1.0 / (distances ** self.power_p)
                    weights /= np.sum(weights)
                    interpolated_grid[i, j] = np.sum(weights * known_values)

        return interpolated_grid

    def calculate_variogram(self, coords, values):
        """
        Calcule l'expérimentation du variogramme spatial (Dépendance Spatiale γ(h)).
        """
        n = len(values)
        h_list = []
        gamma_list = []

        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt((coords[i, 0] - coords[j, 0])**2 + (coords[i, 1] - coords[j, 1])**2)
                gamma = 0.5 * ((values[i] - values[j])**2)
                h_list.append(dist)
                gamma_list.append(gamma)

        df_vario = pd.DataFrame({"distance_deg": h_list, "gamma": gamma_list})
        df_vario["bin_distance"] = np.round(df_vario["distance_deg"], 1)
        variogram = df_vario.groupby("bin_distance")["gamma"].mean().reset_index()
        return variogram

if __name__ == "__main__":
    print("Test Moteur Géostatistique...")
    try:
        from .fetch_nasa_solar import generate_ecowas_grid_solar_data
    except ImportError:
        from fetch_nasa_solar import generate_ecowas_grid_solar_data

    df = generate_ecowas_grid_solar_data()
    coords = df[['longitude', 'latitude']].values
    values = df['ghi_kwh_m2_day'].values

    model = GeostatisticalSolarModel()
    grid_x = np.linspace(-6.0, 9.0, 30)
    grid_y = np.linspace(5.0, 14.0, 30)
    grid_res = model.inverse_distance_weighting(coords, values, grid_x, grid_y)
    print(f"Surface interpolée générée: {grid_res.shape}")
