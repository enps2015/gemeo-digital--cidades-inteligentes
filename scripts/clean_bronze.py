import os
import duckdb
import time

# ==============================================================================
# PIPELINE DE HIGIENIZAÇÃO (BRONZE)
# ==============================================================================
RAW_PARQUET = "data/00_raw/DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet"
BRONZE_PARQUET = "data/01_bronze/DADOS_SOROCABA_BRONZE.parquet"

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def main():
    print_header("INICIANDO HIGIENIZAÇÃO DE DADOS (BRONZE PIPELINE)")
    start_time = time.time()
    
    if not os.path.exists(RAW_PARQUET):
        print(f"[ERRO CRÍTICO] Arquivo original não encontrado em: {RAW_PARQUET}")
        return
        
    os.makedirs("data/01_bronze", exist_ok=True)
    
    con = duckdb.connect(database=':memory:')
    
    # Executando a limpeza de forma otimizada via DuckDB (streaming)
    # 1. Substituir vírgula por ponto na Lat/Lon e fazer o CAST para DOUBLE
    # 2. Fazer o parser da data de VARCHAR para TIMESTAMP
    # 3. Manter as demais colunas intactas
    
    print("[INFO] Executando pipeline de limpeza nos 76 milhões de registros...")
    print("[INFO] Isso pode levar cerca de 1 a 2 minutos. Aguarde...")
    
    query = f"""
        COPY (
            SELECT 
                "NSerie",
                "Endereco",
                "Sentido",
                strptime("Datatrafego", '%d/%m/%Y %H:%M:%S') AS "Datatrafego",
                CAST(REPLACE("Latitude", ',', '.') AS DOUBLE) AS "Latitude",
                CAST(REPLACE("Longitude", ',', '.') AS DOUBLE) AS "Longitude",
                "Placa",
                "Velocidade 1",
                "Velocidade Regul"
            FROM read_parquet('{RAW_PARQUET}')
        ) TO '{BRONZE_PARQUET}' (FORMAT PARQUET, COMPRESSION 'SNAPPY');
    """
    
    con.execute(query)
    
    end_time = time.time()
    size_gb = os.path.getsize(BRONZE_PARQUET) / (1024**3)
    
    print_header(f"PIPELINE CONCLUÍDO EM {end_time - start_time:.2f} SEGUNDOS")
    print(f"[SUCESSO] Base Bronze gerada em: {BRONZE_PARQUET}")
    print(f"[SUCESSO] Novo tamanho do Parquet: {size_gb:.2f} GB")
    
    # Validando o novo schema
    print("\n[VALIDAÇÃO] Novo Schema da Base Bronze:")
    schema_df = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{BRONZE_PARQUET}') LIMIT 1").df()
    print(schema_df[['column_name', 'column_type']])

if __name__ == "__main__":
    main()
