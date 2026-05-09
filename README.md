<div align="center">
  <img src="img/smat_cities01.png" alt="Cidades Inteligentes" width="100%">
</div>

# Gêmeos Digitais: Inferência de Fluxos Origem-Destino com IA
**Desafio Final:** IA Aplicada a Problemas Reais (Mobilidade Urbana)  
**Residência em Gêmeo Digital em 5G** — Facens

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=python&logoColor=white" alt="Folium" />
</div>

<br>

## 👥 A Equipe: Pearsonianos (Desafio 1 Splice)
*   **Binha Ferraz Dauma** | **Ednardo Pinheiro Peixoto** | **Eric Pimentel** | **Luis Felipe Ferreira**
*   **Carlos Delfino** | **Dennis Giancarlo** | **Ana Temoteo** | **Adriano José**

---

## 🎯 Objetivo do Projeto
Gestores públicos de mobilidade necessitam de respostas baseadas em dados para alocação de infraestrutura. O nosso desafio técnico foi **inferir padrões de fluxo de Origem-Destino (O-D)** na cidade de Sorocaba-SP, utilizando uma malha de sensores de tráfego que, originalmente, **não fornecia rótulos explícitos de viagem**. 

Nosso foco foi transformar 76 milhões de registros (pings) desconexos em **Inteligência Acionável** capaz de alimentar as premissas de um Gêmeo Digital Urbano.

---

