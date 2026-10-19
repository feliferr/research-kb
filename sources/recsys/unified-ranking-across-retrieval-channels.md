---
title: Unified Ranking Across Retrieval Channels: A Large-Scale E-Commerce Approach
area: recsys
kind: paper
url: https://usrw-workshop.github.io/2026/papers/206-unified-ranking-across-retrieval-channels-a-large-scale-e-commerce-approach.pdf
authors: [Aditya Gaydhani et al.]
year: 2026
status: triaged
priority: 2
effort: weekend
origin: whatsapp
saved: 2026-10-09
tags: [learning-to-rank, retrieval, e-commerce, fusion]
related: []
---

> **Resumo:** Troca a fusão estática de canais de recuperação (Weighted Interleaving) por um reranker de learning-to-rank sensível ao canal, que recebe os candidatos de todos os canais com o score de cada um e features de comportamento consulta-item.

## Contribuição principal

- Modelo GBDT treinado com LambdaMART sobre um rótulo semanal que combina cliques, adições ao carrinho e compras, ponderados pelo funil de conversão.
- Em produção, com latência p95 de reranking abaixo de 50 ms (conforme o paper).
- Resultados reportados pelos autores (conferir no original): NDCG@8 offline de 0,6620 (controle WI) para 0,7994 (variante completa); no teste A/B de duas semanas, conversão +2,85% e adição ao carrinho +2,81%, ambos significativos a 95%.
- Limitações declaradas: sem garantias de exposição por canal, sem personalização individual, coeficientes do rótulo definidos heuristicamente, dados privados de um único varejista, e queda de CTR em consultas torso e tail para o modelo completo.

## O que dá para replicar ou testar

- Reproduzir a ideia em um dataset público de learning-to-rank (a verificar qual), simulando os "canais" como scores de retrievers distintos, com LightGBM em modo lambdarank.
- O paper cita RRF mas não o avalia: comparar o reranker contra RRF e interleaving é um experimento pequeno e informativo (sugestão da triagem).

## Por que me interessa

Fusão de múltiplos retrievers é um problema recorrente em sistemas de recomendação e busca; o paper traz números de produção e limitações explícitas.

## Estimativa de esforço

- **Leitura:** 30 min.
- **Protótipo:** fim de semana, sem GPU (proposta da triagem).

## Pontos a verificar

- Tabela e números vêm de um resumo da página; conferir no PDF.

## Log

- 2026-10-19: fonte triada.
