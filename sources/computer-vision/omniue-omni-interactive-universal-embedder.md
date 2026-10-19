---
title: Omni-Interactive Universal Embedder (OmniUE)
area: computer-vision
kind: paper
url: https://arxiv.org/abs/2608.27044
authors: [Wei-Yao Wang et al.]
year: 2026
status: triaged
priority: 1
effort: 1h
origin: whatsapp
saved: 2026-09-27
tags: [embeddings, audio-visual, video-retrieval, omni-llm, multimodal]
related: []
---

> **Resumo:** Embedder universal para texto, vídeo e áudio em que o usuário consulta com texto, regiões de interesse visuais e trechos de áudio; segmentadores processam essas interações e as integram a um omni-LLM, que produz embeddings condicionados ao usuário.

## Contribuição principal

- Representações de camadas intermediárias extraídas por tokens treináveis dedicados.
- Segundo o abstract, é o primeiro embedder universal omni-interativo.
- Avaliação citada: MMEB-v2-video, MAEB (áudio), SCaR (interação visual) e o OmniCHOIR, proposto pelos autores para recuperação composicional de áudio com interações omnimodais.

## O que dá para replicar ou testar

Não foi encontrado link de código na página; qualquer protótipo depende de liberação. Alternativa: medir o ganho de consultas interativas (região de interesse) sobre um embedder de vídeo-texto aberto em um subconjunto de recuperação de vídeo.

## Por que me interessa

Fusão audiovisual e recuperação de vídeo condicionada por interação são temas diretos de vídeo multimodal.

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** indefinido sem código (proposta da triagem).

## Pontos a verificar

- Apenas o abstract foi lido; arquitetura e resultados não foram verificados.

## Log

- 2026-10-19: fonte triada a partir do abstract.
