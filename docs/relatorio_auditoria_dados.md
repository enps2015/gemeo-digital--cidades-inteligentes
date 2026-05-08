# Relatório Técnico: Auditoria e Pipeline de Dados (Sorocaba 2026)

Este documento sumariza os resultados da varredura automatizada (*Data Profiling*) executada pelo script `scripts/audit_data.py` utilizando o **DuckDB** sobre a base de dados bruta, e documenta as camadas de transformação de engenharia de dados aplicadas em sequência para viabilizar a modelagem de Inteligência Artificial.

## 1. Informações Estruturais Básicas (Camada Raw)

- **Arquivo Fonte:** `DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet`
- **Volume de Armazenamento:** 5.15 GB
- **Total de Registros (Linhas):** 76.662.221
- **Tempo de Execução da Auditoria:** 14.05 segundos

### Dicionário de Tipagem Bruto (Schema)

| Coluna           | Tipo de Dado no Parquet | Status da Auditoria |
|------------------|-------------------------|---------------------|
| NSerie           | VARCHAR                 | OK                  |
| Endereco         | VARCHAR                 | OK                  |
| Sentido          | VARCHAR                 | OK                  |
| Datatrafego      | VARCHAR                 | Formato de Data     |
| Latitude         | VARCHAR                 | **CRÍTICO**         |
| Longitude        | VARCHAR                 | **CRÍTICO**         |
| Placa            | VARCHAR                 | **CRÍTICO**         |
| Velocidade 1     | DOUBLE                  | OK                  |
| Velocidade Regul | DOUBLE                  | OK                  |

---

## 2. Análise de Completude (Nulos)

Foi feita uma varredura para identificar valores do tipo `NULL`.

| Coluna | Qtd Nulos | % Nulos |
|---|---|---|
| Todas as 9 colunas | 0 | 0.00% |

> [!WARNING]
> A ausência total de nulos (0%) em uma base de IoT/Sensores de 76 milhões de registros indica que os dados brutos já sofreram uma transformação prévia (provavelmente durante a conversão do CSV original) onde os nulos foram imputados, dropados ou substituídos por "strings em branco". 

---

## 3. Validação de Fronteiras e Cardinalidade

### 3.1 Fronteiras Espaço-Temporais
| Métrica | Valor Mínimo | Valor Máximo | Observação de Auditoria |
|---|---|---|---|
| Tempo (`Datatrafego`) | 01/01/2026 00:00:01 | 31/03/2026 23:59:59 | Cobertura exata do 1º Trimestre. |
| Latitude | `-23,44511` | `-23.5324` | **Inconsistência de Formato** |
| Longitude | `-47,43921` | `-47.5146` | **Inconsistência de Formato** |

> [!CAUTION]
> As coordenadas geográficas estavam gravadas como `VARCHAR` e **misturavam vírgulas e pontos** como separador decimal, exigindo um pipeline rigoroso de sanitização.

### 3.2 Cardinalidade Populacional e de Infraestrutura
| Entidade | Contagem Distinta |
|---|---|
| Veículos Únicos (`Placa`) | 3.043.894 |
| Sensores Únicos (`NSerie`)| 61 |

> [!NOTE]
> Identificamos mais de **3 milhões de veículos únicos**, validando nosso fluxo O-D como um reflexo fiel da mobilidade urbana.
> Além disso, o documento do edital afirmava existirem **50 pontos ativos**, mas a base revela **61 sensores únicos**, apontando a presença de radares móveis ou dados fantasmas.

---

## 4. Pipeline de Engenharia de Dados Pós-Auditoria

Com as anomalias diagnosticadas, a base crua foi submetida a um pipeline sequencial de tratamento estrutural (*Data Engineering*) que abandonou a abordagem de amostras simples em favor da extração em camadas lógicas completas:

### 4.1 Camada Bronze (Sanitização e Tipagem)
- **Script:** `scripts/clean_bronze.py`
- **Ação:** O dataset integral de 76 milhões de linhas foi reprocessado via DuckDB.
- **Transformações:** As colunas `Latitude` e `Longitude` tiveram suas vírgulas substituídas por pontos e sofreram *cast* para o tipo matemático `DOUBLE`. A coluna `Datatrafego` foi parseada de texto para `TIMESTAMP`.
- **Resultado:** Geração do arquivo limpo `data/01_bronze/DADOS_SOROCABA_BRONZE.parquet` (5.20 GB).

### 4.2 Camada Silver (Segmentação de Viagens / Matriz O-D)
- **Script:** `scripts/trip_segmentation.py`
- **Ação:** Aplicação da Heurística de **Janela de Inatividade de 45 minutos** (*Trip Sessions*) sobre a base Bronze, extraindo a primeira semana de Janeiro como prova de conceito.
- **Transformações:** Funções de Janela (*Window Functions*) calcularam o *delta* temporal de cada veículo, demarcaram o fim de cada viagem e extraíram a latitude e longitude exatas da Origem e do Destino.
- **Resultado:** Geração da Matriz Origem-Destino `data/02_silver/matriz_od_amostra_1semana.parquet`, contendo **2.143.327 de viagens reais** com duração média de 6.3 minutos, estruturando o caos de pontos assíncronos na verdadeira base de Machine Learning.
