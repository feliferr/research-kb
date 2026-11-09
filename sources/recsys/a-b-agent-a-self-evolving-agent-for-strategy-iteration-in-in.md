---
title: "A/B Agent: A Self-Evolving Agent for Strategy Iteration in Industrial A/B Testing"
area: recsys
kind: paper
authors: [Zhuohang Jiang, Yuxin Chen, Yongsen Pan, Boyang Xia, Zheng Hu, Wenqi Fan, Li Qing, Hongyang Wang, Jun Wang, Zhongbo Sun, Wenwu Ou]
year: 2026
priority: 2
effort: weekend
tags: [agents, rag, ab-testing, recommender-systems, self-evolving]
related: []
url: https://arxiv.org/abs/2608.04625
saved: 2026-11-09
origin: telegram
status: triaged
---

> **Resumo:** O paper propõe um agente em ciclo fechado que organiza estratégias de experimentos A/B passados numa árvore hierárquica de experiência, usa Tree-RAG multi-caminho para gerar novas estratégias de recomendação e atualiza a árvore com o feedback online. Os autores relatam ganho de GMV em um sistema real de e-commerce com vídeos curtos; só o abstract da página arXiv foi lido, não o PDF.

## Contribuição principal

Segundo o abstract: (1) uma árvore de experiência que estrutura estratégias históricas por cenário de negócio, estágio de recomendação, objetivo e contexto experimental, em vez de um armazenamento plano; (2) Tree-RAG multi-caminho para recuperar evidências transferíveis e gerar estratégias executáveis; (3) um laço de auto-evolução que usa resultados de A/B online para ajustar estratégias e atualizar a árvore.

## O que dá para replicar ou testar

Nada direto: a avaliação parece depender de um sistema industrial de recomendação. Um experimento pequeno seria comparar RAG plano com recuperação hierárquica sobre um log sintético de experimentos.

## Por que me interessa

Mostra como estruturar memória de experimentos para agentes que iteram sobre decisões de produto.

## Estimativa de esforço

- **Leitura:** 1h30 (a verificar, o PDF não foi lido)
- **Protótipo:** fim de semana, sem GPU, com dados sintéticos

## Pontos a verificar

- (a verificar) Detalhes de método, baselines e metodologia da avaliação offline: só o abstract foi lido.
- (a verificar) O ganho de 4,829% de GMV e os resultados positivos em métricas guardrail são relatados pelos autores; não foram confirmados no corpo do paper.
- (a verificar) Se há código ou dados públicos.
- Sem duplicata encontrada em `sources/`.

## Log

- 2026-11-09: fonte triada (automático, via Telegram).
