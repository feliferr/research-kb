---
title: Your nDCG Score May Be Correct. But the Conclusion? Stability-Aware Offline Recommender Evaluation
area: recsys
kind: blog
url: https://isg.beel.org/blog/2026/09/27/ndcg-stability-frame-recsys/
authors: [Joeran Beel]
year: 2026
status: triaged
priority: 1
effort: weekend
origin: whatsapp
saved: 2026-09-29
tags: [evaluation, offline-evaluation, reproducibility, ndcg]
related: []
---

> **Resumo:** Defende que um único score (como o nDCG) pode estar correto para a condição reportada e ainda assim levar a uma conclusão frágil: outras condições defensáveis podem inverter o ranking de algoritmos, e scores iguais podem esconder listas muito diferentes.

## Contribuição principal

- Propõe avaliar a estabilidade dos resultados entre condições experimentais: de score, de saída (semelhança das listas) e comparativa (a conclusão A vs. B se mantém?).
- Processo prático: definir um espaço de condições, montar um painel de condições, analisar e reportar por condição.
- O autor cita trabalhos de terceiros como evidência (conferir nos originais): inversão de MF vs. kNN no MovieLens ao ponderar usuários; correlação de Kendall entre 0,53 e 0,76 em 230 configurações sob três estratégias de divisão; duas sementes do GRU4Rec com nDCG@20 quase iguais mas listas muito diferentes.
- Limitações declaradas: sem estimativa empírica de quão frequente é a instabilidade e sem validação de que estabilidade prevê resultados posteriores.

## O que dá para replicar ou testar

- Mini-estudo: um dataset público (ex.: MovieLens), 2 ou 3 estratégias de divisão, 2 ou 3 sementes e 3 algoritmos; medir nDCG, sobreposição das listas (Jaccard ou RBO) e a correlação entre os rankings de algoritmos nas diferentes condições.
- Resultado publicável como lab: uma tabela de estabilidade e um parágrafo sobre quando a conclusão muda.

## Por que me interessa

Avaliação offline confiável é pré-requisito para qualquer experimento de recomendação; o experimento é barato e gera um artefato público.

## Estimativa de esforço

- **Leitura:** 30 min.
- **Protótipo:** fim de semana, sem GPU (proposta da triagem).

## Pontos a verificar

- Os números acima são do blog citando outros trabalhos; não foram conferidos nos papers originais.

## Log

- 2026-10-19: fonte triada.
- 2026-10-19: lab criado: [ndcg-stability](../../labs/ndcg-stability/README.md).
