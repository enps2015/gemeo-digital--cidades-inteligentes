import os
import duckdb
import time
from tabulate import tabulate

# ==============================================================================
# CONFIGURAÇÕES DA AUDITORIA
# ==============================================================================
# ATENÇÃO: Ajuste o caminho abaixo para o local exato do seu arquivo Parquet de 5GB
PARQUET_FILE = "data/00_raw/DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet"

# Caminho local alternativo (descomente se estiver na sua máquina local e não no Colab)
# PARQUET_FILE = "../data/00_raw/DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet"

SAMPLE_OUTPUT = "data/00_raw/sample_sorocaba.parquet"

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def main():
    print_header("INICIANDO AUDITORIA DE DADOS (DUCKDB)")
    start_time = time.time()
    
    if not os.path.exists(PARQUET_FILE):
        print(f"[ERRO CRÍTICO] Arquivo Parquet não encontrado em: {PARQUET_FILE}")
        print("Por favor, atualize a variável PARQUET_FILE no script audit_data.py com o caminho correto.")
        return
        
    size_gb = os.path.getsize(PARQUET_FILE) / (1024**3)
    print(f"[INFO] Arquivo localizado. Tamanho: {size_gb:.2f} GB")

    # Inicia a conexão com o DuckDB em memória
    con = duckdb.connect(database=':memory:')
    
    # 1. INFORMAÇÕES GERAIS E SCHEMA (Variáveis Numéricas/Qualitativas)
    print_header("1. INFORMAÇÕES GERAIS E TIPOS DE VARIÁVEIS")
    
    # Conta total de linhas
    total_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{PARQUET_FILE}')").fetchone()[0]
    print(f"Total de Linhas: {total_rows:,.0f}")
    
    # Extrai schema e tipos
    schema_df = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{PARQUET_FILE}') LIMIT 1").df()
    print("\nEstrutura de Colunas (Schema):")
    print(tabulate(schema_df[['column_name', 'column_type']], headers='keys', tablefmt='psql', showindex=False))
    
    # 2. ANÁLISE DE COMPLETUDE E VALORES NULOS
    print_header("2. ANÁLISE DE COMPLETUDE (NULOS/AUSENTES)")
    columns = schema_df['column_name'].tolist()
    
    null_queries = []
    for col in columns:
        safe_alias = f"nulls_{col.replace(' ', '_')}"
        null_queries.append(f'SUM(CASE WHEN "{col}" IS NULL THEN 1 ELSE 0 END) AS "{safe_alias}"')
        
    null_query_str = ", ".join(null_queries)
    null_counts = con.execute(f"SELECT {null_query_str} FROM read_parquet('{PARQUET_FILE}')").fetchone()
    
    null_results = []
    for i, col in enumerate(columns):
        n_nulls = null_counts[i]
        pct_nulls = (n_nulls / total_rows) * 100 if total_rows > 0 else 0
        null_results.append([col, n_nulls, f"{pct_nulls:.2f}%"])
        
    print(tabulate(null_results, headers=['Coluna', 'Qtd Nulos', '% Nulos'], tablefmt='psql'))
    
    # 3. VALIDAÇÃO DE FRONTEIRAS (SPATIOTEMPORAL) E CARDINALIDADE
    # NOTA: O nome das colunas pode variar. Assumindo nomes comuns. Ajuste se o Parquet tiver nomes diferentes.
    # Vamos verificar quais colunas de tempo, lat, lon, e hash temos disponíveis.
    time_cols = [c for c in columns if 'time' in c.lower() or 'data' in c.lower()]
    lat_cols = [c for c in columns if 'lat' in c.lower()]
    lon_cols = [c for c in columns if 'lon' in c.lower() or 'lng' in c.lower()]
    hash_cols = [c for c in columns if 'placa' in c.lower() or c.lower() == 'hash']
    sensor_cols = [c for c in columns if 'sensor' in c.lower() or 'nserie' in c.lower()]
    
    if time_cols and lat_cols and lon_cols:
        print_header("3. FRONTEIRAS ESPAÇO-TEMPORAIS")
        t_col, lat_col, lon_col = time_cols[0], lat_cols[0], lon_cols[0]
        
        bounds = con.execute(f"""
            SELECT 
                MIN("{t_col}") as min_time, MAX("{t_col}") as max_time,
                MIN("{lat_col}") as min_lat, MAX("{lat_col}") as max_lat,
                MIN("{lon_col}") as min_lon, MAX("{lon_col}") as max_lon
            FROM read_parquet('{PARQUET_FILE}')
        """).df()
        print(tabulate(bounds, headers='keys', tablefmt='psql', showindex=False))
        
    print_header("4. CARDINALIDADE (CONTAGENS ÚNICAS)")
    card_queries = []
    if hash_cols:
        h_col = hash_cols[0]
        card_queries.append(f'COUNT(DISTINCT "{h_col}") as veiculos_unicos')
    if sensor_cols:
        s_col = sensor_cols[0]
        card_queries.append(f'COUNT(DISTINCT "{s_col}") as sensores_unicos')
        
    if card_queries:
        c_query_str = ", ".join(card_queries)
        cardinality = con.execute(f"SELECT {c_query_str} FROM read_parquet('{PARQUET_FILE}')").df()
        print(tabulate(cardinality, headers='keys', tablefmt='psql', showindex=False))

    # 5. EXTRAÇÃO DA AMOSTRA (GOLDEN SAMPLE)
    print_header("5. EXTRAÇÃO DE AMOSTRA PARA DESENVOLVIMENTO (GOLDEN SAMPLE)")
    
    os.makedirs(os.path.dirname(SAMPLE_OUTPUT), exist_ok=True)
    
    if os.path.exists(SAMPLE_OUTPUT):
        print(f"[INFO] Amostra já existe em: {SAMPLE_OUTPUT}")
    else:
        print(f"Extraindo amostra representativa (1%) para desenvolvimento local...")
        # Usando USING SAMPLE do DuckDB para amostragem rápida
        con.execute(f"""
            COPY (
                SELECT * FROM read_parquet('{PARQUET_FILE}') USING SAMPLE 1%
            ) TO '{SAMPLE_OUTPUT}' (FORMAT PARQUET)
        """)
        s_size = os.path.getsize(SAMPLE_OUTPUT) / (1024**2)
        print(f"[SUCESSO] Amostra salva em {SAMPLE_OUTPUT} (Tamanho: {s_size:.2f} MB)")
        
    end_time = time.time()
    print_header(f"AUDITORIA CONCLUÍDA EM {end_time - start_time:.2f} SEGUNDOS")

if __name__ == "__main__":
    main()
