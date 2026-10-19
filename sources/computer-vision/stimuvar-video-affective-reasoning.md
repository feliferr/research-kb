---
title: StimuVAR: Spatiotemporal Stimuli-aware Video Affective Reasoning with MLLMs
area: computer-vision
kind: paper
url: https://arxiv.org/abs/2409.00304
authors: [Yuxiang Guo, Faizan Siddiqui, Yang Zhao, Rama Chellappa, Shao-Yuan Lo]
year: 2024
status: triaged
priority: 2
effort: 1h
origin: whatsapp
saved: 2024-11-27
tags: [video, mllm, affective-reasoning, frame-sampling, token-selection]
related: []
---

> **Resumo:** Framework para raciocínio afetivo sobre vídeo com modelos de linguagem multimodais, que prevê como um vídeo faz o espectador se sentir e explica por quê, direcionando a atenção do modelo para eventos e regiões que provocam emoção.

## Contribuição principal

- Mecanismo em dois níveis: consciência no nível do quadro (amostragem de quadros dirigida por eventos, em vez de amostragem uniforme) e no nível do token (seleção de tubos no espaço de tokens para concentrar o MLLM em regiões espaço-temporais que disparam emoção).
- Dados de instrução para treino afetivo (VAR) e um protocolo de avaliação com várias métricas.
- Segundo o abstract, é o primeiro método baseado em MLLM para raciocínio afetivo centrado no espectador.

## O que dá para replicar ou testar

- Isolar a amostragem de quadros dirigida por eventos: comparar amostragem uniforme com amostragem por eventos como pré-processamento de um MLLM aberto em uma tarefa de perguntas sobre vídeo curto.

## Por que me interessa

A amostragem de quadros orientada por eventos é uma técnica geral para vídeo + MLLM, útil além do domínio afetivo (VideoQA e captioning).

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** fim de semana (proposta da triagem).

## Pontos a verificar

- Só o abstract e a introdução foram lidos; resultados e baselines não foram verificados.

## Log

- 2026-10-19: fonte triada a partir do abstract do PDF salvo.
