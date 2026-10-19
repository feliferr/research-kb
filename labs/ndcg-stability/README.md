---
title: Estabilidade do nDCG na avaliação offline de recomendadores
area: recsys
status: in-progress
source: sources/recsys/ndcg-stability-aware-offline-evaluation.md
tags: [evaluation, offline-evaluation, reproducibility, ndcg, movielens]
started: 2026-10-19
---

> **Objetivo (uma frase):** Medir, em um dataset público, quanto o ranking entre três algoritmos de recomendação e as listas recomendadas mudam quando variam a estratégia de divisão e a semente, mesmo com o nDCG@10 parecido.

## Critério de pronto

Uma tabela de estabilidade com, por algoritmo e condição, o nDCG@10; a sobreposição média (Jaccard@10) das listas entre sementes; a correlação de Kendall entre os rankings de algoritmos nas diferentes condições; e um parágrafo dizendo se alguma conclusão "A é melhor que B" muda entre condições. A seção "O que aprendi" preenchida.

## Baseline

A prática típica: uma única condição de referência (divisão aleatória 80/20 por usuário, semente 0) e só o nDCG@10 de cada algoritmo. O lab compara a conclusão tirada dessa condição com a conclusão do painel completo.

## Painel de condições (rascunho, fechar na tarefa 1)

- **Dataset:** MovieLens 100K (GroupLens). URL oficial usada no `run.py`; a verificar se continua válida.
- **Divisões:** aleatória 80/20 por usuário, leave-last-out por usuário e temporal global.
- **Sementes:** 0, 1 e 2 (afetam a divisão aleatória e a inicialização do SVD).
- **Algoritmos:** popularidade, item-kNN (cosseno) e SVD truncado.
- **Métricas:** nDCG@10, Jaccard@10 entre listas, Kendall τ entre rankings de algoritmos.

## Tarefas (cada uma cabe em 1 a 2 horas)

- [ ] 1. Fechar o painel: confirmar dataset, divisões, sementes e algoritmos em `run.py --list-panel`.
- [ ] 2. Implementar carregamento e divisões; rodar os três algoritmos na condição de referência e registrar o nDCG@10.
- [ ] 3. Estender para o painel completo e salvar, por condição, as métricas e as listas top-10.
- [ ] 4. Calcular a estabilidade: variação do nDCG, Jaccard entre sementes e Kendall τ entre rankings de algoritmos.
- [ ] 5. Escrever resultados e "O que aprendi", com a tabela de estabilidade.

Esta semana (2026-W43): tarefas 1 e 2.

## Como rodar

```bash
cd labs/ndcg-stability
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py --list-panel
python run.py --download      # baixa o MovieLens 100K para data/ (ignorado pelo git)
```

## Resultados

Ainda não há medições.

## O que aprendi

Preencher ao concluir.

## Log

- 2026-10-19: lab criado a partir da fonte; status in-progress.
