---
title: Next Best Action: Causal Constrained Offline RL for Business Action Targeting
area: recsys
kind: paper
url: https://oars-workshop.github.io/papers/Next%20Best%20Action%20Causal%20Constrained%20Offline%20RL%20for%20Business%20Action%20Targeting.pdf
authors: [Surya Ramachandiran et al.]
year: 2026
status: triaged
priority: 1
effort: weekend
origin: whatsapp
saved: 2026-09-27
tags: [next-best-action, offline-rl, causal-inference, constrained-mdp, uplift]
related: []
---

> **Resumo:** Módulo de seleção de ações para intervenções de negócio (ex.: cupons) que corrige o viés dos dados históricos com pesos de propensão auto-normalizados (SNIPW) e resolve a escolha de ações como um MDP restrito (CMDP) pelo dual de programação linear, devolvendo a política e os preços-sombra das restrições.

## Contribuição principal

- Une correção causal off-policy e RL restrito offline em uma única formulação LP, com restrições verificáveis por dualidade (orçamento, exposição, equidade) e preços-sombra que tornam o custo de cada restrição explícito.
- Estudo de caso: 68 semanas de dados proprietários de uma plataforma de rideshare, 8 estágios de ciclo de vida baseados em RFM e ação binária (sem ação ou cupom).
- Resultados reportados (offline, estimados; conferir no paper): +19% de LTV esperado contra a política de comportamento e +8% contra a política míope.
- Limitações declaradas: sem teste A/B, pressupostos causais fortes (ignorabilidade, positividade), estados discretos, ação binária e dados proprietários.

## O que dá para replicar ou testar

- Lab pequeno com dados sintéticos: estados RFM discretos, ação binária, estimação de transições e recompensas com SNIPW e solução do CMDP com `scipy.optimize.linprog`; inspecionar os preços-sombra ao variar o orçamento.
- Comparar com a política míope em simulação, onde a verdade é conhecida (algo que o paper não pode fazer com dados reais).

## Por que me interessa

Liga decisão sequencial, inferência causal e restrições de negócio; o experimento sintético é barato e permite validar o método contra uma verdade conhecida.

## Estimativa de esforço

- **Leitura:** 45 min.
- **Protótipo:** fim de semana, sem GPU (proposta da triagem).

## Pontos a verificar

- Números e hiperparâmetros vêm de um resumo da página; conferir no PDF.

## Log

- 2026-10-19: fonte triada.
