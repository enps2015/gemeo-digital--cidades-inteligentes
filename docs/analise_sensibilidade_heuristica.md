# Análise de Sensibilidade: Heurística da Janela de Inatividade

> **Objetivo:** Avaliar empiricamente a robustez e a estabilidade do threshold de inatividade (45 minutos) adotado na Fase 1 para a segmentação de viagens em uma base massiva de radares.

---

## 1. Contexto da Análise
Em projetos de Gêmeos Digitais voltados para mobilidade inteligente baseada em câmeras/radares (LPR), não existe o conceito explícito de "viagem" com um "Início" e um "Fim". O dado bruto é apenas um *ping* assíncrono.

## 2. Por que essa análise foi feita?
O objetivo desta análise pós-banca é responder cientificamente: *"Por que usamos 45 minutos e o que mudaria estruturalmente na Matriz O-D se usássemos 15, 30, 60 ou 90 minutos?"*

## 3. Explicação da Heurística de Inatividade
O *trade-off* teórico:
- **Sub-segmentação (Janelas longas):** Tende a "fundir" viagens independentes.
- **Super-segmentação (Janelas curtas):** Tende a "estilhaçar" viagens contínuas.

---

## 4. Resultados Extraídos (DuckDB Out-of-Core)

*A tabela abaixo foi gerada automaticamente pelo motor de análise de sensibilidade e reflete os dados reais da última execução.*

| Threshold | Total de Viagens | Duração Média | Duração Mediana | P95 Duração | % O=D | Pares O-D Distintos | Interseção Top 10 | Variação x 45m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 15 min | 2.436.768 | 2.17 min | 0 min | 12 min | 68.3% | 2.517 | 10/10 | +13.69% |
| 30 min | 2.256.844 | 4.12 min | 0 min | 24 min | 64.3% | 2.949 | 10/10 | +5.30% |
| **45 min** | **2.143.327** | **6.33 min** | **0 min** | **37 min** | **62.1%** | **3.039** | **10/10** | **+0.00%** |
| 60 min | 2.057.638 | 8.79 min | 0 min | 52 min | 60.6% | 3.067 | 9/10 | -4.00% |
| 90 min | 1.928.009 | 14.40 min | 0 min | 82 min | 58.5% | 3.093 | 9/10 | -10.05% |

---

## 5. Interpretação e Discussão Automatizada

### Dinâmica das Viagens Curtas e Longas
Como previsto pela teoria de tráfego, janelas curtas sofrem super-segmentação (+13.69% no volume de viagens no limiar de 15 min em relação ao *baseline*). Um achado fundamental desta base é a **Duração Mediana de 0 min**. Isso evidencia que a grande maioria das "viagens" inferidas consiste em detecções isoladas, refletindo a esparsidade da malha de sensores.

### O Threshold de 45 Minutos é Defensável?
**O threshold mostrou-se defensável como compromisso operacional.**
1. **Estabilidade de Rotas Críticas:** O Top 10 corredores (os pares de radares com maior fluxo) demonstra alta estabilidade estrutural (interseção mínima de 9/10 e média de 9.5/10 em relação às demais janelas).
2. **Suavização do Decaimento:** A variação percentual de volume é assintótica. Os 45 minutos atuam como um ponto de compromisso operacional, balanceando a super-fragmentação e a distorção das rotas principais.

## 6. Limitações da Análise
Em prol da honestidade intelectual e rigor acadêmico, as seguintes limitações metodológicas devem ser observadas:
- **Ausência de *Ground Truth*:** Não há dados validados externamente (ex: GPS, apps de navegação) para comprovar categoricamente se as viagens inferidas ocorreram exatamente naqueles minutos. A análise avalia consistência interna.
- **Viés de Sazonalidade:** A validação incidiu apenas sobre a primeira semana de Janeiro (férias escolares). O decaimento de volume pode apresentar formatos diferentes em dias de pico letivo ou chuvas intensas.
- **Mediana 0 min:** O fato da mediana ser sempre 0 evidencia que a grande maioria das "viagens" são pings isolados de radares desconectados, apontando limitações na densidade espacial dos sensores de tráfego de Sorocaba.
- **Não prova valor ótimo:** Esta análise atesta apenas que 45 minutos é metodologicamente estável e seguro; não prova matematicamente ser a "constante universal" ótima da cidade inteligente.

## 7. Próximos Passos
- Estender a inferência cruzando com a velocidade média nos radares.
- Validar em semanas chuvosas ou de pico letivo.
