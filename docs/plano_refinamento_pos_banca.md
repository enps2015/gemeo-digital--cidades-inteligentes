# Plano de Refinamento Pós-Banca — v2-pos-banca-profissional

**Projeto:** Gêmeos Digitais — Inferência de Fluxos O-D com IA (Sorocaba-SP)
**Data da Banca Original:** 09/05/2026
**Data da Auditoria:** 14/05/2026
**Auditor:** Auditoria pós-banca conduzida por Eric Pimentel com apoio de ferramentas de IA generativa.
**Tag da Entrega Original:** `v1-banca-ia-aplicada`

---

> [!IMPORTANT]
> **Premissa Inviolável:** Nenhuma alteração deve ser feita na branch `main` com o objetivo de "reescrever a história" da entrega original. O código que foi à banca está cristalizado na tag `v1-banca-ia-aplicada`. Todas as melhorias propostas neste documento devem ser implementadas na branch `v2-pos-banca-profissional`.

---

## 1. Sumário Executivo da Auditoria

### 1.1 O Que Está Sólido ✅

| Dimensão                                      | Avaliação | Evidência                                                     |
| ---------------------------------------------- | ----------- | -------------------------------------------------------------- |
| Pipeline ETL (Raw → Bronze → Silver → Gold) | Excelente   | 4 camadas claramente delimitadas em scripts independentes      |
| Uso de DuckDB + Parquet                        | Excelente   | Processamento Out-of-Core de 76M linhas em ~14s                |
| Heurística de Trip Segmentation (45 min)      | Boa         | Implementada via Window Functions com lógica de CUMSUM        |
| Escolha do DBSCAN                              | Boa         | Comparativo com K-Means/Agglomerative já documentado          |
| Hotsite (GitHub Pages)                         | Muito Bom   | Responsivo (Desktop 2x2 / Mobile 3x1), dark theme profissional |
| Documentação de Entrega                      | Boa         | 6 relatórios .md + versões PDF                               |
| Apresentação                                 | Entregue    | Slides .pptx e .pdf com QR Code para o site                    |

### 1.2 Lacunas Identificadas 🔴

| #   | Lacuna                                                                            | Gravidade | Impacto                                                          |
| --- | --------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------- |
| L1  | Ausência de `requirements.txt` ou `pyproject.toml`                           | Alta      | Impossível reproduzir o ambiente                                |
| L2  | Ausência de dataset sample no repositório                                       | Alta      | Ninguém pode executar o pipeline sem o Drive                    |
| L3  | README com referências desatualizadas (`desafio1/`, `SEU-USUARIO`)           | Média    | Credibilidade profissional comprometida                          |
| L4  | Nenhum script possui `logging` estruturado                                      | Média    | Prints soltos não são auditáveis em produção                |
| L5  | Hardcoded paths nos scripts (sem `argparse` ou config)                          | Média    | Dificulta portabilidade e CI/CD                                  |
| L6  | Heurística de 45 min sem análise de sensibilidade                               | Média    | Decisão técnica não blindada contra questionamento acadêmico |
| L7  | Baseline report com `Ruídos/Isolados = 0` para DBSCAN                          | Alta      | Contradiz o texto narrativo que cita "radares isolados"          |
| L8  | Sem nota de LGPD/Privacidade no README ou docs                                    | Média    | Risco regulatório em portfólio público                        |
| L9  | Pasta `prompts/` vazia no repositório                                          | Baixa     | Poluição de estrutura                                          |
| L10 | Sem testes automatizados (nem unitários, nem de integração)                    | Alta      | Zero garantia de não-regressão                                 |
| L11 | Notebook `cidades_inteligentes_analises.ipynb` sem contexto                     | Baixa     | Artefato solto, sem link com o pipeline principal                |
| L12 | Equipe duplicada no README (seções 19-21 e 144-152)                             | Baixa     | Redundância visual                                              |
| L13 | Imagem nomeada `smat_cities` (typo: "smart")                                    | Baixa     | Falta de polish em portfólio                                    |
| L14 | Sem `CHANGELOG.md` ou `CONTRIBUTING.md`                                       | Baixa     | Padrão OSS não atendido                                        |
| L15 | Documentação `documentacao_oficial_mvp.md` cita "DBSCAN **ou** K-Means" | Média    | Ambiguidade na decisão arquitetural final                       |

---

## 2. Tarefas de Refinamento

### Prioridade P0 — Reprodutibilidade (Crítico)

---

#### T01: Criar `requirements.txt`

- **Objetivo:** Permitir que qualquer pessoa reproduza o ambiente Python com um único comando.
- **Arquivos afetados:** `requirements.txt` (NOVO)
- **Risco:** Nenhum. Aditivo puro.
- **Esforço:** 10 min
- **Critério de aceite:** `pip install -r requirements.txt` instala todas as dependências sem erro. Versões travadas (`==`).

---

#### T02: Incluir dataset sample no repositório

