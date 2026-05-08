# Documentação Executiva do Projeto: Inferência de Fluxos Origem-Destino com IA
**Projeto:** Gêmeos Digitais TIC51 | **Desafio 1:** Mobilidade Urbana em Sorocaba-SP  

---

## 1. Problema de Negócio e Contexto
A gestão de mobilidade urbana depende da compreensão profunda de como a população se desloca. O desafio proposto exige a inferência de padrões de fluxo Origem-Destino (O-D) a partir de uma base massiva de sensores de tráfego, desprovida de rótulos explícitos de viagem. O objetivo final é traduzir 76 milhões de "pings" de radares em inteligência acionável (Matriz O-D) para subsidiar decisões de políticas públicas (ex: novos trajetos de ônibus e expansão viária).

## 2. Pergunta Analítica
*Como identificar, delimitar e agrupar viagens individuais contínuas em um fluxo de dados de sensores assíncronos, para extrair zonas primárias de Origem e Destino na cidade de Sorocaba?*

## 3. Os Dados e a Engenharia de Estruturação

### 3.1. Estratégia de Engenharia de Dados (Big Data)
O dataset original fornecido (localizado em `data/00_raw/`) em formato CSV era consideravelmente pesado, ultrapassando os 12 GB, o que inviabilizaria a manipulação convencional em memória RAM (ferramentas como Pandas padrão resultariam em falhas de *Out-Of-Memory*). 

Para contornar este gargalo tecnológico, a primeira estratégia adotada foi a **Conversão Estrutural para Parquet**. Essa ação reduziu o tamanho físico do arquivo para **5.15 GB** através de compressão *Snappy* e armazenamento colunar. Acoplada a essa conversão, adotamos o motor de banco de dados **DuckDB**, permitindo a leitura e o processamento matemático do arquivo via streaming (*Out-Of-Core*), processando 76.662.221 registros em meros segundos, sem estourar a memória.

### 3.2. Aspectos Gerais das Variáveis
A base de dados possui 9 variáveis primárias, que apresentaram os seguintes perfis durante nossa auditoria automatizada:
*   `NSerie`, `Endereco`, `Sentido`: Variáveis categóricas que descrevem a identidade, local e direção do sensor.
*   `Datatrafego`: Série temporal que registra o momento exato da passagem do veículo. Originalmente gravada como texto (VARCHAR), exigiu conversão para `TIMESTAMP` matemático no formato numérico brasileiro (`%d/%m/%Y %H:%M:%S`).
*   `Latitude` e `Longitude`: Coordenadas espaciais vitais para o projeto. Apresentaram um erro crônico de tipagem: estavam no formato texto com mistura de vírgulas e pontos decimais. Um pipeline foi construído para higienizar, expurgar as vírgulas e aplicar o *cast* para `DOUBLE`.
*   `Placa`: O hash criptográfico anonimizado de 64 caracteres que identifica o veículo. Diferente de um ambiente controlado, identificamos **3.043.894 veículos únicos** operando no trimestre.
*   `Velocidade 1` e `Velocidade Regul`: Variáveis numéricas contínuas medindo o comportamento dinâmico da via.

### 3.3. A Prova dos 61 Sensores (Infraestrutura Divergente)
O documento oficial do edital cita categoricamente a existência de "50 pontos de coleta ativos". No entanto, nossa equipe submeteu a base a **duas análises de validação cruzada independentes**:
1.  **Extração de Hashes Únicos:** O comando `COUNT(DISTINCT)` extraiu 61 strings únicas para a variável `NSerie`.
2.  **Agrupamento Volumétrico de Prova:** Para afastar falsos positivos, executamos um agrupamento (`GROUP BY NSerie`) listando a volumetria absoluta de cada sensor. O teste comprovou os 61 sensores e revelou o padrão: os sensores do topo (`10xx`) capturam mais de 4 milhões de registros cada, enquanto 11 sensores da base da lista (`80xx`) possuem volumes muito baixos (ex: 10 mil leituras). 

Isso indica falha na documentação do edital e a presença oculta de equipamentos periféricos (como radares móveis, sensores em teste ou câmeras de muralha digital) que foram absorvidos em nossa modelagem sem perda de dados.

