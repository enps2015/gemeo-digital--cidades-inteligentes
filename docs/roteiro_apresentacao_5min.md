# Roteiro de Defesa: Apresentação Executiva (5 Minutos)

Para atender estritamente aos critérios exigidos pelo professor, estruturamos uma apresentação direta e incisiva de 1 slide e 5 blocos de fala. Como você será o "front-man" nos 5 minutos, treine esse roteiro cronometrado (visando 4m e 30s de fala, deixando margem de erro). 

O restante do documento traz o treinamento para a sua equipe blindar as respostas no Q&A.

---

## Estrutura do Slide Único (Altamente Recomendado)
*Não polua com textos longos.* 

**Título:** Inferência de Fluxos Origem-Destino (Mobilidade Inteligente em Sorocaba)
*   **Problema:** Ausência de rotas (76 milhões de registros fragmentados sem Origem/Destino declarados).
*   **Estratégia:** Big Data (DuckDB) ➔ Heurística de Janela de 45 min ➔ IA Não-Supervisionada (DBSCAN).
*   **Solução [Imagens]:** Exibir um Print lado a lado do **Dashboard Temporal** e do **Mapa de Macro-Zonas (Folium)**.
*   **Limitações:** Viés de sensor (pontos cegos na cidade).
*   **Impacto:** Planejamento viário baseado em densidade acionável em tempo real.

---

## O Seu Roteiro de Apresentador

**1. Problema Abordado [0:00 - 0:45]**
> "Bom dia/Boa tarde a todos. O nosso grupo enfrentou um problema real e caótico de cidades inteligentes: como inferir a mobilidade urbana de Sorocaba com uma massa bruta de 76 milhões de registros de radares? O grande gargalo de negócio era a ausência da resposta no dado: nós tínhamos os 'pings' dos veículos passando pela infraestrutura, mas não tínhamos declarações de origem e destino, tampouco a rota percorrida."

**2. Estratégia e Abordagem [0:45 - 1:45]**
> "Nossa estratégia adotou Engenharia de Dados pesada. Convertemos a base para Parquet e processamos tudo via DuckDB em segundos. Como não tínhamos as viagens, nós as criamos matematicamente via 'Sessionização'. Criamos uma heurística: se o carro desaparece de toda a rede por mais de 45 minutos, declaramos aquela viagem como encerrada. Nasce aí o nosso Destino."

**3. Solução Proposta [1:45 - 2:45]**
> "Isso extraiu mais de 2 milhões de rotas reais puras. Contudo, milhares de pontos geram ruído visual. Era necessária a IA. Adotamos o **DBSCAN**, um algoritmo de clusterização espacial não-supervisionado. Ele agrupou esses milhões de fluxos latentes em **3 grandes Macro-Zonas** (A, B e C) na cidade. A solução gerada, como mostram as imagens, é um painel tático interativo que revela os Macro-Corredores de tráfego, validado cientificamente por um Silhouette Score de 0.31."

**4. Limitações Identificadas [2:45 - 3:30]**
> "Atuando com rigor científico, assumimos os limites da solução. Nosso modelo captura a movimentação de mais de 3 milhões de veículos únicos, contudo ele sofre da 'Limitação de Hardware'. Nós captamos e inferimos fluxos majoritariamente onde os 61 sensores estão. O deslocamento intra-bairros periféricos sem cobertura escapa da matriz O-D atual, formando um viés de seleção."

**5. Impacto Potencial da Solução [3:30 - 4:15]**
> "Ainda assim, o impacto da entrega é massivo para o Gêmeo Digital. Com nosso MVP, saímos da intuição política e entramos na precisão algorítmica. O gestor público consegue enxergar a sazonalidade e a direção dos fluxos pesados — quem sai do polo residencial às 7h e deságua no polo comercial. Isso fundamenta a criação de novas faixas viárias, ajuste semafórico inteligente e expansão cirúrgica de frotas de ônibus. Muito obrigado."

---

## Simulação de Q&A: Preparação da Equipe (2 Minutos)
*(Entregue isso para que seus colegas leiam e saibam exatamente como contra-atacar).*

**Pergunta 1 (Professor/Aluno): Por que vocês definiram a 'janela de inatividade' para descobrir o fim da viagem em exatos 45 minutos?**
*   **Resposta Tática (Equipe):** *"Baseado no diâmetro e na densidade demográfica de Sorocaba. Testes com janelas menores cortavam viagens em andamento no trânsito pesado. Já 45 minutos fora do radar é a garantia heurística razoável de que o motorista chegou e estacionou no seu destino (casa, shopping, trabalho). É um limite conservador que blindou nosso modelo contra a fusão indevida de duas viagens independentes do mesmo veículo no dia."*

**Pergunta 2 (Banca Especialista): Por que usar o DBSCAN e não um simples K-Means para agrupar as Macro-Zonas no mapa?**
*   **Resposta Tática (Equipe):** *"O K-Means exige que o cientista de dados adivinhe o parâmetro 'K' — ou seja, defina antes quantas zonas a cidade possui e é muito sensível a *outliers*. O DBSCAN não. Ele descobre zonas puramente baseado na densidade real e lida graciosamente com ruídos. Escolher o DBSCAN foi uma decisão deliberada para deixar os dados nos dizerem onde estão os polos de tráfego, mitigando nosso próprio viés."*

**Pergunta 3 (Aluno Competidor): Eu notei que a documentação falava em 50 sensores, mas vocês citam sempre 61. Por que essa discrepância?**
*   **Resposta Tática (Equipe):** *"Nós rodamos um pipeline de Data Profiling minucioso. Através de varreduras SQL (Count Distinct), a matemática revelou 61 hardwares únicos disparando dados. Alguns possuem volumetria muito baixa e podem ser comissionamentos, equipamentos desativados ou radares móveis recentes, mas seus pings estão na base. Preferimos confiar nos dados brutos provados por código do que em um edital que pode estar desatualizado com a infraestrutura real."*

**Pergunta 4 (Professor): O Silhouette Score do modelo de vocês deu um valor de 0.31. Em ML, sabemos que valores mais altos são melhores. O de vocês é suficiente?**
*   **Resposta Tática (Equipe):** *"Num contexto físico de mobilidade caótica no mundo real, um score de 0.3134 é extremamente satisfatório e válido. Como a métrica vai de -1 a 1, pontuar acima de zero já garante que a coesão interna das Macro-Zonas supera as distâncias entre elas. Significa que nosso DBSCAN obteve fronteiras sólidas entre as zonas da cidade sem superposição caótica."*
