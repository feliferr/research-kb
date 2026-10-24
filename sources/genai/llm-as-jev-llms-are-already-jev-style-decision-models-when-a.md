---
title: "LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them"
area: genai
kind: paper
authors: [Yinheng Li, Justin Wagle]
year: 2026
priority: 2
effort: weekend
tags: [llm, decision-models, routing, fine-tuning, kl-divergence, test-time-reasoning]
related: []
url: https://arxiv.org/abs/2610.02076
saved: 2026-10-24
origin: telegram
status: triaged
---

> **Resumo:** O paper investiga se LLMs genéricos já conseguem fazer "decisão" no estilo Jev (devolver uma distribuição de probabilidade sobre opções predefinidas, sem gerar texto livre), propondo uma receita de inferência sem treino e um objetivo de fine-tuning com âncoras de KL. Segundo o abstract, LLMs modernos já são bons decisores, e o fine-tuning ajuda sobretudo modelos pequenos e roteamento complexo. (Baseado só no abstract da página do arXiv; o PDF não foi lido.)

## Contribuição principal

Segundo o abstract (a verificar no texto completo): framework "LLM-as-Jev" que preserva a arquitetura do backbone; receita de inferência sem treino que, num backbone de 4B, iguala ou supera outras leituras sem treino; suporte a número arbitrário de opções e a decisões multimodais; variante "Thinking Jev", que usa o modo de raciocínio do backbone com orçamento em tempo de teste; e um objetivo de fine-tuning com âncoras de KL que melhora modelos menores sem degradar a geração de texto geral. Experimentos citados com Qwen3.5-4B e Qwen3-0.6B.

## O que dá para replicar ou testar

Pequeno: pegar um modelo aberto pequeno, definir uma tarefa de classificação/roteamento com opções fixas, ler a distribuição sobre as opções a partir dos logits (sem gerar texto) e comparar com prompting generativo e, depois, com um fine-tuning simples com regularização de KL contra o modelo base.

## Por que me interessa

Decisões categóricas com probabilidades calibráveis (roteamento, classificação) sem geração de texto são um padrão geral útil em sistemas com LLMs.

## Estimativa de esforço

- **Leitura:** 45 min (introdução, método, resultados de fine-tuning)
- **Protótipo:** fim de semana, 1 GPU pequena

## Pontos a verificar

- (a verificar) conteúdo acessado apenas via abstract; métodos, benchmarks e números não foram lidos.
- (a verificar) definição exata de "Jev" e de seu sistema proprietário de referência; o abstract diz que arquitetura e treino são proprietários.
- (a verificar) detalhes da receita sem treino e dos baselines comparados.

## Log

- 2026-10-24: fonte triada (automático, via Telegram).
