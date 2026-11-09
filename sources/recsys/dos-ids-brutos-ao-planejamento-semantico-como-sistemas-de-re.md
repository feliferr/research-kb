---
title: "Dos IDs brutos ao planejamento semântico: como sistemas de recomendação usam informação em escala"
area: recsys
kind: topic
priority: 2
effort: weekend
tags: [recsys, semantic-ids, llm, representation-learning]
related: []
saved: 2026-11-08
origin: telegram
status: triaged
---

> **Resumo:** Tópico de estudo sobre a evolução dos sistemas de recomendação, de embeddings de IDs brutos até representações semânticas e planejamento com modelos generativos. Nenhuma fonte foi lida ainda; esta nota só organiza perguntas e uma primeira etapa.

## Contribuição principal

Tópico sem fonte: a nota é uma pergunta de estudo, não um resumo. Reformulação: como os recomendadores passaram de tratar itens e usuários como IDs opacos para incorporar conteúdo, semântica e raciocínio, e o que isso muda no uso de informação em escala?

Perguntas a responder:

1. Quais são as limitações de embeddings baseados apenas em IDs (cold start, cauda longa, falta de conteúdo)?
2. Como itens são representados de forma semântica (por exemplo, IDs semânticos derivados de conteúdo) e como isso se compara a IDs brutos?
3. Que papel modelos de linguagem desempenham: como encoder de conteúdo, como recomendador generativo ou como planejador?
4. O que significa "planejamento" em recomendação e em que cenários ele supera ranking direto?
5. Quais são os custos e trade-offs em escala (latência, treino, atualização do catálogo)?

## O que dá para replicar ou testar

Primeira etapa (1 hora): buscar 2 ou 3 surveys recentes sobre recomendação com LLMs e IDs semânticos, e montar uma tabela comparando representação de itens, tarefa e dataset público usado. Depois, um baseline pequeno comparando embedding de ID com embedding de conteúdo em um dataset público (ex.: MovieLens ou Amazon Reviews).

## Por que me interessa

Entender como a representação de itens e a informação usada condicionam a qualidade de sistemas de recomendação modernos.

## Estimativa de esforço

- **Leitura:** 1 h para o levantamento inicial de fontes; mais depois de selecioná-las
- **Protótipo:** fim de semana, CPU ou 1 GPU pequena

## Pontos a verificar

- (a verificar) fontes ainda não selecionadas
- (a verificar) se o título é de um paper ou survey existente; não foi pesquisado

## Log

- 2026-11-08: fonte triada (automático, via Telegram).
