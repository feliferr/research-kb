---
title: "M-plicits: Neural Implicit Surfaces via Nested Multiscale Residuals"
area: computer-vision
kind: paper
authors: [Vinícius da Silva, Isabelle Melo, Matheus Bessa, Guilherme Schardong, Luiz Schirmer, André Araújo, Nuno Gonçalves, Hélio Lopes, Alberto Raposo, Luiz Velho, Tiago Novello]
year: 2026
priority: 2
effort: weekend
tags: [neural-implicit-surfaces, sdf, multiscale, denoising, 3d-reconstruction, level-of-detail]
related: []
url: https://dsilvavinicius.github.io/m-plicits/
saved: 2026-10-26
origin: telegram
status: triaged
---

> **Resumo:** Representa uma superfície como soma de redes pequenas: uma rede base compacta e limitada em banda captura a forma grossa, e redes residuais refinam o detalhe só numa faixa fina ao redor da superfície anterior. Segundo a página do projeto, isso mantém a superfície limpa com scans ruidosos e permite renderização em tempo real e níveis de detalhe; li apenas a página do projeto, não o paper.

## Contribuição principal

Segundo a página do projeto (NeurIPS 2026): cada soma parcial das redes é uma SDF válida, então prefixos servem como níveis de detalhe. Como o ruído fora da superfície nunca é ajustado, ele é filtrado por construção. A página reporta sphere tracing a 35–180 FPS, extração de malha por marching cubes com culling até 5× mais rápida e cerca de 247 mil parâmetros no detalhe total, avaliado em oito formas com 1% de ruído contra iNGP (comparações com BACON, IDF e Poisson ficam no paper). Números não conferidos no paper.

## O que dá para replicar ou testar

Código, modelos e nuvens de pontos (limpas, ruidosas e com outliers) são públicos segundo a página. Teste pequeno: rodar o treino em uma das formas ruidosas e comparar o erro de superfície das somas parciais com o modelo completo.

## Por que me interessa

Curiosidade sobre representações neurais compactas de geometria 3D robustas a ruído e com níveis de detalhe.

## Estimativa de esforço

- **Leitura:** ~1h (paper completo, seções de método e experimentos)
- **Protótipo:** fim de semana, 1 GPU (a verificar)

## Pontos a verificar

- (a verificar) Resultados e comparações (iNGP, BACON, IDF, screened Poisson) só foram lidos como resumidos na página do projeto; confirmar no paper (https://arxiv.org/abs/2609.28684, link indicado na página).
- (a verificar) Código: https://github.com/dsilvavinicius/m-plicits; modelos: https://huggingface.co/dsilvavinicius/m-plicits.
- (a verificar) Ano e venue (NeurIPS 2026) conforme a página do projeto.

## Log

- 2026-10-26: fonte triada (automático, via Telegram).
