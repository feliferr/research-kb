---
title: Automating coherent long-form video generation (AI video co-director)
area: computer-vision
kind: blog
url: https://research.google/blog/coherent-long-form-video-generation/
authors: [Yale Song, Yiwen Song]
year: 2026
status: triaged
priority: 3
effort: 1h
origin: whatsapp
saved: 2026-09-28
tags: [video-generation, multi-agent, long-form, consistency]
related: []
---

> **Resumo:** Post que apresenta um framework multiagente que planeja a continuidade visual de narrativas em vários planos e gera vídeos longos e consistentes, como camada de orquestração sobre modelos de geração fechados.

## Contribuição principal

- Quatro frameworks complementares descritos: Co-Director (bandit multi-armado com juiz MLLM para escolher configurações criativas), CANVAS (storyboard com memória visual persistente), A²RD (geração autorregressiva por segmentos com memória multimodal) e VQQA (refino em circuito fechado do prompt com críticas de um modelo visão-linguagem).
- Problemas atacados: semantic drift, falhas em cascata, feature drift e content collapse.
- Benchmarks citados: GenAD-Bench, HardContinuityBench, LVBench-C, ViStoryBench, VBench-Long, entre outros. O texto traz um número de pico (81,4 no GenAD-Bench) e poucos valores além disso.

## O que dá para replicar ou testar

Nada direto: depende de modelos fechados. Possível ideia pequena: usar um juiz MLLM para medir consistência temporal de personagens em um conjunto curto de clipes.

## Por que me interessa

Os mecanismos de memória e de avaliação de continuidade são reaproveitáveis em compreensão de vídeo longo, mesmo que a geração em si fique fora do escopo.

## Estimativa de esforço

- **Leitura:** 20 a 30 min.
- **Protótipo:** não recomendado agora (proposta da triagem).

## Pontos a verificar

- Os papers dos quatro componentes são citados no post por identificador arXiv, mas não foram abertos: Co-Director, CANVAS, A²RD e VQQA (a verificar nos originais).
- O post não declara se há código dos métodos liberado.

## Log

- 2026-10-19: fonte triada a partir do post.
