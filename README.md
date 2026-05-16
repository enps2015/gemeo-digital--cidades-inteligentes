<div align="center">
  <img src="img/smat_cities01.png" alt="Cidades Inteligentes" width="100%">
</div>

# Inferência de Fluxos Origem-Destino para um MVP de Gêmeo Digital Urbano

**Desafio da Etapa de IA Aplicada:** Mobilidade Urbana (Sorocaba-SP)
**Residência em Gêmeo Digital em 5G** — Facens

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=python&logoColor=white" alt="Folium" />
</div>

<br>

## 👥 Equipe: Pearsonianos (Desafio 1 Splice)

- **Binha Ferraz Dauma** | **Ednardo Pinheiro Peixoto** | **Eric Pimentel** | **Luis Felipe Ferreira**
- **Carlos Delfino** | **Dennis Giancarlo** | **Ana Temoteo** | **Adriano José**

---

## 📌 Versão de banca vs. refinamento pós-banca

Este repositório contém duas versões documentadas:

| Versão                    | Tag / Branch                       | Data                   | Descrição                                                                                                              |
| ------------------------- | ---------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Entrega de banca**      | Tag `v1-banca-ia-aplicada`         | 09/05/2026             | Versão integral defendida na banca da Residência. Preservada como marco histórico imutável.                            |
| **Refinamento pós-banca** | Branch `v2-pos-banca-profissional` | A partir de 15/05/2026 | Correções documentais, adição de limitações e melhorias de reprodutibilidade. Nenhuma alteração de lógica nos modelos. |

Para acessar a versão exata da banca: `git checkout v1-banca-ia-aplicada`

As diferenças entre as versões estão registradas no [`CHANGELOG.md`](CHANGELOG.md).

---

## 🎯 Objetivo do Projeto

Gestores públicos de mobilidade necessitam de dados estruturados para decisões de alocação de infraestrutura. O desafio técnico deste projeto foi **inferir padrões de fluxo Origem-Destino (O-D)** na cidade de Sorocaba-SP, a partir de uma malha de 61 sensores de tráfego que não fornecia rótulos explícitos de viagem.

O pipeline transforma 76 milhões de registros (pings de sensores) em uma Matriz O-D agregada por Macro-Zonas, utilizável como insumo para planejamento de mobilidade urbana, análise de corredores viários e apoio à tomada de decisão pública.

---

## 💾 Acesso à Base de Dados (Google Drive)

