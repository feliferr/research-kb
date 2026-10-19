---
title: GenPage: Towards End-to-End Generative Homepage Construction at Netflix
area: recsys
kind: paper
url: https://arxiv.org/abs/2606.31031v2
authors: [Lequn Wang, Jiangwei Pan, Linas Baltrunas]
year: 2026
status: triaged
priority: 2
effort: 1h
origin: whatsapp
saved: 2026-09-28
tags: [generative-recommendation, transformer, homepage, llm-style-training]
related: []
---

> **Resumo:** Substitui a pilha de recomendação em vários estágios por um único transformer que, dado usuário e contexto, gera de forma autorregressiva a página inicial inteira, com várias fileiras.

## Contribuição principal

- Treino em receita de LLM: pré-treino em páginas de produção e pós-treino por classificação binária ponderada (WBC) ou aprendizado por reforço.
- Técnicas de implantação: cold start, frescor do modelo, regras de negócio e eficiência de serving.
- Segundo o abstract: ganho significativo em teste A/B online na métrica de engajamento usada para decisões de lançamento e redução de 20% na latência de serving.
- Achados offline destacados: enriquecer o prompt rende mais do que aumentar a capacidade do modelo; o pós-treino com RL aumenta a diversidade da página.

## O que dá para replicar ou testar

Pouco direto: avaliação com dados de produção. Uma versão reduzida (lista estruturada gerada por um transformer pequeno em dataset público) é possível, mas está por definir.

## Por que me interessa

Referência atual de recomendação generativa end-to-end em escala industrial e de como lidar com cold start e regras de negócio nesse paradigma.

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** a definir.

## Pontos a verificar

- Apenas o abstract e os metadados foram lidos; experimentos e detalhes de método não foram verificados.
- DOI informado na página: 10.1145/3773078.3831915.

## Log

- 2026-10-19: fonte triada a partir do abstract.
