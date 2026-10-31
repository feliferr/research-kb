---
title: Retrofitting Recurrent Vision-Language Models from Pretrained Backbones
area: genai
kind: paper
authors: [Madhav Iyengar, Andreas Geiger, Hilde Kühne]
year: 2026
priority: 2
effort: weekend
tags: [vlm, depth-recurrence, model-compression, distillation, multimodal]
related: []
url: https://arxiv.org/pdf/2610.22075
saved: 2026-10-31
origin: telegram
status: triaged
---

> **Resumo:** O paper adapta depth recurrence (repetir um bloco de camadas) a VLMs já pré-treinados: poda camadas do backbone de linguagem, repete um subconjunto e recupera o desempenho com treino em três etapas e distillation. No TinyLLaVA-1.4B, reporta redução de 23,3% nos parâmetros do modelo de linguagem; li apenas o abstract/resumo da página do arXiv, não o PDF completo.

## Contribuição principal

- Método para "retrofit" de recorrência em profundidade: poda camadas do backbone de linguagem, faz loop sobre parte das restantes e usa um adapter linear em cada passo para combinar a saída do bloco com representações anteriores dos tokens.
- Recuperação em três etapas (pré-treino só de linguagem, alinhamento do projector, instruction tuning visual completo), com distillation do modelo original não recorrente na primeira e na última.
- Segundo o abstract: supera um baseline sem recorrência treinado com os mesmos dados de recuperação, e supera converter um LM recorrente em VLM com os mesmos dados. Melhora em benchmarks de raciocínio e fica no mesmo nível em compreensão visual básica.
- Ablações sobre o adapter entre recorrências e sobre um bloco recorrente maior.

## O que dá para replicar ou testar

Poda + loop de algumas camadas em um VLM pequeno (por exemplo, TinyLLaVA) e comparação com o modelo podado sem recorrência, usando benchmarks públicos de VLM. Depende de o código e os checkpoints estarem disponíveis (a verificar).

## Por que me interessa

Reduzir parâmetros de VLMs mantendo capacidade de raciocínio é relevante para inferência eficiente.

## Estimativa de esforço

- **Leitura:** ~1h (método e ablações)
- **Protótipo:** fim de semana, 1 GPU (a verificar, depende do código disponível)

## Pontos a verificar

- (a verificar) conteúdo lido só no abstract/página `abs`; detalhes de método, benchmarks e números não foram confirmados no PDF.
- (a verificar) disponibilidade de código e checkpoints.
- (a verificar) quais benchmarks de raciocínio e de compreensão visual foram usados e o tamanho dos ganhos.

## Log

- 2026-10-31: fonte triada (automático, via Telegram).