## 💾 Acesso à Base de Dados (Google Drive)
Os dados massivos originais não estão hospedados neste repositório devido ao seu volume (> 5GB). 
Toda a base de dados que compõe as pastas `data/00_raw` até `data/03_gold` encontra-se [**Disponível neste Link do Google Drive**](https://drive.google.com/drive/folders/1Gw9GFrNwx6wabkjHKkRqk0U1aJmJ-wy5?usp=drive_link). 
Para executar os códigos localmente, faça o download do conteúdo do link e coloque-o na raiz do projeto dentro da pasta `data/`.

---

## 🏗️ Estrutura do Projeto
O repositório está organizado segundo as melhores práticas de Engenharia de Software para Ciência de Dados:

```text
📦 desafio1/
 ┣ 📂 data/             # (Baixar do Drive) Bases divididas em Raw, Bronze, Silver e Gold
 ┣ 📂 docs/             # Documentação técnica, Canvas PDF e artefatos executivos
 ┣ 📂 img/              # Assets estáticos de imagem
 ┣ 📂 notebooks/        # Experimentações iniciais em Jupyter
 ┣ 📂 scripts/          # Pipeline algorítmico principal (.py)
 ┃ ┣ 📜 audit_data.py                  # Profiling e Data Quality
 ┃ ┣ 📜 clean_bronze.py                # Higienização e tipagem (Camada Bronze)
 ┃ ┣ 📜 trip_segmentation.py           # Window Functions para Matriz O-D (Camada Silver)
 ┃ ┣ 📜 spatial_clustering_ia.py       # Modelo DBSCAN Não-Supervisionado (Camada Gold)
 ┃ ┣ 📜 generate_temporal_analysis.py  # Dashboard interativo Plotly
 ┃ ┗ 📜 generate_map.py                # Mapa Geoespacial Folium (Gêmeo Digital)
 ┣ 📜 index.html        # Hotsite/Portfólio Web (MVP Executivo)
 ┗ 📜 README.md         # Você está aqui
```

---

## ⚙️ Engenharia de Dados (Pipeline ETL)
Construímos uma arquitetura de dados escalável para processar volumes massivos sem estouro de memória (RAM), utilizando processamento *Out-Of-Core* via **DuckDB** e compressão colunar **Parquet**.

O pipeline flui estritamente por 4 camadas:
1.  **Camada Raw (`00_raw`):** Os arquivos CSV pesados originados da captura de IoT (Sensores).
2.  **Camada Bronze (`01_bronze` - *clean_bronze.py*):** Ingestão bruta, higienização de separadores decimais falhos (vírgulas vs pontos) e conversão de strings de datas para objetos matemáticos de tempo (`TIMESTAMP`).
3.  **Camada Silver (`02_silver` - *trip_segmentation.py*):** Onde a mágica analítica acontece. Aplicação de *Window Functions* para criar uma **Janela de Inatividade de 45 minutos**. Se um carro desaparece dos radares por mais de 45 minutos, declaramos sua rota como finalizada matematicamente. Aqui nasce a primeira *Matriz Origem-Destino Bruta*.
4.  **Camada Gold (`03_gold` - *spatial_clustering_ia.py*):** A Inteligência Artificial em ação. O algoritmo geoespacial **DBSCAN** consome os pares O-D da camada Silver para agrupar as coordenadas físicas em pólos de alta densidade veicular. A IA formou **3 Macro-Zonas**, obtendo um *Silhouette Score* de `0.3134` (alta coesão espacial). O output final é a matriz de Macro-Corredores pronta para BI.

---

## 🖥️ Como Executar o Projeto Localmente

**1. Instalação e Preparação:**
```bash
# Clone este repositório
git clone https://github.com/SEU-USUARIO/desafio1.git
cd desafio1

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Linux/Mac
.venv\Scripts\activate     # No Windows

# Instale as bibliotecas principais
pip install duckdb pandas scikit-learn plotly folium numpy
```
*Lembrete: Baixe a pasta `data/` do Google Drive e insira na raiz antes de prosseguir.*

**2. Ordem de Execução do Pipeline:**
```bash
# 1. Auditoria e Limpeza (Opcional se já baixar os parquets prontos)
python scripts/audit_data.py
python scripts/clean_bronze.py

# 2. Extração da Matriz Origem-Destino
python scripts/trip_segmentation.py

# 3. Modelagem IA Não-Supervisionada
python scripts/spatial_clustering_ia.py

# 4. Geração do Gêmeo Digital Visuais
python scripts/generate_temporal_analysis.py
python scripts/generate_map.py
```

---

## 🌐 Portfólio Interativo (MVP Web)
Como coroamento do projeto, consolidamos os dados em uma página executiva otimizada para o **GitHub Pages**. 
O site de portfólio está disponível publicamente via **[GitHub Pages (Clique Aqui)](https://enps2015.github.io/gemeo-digital--cidades-inteligentes/)** e foi desenhado com estética *Dark/Cyber* para materializar o conceito de "Smart City". Nele, disponibilizamos:
*   As regras do nosso **Business Model Canvas** em cards interativos.
*   **Dashboard Temporal:** Gráficos interativos renderizados em Plotly.
*   **Mapa Interativo de Fluxo:** Mapa tático Folium desenhando fisicamente a animação de tráfego pesado operando entre os centros de massa (Macro-Zonas) definidos pela Inteligência Artificial.

---

## 🏆 Atualizações Pós-Banca (Homologação Final)
Após a defesa bem-sucedida do projeto, realizamos um refinamento técnico profissional no repositório para cristalizar nossas entregas:
*   **Comprovação Algorítmica (Baseline):** Criação do script `scripts/compare_models_baseline.py`, que executa o K-Means e o Agglomerative Clustering contra a nossa base. Isso provou matematicamente e geograficamente a superioridade do **DBSCAN** (escolhido originalmente) para a semântica de mobilidade viária.
*   **Novo Relatório Analítico:** Geração do documento `docs/baseline_model_comparison.md` (e sua versão PDF), detalhando o rigor técnico da análise comparativa dos três algoritmos.
*   **Refinamento de UX/UI (Hotsite):** Auditoria de CSS e aplicação de responsividade extrema no arquivo `index.html`. Foram aplicadas diretivas de isolamento de layout, garantindo que o painel Plotly (`2x2` no Desktop e `3x1` no celular) e o mapa dinâmico Folium sejam consumidos com perfeição visual em qualquer tela.
*   **Atualização Documental:** Inclusão nominal de todos os membros da equipe nos relatórios em formato Markdown e geração de todas as vias consolidadas em PDF, juntamente com a apresentação de encerramento (`Apresentacao-do-desafio1-splice.pdf`).

---

## 🚧 Desafios Encontrados e Soluções Adotadas
*   **Problema (Estouro de Memória):** Notebooks congelando ao tentar ler a base raw (12GB csv).  
    *Solução:* Adoção da arquitetura *DuckDB + Parquet* em streaming.
*   **Problema (Ausência de Target/Variável Alvo):** Nenhuma coluna dizia para onde os carros iam.  
    *Solução:* Desenvolvimento de uma heurística espaço-temporal de 45 minutos para "recortar" o histórico do veículo em sub-viagens.
*   **Problema (Divergência Documental):** O edital falava em 50 sensores, mas a base continha lixo e radares anômalos.  
    *Solução:* Script rigoroso de *Data Profiling* para atestar os 61 equipamentos físicos reais e remover hardwares "fantasmas".

## 🚀 Melhorias Futuras e Roadmap
1.  **Integração em Tempo Real (Kafka/Streaming):** Evoluir o pipeline em lote (*batch*) para ingestão de dados por telemetria contínua.
2.  **Machine Learning Preditivo (Deep Learning):** Alimentar Redes Neurais Long Short-Term Memory (LSTM) com o resultado das nossas Macro-Zonas para não apenas ler o presente, mas **prever engarrafamentos** em janelas de 30 minutos no futuro.
3.  **Fusão de Dados (Clima e Eventos):** Enriquecer a matriz com dados meteorológicos e agenda da cidade (shows, feriados) para criar um Gêmeo Digital responsivo ao ambiente urbano vivo.

---
> *Desenvolvido para o módulo final da Residência em Gêmeo Digital em 5G (Facens) - Ano 2026*

---
## Equipe: Pearsonianos - Desafio 1 Splice
* Binha Ferraz Dauma
* Ednardo Pinheiro Peixoto
* Eric Pimentel
* Luis Felipe Ferreira
* Carlos Delfino
* Dennis Giancarlo
* Ana Temoteo
* Adriano José
