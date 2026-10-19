---
title: VideoMAE V2 and V-JEPA (explainer)
area: computer-vision
kind: blog
url: https://mlhonk.substack.com/p/65-videomae-v2-and-v-jepa
authors: [Massimiliano Viola]
year: 2026
status: reading
priority: 1
effort: weekend
origin: whatsapp
saved: 2026-08-15
tags: [video, self-supervised, masked-autoencoders, jepa, representation-learning]
related: []
---

> **Resumo:** Post que compara duas evoluções do aprendizado auto-supervisionado de vídeo: o VideoMAE V2, que escala a reconstrução de pixels com mascaramento duplo, e o V-JEPA, que prevê features latentes em vez de pixels.

## Contribuição principal

- **VideoMAE V2:** o decoder processa só um subconjunto dos tokens (mascaramento duplo), reduzindo memória e acelerando o pré-treino; escala até ViT-Giant. Limitação apontada: reconstrução de pixels tende a dar representações congeladas fracas.
- **V-JEPA:** encoder de contexto vê só os tokens não mascarados, encoder alvo atualizado por média móvel exponencial e um preditor leve que prevê as features alvo (perda L1), sem decoder de pixels.
- Segundo o post, o V-JEPA supera os métodos de reconstrução de pixels em avaliação congelada e em few-shot, com treino mais curto.
- Papers originais citados: VideoMAE V2 (arXiv 2303.16727) e V-JEPA (arXiv 2404.08471). Ambos seguem no inbox para triagem.

## O que dá para replicar ou testar

- Extrair features congeladas de um modelo de cada família (checkpoints públicos, a verificar) e comparar sonda linear e few-shot em um subconjunto pequeno de um benchmark de ação.

## Por que me interessa

Base de representações de vídeo para raciocínio temporal e tarefas de compreensão com poucos rótulos.

## Estimativa de esforço

- **Leitura:** 30 min (e depois os dois papers).
- **Protótipo:** fim de semana, 1 GPU (proposta da triagem).

## Pontos a verificar

- Resumo de um post de terceiros; as afirmações de desempenho devem ser conferidas nos papers.

## Log

- 2026-10-19: fonte triada.
- 2026-10-19: movida para reading (plano 2026-W43).