- **Objetivo:** Disponibilizar uma amostra mínima (~5 MB) dos dados Gold no próprio repositório, permitindo que os scripts de visualização (`generate_map.py`, `generate_temporal_analysis.py`) rodem sem acesso ao Google Drive.
- **Arquivos afetados:** `data/sample/` (NOVO), scripts de visualização (apontar para sample como fallback)
- **Risco:** Baixo. Garantir que nenhum hash de placa real vaze na amostra.
- **Esforço:** 30 min
- **Critério de aceite:** `python scripts/generate_map.py` roda com sucesso usando apenas os arquivos commitados no repositório. README atualizado com instruções.

---

#### T03: Corrigir inconsistência no Baseline Report (Ruídos = 0)

- **Objetivo:** O relatório `baseline_model_comparison.md` mostra `Ruídos/Isolados = 0` para o DBSCAN, enquanto o texto narrativo do mesmo documento e do README cita "radares periféricos isolados". Isso é uma contradição factual que destruiria a credibilidade numa revisão técnica.
- **Arquivos afetados:** `scripts/compare_models_baseline.py`, `docs/baseline_model_comparison.md`
- **Risco:** Médio. Requer re-execução do script com os dados.
- **Esforço:** 30 min
- **Critério de aceite:** A coluna "Ruídos/Isolados" do DBSCAN reflete o valor real retornado pelo modelo. Texto narrativo coerente com a tabela.

---

### Prioridade P1 — Rigor Metodológico

---

#### T04: Análise de Sensibilidade da Heurística de 45 minutos

- **Objetivo:** Criar um script que varia o threshold de inatividade (15, 30, 45, 60, 90 min) e registra o impacto no número de viagens e na duração média. Isso blinda a decisão contra questionamento acadêmico.
- **Arquivos afetados:** `scripts/sensitivity_analysis.py` (NOVO), `docs/analise_sensibilidade_heuristica.md` (NOVO)
- **Risco:** Nenhum. Aditivo.
- **Esforço:** 1h
- **Critério de aceite:** Tabela mostrando a relação threshold × nº viagens × duração média. Gráfico de cotovelo (elbow) justificando os 45 min como ponto ótimo.

---

#### T05: Resolver ambiguidade "DBSCAN ou K-Means" na documentação MVP

- **Objetivo:** A `documentacao_oficial_mvp.md` (Seção 5, Passo 2) cita "DBSCAN ou K-Means Espacial", como se a decisão não tivesse sido tomada. Na versão profissional, a redação deve refletir a escolha final consolidada.
- **Arquivos afetados:** `docs/documentacao_oficial_mvp.md`
- **Risco:** Nenhum.
- **Esforço:** 10 min
- **Critério de aceite:** Texto unificado citando exclusivamente o DBSCAN como modelo adotado, com referência ao baseline comparativo.

---

#### T06: Adicionar nota de LGPD e Privacidade de Dados

- **Objetivo:** Registrar formalmente que os dados de placas foram previamente anonimizados (hash SHA-256 de 64 caracteres) pelo órgão fornecedor, e que nenhum dado pessoal identificável (PII) transita pelo pipeline.
- **Arquivos afetados:** `README.md` (nova seção), `docs/documentacao_oficial_mvp.md`
- **Risco:** Nenhum. Essencial para portfólio público e LinkedIn.
- **Esforço:** 15 min
- **Critério de aceite:** Seção "Privacidade e Conformidade LGPD" presente no README com declaração explícita do tratamento de anonimização.

---

### Prioridade P2 — Qualidade de Código e Portfólio

---

#### T07: Refatorar scripts com `logging` e `argparse`

- **Objetivo:** Substituir `print()` por `logging.info()` / `logging.error()` em todos os 7 scripts. Adicionar `argparse` para que os caminhos de entrada/saída sejam configuráveis via CLI.
- **Arquivos afetados:** Todos os 7 scripts em `scripts/`
- **Risco:** Médio. Requer testes manuais de regressão.
- **Esforço:** 2h
- **Critério de aceite:** Cada script aceita `--input` e `--output` como argumentos opcionais. Logs com timestamp e nível (INFO/ERROR/WARNING).

---

#### T08: Corrigir README (referências desatualizadas)

- **Objetivo:** Eliminar referências fantasmas: `📦 desafio1/` → `📦 gemeo-digital--cidades-inteligentes/`, `github.com/SEU-USUARIO/desafio1.git` → URL real do repositório. Remover duplicação da seção de equipe. Adicionar o `compare_models_baseline.py` na árvore de estrutura.
- **Arquivos afetados:** `README.md`
- **Risco:** Nenhum.
- **Esforço:** 15 min
- **Critério de aceite:** Zero referências a "desafio1" ou "SEU-USUARIO". Árvore de projeto reflete 100% dos arquivos reais.

---

#### T09: Adicionar `CHANGELOG.md`

