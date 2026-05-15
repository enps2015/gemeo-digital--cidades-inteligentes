# Plano de Refinamento Pós-Banca v2

**Projeto:** Gêmeos Digitais — Inferência de Fluxos O-D com IA (Sorocaba-SP)
**Data da Banca Original:** 09/05/2026
**Data desta Revisão:** 15/05/2026
**Autoria da Revisão:** Auditoria técnica pós-banca conduzida pelo integrante Eric Pimentel, com assistência de ferramentas de IA generativa (modelo Claude/Antigravity). Nenhum auditor externo, professor ou certificador participou desta revisão.
**Tag da Entrega Original:** `v1-banca-ia-aplicada`

---

> [!IMPORTANT]
> **Premissa de Integridade Histórica**
> A versão entregue à banca em 09/05/2026 está preservada na tag `v1-banca-ia-aplicada`. A branch `main` pode evoluir livremente após a criação dessa tag, desde que o CHANGELOG registre explicitamente a fronteira entre "o que foi entregue" e "o que foi refinado depois". A tag é imutável e funciona como prova documental. A branch `v2-pos-banca-profissional` será utilizada como espaço de trabalho para as melhorias, sendo posteriormente incorporada à `main` via merge documentado.

---

## 1. Correções Aplicadas sobre o Plano v1

O plano v1 (`docs/plano_refinamento_pos_banca.md`) continha imprecisões que, se publicadas, comprometeriam a credibilidade do portfólio. Esta seção documenta o que foi corrigido e por quê.

| #  | Problema no v1                                                                                  | Correção no v2                                                                              | Justificativa                                                                                                                                                                                |
| -- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1 | Afirmava "hash SHA-256 de 64 caracteres" para o campo `Placa` sem verificação programática | Substituído por "campo anonimizado (hash de comprimento fixo), conforme recebido no dataset" | Não foi executada validação criptográfica do algoritmo de hash. Afirmar SHA-256 sem prova é desonesto.                                                                                  |
| C2 | Premissa de que a `main` não pode ser alterada                                               | Corrigido: a `main` pode evoluir; a tag preserva o marco histórico                         | Travar a `main` é impraticável e desnecessário. A tag cumpre a função de preservação.                                                                                               |
| C3 | T06 dizia "Conformidade LGPD"                                                                   | Substituído por "Nota de Privacidade de Dados" com linguagem prudente                        | Conformidade LGPD requer parecer jurídico. O projeto pode apenas declarar as medidas técnicas observadas.                                                                                  |
| C4 | T04 dizia "justificando os 45 min como ponto ótimo"                                            | Substituído por "avaliar o 45 min como ponto de compromisso metodológico"                   | Sem análise de sensibilidade executada, chamar qualquer valor de "ótimo" é afirmação vazia.                                                                                             |
| C5 | `Ruídos/Isolados = 0` no baseline report, mas texto narrativo cita "radares isolados"        | Tarefa dividida: (a) investigar factualmente o valor real; (b) alinhar narrativa ao dado      | O código calcula `(labels == -1).sum()`, que pode ter retornado 0 legitimamente com `eps=2.0km` e `min_samples=2`. Se for isso, o texto narrativo é que está errado, não a tabela. |
| C6 | T02 tratava dataset sample como tarefa única                                                   | Dividido em: sample Gold para visualização + sample sintético para smoke tests             | Propósitos diferentes exigem artefatos diferentes.                                                                                                                                          |
| C7 | T11 (testes) dependia implicitamente dos dados do Google Drive                                  | Corrigido: testes rodam exclusivamente sobre fixtures locais                                  | Teste que depende de recurso externo não é teste.                                                                                                                                          |
| C8 | T13 (renomear imagens) estava como P3 junto com testes e diagrama                               | Rebaixado para tarefa cosmética na Fase 4                                                    | Não é excelência acadêmica. É polimento visual.                                                                                                                                         |

---

## 2. Inventário Factual do Repositório

### 2.1 O Que Está Sólido ✅

| Dimensão                                      | Avaliação | Evidência Verificável                                           |
| ---------------------------------------------- | ----------- | ----------------------------------------------------------------- |
| Pipeline ETL (Raw → Bronze → Silver → Gold) | Sólido     | 4 scripts independentes com separação clara de responsabilidade |
| Processamento Out-of-Core                      | Sólido     | DuckDB + Parquet processando 76M linhas sem OOM                   |
| Heurística de Trip Segmentation               | Funcional   | Window Functions + CUMSUM em `trip_segmentation.py`             |
| Comparativo de Modelos                         | Presente    | Script `compare_models_baseline.py` com 3 algoritmos            |
| Hotsite (GitHub Pages)                         | Funcional   | Layout responsivo Desktop/Mobile com isolamento de iframe         |
| Documentação de Entrega                      | Presente    | 6 relatórios .md + versões PDF + slides                         |

