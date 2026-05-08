import os
import duckdb
import time
from tabulate import tabulate

# ==============================================================================
# ENGENHARIA DE FEATURES: TRIP SEGMENTATION
# ==============================================================================
BRONZE_PARQUET = "data/01_bronze/DADOS_SOROCABA_BRONZE.parquet"
SILVER_DIR = "data/02_silver"
SILVER_OD_PARQUET = f"{SILVER_DIR}/matriz_od_amostra_1semana.parquet"

# Heurística: Tempo máximo de silêncio para considerar que a viagem acabou
MAX_INACTIVITY_MINUTES = 45

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def main():
    print_header(f"SEGMENTAÇÃO DE VIAGENS (INATIVIDADE > {MAX_INACTIVITY_MINUTES} MIN)")
    start_time = time.time()
    
    if not os.path.exists(BRONZE_PARQUET):
        print(f"[ERRO CRÍTICO] Base Bronze não encontrada: {BRONZE_PARQUET}")
        return
        
    os.makedirs(SILVER_DIR, exist_ok=True)
    con = duckdb.connect(database=':memory:')
    
    print("[INFO] Processando 1ª Semana de Janeiro/2026 para validação heurística...")
    
    # Pipeline SQL Complexo em DuckDB (CTEs)
    query = f"""
    -- 1. Filtrar apenas a primeira semana (Amostragem Cronológica Íntegra)
    WITH amostra_semana AS (
        SELECT *
        FROM read_parquet('{BRONZE_PARQUET}')
        WHERE Datatrafego >= '2026-01-01 00:00:00' 
          AND Datatrafego < '2026-01-08 00:00:00'
    ),
    
    -- 2. Ordenar por placa e tempo, obtendo o tempo da leitura anterior
    ordem_trajetoria AS (
        SELECT 
            Placa,
            Datatrafego,
            NSerie as Sensor,
            Latitude,
            Longitude,
            LAG(Datatrafego) OVER (PARTITION BY Placa ORDER BY Datatrafego) as prev_time
        FROM amostra_semana
    ),
    
    -- 3. Calcular delta_time em minutos e marcar início de novas viagens
    -- Uma nova viagem começa se for o primeiro registro (prev_time IS NULL) 
    -- OU se a diferença de tempo > MAX_INACTIVITY_MINUTES
    delta_calc AS (
        SELECT 
            *,
            date_diff('minute', prev_time, Datatrafego) as delta_minutos,
            CASE 
                WHEN prev_time IS NULL THEN 1
                WHEN date_diff('minute', prev_time, Datatrafego) > {MAX_INACTIVITY_MINUTES} THEN 1
                ELSE 0 
            END as is_new_trip
        FROM ordem_trajetoria
    ),
    
    -- 4. Criar um ID único de viagem usando Soma Cumulativa (CUMSUM)
    trip_ids AS (
        SELECT 
            *,
            SUM(is_new_trip) OVER (PARTITION BY Placa ORDER BY Datatrafego) as trip_seq
        FROM delta_calc
    ),
    
    -- 5. Mesclar a Placa com a Sequência para gerar um ID Global Absoluto
    trip_data AS (
        SELECT 
            *,
            Placa || '_' || CAST(trip_seq AS VARCHAR) as trip_id
        FROM trip_ids
    )
    
    -- 6. Agregar para gerar a Matriz Origem-Destino Bruta
    SELECT 
        trip_id,
        Placa,
        MIN(Datatrafego) as hora_inicio,
        MAX(Datatrafego) as hora_fim,
        date_diff('minute', MIN(Datatrafego), MAX(Datatrafego)) as duracao_viagem_minutos,
        COUNT(*) as total_pontos_lidos,
        
        -- O PRIMEIRO sensor e coordenada lida na viagem (Origem)
        FIRST(Sensor ORDER BY Datatrafego) as origem_sensor,
        FIRST(Latitude ORDER BY Datatrafego) as origem_lat,
        FIRST(Longitude ORDER BY Datatrafego) as origem_lon,
        
        -- O ÚLTIMO sensor e coordenada lida na viagem (Destino)
        LAST(Sensor ORDER BY Datatrafego) as destino_sensor,
        LAST(Latitude ORDER BY Datatrafego) as destino_lat,
        LAST(Longitude ORDER BY Datatrafego) as destino_lon
        
    FROM trip_data
    GROUP BY trip_id, Placa
    ORDER BY hora_inicio
    """
    
    print("[INFO] Executando Window Functions para segmentação de trajetórias...")
    od_matrix = con.execute(query).df()
    
    # Salva o resultado
    con.execute(f"COPY (SELECT * FROM od_matrix) TO '{SILVER_OD_PARQUET}' (FORMAT PARQUET)")
    
    end_time = time.time()
    print_header(f"PIPELINE CONCLUÍDO EM {end_time - start_time:.2f} SEGUNDOS")
    print(f"[SUCESSO] Matriz O-D da 1ª Semana salva em: {SILVER_OD_PARQUET}")
    
    print("\n[RESULTADOS DA HEURÍSTICA]")
    print(f"Total de Viagens Identificadas na 1ª Semana: {len(od_matrix):,}")
    print(f"Média de duração das viagens: {od_matrix['duracao_viagem_minutos'].mean():.1f} minutos")
    
    print("\nAmostra das primeiras 3 viagens extraídas:")
    cols_to_show = ['trip_id', 'hora_inicio', 'duracao_viagem_minutos', 'origem_sensor', 'destino_sensor']
    print(tabulate(od_matrix[cols_to_show].head(3), headers='keys', tablefmt='psql', showindex=False))

if __name__ == "__main__":
    main()
