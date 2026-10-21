---
title: Calibrated News Recommendation under Dynamic Feedback Loops: A Simulation Study
area: recsys
kind: paper
authors: [Caio Andrade, Marcelo Manzato]
year: 2026
priority: 2
effort: weekend
tags: [calibration, feedback-loop, news-recommendation, simulation, fairness]
url: https://sol.sbc.org.br/index.php/webmedia/article/view/46087/45846
saved: 2026-10-21
origin: telegram
status: triaged
---

> **Resumo:** Estudo de simulação que compara recomendadores calibrados e não calibrados em ciclos de feedback dinâmicos, usando ambientes semi-sintéticos do portal de notícias Globo.com. Pelo abstract, a calibração aumenta a fragmentação e a miscalibração ao longo do tempo, ao contrário do esperado; só o abstract da página oficial foi lido, não o PDF.

## Contribuição principal

Segundo o abstract (página do artigo no WebMedia, 32º Simpósio Brasileiro de Multimídia e Web): avalia calibração, diversidade e fragmentação ao longo do tempo num framework de simulação dinâmica. Resultados relatados: a calibração aumenta a fragmentação e reduz levemente a cobertura do catálogo; o filtro de exposição (remover itens já vistos) afeta a diversidade, que nas listas calibradas começa mais alta e cai, enquanto nas não calibradas cresce com oscilações cíclicas; a miscalibração sobe nas variantes calibradas e cai nas não calibradas.

## O que dá para replicar ou testar

Montar uma simulação simples de feedback loop sobre um dataset público de notícias (o artigo usa dados do Globo.com, a verificar disponibilidade) e comparar um baseline com e sem reranking calibrado, medindo miscalibração e diversidade por rodada.

## Por que me interessa

Mostra como métricas de recomendação podem se comportar de modo diferente no longo prazo do que numa avaliação estática.

## Estimativa de esforço

- **Leitura:** a definir; PDF não lido (provavelmente 30 a 45 min) (a verificar)
- **Protótipo:** fim de semana, sem GPU necessária (a verificar)

## Pontos a verificar

- (a verificar) conteúdo completo não acessado: o fetch do PDF devolveu só o título; o resumo vem do abstract da página do artigo.
- (a verificar) método de calibração, modelos recomendadores, detalhes da simulação e magnitude dos efeitos.
- (a verificar) disponibilidade de código e do dataset semi-sintético.

## Log

- 2026-10-21: fonte triada (automático, via Telegram).