### 2.2 Lacunas Verificadas 🔴

| #   | Lacuna                                                                         | Gravidade | Verificação                                                            |
| --- | ------------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------ |
| L1  | Sem `requirements.txt`                                                       | Alta      | Não existe o arquivo no repositório                                    |
| L2  | Sem dataset sample commitado                                                   | Alta      | Pasta `data/` inteira está no `.gitignore`                          |
| L3  | README contém `📦 desafio1/` e `git clone .../SEU-USUARIO/desafio1.git`   | Média    | Linhas 43 e 77 do README.md                                              |
| L4  | Baseline report:`Ruídos = 0` com texto dizendo "isolou radares como ruído" | Alta      | Linha 9 (tabela) vs Linha 16 (texto) de `baseline_model_comparison.md` |
| L5  | `documentacao_oficial_mvp.md` cita "DBSCAN **ou** K-Means"             | Média    | Linha 47 do arquivo                                                      |
| L6  | Heurística de 45 min sem análise de sensibilidade                            | Média    | Nenhum script ou documento avalia outros thresholds                      |
| L7  | Sem nota de privacidade de dados                                               | Média    | Nenhuma menção a anonimização/pseudonimização no README            |
| L8  | Scripts usam `print()` sem `logging`                                       | Baixa     | Todos os 7 scripts                                                       |
| L9  | Paths hardcoded sem `argparse`                                               | Baixa     | Todos os 7 scripts                                                       |
| L10 | Pasta `prompts/` vazia                                                       | Baixa     | Diretório vazio commitado                                               |
| L11 | Equipe duplicada no README                                                     | Baixa     | Seções 19-21 e 144-152                                                 |
| L12 | Sem testes automatizados                                                       | Média    | Nenhum diretório `tests/`                                             |
| L13 | Typo `smat_cities` (falta o "r" de smart)                                    | Baixa     | 4 arquivos em `img/`                                                   |
| L14 | Sem CHANGELOG.md                                                               | Baixa     | Arquivo inexistente                                                      |
| L15 | Notebook sem cabeçalho ou conexão com pipeline                               | Baixa     | `notebooks/cidades_inteligentes_analises.ipynb`                        |

---

## 3. Tarefas de Refinamento — Organizadas por Fase

### Fase 0 — Segurança Histórica

> Objetivo: Garantir que a versão da banca está preservada de forma auditável e que existe um espaço limpo para trabalhar.

---

#### T00: Verificar e publicar a tag `v1-banca-ia-aplicada`

- **Objetivo:** Confirmar que a tag existe localmente e está publicada no remote. Caso contrário, criá-la no commit exato da entrega.
- **Arquivos afetados:** Nenhum (operação Git pura)
- **Risco:** Nenhum.
- **Esforço:** 5 min
- **Critério de aceite:** `git tag -l` mostra `v1-banca-ia-aplicada`. `git ls-remote --tags origin` confirma presença no remote.

---

#### T01: Criar branch `v2-pos-banca-profissional`

- **Objetivo:** Isolar todo o trabalho de refinamento numa branch dedicada. A main evolui via merge documentado.
- **Arquivos afetados:** Nenhum (operação Git pura)
- **Risco:** Nenhum.
- **Esforço:** 2 min
- **Critério de aceite:** `git branch` mostra `v2-pos-banca-profissional` ativa.

---

### Fase 1 — Verdade Documental

> Objetivo: Eliminar afirmações falsas, ambíguas ou contraditórias na documentação existente. Sem esta fase, o projeto não é publicável como portfólio.

---

#### T02: Investigar e corrigir a contradição `Ruídos = 0` no baseline

- **Objetivo:** O relatório `baseline_model_comparison.md` mostra `Ruídos/Isolados = 0` para o DBSCAN (linha 9), mas o texto narrativo (linha 16) afirma "isolou cientificamente [N] radares como ruído periférico". Uma destas afirmações é falsa. A tarefa é:
  1. Re-executar `compare_models_baseline.py` e capturar o valor real de `(labels == -1).sum()`.
  2. Se o valor real for 0: corrigir o texto narrativo para não afirmar isolamento de ruído que não ocorreu.
  3. Se o valor real for > 0: corrigir a tabela.
