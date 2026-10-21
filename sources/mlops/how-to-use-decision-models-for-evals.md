---
title: How To Use Decision Models for Evals
area: mlops
kind: blog
authors: [Hamel Husain, Antaripa Saha]
year: 2026
priority: 2
effort: 1h
tags: [evals, llm-as-judge, decision-models, calibration, threshold-tuning, cost]
related: []
url: https://hamel.dev/blog/posts/decision-model-evals/
saved: 2026-10-21
origin: telegram
status: triaged
---

> **Resumo:** O post propõe usar "decision models" (classificadores rápidos e baratos que devolvem uma probabilidade) no lugar de LLM judges em evals automatizados, ajustando o limiar de decisão em vez de usar 0,50 e checando a calibração das probabilidades. Os autores comparam seis modelos em 98 traces de produção de um agente, pesando F1, custo e calibração (conteúdo lido via WebFetch, que devolve um resumo da página, não o texto integral).

## Contribuição principal

Um roteiro prático para escolher e configurar um decision model como juiz de evals: fixar o prompt do juiz, definir mínimos de precisão e recall, ajustar o limiar de cada modelo por validação cruzada estratificada (5 folds, maximizando F1), comparar custo por 100 execuções e, se as notas forem usadas como confiança, verificar calibração com diagramas de confiabilidade, Platt scaling e Brier score. No experimento relatado, o modelo com maior F1 (~0,87) foi também o mais caro, e o mais barato teve F1 ~0,79. Os autores ressalvam que os resultados dependem da tarefa e dos dados.

## O que dá para replicar ou testar

Pegar um conjunto pequeno de exemplos rotulados públicos (por exemplo, respostas de um chatbot marcadas como falha ou não) e comparar limiar 0,50 contra limiar ajustado por CV, medindo precisão, recall e F1. Depois, desenhar um reliability diagram e testar Platt scaling com `scikit-learn`.

## Por que me interessa

Avaliação automatizada de sistemas generativos é um problema geral, e a combinação de ajuste de limiar, custo e calibração é uma técnica reaproveitável.

## Estimativa de esforço

- **Leitura:** ~30 min
- **Protótipo:** 1 a 2 horas com dataset público pequeno e um classificador qualquer

## Pontos a verificar

- (a verificar) números de F1, custo e Brier citados acima vêm do resumo da página, não de leitura integral das tabelas.
- (a verificar) versões e nomes dos modelos comparados (Jev, Perplexity, Liquid, Cloudflare, OpenAI) e se há código ou dados públicos para reproduzir.
- (a verificar) se o dataset de 98 traces é público; pelo resumo, parece ser de um agente de produção.
- (a verificar) relação com o framework Decision4Rec já catalogado em `sources/`, se houver.

## Log

- 2026-10-21: fonte triada (automático, via Telegram).