## 4. Definição Categórica da Variável-Alvo
Em Ciência de Dados, problemas de clusterização (Não-Supervisionados) não possuem uma variável-alvo ("Y") pré-rotulada clássica. Nosso desafio primário foi **criar as variáveis matemáticas** que alimentariam o algoritmo de Machine Learning.

Para não dar margens a más interpretações na banca, definimos a extração dos dados alvo (Features) através da heurística de **Sessões de Trajetória (Trip Sessions)** com base em uma **Janela de Inatividade**:
1.  **A Regra de Delimitação:** Se a placa 'X' passa por um sensor e desaparece do radar de toda a cidade por **mais de 45 minutos**, o motor de banco de dados encerra aquela viagem. O último sensor detectado torna-se o **Destino**. O próximo reaparecimento da placa será classificado como uma nova **Origem**.
2.  **As Variáveis-Alvo do Algoritmo:** As features estruturadas que alimentam o nosso Machine Learning são **exclusivamente geoespaciais**. O algoritmo consumirá:
    *   `[origem_lat, origem_lon]` 
    *   `[destino_lat, destino_lon]`

Esta lógica estruturada extraiu **2.1 milhões de viagens contínuas puras** (com duração média de 6.3 minutos) apenas na primeira semana de janeiro, transformando 76 milhões de pings desconexos na nossa verdadeira base de Inteligência Artificial.

## 5. Estratégia de Inteligência Artificial (Machine Learning)
1. **Passo 1 - Engenharia de Features (Heurística):** O pipeline em DuckDB calculou o Delta de Tempo (*Window Functions*) para extrair as matrizes O-D em frações de segundos.
2. **Passo 2 - IA Não-Supervisionada (Clusterização Espacial):** Com as coordenadas de Origem e Destino geradas, a inteligência da solução aplica o **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) ou **K-Means Espacial**. 
   * *O Porquê Técnico:* 2.1 milhões de rotas puras não geram decisão de negócio. O algoritmo de ML agrupará pontos de paradas muito próximos, fundindo-os em macro **Zonas de Densidade**. Ele varre o mapa identificando onde há aglomeração matemática de partidas e chegadas.

## 6. Métricas Oficiais de Avaliação Adotadas
Dado o caráter Não-Supervisionado (Clusterização) do projeto, descartamos formalmente métricas de classificação categórica (como F1-Score ou AUC-ROC) e adotaremos as seguintes métricas científicas:

1. **Silhouette Score (Coeficiente de Silhueta):** Métrica matemática que varia de -1 a 1. Ela medirá o quão coesos estão os nossos clusters de zonas da cidade (distância intra-cluster) em relação a zonas vizinhas (distância inter-cluster). Um score positivo próximo de 1 indica que o agrupamento espacial das origens/destinos funcionou com excelência.
2. **Avaliação Georreferenciada (Inspeção Qualitativa):** Avaliação de "Falsos Positivos" semânticos no mundo real. O modelo será validado sobrepondo as "Zonas" criadas pela IA em um mapa rodoviário real de Sorocaba. Se a IA gerar um polo de fluxo intenso no meio de um lago ou em área de mata fechada, o modelo falhou em coerência e precisará de ajustes no raio de distância do cluster.

## 7. O Produto Final: MVP a ser Apresentado
Nossa entrega de Produto Mínimo Viável (Sábado) não será apenas um notebook com códigos abstratos, mas uma demonstração de Inteligência Acionável para gestão pública. O MVP consistirá de:

1.  **Pipeline Transparente:** Um Notebook limpo mostrando a rápida transformação do caos de 76 milhões de linhas para a extração purificada das viagens (A Auditoria e a Matriz O-D).
2.  **O Mapa de Calor Interativo (Heatmap Georreferenciado):** 
    *   Utilizando bibliotecas como `Folium` ou `Kepler.gl`, apresentaremos o mapa de Sorocaba plotado com as verdadeiras "Zonas de Calor" reveladas pelo algoritmo de Clusterização.
    *   Haverá distinção visual clara entre as Zonas de **Alta Origem** (Pólos residenciais matinais) e Zonas de **Alto Destino** (Pólos comerciais/industriais).
    *   **Insights Acionáveis:** A apresentação culminará na demonstração de 2 ou 3 grandes fluxos anômalos ou hiper-densos descobertos pela IA, servindo de base teórica imediata para o redirecionamento de linhas de ônibus urbanos.
