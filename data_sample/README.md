# Diretório de Dados de Amostra (Sample Data)

> **⚠️ AVISO IMPORTANTE SOBRE PRIVACIDADE E VOLUME DE DADOS**
> A base de dados original do projeto ("DADOS_SOROCABA_JANEIRO_A_ABRIL_2026.parquet") possui mais de 5GB e contém hashes identificadores de placas de veículos.
> Por restrições de volume (limites do GitHub) e por princípios rígidos de **Privacidade e Proteção de Dados**, os dados reais **NÃO SÃO VERSIONADOS** neste repositório.

Este diretório (`data_sample/`) destina-se exclusivamente a armazenar **dados sintéticos ou amostrais descaracterizados**, gerados mecanicamente para fins de *Smoke Test*.

## Uso para Avaliação
Se você é um avaliador, recrutador ou professor e deseja testar a execução do pipeline de dados na sua máquina sem baixar os 5GB originais:
1. Siga as instruções em `docs/reprodutibilidade.md`.
2. O script `scripts/generate_demo_data.py` criará arquivos fictícios.
3. Estes dados sintéticos servem **apenas para validar se o código executa de ponta a ponta sem erros de dependência**, garantindo a qualidade de software do pipeline. No entanto, os mapas, dashboards e clusters resultantes **não terão significado analítico real**.
