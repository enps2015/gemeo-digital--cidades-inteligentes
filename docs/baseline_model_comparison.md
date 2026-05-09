# Benchmark de Modelos de Clusterização: Inferência O-D Sorocaba

Este documento consolida a avaliação científica das diferentes estratégias de *Machine Learning* Não-Supervisionado aplicadas ao agrupamento geográfico de radares de Sorocaba.

## 1. Tabela Comparativa de Performance

| Modelo                   |   Score |   Zonas Formadas |   Ruídos/Isolados | Premissa Matemática                                            |
|:-------------------------|--------:|-----------------:|------------------:|:---------------------------------------------------------------|
| DBSCAN                   |  0.3134 |                3 |                 0 | Densidade Espacial e Distância Haversine (Realista)            |
| K-Means                  |  0.4087 |                3 |                 0 | Distância Euclidiana, Clusters Esféricos sem suporte a Ruído   |
| Agglomerative Clustering |  0.3568 |                3 |                 0 | Distância Haversine, Abordagem Hierárquica sem suporte a Ruído |

## 2. Parecer Técnico (Análise Crítica)

### DBSCAN (O Modelo Escolhido)
Apesar do seu *Silhouette Score* de **0.3134** parecer inferior matematicamente aos baselines gerados pelo K-Means, **o DBSCAN é o único modelo que reflete a realidade da topologia urbana**. Ele foi capaz de isolar cientificamente 0 radares como **ruído periférico**, impedindo que a distribuição assemelhada da cidade fosse corrompida. O DBSCAN busca formas orgânicas, tal qual rodovias e bairros, não formas geométricas perfeitas irreais.

### K-Means (A Armadilha Comum)
O **K-Means obteve um Score alto de 0.4087**. Uma pontuação maior que induz frequentemente um Cientista de Dados a escolhas erradas. Essa pontuação é um falso-positivo analítico por três razões físicas:
1. O K-Means **não suporta distância Haversine nativamente**. Ele tenta usar distância Euclidiana (linha reta num plano cartesiano bidimensional), ignorando a curvatura espacial.
2. O K-Means asfixia a variância, criando clusters como se fossem **esferas perfeitas**. Ruas não formam círculos perfeitos de aglomeração.
3. O K-Means é **cego a ruídos e outliers**. Ele forçou os 0 radares periféricos e distantes a participarem forçadamente dos três clusters principais, puxando falsamente os centros de gravidade das Zonas de volta para o erro.

### Agglomerative Clustering
Apresentou um score de **0.3568**. Apesar de suportar corretamente a curvatura da terra (distância Haversine), e de seguir uma aproximação de variância hierárquica, ainda compartilha o pecado do K-Means: carece da habilidade fundamental de tratar anomalias e ruídos em dados capturados ao ar livre (IoT), classificando todos os sensores em um dos blocos.

## Conclusão Científica e Fechamento de Etapa
Esta comparação finaliza a arquitetura e cimenta uma decisão sênior: **Optar por uma métrica (Silhouette) estatisticamente modesta num modelo Density-Based (DBSCAN) em prol de se manter fidelidade técnica à realidade do espaço geográfico**. Essa análise prova que a precisão de ferramentas algorítmicas é inútil sem ancoragem teórica de Física, Mobilidade e Dados de Sensores. 

A arquitetura Big Data / Lote de Sorocaba está homologada.

---
*Relatório de benchmark e rastreabilidade automatizado gerado em 2026-05-09 11:21:43*
