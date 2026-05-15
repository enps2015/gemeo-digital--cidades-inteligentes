# Benchmark de Modelos de Clusterização: Inferência O-D Sorocaba

Este documento consolida a avaliação comparativa das estratégias de clusterização não-supervisionada aplicadas ao agrupamento geográfico dos 61 sensores de tráfego de Sorocaba.

## 1. Tabela Comparativa de Performance

| Modelo                   |   Score |   Zonas Formadas |   Ruídos/Isolados | Premissa Matemática                                            |
|:-------------------------|--------:|-----------------:|------------------:|:---------------------------------------------------------------|
| DBSCAN                   |  0.3134 |                3 |                 0 | Densidade Espacial e Distância Haversine                       |
| K-Means                  |  0.4087 |                3 |                 0 | Distância Euclidiana, Clusters Esféricos, sem suporte a ruído  |
| Agglomerative Clustering |  0.3568 |                3 |                 0 | Distância Euclidiana (linkage average), sem suporte a ruído    |

> **Nota sobre Ruídos/Isolados = 0 (DBSCAN):** Com os parâmetros adotados (`eps=2.0 km`, `min_samples=2`), todos os 61 sensores foram atribuídos a algum dos 3 clusters. Nenhum sensor foi classificado como ruído (`label == -1`). Isso significa que, para esta configuração, a **capacidade de isolamento de ruído** do DBSCAN — uma de suas vantagens teóricas — **não foi exercida na prática**. A malha de sensores de Sorocaba, com raio de 2 km entre vizinhos, não apresentou pontos suficientemente isolados para acionar esse mecanismo.

## 2. Parecer Técnico (Análise Comparativa)

### DBSCAN (Modelo Adotado)

O DBSCAN obteve o menor Silhouette Score (0.3134) entre os três modelos. Essa métrica, isoladamente, não indica desempenho inferior: o Silhouette Score mede a separação geométrica entre clusters, e valores moderados são esperados em dados geoespaciais urbanos onde as fronteiras entre zonas são naturalmente difusas.

A escolha pelo DBSCAN fundamenta-se em duas propriedades relevantes para o domínio de mobilidade urbana:

1. **Métrica Haversine nativa:** O DBSCAN da scikit-learn aceita distância Haversine diretamente, respeitando a curvatura terrestre. O raio `eps` tem significado físico real (quilômetros).
2. **Não requer definição prévia de k:** O número de clusters emerge dos dados, ao contrário do K-Means e do Agglomerative, que exigem especificação antecipada.

O fato de todos os sensores terem sido absorvidos em clusters (sem ruído detectado) é consistente com a densidade da malha de radares em Sorocaba. Com parâmetros mais restritivos (ex: `eps=1.0 km`), sensores periféricos poderiam ser isolados — mas isso não foi explorado nesta versão.

### K-Means

O K-Means obteve o maior Silhouette Score (0.4087). Contudo, esse resultado deve ser interpretado com cautela:

1. O K-Means opera com distância Euclidiana sobre coordenadas (lat, lon), o que introduz distorção em relação a distâncias geográficas reais.
2. Pressupõe clusters convexos e de tamanhos similares — premissas que não se sustentam necessariamente em malhas viárias urbanas.
3. Não possui mecanismo de detecção de outliers; todos os pontos são atribuídos ao cluster mais próximo.

O score superior reflete clusters mais geometricamente separados, não necessariamente agrupamentos mais coerentes com a semântica de mobilidade.

### Agglomerative Clustering

Apresentou score intermediário (0.3568). A implementação utilizada operou com distância Euclidiana e linkage average. Compartilha com o K-Means a limitação de atribuir todos os pontos a clusters sem detecção de anomalias.

## 3. Conclusão

O DBSCAN foi adotado como modelo de produção por oferecer suporte nativo a distância geodésica e por não exigir definição prévia do número de clusters. O Silhouette Score de 0.3134 representa separação moderada, coerente com a distribuição geográfica dos sensores em Sorocaba.

A comparação com K-Means e Agglomerative Clustering serve como baseline para contextualizar a escolha, não para declarar superioridade absoluta de um modelo sobre outro.

---
*Relatório de benchmark gerado automaticamente em 2026-05-09 11:21:43 (data de execução original).*
*Narrativa revisada em 2026-05-15 para alinhar texto à evidência factual.*

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
