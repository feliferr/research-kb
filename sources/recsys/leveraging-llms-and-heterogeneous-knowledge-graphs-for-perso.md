---
title: Leveraging LLMs and Heterogeneous Knowledge Graphs for Persona-Driven Session-Based Recommendation
area: recsys
kind: paper
authors: [Muskan Gupta, Suraj Thapa, Jyotsana Khatri]
year: 2026
priority: 2
effort: weekend
tags: [session-based-recommendation, knowledge-graph, llm-embeddings, personas, reranking]
related: []
url: https://arxiv.org/abs/2604.06928
saved: 2026-11-08
origin: telegram
status: triaged
---

> **Resumo:** O paper propõe inferir personas latentes de usuários a partir de um grafo de conhecimento heterogêneo (com embeddings de itens gerados por LLM) e usá-las para melhorar recomendação baseada em sessões anônimas. Segundo o abstract, há ganhos consistentes sobre modelos sequenciais em Amazon Books e Amazon Movies & TV; só o abstract foi lido, não o texto completo.

## Contribuição principal

Em dois estágios: (1) constrói um grafo com interações usuário-item, relações item-item, item-atributo e metadados da DBpedia, e aprende personas de forma não supervisionada com Heterogeneous Deep Graph Infomax, partindo de embeddings de itens gerados por LLM; (2) combina personas e embeddings em um recomendador modificado que gera candidatos, depois reranqueados por um modelo sequencial base para focar na intenção da sessão atual.

## O que dá para replicar ou testar

Reproduzir em escala pequena num subconjunto público do Amazon (Books ou Movies & TV): comparar um baseline sequencial (ex.: GRU4Rec/SASRec) com e sem embeddings de persona, e uma ablação trocando embeddings de LLM por embeddings aleatórios ou de ID.

## Por que me interessa

Mostra como combinar LLMs com estrutura relacional para personalização quando há pouco histórico do usuário.

## Estimativa de esforço

- **Leitura:** ~1h (abstract, método e tabela de resultados)
- **Protótipo:** fim de semana, uma GPU modesta

## Pontos a verificar

- (a verificar) detalhes do método, hiperparâmetros, baselines e métricas: apenas o abstract foi lido.
- (a verificar) magnitude dos ganhos e se há código público.

## Log

- 2026-11-08: fonte triada (automático, via Telegram).
