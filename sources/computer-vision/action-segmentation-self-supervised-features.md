---
title: Action Segmentation Through Self-Supervised Video Features and Positional-Encoded Embeddings
area: computer-vision
kind: paper
authors: [Guilherme de A. P. Marques et al.]
status: triaged
priority: 1
effort: weekend
origin: whatsapp
saved: 2024-02-26
tags: [video, action-segmentation, self-supervised, dino, clustering, unsupervised]
related: []
---

> **Resumo:** Método de segmentação de ações em vídeo sem análise inicial e sem dados anotados: extrai features de modelos pré-treinados, aplica codificação posicional e agrupa com um algoritmo de clustering, supondo que cada cluster corresponda a uma ação distinguível.

## Contribuição principal

- Features avaliadas: DINO (auto-supervisionado) e I3D e SlowFast (espaço-temporais). Clustering: FINCH e KMeans. Também estuda o efeito do tamanho dos trechos de vídeo usados para gerar os vetores de features.
- Segundo o abstract, os resultados são competitivos nos benchmarks Breakfast e INRIA Instructional Videos; o melhor resultado usa features DINO, clustering FINCH e codificação posicional.

## O que dá para replicar ou testar

- Pipeline pequeno e barato: DINO + codificação posicional + FINCH em um subconjunto do Breakfast, medindo a qualidade da segmentação e o efeito do tamanho do trecho.
- Extensão natural: trocar DINO por features de modelos de vídeo recentes (ver a nota do VideoMAE V2 e V-JEPA).

## Por que me interessa

Segmentação temporal sem supervisão é uma base para captioning denso e raciocínio temporal em vídeo, com um pipeline simples de reproduzir.

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** fim de semana, 1 GPU (proposta da triagem).

## Pontos a verificar

- Link público e ano de publicação não constam no PDF salvo (a verificar); só o abstract e a introdução foram lidos.

## Log

- 2026-10-19: fonte triada a partir do abstract do PDF salvo.
