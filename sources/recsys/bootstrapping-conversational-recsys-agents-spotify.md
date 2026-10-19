---
title: Bootstrapping Conversational Recommendation Agents at Spotify
area: recsys
kind: blog
url: https://research.atspotify.com/2026/9/bootstrapping-conversational-recommendation-agents-at-spotify-synthetic-data-generation-and-self-improvement-loops
authors: [E. Palumbo et al.]
year: 2026
status: triaged
priority: 2
effort: weekend
origin: whatsapp
saved: 2026-09-27
tags: [conversational-recsys, synthetic-data, llm-judge, agents]
related: [genai/llm-as-a-judge-lifecycle-netflix.md]
---

> **Resumo:** Pipeline para resolver o cold start de agentes conversacionais de recomendação sem dados reais de conversa: planos de diálogo abstratos, um simulador de usuário (UserLLM) que os executa contra o agente, avaliação por LLM juiz com rubricas por instância e um ciclo de auto-aperfeiçoamento com revisão humana.

## Contribuição principal

- Geração de conversas multi-turno sintéticas a partir de prompts de turno único, avaliadas por LLM juiz.
- Ciclo de auto-aperfeiçoamento: amostra planos, identifica falhas e usa agentes de código para propor ajustes no prompt e nas ferramentas; distingue falhas de confiabilidade (otimização contrastiva) de falhas de capacidade (refino iterativo).
- Números do post (conferir no original): validação humana em cerca de 100 conversas com cinco anotadores cada (98% exercitaram a capacidade pretendida, 93% realistas, 97% de vereditos do juiz corretos); pass@1 com ganho relativo de 8% após uma execução do ciclo; A/B de duas semanas com cerca de 15M de usuários (+14% de escuta adicional, +5% de usuários ativos semanais, -5% de pulos).
- Falhas observadas: qualidade cai após quatro turnos, parâmetros errados em chamadas de ferramenta e perda de restrições ao resumir pedidos.

## O que dá para replicar ou testar

- Mini-versão: agente de recomendação sobre um catálogo público pequeno, com planner, simulador de usuário e juiz; medir queda de qualidade por número de turnos.

## Por que me interessa

Combina agentes, recomendação e avaliação com LLM juiz, e mostra um método concreto para sair do cold start de dados.

## Estimativa de esforço

- **Leitura:** 30 min.
- **Protótipo:** fim de semana, usando API de LLM (proposta da triagem).

## Pontos a verificar

- O post não tem seção de limitações; pontos fracos prováveis (amostra humana pequena, dados sintéticos, uma única execução do ciclo) são inferências da triagem.

## Log

- 2026-10-19: fonte triada.
