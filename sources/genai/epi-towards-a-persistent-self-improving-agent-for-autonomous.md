---
title: "Epi: Towards a Persistent, Self-Improving Agent for Autonomous Research"
area: genai
kind: paper
authors: [Yue Huang, Zhangchen Xu, Xiaonan Luo, Zheyuan Liu, Lichi Li, Yiping Wang, Peiyang Song, Eric Gabriel Ramos, Enze Xie, Olexandr Isayev, Paul Liang, Nouha Dziri, Huan Sun, Jianfeng Gao, Ying Liu, Misha Sra, Xiangliang Zhang, Alex Pentland, Zichen Chen]
year: 2026
priority: 2
effort: weekend
tags: [agents, memory, autonomous-research, long-horizon]
related: []
url: https://arxiv.org/pdf/2610.24944
saved: 2026-10-21
origin: telegram
status: triaged
---

> **Resumo:** O paper apresenta o Épi, um agente de pesquisa autônoma que mantém uma investigação ao longo de várias sessões do modelo, combinando histórico persistente, memória hierárquica, ramificação e revisão independente, com resultados avaliados por um verificador fixo. Os autores reportam 120 resultados "recordes" em limites numéricos e construções matemáticas e uma variante leve (Épi-turbo) para código de pesquisa operacional. Lido apenas o abstract/resumo da página do arXiv; o PDF completo não foi lido.

## Contribuição principal

Segundo o abstract: um desenho de agente com continuidade entre sessões (histórico de pesquisa persistente, memória hierárquica, branching e revisão independente). Resultados reportados: 120 recordes (20 limites numéricos em 12 famílias e 100 construções em 8 famílias), uma prova assistida por computador da conjectura de Tuza para uma classe restrita de split graphs, e evidência de que o limite de Cohn-Elkies por programação linear não é justo nas dimensões 10 e 11. O Épi-turbo, em 30 tarefas do FrontierOR, teria pontuação 5,4% maior que o Codex com o mesmo modelo base, a 64% do custo (números do abstract, não verificados no texto).

## O que dá para replicar ou testar

Nada direto no curto prazo. Um experimento pequeno seria montar um loop de agente com memória em arquivos entre sessões e um verificador fixo sobre um problema de otimização pequeno, comparando com execução sem memória.

## Por que me interessa

Interesse genérico em agentes de longo prazo, memória persistente e avaliação com verificadores objetivos.

## Estimativa de esforço

- **Leitura:** ~1h30 (abstract, arquitetura de memória e seções de avaliação)
- **Protótipo:** fim de semana, para um loop mínimo com memória e verificador

## Pontos a verificar

- (a verificar) Detalhes da arquitetura de memória e de revisão independente: só o abstract foi lido.
- (a verificar) Os números (120 recordes, +5,4% sobre o Codex, 64% do custo) e a metodologia de comparação no FrontierOR.
- (a verificar) Como o verificador fixo evita sobreajuste dos resultados e o que conta como "recorde".

## Log

- 2026-10-21: fonte triada (automático, via Telegram).
