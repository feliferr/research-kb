---
title: "Advancing Generative Recommendation Inference: colaboração Spotify e NVIDIA no TensorRT LLM"
area: recsys
kind: blog
authors: [Ivo Senese, Reid Wilbur, Mark VanMiddlesworth, Guy Stone, Marek Pikulski, Stefan Niebler, Alexander Young]
year: 2026
priority: 2
effort: 1h
tags: [generative-recommendation, llm-inference, tensorrt-llm, beam-search, soft-tokens, serving]
related: []
url: https://engineering.atspotify.com/2026/10/advancing-generative-recommendation-inference-our-collaboration-with-nvidia-on-tensorrt-llm
saved: 2026-10-24
origin: telegram
status: triaged
---

> **Resumo:** O post descreve como a engenharia do Spotify e da NVIDIA estenderam o TensorRT LLM (beam search no sampler, scoring de vários itens por requisição e injeção de soft tokens de usuário) para servir recomendação generativa com um LLM no lugar do vLLM. Reporta redução de custo de até 54% em beam search e até 7% em scoring com um modelo Qwen3 1.7B, sem números detalhados no texto.

## Contribuição principal

- Contexto: migração de pipelines de recomendação em vários estágios para um único modelo de linguagem personalizado; o primeiro sistema em produção (podcasts) rodava em vLLM, cujo beam search fica fora do motor de GPU e gera gargalo de CPU e trabalho redundante.
- Beam search dentro do sampler do TensorRT LLM, com overlap scheduling e sampler reescrito em PyTorch.
- Multi-item scoring: vários candidatos pontuados numa só requisição, com custo linear no número de candidatos.
- Soft tokens: plugin customizado de Qwen3 (suporte a modelos out-of-tree) que projeta vetores de usuário no espaço de embeddings do LLM e os insere via parâmetros multimodais.
- Mudanças upstream citadas: saída multi-sequência de beam search, modelos out-of-tree no trtllm-serve, entrada `image_embeds`, scoring multi-item na API Python (versões 1.2.0rc3 a 1.3.0rc20).
- Referências do post: PLUM (arXiv 2510.07784), paper de semantic IDs de podcasts (arXiv 2603.17540), Embedding to Prefix (arXiv 2505.17051).

## O que dá para replicar ou testar

Medir, com um modelo pequeno aberto (ex.: Qwen3 1.7B) e um dataset público de recomendação, throughput e latência de beam search e de scoring de N candidatos em vLLM versus TensorRT LLM, numa GPU única.

## Por que me interessa

Mostra o lado de serving da recomendação generativa: custo de inferência de beam search e scoring pesa tanto quanto a qualidade do modelo.

## Estimativa de esforço

- **Leitura:** cerca de 30 min, mais os três papers referenciados se houver interesse.
- **Protótipo:** fim de semana, 1 GPU (a verificar a compatibilidade das versões do TensorRT LLM).

## Pontos a verificar

- (a verificar) Conteúdo lido via WebFetch (resumo automático da página), não a página integral; confira detalhes e gráficos no original.
- (a verificar) Os números de benchmark estão apenas em gráficos; o texto traz só "até 54%" e "até 7%", sem baseline exata.
- (a verificar) O post não informa se o plugin de soft tokens para Qwen3 foi liberado como código aberto.
- (a verificar) Papers referenciados (PLUM etc.) não foram lidos; IDs vêm do post.

## Log

- 2026-10-24: fonte triada (automático, via Telegram).