- **Arquivos afetados:** `scripts/compare_models_baseline.py` (verificação), `docs/baseline_model_comparison.md`
- **Risco:** Médio. Pode alterar a narrativa de defesa do DBSCAN.
- **Esforço:** 30 min
- **Critério de aceite:** Tabela e texto narrativo 100% coerentes entre si. Valor de ruídos verificado programaticamente e registrado.

> [!CAUTION]
> Se `Ruídos = 0` for factualmente correto (ou seja, com `eps=2.0km` e `min_samples=2`, todos os 61 sensores ficaram dentro de clusters), então o argumento de "capacidade de isolamento de ruído" do DBSCAN deixa de ser uma vantagem *demonstrada* e passa a ser apenas uma *capacidade teórica*. A narrativa de defesa deve ser ajustada para refletir isso com honestidade.

---

#### T03: Resolver ambiguidade "DBSCAN ou K-Means" na documentação MVP

- **Objetivo:** A `documentacao_oficial_mvp.md` (linha 47) cita "DBSCAN ou K-Means Espacial" como se a decisão não estivesse tomada. Na versão pós-banca, a redação deve refletir a decisão final: DBSCAN foi adotado, e um comparativo posterior confirmou a escolha.
- **Arquivos afetados:** `docs/documentacao_oficial_mvp.md`
- **Risco:** Nenhum.
- **Esforço:** 10 min
- **Critério de aceite:** Texto cita DBSCAN como modelo implementado, com nota de rodapé apontando para o baseline comparativo.

---

#### T04: Corrigir referências fantasmas no README

- **Objetivo:** Eliminar:
  - `📦 desafio1/` → `📦 gemeo-digital--cidades-inteligentes/`
  - `git clone .../SEU-USUARIO/desafio1.git` → URL real
  - Adicionar `compare_models_baseline.py` na árvore
  - Remover duplicação da seção de equipe (linhas 144-152)
- **Arquivos afetados:** `README.md`
- **Risco:** Nenhum.
- **Esforço:** 15 min
- **Critério de aceite:** Zero referências a "desafio1" ou "SEU-USUARIO". Árvore de projeto lista todos os scripts existentes.

---

#### T05: Adicionar nota de privacidade de dados (linguagem prudente)

- **Objetivo:** Registrar no README que o campo `Placa` no dataset original contém valores anonimizados (hash de comprimento fixo), conforme disponibilizado pelo órgão fornecedor da base. O pipeline não armazena nem processa dados pessoais identificáveis (PII) em nenhuma camada.
- **Arquivos afetados:** `README.md` (nova seção), `docs/documentacao_oficial_mvp.md` (ajuste pontual)
- **Risco:** Nenhum.
- **Esforço:** 15 min
- **Critério de aceite:** Seção "Privacidade e Tratamento de Dados" presente no README com as seguintes restrições de linguagem:
  - ✅ "O campo `Placa` contém hashes de comprimento fixo, conforme recebido no dataset fornecido"
  - ✅ "O pipeline não armazena nem processa dados pessoais identificáveis"
  - ❌ NÃO afirmar "conformidade plena com a LGPD" (requer parecer jurídico)
  - ❌ NÃO afirmar "SHA-256" sem verificação programática do algoritmo de hash

---

### Fase 2 — Reprodutibilidade

> Objetivo: Permitir que qualquer pessoa clone o repositório e execute pelo menos as visualizações sem depender de recursos externos.

---

#### T06: Criar `requirements.txt` com versões travadas

- **Objetivo:** Exportar as dependências do `.venv` ativo com versões exatas (`==`).
- **Arquivos afetados:** `requirements.txt` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 10 min
- **Critério de aceite:** `pip install -r requirements.txt` em venv limpo instala tudo sem erro. Arquivo contém pelo menos: `duckdb`, `pandas`, `numpy`, `scikit-learn`, `plotly`, `folium`, `tabulate`.

---

#### T07a: Incluir sample da camada Gold para visualizações

- **Objetivo:** Commitar no repositório uma cópia reduzida (~5 MB) dos arquivos Gold (`sensores_clusterizados.parquet` e `matriz_od_macro_zonas.parquet`) e da Matriz O-D Silver, para que `generate_map.py` e `generate_temporal_analysis.py` funcionem sem o Google Drive.
- **Arquivos afetados:** `data/sample/` (NOVO), `.gitignore` (exceção para `data/sample/`), `README.md` (instruções)
- **Risco:** Baixo. Verificar que os Parquets Gold não contêm a coluna `Placa` (sensores e zonas agregadas não contêm PII).
- **Esforço:** 20 min
- **Critério de aceite:** `python scripts/generate_map.py --input data/sample/` produz mapa sem erro. Nenhum hash de veículo presente nos arquivos commitados.

