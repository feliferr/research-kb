---
title: "Decision4Rec: A Jev-Inspired Framework of Decision Models on Knowledge and Active Graphs for Multi-Agent Recommender Systems"
area: recsys
kind: paper
authors: [Marco Polignano, Het Darshan Mehta, Pasquale Lops, Ernesto William De Luca, Giovanni Semeraro]
year: 2026
priority: 2
effort: weekend
tags: [recsys, llm, reranking, multi-agent, knowledge-graph, decision-models]
related: []
url: https://arxiv.org/html/2610.26035v1
saved: 2026-10-21
origin: telegram
status: triaged
---

> **Resumo:** O paper propõe o Decision4Rec, um framework aberto em que um "decision model" (modelo de linguagem que devolve uma probabilidade por opção, em vez de gerar texto) reordena candidatos produzidos por um grafo de conhecimento e um pool multiagente, com fusão final com o score de um ranker. Segundo o abstract e o resumo lido, há ganhos de 25–36% em NDCG@10 sobre o melhor baseline treinado em catálogos Amazon esparsos, e quase empate no Steam, que é denso; li apenas a primeira parte do texto (cerca de 100 mil dos 169 mil caracteres).

## Contribuição principal

- Framework modular com quatro peças: grafo de conhecimento que descreve cada cenário em afirmações curtas em escalas do próprio cenário, pool multiagente (com um recomendador sequencial treinado, SASRecF, como um dos agentes), slot para o decision model e etapa de fusão (modelo de escolha estilo Luce combinado ao score do ranker).
- Decision models "Kev" (0,8B a 27B) treinados com LoRA em escolhas reais de três domínios (Amazon Video Games, Amazon Musical Instruments, Steam) e reutilizados sem retreino em domínios retidos (Amazon Industrial and Scientific, MovieLens-1M).
- Resultados reportados: a maior parte do ganho vem do pool; o modelo de 27B adiciona só 5–6% sobre o de 0,8B em três de quatro domínios; um Kev de 0,8B treinado supera o Jev comercial em onze de quinze configurações; em MovieLens-1M o ganho é de 5–7%.
- Três regras para montar registros de treino de rerankers, cada uma ligada a um erro encontrado nas primeiras execuções.
- Código, configurações e modelos treinados são linkados no paper.

## O que dá para replicar ou testar

Rodar o repositório público do paper em um dos datasets públicos (por exemplo MovieLens-1M) com o decision model de 0,8B e comparar NDCG@10 com o baseline sequencial sozinho, depois fazer uma ablação trocando o decision model por uma ordem aleatória de candidatos.

## Por que me interessa

Mostra um caminho para usar LLMs pequenos como rerankers que transferem entre domínios, com comparação honesta contra uma ordem aleatória.

## Estimativa de esforço

- **Leitura:** 1h30, priorizando método, fusão e a seção de ablações.
- **Protótipo:** fim de semana, 1 GPU (a verificar, depende do tamanho do modelo e dos dados).

## Pontos a verificar

- (a verificar) A segunda parte do texto (cerca de 69 mil caracteres finais, provavelmente discussão, limitações e apêndices) não foi lida.
- (a verificar) Os números acima vêm do abstract e do resumo da página; confirmar nas tabelas, incluindo testes de significância e a definição exata dos baselines.
- (a verificar) Disponibilidade e licença do código e dos modelos nos links indicados pelo paper (GitHub e Hugging Face).
- (a verificar) Detalhes do "Jev" comercial e do que o paper chama de "Kev", pois a descrição aqui vem apenas do resumo.
- A URL do arXiv é de outubro de 2026 (v1); checar se há versões posteriores.

## Log

- 2026-10-21: fonte triada (automático, via Telegram).
