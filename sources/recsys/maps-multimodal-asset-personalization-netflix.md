---
title: MAPS: Netflix's Multimodal Asset Personalization at Scale
area: recsys
kind: blog
url: https://netflixtechblog.com/maps-netflixs-multimodal-asset-personalization-at-scale-32f96320785e
authors: [Emma Yanyang Kong et al.]
year: 2026
status: triaged
priority: 1
effort: 1h
origin: whatsapp
saved: 2026-09-01
tags: [multimodal, cold-start, embeddings, clip, personalization]
related: []
---

> **Resumo:** Como embeddings multimodais permitem que modelos de recomendação de assets (artes de capa e prévias em vídeo) considerem o conteúdo visual, sonoro e textual, atacando o cold start de títulos novos.

## Contribuição principal

- Três sistemas em produção: personalização de artes, ranqueamento de artes sensível à busca e personalização de prévias em vídeo.
- Artes: embedding CLIP concatenado ao ID aprendido do asset, passado por uma camada MLP; um modelo único substitui cinco modelos por canvas; exemplos ponderados pelo valor de longo prazo da interação.
- Prévias: um modelo fundacional multimodal por shot (MediaFM) que funde sinais visuais, de áudio e de legenda.
- Método barato de seleção: uma tarefa proxy com sonda linear sobre o embedding, usada para filtrar candidatos antes de testes A/B completos.
- Resultado qualitativo do post: a ordem MediaFM > SeqCLIP > apenas IDs aparece nos dados offline, online e na sonda linear. Os números do post são, em sua maioria, relativos.

## O que dá para replicar ou testar

- A tarefa proxy: avaliar embeddings candidatos com uma sonda linear em uma tarefa barata antes de treinar o recomendador completo, em um dataset público com imagens (a definir).

## Por que me interessa

Recomendação multimodal com cold start e uma metodologia de seleção de embeddings que economiza testes online.

## Estimativa de esforço

- **Leitura:** 30 min.
- **Protótipo:** fim de semana (proposta da triagem).

## Pontos a verificar

- É um post de blog: faltam hiperparâmetros, tamanhos de dados e vários valores; resultados da própria empresa, sem replicação independente.

## Log

- 2026-10-19: fonte triada.
