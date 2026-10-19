---
title: Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents
area: genai
kind: paper
url: https://arxiv.org/abs/2609.00006
authors: [Paul Barbaste, Tristan Darrigol, Germain Vu, Tom Wiltberger]
year: 2026
status: triaged
priority: 1
effort: weekend
origin: whatsapp
saved: 2026-10-06
tags: [agents, coding-agents, harness, architecture]
related: []
---

> **Resumo:** Estudo de código-fonte de onze harnesses de agentes de programação em produção (mais um meta-harness como contraponto), tratando o harness como o runtime que liga o LLM ao mundo: loop, ferramentas, gestão de contexto, segurança, orquestração e extensão.

## Contribuição principal

- Mapa de sete subsistemas canônicos de um harness.
- Segundo o abstract: 13 observações transversais, 29 padrões de design recorrentes e 18 recomendações, além de um andaime mínimo de cerca de 90 linhas.
- Padrões de adoção citados no abstract: SKILL.md em 9 de 11 sistemas e ACP em 6.
- Corpus: cerca de quatro milhões de linhas em Python, TypeScript e Rust.

## O que dá para replicar ou testar

- Implementar o andaime mínimo (loop + ferramentas + gestão de contexto) e medir em tarefas pequenas, comparando duas estratégias de gestão de contexto.
- Usar os 29 padrões como checklist para auditar um agente próprio.

## Por que me interessa

Dá vocabulário e arquitetura de referência para construir e avaliar agentes de forma sistemática, em vez de ad hoc.

## Estimativa de esforço

- **Leitura:** 1 a 2 h (o paper completo é longo; começar pelos padrões e recomendações).
- **Protótipo:** fim de semana (proposta da triagem).

## Pontos a verificar

- Apenas o abstract foi lido; padrões, recomendações e metodologia não foram verificados.
- A data de submissão exibida na página (jul/2026) não bate com o prefixo do identificador (2609); conferir.

## Log

- 2026-10-19: fonte triada a partir do abstract.