Os dados originais não estão hospedados neste repositório devido ao seu volume (> 5GB).
A base de dados que compõe as pastas `data/00_raw` até `data/03_gold` está [**disponível neste link do Google Drive**](https://drive.google.com/drive/folders/1Gw9GFrNwx6wabkjHKkRqk0U1aJmJ-wy5?usp=drive_link).
Para executar os scripts localmente, faça o download e coloque o conteúdo na pasta `data/` na raiz do projeto.

---

## 🏗️ Estrutura do Projeto

```text
📦 gemeo-digital--cidades-inteligentes/
 ┣ 📂 data/             # (Baixar do Drive) Bases divididas em Raw, Bronze, Silver e Gold
 ┣ 📂 data_sample/      # Dados sintéticos/amostrais para testes rápidos (sem PII)
 ┣ 📂 docs/             # Documentação técnica, Canvas PDF e artefatos executivos
 ┃ ┣ 📜 reprodutibilidade.md           # Guia de execução e Smoke Test
 ┃ ┣ 📜 analise_sensibilidade_heuristica.md # Relatório de estabilidade metodológica
 ┃ ┗ 📜 analise_sensibilidade_heuristica.html # Dashboard HTML interativo
 ┣ 📂 img/              # Assets estáticos de imagem
 ┣ 📂 notebooks/        # Experimentações iniciais em Jupyter
 ┣ 📂 scripts/          # Pipeline algorítmico principal (.py)
 ┃ ┣ 📜 audit_data.py                  # Profiling e Data Quality
 ┃ ┣ 📜 clean_bronze.py                # Higienização e tipagem (Camada Bronze)
 ┃ ┣ 📜 trip_segmentation.py           # Window Functions para Matriz O-D (Camada Silver)
 ┃ ┣ 📜 spatial_clustering_ia.py       # Modelo DBSCAN (Camada Gold)
 ┃ ┣ 📜 compare_models_baseline.py     # Comparativo: DBSCAN vs K-Means vs Agglomerative
 ┃ ┣ 📜 generate_temporal_analysis.py  # Dashboard interativo Plotly
 ┃ ┣ 📜 generate_map.py                # Mapa Geoespacial Folium
 ┃ ┣ 📜 generate_demo_data.py          # Gerador de dados sintéticos para avaliação
 ┃ ┗ 📜 sensitivity_inactivity_window.py # Análise paramétrica da heurística de segmentação
 ┣ 📜 index.html        # Hotsite/Portfólio Web (GitHub Pages)
 ┣ 📜 CHANGELOG.md      # Registro de versões e alterações
 ┣ 📜 requirements.txt  # Dependências e bibliotecas do projeto (versões travadas)
 ┗ 📜 README.md         # Este arquivo
```

---

## ⚙️ Pipeline de Dados (ETL)

O processamento utiliza DuckDB para leitura out-of-core e Parquet para armazenamento colunar comprimido, permitindo processar os 76M de registros sem estouro de memória.

O pipeline flui por 4 camadas:

1. **Camada Raw (`00_raw`):** Dados brutos dos sensores IoT, originalmente disponibilizados em CSV e convertidos para Parquet na ingestão inicial para processamento eficiente com DuckDB.
2. **Camada Bronze (`01_bronze` — `clean_bronze.py`):** Ingestão, correção de separadores decimais (vírgulas → pontos) e conversão de strings de data para `TIMESTAMP`.
3. **Camada Silver (`02_silver` — `trip_segmentation.py`):** Segmentação de viagens via Window Functions. Aplica-se uma **janela de inatividade de 45 minutos**: se um veículo desaparece dos sensores por mais de 45 min, a viagem é encerrada. Esse threshold foi adotado como heurística operacional inicial e **ainda não foi calibrado empiricamente para Sorocaba** (ver [Limitações](#-limitações-conhecidas)). Resultado: ~2.1 milhões de viagens na 1ª semana de janeiro.
4. **Camada Gold (`03_gold` — `spatial_clustering_ia.py`):** Clusterização DBSCAN (`eps=2.0 km`, `min_samples=2`, métrica Haversine) aplicada sobre as **coordenadas geográficas dos 61 sensores físicos**. O algoritmo formou **3 Macro-Zonas** (Silhouette Score 0.3134 — separação moderada). Os pares O-D extraídos na camada Silver são então **agregados por Macro-Zona**, gerando a Matriz O-D final entre corredores. Detalhes no [comparativo baseline](docs/baseline_model_comparison.md).

---

## 🚀 Teste Rápido / Avaliadores (Smoke Test)

Não quer baixar os >5GB de dados originais?
Preparamos um **[Guia de Reprodutibilidade e Teste Rápido (Smoke Test)](docs/reprodutibilidade.md)** para gerar dados sintéticos em segundos e validar a execução da arquitetura e dos algoritmos de ponta a ponta na sua máquina.

---

## 🖥️ Como Executar o Projeto Localmente

**1. Instalação e Preparação:**

```bash
# Clone este repositório
git clone https://github.com/enps2015/gemeo-digital--cidades-inteligentes.git
cd gemeo-digital--cidades-inteligentes

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Linux/Mac
.venv\Scripts\activate     # No Windows

# Instale as dependências do projeto
pip install -r requirements.txt
```

_Baixe a pasta `data/` do Google Drive e insira na raiz antes de prosseguir._

**2. Ordem de Execução do Pipeline:**

```bash
# 1. Auditoria e Limpeza (opcional se já baixou os Parquets prontos)
python scripts/audit_data.py
python scripts/clean_bronze.py

# 2. Extração da Matriz Origem-Destino
python scripts/trip_segmentation.py

# 3. Clusterização Espacial
python scripts/spatial_clustering_ia.py

# 4. Geração de Visualizações
python scripts/generate_temporal_analysis.py
python scripts/generate_map.py

# (Opcional) Comparativo de modelos baseline
python scripts/compare_models_baseline.py
```

---

## 🌐 Portfólio Interativo (GitHub Pages)

Os resultados do projeto estão consolidados em uma página web publicada via **[GitHub Pages](https://enps2015.github.io/gemeo-digital--cidades-inteligentes/)**. A página disponibiliza:

- Cards com o **Business Model Canvas** do projeto.
- **Dashboard Temporal:** gráficos interativos Plotly com a distribuição horária e diária dos fluxos.
- **Mapa Interativo de Fluxo:** mapa Folium com representação visual dos corredores entre as Macro-Zonas identificadas pelo DBSCAN.

---

## 🔒 Privacidade e Tratamento de Dados

- O campo `Placa` foi recebido como identificador pseudonimizado (hash de comprimento fixo), conforme disponibilizado pelo órgão fornecedor da base. O pipeline não executa nenhum processo de anonimização adicional.
- Na camada Silver, esse identificador é utilizado exclusivamente para reconstrução temporal das trajetórias (segmentação de viagens por veículo). Ele não é exposto em nenhuma saída pública.
- As visualizações públicas (dashboard, mapa, hotsite) operam exclusivamente com dados agregados por sensor, Macro-Zona e corredor — sem granularidade individual de veículo.
- O projeto **não tenta reidentificar indivíduos** a partir dos hashes nem cruza dados com bases externas.
- Este projeto **não declara conformidade plena com a LGPD**, pois tal afirmação requer parecer jurídico formal que não foi obtido.
---

## 🔬 Análise de Sensibilidade da Heurística
Para garantir a governança estrutural da Matriz O-D, desenvolvemos o script paramétrico `sensitivity_inactivity_window.py` (Fase 3 pós-banca). Ele testou limites temporais de **15, 30, 45, 60 e 90 minutos**. Os resultados indicaram que 45 minutos atua como um **compromisso operacional defensável**, pois retém alta estabilidade nos corredores O-D críticos e reduz a super-fragmentação de viagens curtas. Mais detalhes no [Relatório Metodológico](docs/analise_sensibilidade_heuristica.md) e no [Dashboard Interativo](docs/analise_sensibilidade_heuristica.html).

---

## ⚠️ Limitações Conhecidas

1. **Amostragem temporal limitada:** A Matriz O-D foi construída sobre a 1ª semana de janeiro/2026 (7 dias). Não há validação cruzada com outras semanas ou meses. Generalizações para outros períodos devem ser feitas com cautela.
2. **Granularidade dos sensores:** O DBSCAN clusteriza 61 pontos fixos (sensores). A resolução espacial é limitada pela densidade da malha de radares, não pela capacidade do algoritmo.
3. **Heurística de 45 minutos sem ground truth externo:** O threshold de inatividade (45 min) foi submetido à análise de sensibilidade comparando diferentes thresholds e mostrou-se um bom compromisso operacional. Contudo, não há validação com dados validados externamente (ex: GPS de frota) para atestar inquestionavelmente se as viagens inferidas espelham exatamente a realidade física daquela semana, avaliando apenas a consistência interna.
4. **Silhouette Score moderado:** O valor de 0.3134 indica separação moderada entre clusters. É um resultado típico para dados geoespaciais urbanos onde as fronteiras entre zonas são naturalmente difusas — não é indicativo de falha, mas também não constitui evidência de excelência.
5. **DBSCAN com Ruídos = 0:** Com os parâmetros adotados (`eps=2.0 km`, `min_samples=2`), todos os 61 sensores foram absorvidos em clusters. A capacidade de isolamento de ruído do DBSCAN — uma de suas vantagens teóricas — não foi exercida nesta configuração.
6. **Reprodutibilidade parcial:** o projeto já possui requirements.txt e smoke test sintético, mas a reprodução completa dos resultados oficiais ainda depende do download externo da base original.
7. **Sem testes automatizados:** O pipeline não possui suite de testes.
8. **Dependência de dados externos:** A execução completa do pipeline depende do download da base de dados via Google Drive.

---

## 🚧 Desafios Técnicos e Soluções Adotadas

- **Estouro de memória:** Notebooks não suportavam a base raw (~12GB CSV). Solução: arquitetura DuckDB + Parquet em processamento out-of-core.
- **Ausência de variável-alvo:** Nenhuma coluna indicava destino dos veículos. Solução: heurística de segmentação espaço-temporal (janela de 45 min de inatividade).
- **Divergência na documentação do edital:** O edital citava 50 sensores, mas a base continha 61 equipamentos distintos. Solução: script de profiling (`audit_data.py`) com validação cruzada (`COUNT(DISTINCT NSerie)` + agrupamento volumétrico).

---

## 🔮 Possíveis Evoluções

1. **Ingestão em tempo real:** Evoluir o pipeline batch para ingestão por streaming (ex: Kafka).
2. **Modelos preditivos:** Utilizar os dados de fluxo para alimentar modelos de previsão de congestionamento (ex: LSTM).
3. **Enriquecimento de contexto:** Integrar dados meteorológicos e calendário de eventos para análise multivariada dos fluxos.

---

> _Desenvolvido para o módulo IA Aplicada da Residência em Gêmeo Digital em 5G (Facens) — 2026_
