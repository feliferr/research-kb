---
title: "RAG-Anything: All-in-One RAG Framework"
area: genai
kind: repo
authors: [Zirui Guo, Xubin Ren, Lingrui Xu, Jiahao Zhang, Chao Huang]
year: 2025
priority: 2
effort: weekend
tags: [rag, multimodal, knowledge-graph, document-parsing, lightrag]
related: []
url: https://github.com/HKUDS/RAG-Anything
saved: 2026-10-21
origin: telegram
status: triaged
---

> **Resumo:** Framework open source (MIT) do grupo HKUDS, construído sobre o LightRAG, para fazer RAG sobre documentos que misturam texto, imagens, tabelas e equações num único pipeline. Combina parsing de documentos, um grafo de conhecimento multimodal e recuperação híbrida (vetorial + grafo); só o README foi lido, não o relatório técnico.

## Contribuição principal

Segundo o README, o pipeline tem parsing (MinerU, Docling ou PaddleOCR), processadores especializados por tipo de conteúdo, um grafo de conhecimento com relações entre modalidades e recuperação híbrida. Suporta PDFs, documentos Office, imagens, TXT/MD e HTML (só via Docling). Consultas em modos texto (hybrid, local, global, naive) ou com conteúdo multimodal. Há um relatório técnico associado (arXiv:2510.12323).

## O que dá para replicar ou testar

Instalar via `pip install raganything`, indexar um conjunto pequeno de PDFs públicos com tabelas e figuras e comparar as respostas com um RAG só de texto sobre as mesmas perguntas.

## Por que me interessa

Referência prática para RAG sobre documentos com conteúdo não textual.

## Estimativa de esforço

- **Leitura:** 30 min no README; mais 1h se for ler o relatório técnico.
- **Protótipo:** fim de semana; requer modelos de LLM, visão e embeddings, e LibreOffice para arquivos Office.

## Pontos a verificar

- (a verificar) resultados e comparações com baselines do relatório técnico (arXiv:2510.12323), não lido.
- (a verificar) maturidade do projeto e qualidade do parsing em documentos reais.
- (a verificar) requisitos para áudio e vídeo (o README menciona extras opcionais).

## Log

- 2026-10-21: fonte triada (automático, via Telegram).
