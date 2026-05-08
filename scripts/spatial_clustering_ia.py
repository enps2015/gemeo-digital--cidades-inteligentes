import os
import duckdb
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import time

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

BRONZE_PARQUET = "data/01_bronze/DADOS_SOROCABA_BRONZE.parquet"
SILVER_OD_PARQUET = "data/02_silver/matriz_od_amostra_1semana.parquet"
GOLD_DIR = "data/03_gold"
GOLD_MACRO_OD_PARQUET = f"{GOLD_DIR}/matriz_od_macro_zonas.parquet"
GOLD_SENSORS_PARQUET = f"{GOLD_DIR}/sensores_clusterizados.parquet"

def main():
    print_header("CAMADA GOLD: CLUSTERIZAÇÃO ESPACIAL DE MACRO-ZONAS (DBSCAN)")
    start_time = time.time()
    
    os.makedirs(GOLD_DIR, exist_ok=True)
    con = duckdb.connect()
    
    # 1. Extrair Sensores Únicos da Base
    print("[1/5] Extraindo coordenadas únicas dos sensores...")
    query_sensors = f"""
        SELECT 
            "NSerie" as sensor_id,
            FIRST(Latitude) as lat,
            FIRST(Longitude) as lon,
            COUNT(*) as volume
        FROM read_parquet('{BRONZE_PARQUET}')
        GROUP BY "NSerie"
    """
    df_sensors = con.execute(query_sensors).df()
    
    if len(df_sensors) < 2:
        print("[ERRO] Número insuficiente de sensores para clusterização.")
        return
        
    print(f"Sensores encontrados: {len(df_sensors)}")
    
    # 2. IA Não-Supervisionada: DBSCAN
    print("[2/5] Aplicando Inteligência Artificial (DBSCAN) para Macro-Zonas...")
    
    # Converter coordenadas para Radianos para cálculo Haversine
    coords_rad = np.radians(df_sensors[['lat', 'lon']].values)
    
    # Parâmetros: Raio de busca de ~2.0 km.
    # Fórmula: eps = distance_km / earth_radius_km
    kms_per_radian = 6371.0088
    epsilon = 2.0 / kms_per_radian
    
    # min_samples = 2 para permitir zonas pequenas (já que são equipamentos fixos raros)
    dbscan = DBSCAN(eps=epsilon, min_samples=2, metric='haversine')
    cluster_labels = dbscan.fit_predict(coords_rad)
    
    df_sensors['cluster_id'] = cluster_labels
    
    # 3. Validação Científica (Silhouette Score)
    print("[3/5] Computando métrica de validação (Silhouette Score)...")
    valid_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    
    if valid_clusters > 1:
        # Calcular apenas para os pontos não classificados como ruído (-1)
        mask = cluster_labels != -1
        if mask.sum() > 1 and len(set(cluster_labels[mask])) > 1:
            score = silhouette_score(coords_rad[mask], cluster_labels[mask], metric='haversine')
            print(f"-> Silhouette Score Espacial: {score:.4f} (Valores > 0 indicam boa coesão)")
        else:
            print("-> Silhouette Score não calculável (Apenas 1 cluster não-ruído)")
    else:
        print("-> DBSCAN não encontrou múltiplos clusters com os parâmetros atuais.")
        
    # Nomear Clusters e Criar Coordenadas de Centróides
    def name_cluster(cid):
        if cid == -1: return "Zona Periférica Isolada"
        return f"Macro-Zona {chr(65 + int(cid))}" # Zona A, Zona B...
        
    df_sensors['nome_zona'] = df_sensors['cluster_id'].apply(name_cluster)
    
    # Calcular centro de massa de cada zona (Centróide)
    centroids = df_sensors[df_sensors['cluster_id'] != -1].groupby('cluster_id')[['lat', 'lon']].mean().reset_index()
    centroids.rename(columns={'lat': 'centroide_lat', 'lon': 'centroide_lon'}, inplace=True)
    
    df_sensors = pd.merge(df_sensors, centroids, on='cluster_id', how='left')
    
    # Para ruídos, o próprio sensor é o centróide
    df_sensors['centroide_lat'] = df_sensors['centroide_lat'].fillna(df_sensors['lat'])
    df_sensors['centroide_lon'] = df_sensors['centroide_lon'].fillna(df_sensors['lon'])
    
    # Salvar o dicionário de sensores agrupados
    con.execute(f"COPY (SELECT * FROM df_sensors) TO '{GOLD_SENSORS_PARQUET}' (FORMAT PARQUET)")
    print(f"-> Sensores Agrupados salvos em: {GOLD_SENSORS_PARQUET}")
    
    # 4. Transformação da Matriz O-D (Cruzamento Silver -> Gold)
    print("[4/5] Elevando Matriz O-D de nível de equipamento para nível de Macro-Zona...")
    query_gold = f"""
        WITH silver_od AS (
            SELECT * FROM read_parquet('{SILVER_OD_PARQUET}')
            WHERE origem_sensor != destino_sensor
        ),
        sensores AS (
            SELECT * FROM df_sensors
        )
        SELECT 
            s1.nome_zona as origem_zona,
            s1.centroide_lat as origem_lat,
            s1.centroide_lon as origem_lon,
            
            s2.nome_zona as destino_zona,
            s2.centroide_lat as destino_lat,
            s2.centroide_lon as destino_lon,
            
            COUNT(*) as volume_viagens,
            AVG(silver_od.duracao_viagem_minutos) as duracao_media_minutos
        FROM silver_od
        JOIN sensores s1 ON silver_od.origem_sensor = s1.sensor_id
        JOIN sensores s2 ON silver_od.destino_sensor = s2.sensor_id
        GROUP BY 1, 2, 3, 4, 5, 6
        ORDER BY volume_viagens DESC
    """
    df_gold_macro = con.execute(query_gold).df()
    
    # Salvar Matriz O-D Consolidada
    con.execute(f"COPY (SELECT * FROM df_gold_macro) TO '{GOLD_MACRO_OD_PARQUET}' (FORMAT PARQUET)")
    
    # 5. Relatório Executivo
    print("[5/5] Resumo da Inteligência Acionável:")
    print(f"Total de Zonas Formadas: {valid_clusters}")
    print(f"Sensores agrupados em Zonas Principais: {(df_sensors['cluster_id'] != -1).sum()}")
    print(f"Sensores isolados (Ruído Periférico): {(df_sensors['cluster_id'] == -1).sum()}")
    print("\nTOP 3 Macro-Corredores Descobertos pela IA:")
    cols_view = ['origem_zona', 'destino_zona', 'volume_viagens', 'duracao_media_minutos']
    
    from tabulate import tabulate
    print(tabulate(df_gold_macro[df_gold_macro['origem_zona'] != df_gold_macro['destino_zona']][cols_view].head(3), headers='keys', tablefmt='psql', showindex=False))
    
    end_time = time.time()
    print_header(f"SUCESSO! PIPELINE GOLD EXECUTADO EM {end_time - start_time:.2f} s")

if __name__ == "__main__":
    main()
