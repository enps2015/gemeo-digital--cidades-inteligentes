# Guia de Reprodutibilidade e Teste (Smoke Test)

Este guia foi elaborado para recrutadores, avaliadores técnicos e professores que desejam validar a execução local do pipeline de Engenharia de Dados e Machine Learning (DBSCAN) deste projeto, sem a necessidade de baixar os >5GB de dados originais.

---

## 1. O que é o Smoke Test?

Criamos um script gerador de dados **totalmente sintéticos e fictícios**. Ele recria a estrutura mínima compatível com os scripts principais e os tipos de dados das tabelas originais da Camada Raw. As coordenadas geográficas são geradas aleatoriamente em torno de Sorocaba-SP apenas para que o modelo espacial funcione mecanicamente. Nenhum comportamento real de mobilidade urbana é simulado.

> **Aviso:** Os gráficos gerados ao final, as volumetrias e as zonas identificadas pelo algoritmo DBSCAN **não terão valor analítico real**. O único objetivo deste teste é demonstrar que as engrenagens de código (DuckDB, ETL, e scikit-learn) executam sem erros.

---

## 2. Passo a Passo para Execução

### Passo 2.1: Preparar o Ambiente
Recomendamos o uso de um ambiente virtual Python (versão 3.9 ou superior).

```bash
# Clone o repositório
git clone https://github.com/enps2015/gemeo-digital--cidades-inteligentes.git
cd gemeo-digital--cidades-inteligentes

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Linux/Mac
# .venv\Scripts\activate   # No Windows

# Instale as dependências com versões travadas
pip install -r requirements.txt
```

### Passo 2.2: Gerar os Dados Sintéticos
Execute o script gerador. Ele criará o diretório `data/00_raw` (se não existir) e depositará o arquivo Parquet fictício no local esperado pelos scripts principais.

```bash
python scripts/generate_demo_data.py
```
*(O script contém proteções e emitirá um aviso pedindo confirmação caso você já possua um arquivo grande de dados reais nessa pasta, para evitar exclusão acidental).*

### Passo 2.3: Executar o Pipeline de Ponta a Ponta
Como os scripts principais (originais do projeto) estão programados para ler a pasta `data/`, você precisará copiar o arquivo gerado para o diretório correto:

```bash
mkdir -p data/00_raw
cp data_sample/00_raw/DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet data/00_raw/
```
*(Se você já possui a base original de 5GB baixada, renomeie-a temporariamente para evitar sobrescrevê-la).*

Agora, execute as camadas do pipeline na ordem cronológica:

```bash
# 1. Auditoria e Higienização (Camadas Raw e Bronze)
python scripts/audit_data.py
python scripts/clean_bronze.py

# 2. Heurística de Segmentação de Viagens (Camada Silver)
python scripts/trip_segmentation.py

# 3. Inteligência Artificial: Clusterização Espacial (Camada Gold)
python scripts/spatial_clustering_ia.py

# 4. Produtos de Dados (Dashboard e Mapa)
python scripts/generate_temporal_analysis.py
python scripts/generate_map.py
```

### Passo 2.4: Verificar Resultados
Ao final, o pipeline terá gerado artefatos em HTML, como o `mapa_fluxo_sorocaba.html` e possíveis relatórios. Abra-os em seu navegador para validar a execução.
