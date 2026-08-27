# -*- coding: utf-8 -*-
"""
Projet 4 - PySpark & Hive SQL Distributed Pipeline
Aggregates high-frequency 15-minute smart meter consumption across 321 clients.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max as spark_max, sum as spark_sum, date_trunc
import os
import sys

def run_spark_pipeline(data_file_path=None):
    """
    Initializes PySpark Session with Hive SQL support and executes distributed query.
    """
    print("Initialisation de la session PySpark avec support Hive SQL...")
    spark = SparkSession.builder \
        .appName("WAPP_BigData_Power_Analytics") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    # Generate synthetic high-volume dataset if file does not exist
    if not data_file_path or not os.path.exists(data_file_path):
        print("Génération d'un échantillon Spark distribué...")
        data = []
        import datetime
        base_time = datetime.datetime(2024, 1, 1, 0, 0)
        for i in range(1000):
            t_str = (base_time + datetime.timedelta(minutes=15 * i)).strftime("%Y-%m-%d %H:%M:%S")
            data.append((t_str, float(1.2 + (i % 10) * 0.5), float(2.1 + (i % 7) * 0.3), float(0.8 + (i % 5) * 0.2)))
        
        df = spark.createDataFrame(data, ["timestamp", "client_1", "client_2", "client_3"])
    else:
        df = spark.read.option("header", "true").option("delimiter", ";").csv(data_file_path)

    # Register Temp View for Hive SQL
    df.createOrReplaceTempView("electricity_consumption")

    # Hive SQL Query
    hive_query = """
    SELECT 
        DATE_TRUNC('hour', CAST(timestamp AS TIMESTAMP)) AS heure_mesure,
        ROUND(AVG(CAST(client_1 AS FLOAT)), 3) AS charge_moyenne_client1_kw,
        ROUND(MAX(CAST(client_1 AS FLOAT)), 3) AS charge_pointe_client1_kw,
        ROUND(AVG(CAST(client_2 AS FLOAT)), 3) AS charge_moyenne_client2_kw
    FROM electricity_consumption
    GROUP BY heure_mesure
    ORDER BY heure_mesure DESC
    """

    print("Exécution de la requête Hive SQL sous PySpark...")
    result_df = spark.sql(hive_query)
    result_df.show(15, truncate=False)

    return result_df.toPandas()

if __name__ == "__main__":
    res = run_spark_pipeline()
    print("✅ PySpark Pipeline executed successfully.")
