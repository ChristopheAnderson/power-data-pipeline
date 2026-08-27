# -*- coding: utf-8 -*-
"""
Projet 7 - Moteur d'Optimisation de l'Economic Dispatch & Locational Marginal Pricing (LMP)
Modélisation du Marché Régional de l'Électricité WAPP / ARREC / ERERA.
"""
import pandas as pd
import numpy as np

class WAPPMarketDispatchOptimizer:
    def __init__(self):
        # Offres des centrales de production régionales
        self.generators = [
            {"node": "Nœud Cotonou (Bénin)", "filiere": "Gaz / IPP Maria Gleta", "capacity_mw": 120, "marginal_cost_usd_mwh": 65.0},
            {"node": "Nœud Akosombo (Ghana)", "filiere": "Hydraulique Akosombo", "capacity_mw": 500, "marginal_cost_usd_mwh": 25.0},
            {"node": "Nœud Taabo (Côte d'Ivoire)", "filiere": "Hydraulique / Gaz Mixture", "capacity_mw": 450, "marginal_cost_usd_mwh": 35.0},
            {"node": "Nœud Egbin (Nigeria)", "filiere": "Gaz Thermique Egbin", "capacity_mw": 800, "marginal_cost_usd_mwh": 45.0},
            {"node": "Nœud Nagbegou (Burkina)", "filiere": "Solaire + Diesel Backup", "capacity_mw": 100, "marginal_cost_usd_mwh": 90.0}
        ]

    def solve_economic_dispatch(self, total_regional_demand_mw=1500.0, line_congestion_penalty=5.0):
        """
        Résout le problème d'Economic Dispatch (OPF simplifié) pour satisfaire la demande au coût minimal.
        Calcul du Prix Marginal Nodal (LMP) par nœud.
        """
        df_gen = pd.DataFrame(self.generators).sort_values("marginal_cost_usd_mwh")
        
        remaining_demand = total_regional_demand_mw
        dispatched_mw = []

        system_marginal_price = 0.0

        for idx, row in df_gen.iterrows():
            cap = row["capacity_mw"]
            cost = row["marginal_cost_usd_mwh"]
            
            if remaining_demand <= 0:
                p_mw = 0.0
            elif remaining_demand >= cap:
                p_mw = cap
                remaining_demand -= cap
                system_marginal_price = cost
            else:
                p_mw = remaining_demand
                remaining_demand = 0.0
                system_marginal_price = cost

            dispatched_mw.append(p_mw)

        df_gen["dispatched_mw"] = dispatched_mw
        df_gen["unit_load_pct"] = np.round((df_gen["dispatched_mw"] / df_gen["capacity_mw"]) * 100.0, 1)
        
        # Calculate Nodal Price LMP = System Marginal Price + Congestion Component using np.round for pandas/numpy compatibility
        df_gen["nodal_lmp_usd_mwh"] = np.round(system_marginal_price + np.random.uniform(0, line_congestion_penalty, len(df_gen)), 2)

        total_market_cost_usd = (df_gen["dispatched_mw"] * df_gen["marginal_cost_usd_mwh"]).sum()

        return df_gen, system_marginal_price, total_market_cost_usd

if __name__ == "__main__":
    opt = WAPPMarketDispatchOptimizer()
    df_res, smp, total_cost = opt.solve_economic_dispatch(1600.0)
    print("--- RESULTATS OPTIMISATION MARCHÉ WAPP ---")
    print(f"Prix Marginal Système (SMP): ${smp}/MWh")
    print(f"Coût Total de Production: ${total_cost:,.2f}")
    print(df_res)