- **Objetivo:** Registrar cronologicamente as versões e decisões do projeto.
- **Arquivos afetados:** `CHANGELOG.md` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 20 min
- **Critério de aceite:** Entradas para `v1-banca-ia-aplicada` (09/05/2026) e `v2-pos-banca-profissional`.

---

#### T10: Limpar artefatos órfãos

- **Objetivo:** Remover a pasta `prompts/` (vazia) e avaliar o notebook `cidades_inteligentes_analises.ipynb` — documentá-lo como exploração inicial ou removê-lo.
- **Arquivos afetados:** `prompts/` (DELETE), `notebooks/cidades_inteligentes_analises.ipynb` (avaliar)
- **Risco:** Baixo.
- **Esforço:** 10 min
- **Critério de aceite:** Nenhum diretório vazio. Notebook com cabeçalho descritivo ou removido com justificativa no CHANGELOG.

---

### Prioridade P3 — Excelência e Blindagem Acadêmica

---

#### T11: Adicionar testes automatizados mínimos

- **Objetivo:** Criar `tests/test_pipeline.py` com pelo menos 3 testes: (1) validar que o schema do Parquet Bronze possui as colunas esperadas; (2) validar que a Matriz O-D não contém `trip_id` duplicados; (3) validar que o DBSCAN retorna ≥ 2 clusters não-ruído.
- **Arquivos afetados:** `tests/test_pipeline.py` (NOVO), `requirements.txt` (adicionar `pytest`)
- **Risco:** Baixo.
- **Esforço:** 1.5h
- **Critério de aceite:** `pytest tests/` passa com 3/3 green.

---

#### T12: Gerar diagrama de arquitetura do pipeline

- **Objetivo:** Criar um diagrama Mermaid (ou imagem) mostrando o fluxo `CSV → Parquet → Bronze → Silver → Gold → Visualização`, com as ferramentas em cada camada. Embed no README.
- **Arquivos afetados:** `README.md`, `img/diagrama_pipeline.png` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 30 min
- **Critério de aceite:** Diagrama renderizado no README do GitHub.

---

#### T13: Corrigir typo nas imagens (`smat_cities` → `smart_cities`)

- **Objetivo:** Renomear os arquivos de imagem para eliminar o typo "smat". Atualizar referências no `index.html` e `README.md`.
- **Arquivos afetados:** `img/smat_cities*.png` (RENAME), `index.html`, `README.md`
- **Risco:** Baixo. Requer atualização de referências em 2 arquivos.
- **Esforço:** 10 min
- **Critério de aceite:** Nenhum arquivo contém "smat" no nome. Site e README renderizam as imagens corretamente.

---

#### T14: Criar postagem técnica para LinkedIn

- **Objetivo:** Redigir um post técnico de portfólio (~800 palavras) descrevendo o problema, a solução e os resultados. Incluir screenshots do mapa e do dashboard.
- **Arquivos afetados:** `docs/linkedin_post_draft.md` (NOVO)
- **Risco:** Nenhum.
- **Esforço:** 45 min
- **Critério de aceite:** Post revisado, com métricas concretas (76M registros, 2.1M viagens, 3 Macro-Zonas), links para o GitHub Pages e repositório.

---

## 3. Ordem de Execução Recomendada

```text
Fase 1 (P0 — Reprodutibilidade)     → T01 → T02 → T03 → T08
Fase 2 (P1 — Rigor Metodológico)    → T04 → T05 → T06
Fase 3 (P2 — Qualidade de Código)   → T07 → T09 → T10
Fase 4 (P3 — Blindagem Acadêmica)   → T11 → T12 → T13 → T14
```

---

## 4. Workflow Git Proposto

```bash
# 1. Criar a branch de trabalho a partir da main atual
git checkout main
git checkout -b v2-pos-banca-profissional

# 2. Implementar as tarefas em commits atômicos
git commit -m "feat(T01): adiciona requirements.txt com versões travadas"
git commit -m "feat(T02): inclui dataset sample Gold no repositório"
# ... (um commit por tarefa)

# 3. Ao finalizar, criar a tag profissional
git tag v2-pos-banca-profissional

# 4. Push da branch e da tag
git push origin v2-pos-banca-profissional
git push origin v2-pos-banca-profissional --tags
```

---

## 5. Estimativa de Esforço Total

| Prioridade       | Tarefas              | Esforço Estimado   |
| ---------------- | -------------------- | ------------------- |
| P0 (Crítico)    | T01, T02, T03, T08   | ~1h 25min           |
| P1 (Rigor)       | T04, T05, T06        | ~1h 25min           |
| P2 (Qualidade)   | T07, T09, T10        | ~2h 30min           |
| P3 (Excelência) | T11, T12, T13, T14   | ~2h 55min           |
| **TOTAL**  | **14 tarefas** | **~8h 15min** |

---

> [!TIP]
> As tarefas P0 e P1 são suficientes para transformar este projeto em um portfólio de nível profissional publicável no LinkedIn. As tarefas P2 e P3 elevam-no para padrão de repositório open-source auditável.

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
