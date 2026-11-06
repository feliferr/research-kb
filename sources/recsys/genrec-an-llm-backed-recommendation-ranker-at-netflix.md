---
title: "GenRec: An LLM-Backed Recommendation Ranker at Netflix"
area: recsys
kind: paper
authors: [Ying Li, Shradha Sehgal, Arjun Rao, Rein Houthooft, Yaochen Zhu, Ashish Rastogi]
year: 2026
priority: 2
effort: 1h
tags: [llm, ranking, context-engineering, serving, prefill-only]
related: []
url: https://arxiv.org/abs/2608.10257v2
saved: 2026-11-05
origin: telegram
status: triaged
---

> **Resumo:** O paper descreve o GenRec, um ranker de recomendação baseado em um LLM de fundação que usa descrições em texto do histórico e do contexto do usuário no lugar de milhares de features feitas à mão. Segundo o abstract, ele supera o ranker de produção num grande teste A/B e usa inferência só com prefill para reduzir o custo de serving. Só o abstract (página do arXiv) foi lido, não o PDF.

## Contribuição principal

Pelo abstract: pós-treino de um LLM adaptado ao catálogo para ranking, com verbalização da entrada, engenharia de contexto, construção dos dados de treino, integração de sinais de recompensa, escolha de arquitetura e serving barato via prefill-only. Os autores defendem a passagem de feature engineering para context engineering e de arquiteturas especializadas para modelos de fundação compartilhados.

## O que dá para replicar ou testar

Nada direto no modelo em si (dados e modelo proprietários). Dá para testar em pequena escala a ideia de verbalizar histórico de interações em texto e ranquear candidatos com um LLM pequeno em prefill-only, comparando com um baseline clássico num dataset público (por exemplo MovieLens).

## Por que me interessa

Mostra como LLMs podem substituir pipelines de features em ranking de recomendação, tema central de recsys aplicado.

## Estimativa de esforço

- **Leitura:** a definir (só o abstract foi lido); provavelmente 1h para as seções de verbalização, treino e serving
- **Protótipo:** fim de semana, 1 GPU (a verificar)

## Pontos a verificar

- (a verificar) conteúdo do PDF completo: métricas, tamanhos de ganho e detalhes do serving; apenas o abstract foi lido.
- (a verificar) o identificador arXiv 2608.10257v2 e as datas de submissão (10/08/2026) e revisão (21/08/2026) vêm da página do arXiv.
- (a verificar) generalização dos resultados fora do ambiente do paper.

## Log

- 2026-11-05: fonte triada (automático, via Telegram).
