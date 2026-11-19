---
title: "PRAGMA: Revolut Foundation Model"
area: recsys
kind: paper
authors: [Maxim Ostroukhov, Ruslan Mikhailov, Vladimir Iashin, Artem Sokolov, Andrei Akshonov, Vitaly Protasov, Andrey Goncharov, Dmitrii Beloborodov, Vince Mullin, Roman Yokunda Enzmann, Georgios Kolovos, Jason Renders, Pavel Nesterov, Anton Repushko]
year: 2026
priority: 2
effort: weekend
tags: [foundation-model, event-sequences, masked-modeling, embeddings, finance, fraud-detection]
related: []
url: https://arxiv.org/abs/2604.08649
saved: 2026-11-19
origin: telegram
status: triaged
---

> **Resumo:** O paper apresenta o PRAGMA, uma família de modelos fundacionais baseados em Transformer, pré-treinados com masked modeling sobre sequências de eventos bancários. Segundo o abstract, um modelo linear sobre os embeddings já vai bem em tarefas como credit scoring, detecção de fraude e previsão de lifetime value, e um fine-tuning leve melhora ainda mais. (Li apenas o abstract da página do arXiv, não o paper completo.)

## Contribuição principal

Pelo abstract: um objetivo de pré-treinamento auto-supervisionado desenhado para registros financeiros discretos e de tamanho variável, e a proposta de usar o modelo como camada de representação geral para aplicações financeiras, partindo de sequências brutas de eventos. Detalhes de arquitetura, dados, métricas e baselines não foram lidos.

## O que dá para replicar ou testar

Em escala pequena: pré-treinar um Transformer com masked modeling sobre uma sequência de eventos pública (por exemplo, dados transacionais sintéticos ou públicos de fraude/crédito) e comparar probing linear nos embeddings contra um baseline com features agregadas feitas à mão. Escolha de dataset ainda a definir.

## Por que me interessa

Representações aprendidas de sequências de eventos de usuários são um tema comum a modelagem de usuário em recomendação e a modelos tabulares/temporais.

## Estimativa de esforço

- **Leitura:** (a verificar) cerca de 1h para o paper completo; ainda não lido além do abstract.
- **Protótipo:** fim de semana, em escala reduzida e com dados públicos.

## Pontos a verificar

- (a verificar) Resultados quantitativos, tamanhos de modelo e baselines: não constam no abstract lido.
- (a verificar) Se o paper libera código, pesos ou dados: não confirmado.
- (a verificar) Área: classifiquei como `recsys` por modelagem de comportamento de usuário; também poderia caber em `genai` ou `mlops`.
- Datas segundo a página do arXiv: v1 em 9/04/2026, v2 em 24/08/2026.

## Log

- 2026-11-19: fonte triada (automático, via Telegram).
