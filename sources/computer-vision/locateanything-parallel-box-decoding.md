---
title: LocateAnything: grounding e detecção rápidos com Parallel Box Decoding
area: computer-vision
kind: paper
url: https://research.nvidia.com/labs/lpr/locate-anything/
authors: [Shihao Wang et al.]
year: 2026
status: triaged
priority: 2
effort: weekend
origin: whatsapp
saved: 2026-10-18
tags: [grounding, detection, vlm, efficiency]
related: []
---

> **Resumo:** Framework de grounding e detecção para modelos visão-linguagem que prevê cada caixa (ou ponto) em um único passo de forward (Parallel Box Decoding), em vez de gerar as coordenadas token a token.

## Contribuição principal

- Parallel Box Decoding (PBD) com três modos de inferência: Fast, Slow e Hybrid (rápido por padrão, lento quando a saída paralela parece pouco confiável).
- Arquitetura citada na página: encoder visual Moon-ViT, decoder Qwen2.5 e projetor MLP.
- Conforme a página do projeto (conferir no paper): 12,7 caixas/s em uma H100 no modo Hybrid, contra 1,1 do Qwen3-VL e 5,0 do Rex-Omni; e um dataset próprio, o LocateAnything-Data (138M de consultas e 785M de caixas).
- Benchmarks listados: LVIS, COCO, Dense200, VisDrone, ScreenSpot-Pro, DocLayNet, M6Doc, TotalText, HumanRef e RefCOCOg.

## O que dá para replicar ou testar

- Rodar o modelo em frames amostrados de vídeos e medir caixas/s e qualidade em IoU alto contra um VLM que decodifica token a token.
- Ablação simples: modo Fast vs. Hybrid em um subconjunto pequeno de um benchmark público.

## Por que me interessa

Grounding eficiente é um bloco de construção para entender vídeo (localizar objetos e eventos ao longo do tempo) com custo de inferência menor.

## Estimativa de esforço

- **Leitura:** 30 a 45 min (a página e as seções de método do paper).
- **Protótipo:** fim de semana, 1 GPU (prioridade e esforço são propostas da triagem).

## Pontos a verificar

- Só a página do projeto foi lida, não o paper completo.
- A página lista repositório, modelo `nvidia/LocateAnything-3B`, demo e dataset no Hugging Face; os links não foram abertos (a verificar a liberação).

## Log

- 2026-10-19: fonte triada a partir da página do projeto.
