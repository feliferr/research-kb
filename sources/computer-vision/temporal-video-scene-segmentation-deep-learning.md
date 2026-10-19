---
title: Temporal video scene segmentation using deep-learning
area: computer-vision
kind: paper
url: https://doi.org/10.1007/s11042-020-10450-2
authors: [Tiago Henrique Trojahn, Rudinei Goularte]
year: 2021
status: triaged
priority: 1
effort: 1h
origin: whatsapp
saved: 2024-01-11
tags: [video, scene-segmentation, multimodal-fusion, cnn-rnn, temporal]
related: []
---

> **Resumo:** Propõe uma arquitetura multimodal que combina CNN e RNN para segmentar um vídeo em cenas, buscando capturar dependências temporais entre features de baixo nível que CNNs sozinhas modelam mal.

## Contribuição principal

- Segundo o abstract, os melhores resultados em segmentação temporal de cenas vêm de abordagens multimodais; o trabalho propõe uma fusão antecipada (early fusion) com uma arquitetura que combina CNN e RNN, indo além de aplicar uma RNN diretamente.
- Os autores relatam melhor eficácia do que técnicas relacionadas em um dataset público de vídeo (o nome do dataset não consta no abstract).
- Publicado em Multimedia Tools and Applications (Springer).

## O que dá para replicar ou testar

- Reimplementar a ideia com extratores modernos (features de vídeo e áudio pré-treinadas) e um modelo temporal leve, comparando com a arquitetura CNN+RNN como baseline histórico.

## Por que me interessa

Segmentação de cenas e raciocínio temporal em vídeo; ponto de partida clássico para comparar com abordagens atuais baseadas em embeddings e LLMs.

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** a definir (proposta da triagem).

## Pontos a verificar

- Só o abstract e o início da introdução foram lidos; arquitetura, dataset e números não foram verificados.

## Log

- 2026-10-19: fonte triada a partir do abstract do PDF salvo.