---

#### T07b: Criar sample sintético mínimo para smoke test do pipeline

- **Objetivo:** Gerar um script `scripts/create_test_fixtures.py` que produz um Parquet sintético de ~100 linhas simulando a estrutura Raw/Bronze (com coordenadas fictícias dentro da região de Sorocaba e hashes aleatórios). Esse artefato permite rodar testes e validações sem dados reais.
- **Arquivos afetados:** `scripts/create_test_fixtures.py` (NOVO), `data/fixtures/` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 30 min
- **Critério de aceite:** `python scripts/create_test_fixtures.py` gera `data/fixtures/bronze_fixture.parquet`. Arquivo pesa < 1 MB. Dados são explicitamente fictícios (documentado no cabeçalho do script).

---

### Fase 3 — Rigor Científico

> Objetivo: Blindar as decisões metodológicas com evidência empírica, sem afirmar conclusões antes de executar as análises.

---

#### T08: Análise de sensibilidade da heurística de 45 minutos

- **Objetivo:** Criar um script que varia o threshold de inatividade (15, 30, 45, 60, 90 min) e registra, para cada valor:
  - Número total de viagens extraídas
  - Duração média das viagens
  - Mediana da duração
  - % de viagens com duração < 2 min (indicador de fragmentação)
  - % de viagens com duração > 120 min (indicador de sub-segmentação)
- **Arquivos afetados:** `scripts/sensitivity_analysis.py` (NOVO), `docs/analise_sensibilidade_heuristica.md` (NOVO)
- **Risco:** Nenhum. Aditivo puro.
- **Esforço:** 1h
- **Critério de aceite:**
  - Tabela com os 5 thresholds e as 5 métricas acima
  - ✅ Linguagem: "Os 45 minutos representam um ponto de compromisso metodológico que equilibra fragmentação e sub-segmentação"
  - ❌ NÃO usar: "ponto ótimo", "valor ideal" ou "comprovado matematicamente"
  - Se os dados mostrarem que outro threshold é claramente melhor, documentar isso honestamente

---

#### T09: Adicionar testes automatizados mínimos (sobre fixtures)

- **Objetivo:** Criar `tests/test_pipeline.py` com testes que rodam exclusivamente sobre os fixtures locais (gerados por T07b), nunca dependendo do Google Drive.
- **Testes mínimos:**
  1. Fixture Bronze possui as 9 colunas esperadas com tipos corretos
  2. Trip Segmentation sobre fixture gera `trip_id` sem duplicatas
  3. DBSCAN sobre coordenadas fixture retorna pelo menos 1 cluster não-ruído
- **Arquivos afetados:** `tests/test_pipeline.py` (NOVO), `requirements.txt` (adicionar `pytest`)
- **Risco:** Baixo.
- **Esforço:** 1.5h
- **Critério de aceite:** `pytest tests/ -v` passa com 3/3 green. Nenhum teste acessa rede ou Google Drive.

---

### Fase 4 — Portfólio e Exposição

> Objetivo: Polish final para publicação profissional. Nenhuma destas tarefas altera a substância técnica do projeto.

---

#### T10: Adicionar `CHANGELOG.md`

- **Objetivo:** Registrar cronologicamente as versões, separando claramente:
  - `v1-banca-ia-aplicada` (09/05/2026) — o que foi entregue
  - `v2-pos-banca-profissional` — o que foi refinado depois
- **Arquivos afetados:** `CHANGELOG.md` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 20 min
- **Critério de aceite:** Documento com pelo menos 2 entradas versionadas, sem misturar as duas fases.

---

#### T11: Refatorar scripts com `logging` e `argparse`

- **Objetivo:** Substituir `print()` por `logging` estruturado. Adicionar `argparse` para paths configuráveis.
- **Arquivos afetados:** Todos os 7 scripts em `scripts/`
- **Risco:** Médio. Requer validação manual de regressão.
- **Esforço:** 2h
- **Critério de aceite:** Scripts aceitam `--input` e `--output`. Logs com timestamp. Comportamento default idêntico ao atual (backward compatible).

---

#### T12: Gerar diagrama de arquitetura do pipeline

- **Objetivo:** Diagrama Mermaid mostrando `CSV → Parquet → Bronze → Silver → Gold → Visualização`.
- **Arquivos afetados:** `README.md`
- **Risco:** Nenhum.
- **Esforço:** 30 min
- **Critério de aceite:** Diagrama renderizado no README do GitHub.

