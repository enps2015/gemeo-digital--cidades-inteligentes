# Changelog

Todas as alterações relevantes deste projeto são documentadas neste arquivo.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [v2-pos-banca-profissional] — Em andamento

Refinamento técnico e documental conduzido **após** a defesa em banca.
Nenhuma alteração nesta seção existia na versão entregue à banca.

### Corrigido

- README: referências desatualizadas (`desafio1/`, `SEU-USUARIO`) substituídas pelos nomes reais do repositório
- README: seção de equipe duplicada removida
- README: linguagem promocional substituída por redação técnica factual
- `docs/baseline_model_comparison.md`: narrativa sobre isolamento de ruídos pelo DBSCAN alinhada ao dado factual (`Ruídos = 0`)
- `docs/documentacao_oficial_mvp.md`: ambiguidade "DBSCAN ou K-Means" resolvida — texto reflete a decisão final pelo DBSCAN

### Adicionado

- `CHANGELOG.md`: este arquivo, separando explicitamente o que foi entregue à banca do que foi refinado depois
- README: seção "Privacidade e Tratamento de Dados"
- README: seção "Limitações Conhecidas"
- README: seção "Versão de banca vs. refinamento pós-banca"
- `requirements.txt` para ambiente virtual controlável
- Guia oficial de reprodutibilidade (`docs/reprodutibilidade.md`)
- Diretório `data_sample/` isolado para prevenção de perda de dados originais
- Gerador de dados sintéticos para smoke test (`scripts/generate_demo_data.py`)
- Exportação local dinâmica de estatísticas em `data/stats.js`
- Hotsite (`index.html`) dinâmico reagindo ativamente à base de dados processada

---

## [v1-banca-ia-aplicada] — 2026-05-09

Versão entregue e defendida na banca da Residência em Gêmeo Digital em 5G (Facens).
**Esta versão está preservada integralmente na tag Git `v1-banca-ia-aplicada`.**

### Entregue

- Pipeline ETL completo: Raw → Bronze → Silver → Gold (4 camadas)
- Processamento out-of-core de 76M registros via DuckDB + Parquet
- Heurística de segmentação de viagens (janela de inatividade de 45 min)
- Clusterização espacial DBSCAN (3 Macro-Zonas, Silhouette Score 0.3134)
- Mapa geoespacial interativo (Folium)
- Dashboard temporal interativo (Plotly)
- Hotsite/portfólio em GitHub Pages (`index.html`)
- Comparativo de modelos baseline (`compare_models_baseline.py`)
- Documentação técnica: 6 relatórios .md + versões PDF + apresentação
