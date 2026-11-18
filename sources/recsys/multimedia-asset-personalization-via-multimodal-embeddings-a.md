---
title: "Multimedia Asset Personalization via Multimodal Embeddings at Netflix"
area: recsys
kind: paper
authors: [Emma Yanyang Kong, Aditya Deshpande, Bowei Yan, Asad Abbasi, Santiago Castro, Avneesh Saluja, David Fagnan, Ashish Rastogi]
year: 2026
priority: 2
effort: 1h
tags: [multimodal, embeddings, personalization, cold-start, clip, production]
related: []
url: https://arxiv.org/pdf/2608.18322
saved: 2026-11-17
origin: telegram
status: triaged
---

> **Resumo:** O paper relata como embeddings multimodais (CLIP para imagens, um modelo tri-modal para trechos de vídeo) substituíram modelos baseados só em IDs na escolha de artwork e previews personalizados, melhorando o cold-start. Também compartilha lições de produção, como uma tarefa-proxy offline para avaliar embeddings antes de testes A/B. (Li apenas a página abstract do arXiv, não o PDF completo.)

## Contribuição principal

Segundo o abstract: (1) embeddings de imagem CLIP num modelo two-tower permitem um único modelo para os cinco tipos de canvas de artwork, com cold-start bem melhor, e o espaço conjunto texto-imagem torna a personalização sensível à consulta em busca; (2) para previews em vídeo, o MediaFM, modelo fundacional interno que funde sinais visuais, de áudio e de texto temporizado, supera baselines só visuais em avaliação offline e em testes A/B online; (3) uma tarefa-proxy offline (prever o vencedor por popularidade a partir dos embeddings) ordena modelos e versões de embedding antes de integrações caras. O paper também discute infraestrutura de embeddings compartilhada e serving de baixa latência.

## O que dá para replicar ou testar

Em escala pequena: comparar um two-tower com IDs apenas contra um com embeddings CLIP de imagem como feature, num dataset público com itens frios (cold-start), e testar uma tarefa-proxy simples de ranqueamento de embeddings. O MediaFM é interno e não reproduzível.

## Por que me interessa

Mostra de forma prática como incorporar embeddings de modelos fundacionais em recomendadores e como avaliá-los barato.

## Estimativa de esforço

- **Leitura:** cerca de 1h (a verificar, conforme o tamanho do PDF)
- **Protótipo:** fim de semana, uma GPU modesta ou só CPU com embeddings pré-calculados

## Pontos a verificar

- (a verificar) Detalhes de métricas, ganhos numéricos e arquitetura: não lidos, só o abstract foi acessado.
- (a verificar) Disponibilidade de código ou dados públicos: o MediaFM parece interno.

## Log

- 2026-11-17: fonte triada (automático, via Telegram).
