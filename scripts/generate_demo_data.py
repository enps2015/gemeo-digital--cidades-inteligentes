import os
import sys
import pandas as pd
import numpy as np
import uuid
import time
from datetime import datetime, timedelta

# ==============================================================================
# SCRIPT DE GERAÇÃO DE DADOS SINTÉTICOS PARA SMOKE TEST
# ==============================================================================
# Este script gera dados FICTÍCIOS que simulam a estrutura do banco original de 5GB.
# O único propósito é permitir que avaliadores rodem o pipeline (audit, bronze,
# silver, gold) sem necessitar dos dados reais sensíveis.
# Os dados geográficos e os hashes de veículos gerados aqui NÃO são reais e
# não refletem a mobilidade urbana da cidade.
# ==============================================================================

RAW_DIR = "data_sample/00_raw"
TARGET_FILE = os.path.join(RAW_DIR, "DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet")
NUM_RECORDS = 50000

def print_warning():
    print("\n" + "="*80)
    print("  AVISO: GERAÇÃO DE DADOS SINTÉTICOS (SMOKE TEST)")
    print("="*80)
    print("Este script gerará um conjunto de dados TOTALMENTE FICTÍCIO.")
    print("Objetivo: Testar a execução técnica do pipeline sem baixar os >5GB originais.")
    print("Os mapas e clusters gerados a partir daqui NÃO POSSUEM VALOR ANALÍTICO.\n")

def check_existing_data():
    if os.path.exists(TARGET_FILE):
        size_mb = os.path.getsize(TARGET_FILE) / (1024 * 1024)
        if size_mb > 100: # Se for maior que 100MB, provavelmente é o arquivo real
            print(f"[ALERTA CRÍTICO] Arquivo existente detectado em {TARGET_FILE} ({size_mb:.2f} MB).")
            print("Parece ser a base de dados original. O script abortará para não sobrescrever dados reais.")
            print("Se deseja gerar dados de teste, remova ou renomeie o arquivo original primeiro.")
            sys.exit(1)
        else:
            print(f"[INFO] Arquivo sintético anterior detectado ({size_mb:.2f} MB). Será sobrescrito.")

def generate_data():
    os.makedirs(RAW_DIR, exist_ok=True)
    
    print(f"[INFO] Gerando {NUM_RECORDS} registros fictícios...")
    
    # 1. Gerar sensores fictícios (agrupados em 3 áreas de Sorocaba para o DBSCAN funcionar)
    np.random.seed(42)
    # Area 1: Centro (-23.50, -47.45)
    # Area 2: Norte (-23.45, -47.48)
    # Area 3: Leste (-23.52, -47.40)
    
    sensors = []
    for i in range(1, 21): # 20 sensores no total
        area = i % 3
        if area == 0:
            lat, lon = -23.50 + np.random.normal(0, 0.01), -47.45 + np.random.normal(0, 0.01)
        elif area == 1:
            lat, lon = -23.45 + np.random.normal(0, 0.01), -47.48 + np.random.normal(0, 0.01)
        else:
            lat, lon = -23.52 + np.random.normal(0, 0.01), -47.40 + np.random.normal(0, 0.01)
            
        # Converter para formato de string com vírgula esperado pela camada raw original
        lat_str = f"{lat:.6f}".replace('.', ',')
        lon_str = f"{lon:.6f}".replace('.', ',')
        
        sensors.append({
            'NSerie': f"SENS_{1000+i}",
            'Endereco': f"AV. FICTICIA {i}, SOROCABA",
            'Latitude': lat_str,
            'Longitude': lon_str
        })
        
    # 2. Gerar identificadores fictícios de veículos para smoke test
    num_vehicles = 500
    vehicles = [f"veh_demo_{i:04d}_{uuid.uuid4().hex}" for i in range(num_vehicles)]
    
    # 3. Gerar passagens (pings)
    # Simulando viagens: um veículo passa por vários sensores em sequência
    records = []
    base_time = datetime(2026, 1, 1, 6, 0, 0)
    
    for v in vehicles:
        # Cada veículo faz de 2 a 5 viagens
        num_trips = np.random.randint(2, 6)
        current_time = base_time + timedelta(hours=np.random.randint(0, 48))
        
        for _ in range(num_trips):
            # Uma viagem tem de 2 a 10 pings espaçados por minutos
            num_pings = np.random.randint(2, 11)
            for _ in range(num_pings):
                sensor = np.random.choice(sensors)
                current_time += timedelta(minutes=np.random.randint(1, 15))
                
                records.append({
                    'NSerie': sensor['NSerie'],
                    'Endereco': sensor['Endereco'],
                    'Sentido': np.random.choice(['C/B', 'B/C', 'N/S', 'S/N']),
                    'Datatrafego': current_time.strftime('%d/%m/%Y %H:%M:%S'),
                    'Latitude': sensor['Latitude'],
                    'Longitude': sensor['Longitude'],
                    'Placa': v,
                    'Velocidade 1': np.random.randint(30, 80),
                    'Velocidade Regul': 60
                })
                
    # Completar os registros com pings aleatórios para atingir NUM_RECORDS
    while len(records) < NUM_RECORDS:
        sensor = np.random.choice(sensors)
        v = np.random.choice(vehicles)
        random_time = base_time + timedelta(days=np.random.randint(0, 7), hours=np.random.randint(0, 24))
        
        records.append({
            'NSerie': sensor['NSerie'],
            'Endereco': sensor['Endereco'],
            'Sentido': np.random.choice(['C/B', 'B/C']),
            'Datatrafego': random_time.strftime('%d/%m/%Y %H:%M:%S'),
            'Latitude': sensor['Latitude'],
            'Longitude': sensor['Longitude'],
            'Placa': v,
            'Velocidade 1': np.random.randint(30, 80),
            'Velocidade Regul': 60
        })
        
    df = pd.DataFrame(records[:NUM_RECORDS])
    
    # Salvar em parquet usando engine pyarrow/fastparquet do pandas
    print(f"[INFO] Salvando {NUM_RECORDS} registros em formato Parquet...")
    df.to_parquet(TARGET_FILE, compression='snappy')
    
    size_mb = os.path.getsize(TARGET_FILE) / (1024 * 1024)
    print(f"[SUCESSO] Base fictícia gerada: {TARGET_FILE} ({size_mb:.2f} MB).")
    print("\nPara rodar os scripts originais, copie este arquivo para 'data/00_raw/'.")
    print("⚠️ CUIDADO: Renomeie sua base real de 5GB antes de copiar para não sobrescrevê-la!")

if __name__ == "__main__":
    print_warning()
    check_existing_data()
    
    # Verifica dependência antes de rodar
    try:
        import pyarrow
    except ImportError:
        print("[ERRO] A biblioteca 'pyarrow' é necessária para salvar Parquet. Rode: pip install pyarrow")
        sys.exit(1)
        
    start = time.time()
    generate_data()
    print(f"Tempo total de geração: {time.time() - start:.2f} segundos")