---

#### T13: Limpar artefatos órfãos

- **Objetivo:** Remover `prompts/` (vazia). Documentar o notebook como exploração inicial ou removê-lo.
- **Arquivos afetados:** `prompts/` (DELETE), `notebooks/` (avaliar)
- **Risco:** Baixo.
- **Esforço:** 10 min
- **Critério de aceite:** Nenhum diretório vazio. Artefatos justificados no CHANGELOG.

---

#### T14: Corrigir typo nas imagens (`smat_cities` → `smart_cities`)

- **Objetivo:** Renomear imagens e atualizar referências.
- **Arquivos afetados:** `img/smat_cities*.png` (RENAME), `index.html`, `README.md`
- **Risco:** Baixo.
- **Esforço:** 10 min
- **Critério de aceite:** Nenhum arquivo com "smat". Site e README renderizam corretamente.

---

#### T15: Redigir postagem técnica para LinkedIn

- **Objetivo:** Post de portfólio (~800 palavras) descrevendo problema, solução e resultados com métricas concretas e links.
- **Arquivos afetados:** `docs/linkedin_post_draft.md` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 45 min
- **Critério de aceite:**
  - ✅ Métricas verificáveis (76M registros, 2.1M viagens, 3 Macro-Zonas)
  - ✅ Links para GitHub Pages e repositório
  - ✅ Crédito à equipe
  - ❌ NÃO incluir: títulos inflados, credenciais fictícias ou linguagem de "superiority"

---

## 4. Workflow Git

```bash
# Fase 0: Segurança Histórica
git tag v1-banca-ia-aplicada         # Se ainda não existir no remote
git push origin v1-banca-ia-aplicada
git checkout -b v2-pos-banca-profissional

# Fase 1-4: Commits atômicos por tarefa
git commit -m "fix(T02): corrige contradição Ruídos=0 no baseline report"
git commit -m "fix(T03): resolve ambiguidade DBSCAN/K-Means na doc MVP"
git commit -m "fix(T04): corrige referências desatualizadas no README"
git commit -m "feat(T05): adiciona nota de privacidade de dados"
git commit -m "feat(T06): adiciona requirements.txt"
# ... etc

# Finalização
git tag v2-pos-banca-profissional
git checkout main
git merge v2-pos-banca-profissional --no-ff -m "merge: incorpora refinamentos pós-banca v2"
git push origin main --tags
```

---

## 5. Estimativa de Esforço Total

| Fase                               | Tarefas                      | Esforço Estimado   |
| ---------------------------------- | ---------------------------- | ------------------- |
| Fase 0 — Segurança Histórica    | T00, T01                     | ~7 min              |
| Fase 1 — Verdade Documental       | T02, T03, T04, T05           | ~1h 10min           |
| Fase 2 — Reprodutibilidade        | T06, T07a, T07b              | ~1h                 |
| Fase 3 — Rigor Científico        | T08, T09                     | ~2h 30min           |
| Fase 4 — Portfólio e Exposição | T10, T11, T12, T13, T14, T15 | ~3h 55min           |
| **TOTAL**                    | **16 tarefas**         | **~8h 42min** |

---

## 6. Declaração de Limitações Conhecidas

Este plano reconhece explicitamente as seguintes limitações do projeto que **não serão corrigidas** nesta versão, mas devem ser declaradas com transparência:

1. **Amostragem Temporal:** A Matriz O-D foi construída sobre a 1ª semana de janeiro/2026 (7 dias). Não há validação cruzada com outras semanas ou meses. Generalizações devem ser feitas com cautela.
2. **Granularidade dos Sensores:** O DBSCAN clusteriza 61 pontos fixos (sensores). A resolução espacial é limitada pela densidade da malha de radares, não pela capacidade do algoritmo.
3. **Heurística de 45 min:** Adotada com base em literatura de mobilidade urbana, mas sem calibração empírica específica para Sorocaba. A análise de sensibilidade (T08) visa documentar, não necessariamente validar, esta escolha.
4. **Silhouette Score:** O valor de 0.31 indica separação moderada. Não é "excelente" nem "ruim". É um resultado típico para dados geoespaciais urbanos onde as fronteiras entre clusters são naturalmente difusas.

---

> [!WARNING]
> Este plano substitui integralmente o `plano_refinamento_pos_banca.md` (v1). O documento v1 continha imprecisões documentadas na Seção 1 acima e não deve ser utilizado como referência de execução.

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
