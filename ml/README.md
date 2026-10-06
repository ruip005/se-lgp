# ml/

Treino e avaliação dos classificadores.

- Os dados vêm de `data/` (CSVs de landmarks gerados pelo script de recolha — nunca imagens).
- Avaliação **sempre por pessoa** (`sklearn.model_selection.LeaveOneGroupOut`), nunca split aleatório por amostra.
- Modelos treinados vão para `models/` (fora do Git) e as métricas para o Notion.
