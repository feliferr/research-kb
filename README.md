# research-kb

Base de conhecimento aberta com o que eu leio, estudo e prototipo em IA aplicada: Computer Vision, NLP, RecSys, GenAI e MLOps, com ênfase em vídeo multimodal.

A ideia é fechar o ciclo que costuma travar: **salvar → triar → ler → prototipar → registrar o que aprendi**. Cada fonte tem status, prioridade e esforço estimado; cada semana tem no máximo três itens; cada protótipo termina com um resultado público.

## Como funciona

1. **Captura.** Links, PDFs e tópicos chegam por um bot do Telegram (o resumo volta com botões Publicar/Descartar; ver [pipeline/SETUP.md](pipeline/SETUP.md)) ou em `inbox/` (importados do WhatsApp/X ou colados à mão).
2. **Triagem.** Cada item vira uma nota em `sources/<area>/` com resumo curto, esforço e prioridade.
3. **Estudo semanal.** Um plano em `study/weeks/` escolhe uma fonte para ler, uma para prototipar e uma para revisar.
4. **Protótipo.** Fontes que valem a prática viram um mini-projeto em `labs/`, com critério de pronto e seção "O que aprendi".

Detalhes das convenções em [CLAUDE.md](CLAUDE.md) e da cadência em [study/plan.md](study/plan.md).

<!-- BEGIN:INDEX -->
**Fontes:** 27 · **Labs:** 1

**Fontes por status:** triaged: 26 · reading: 1 · noted: 0 · prototyped: 0 · archived: 0

## Áreas

| Área | Fontes | Lendo | Anotadas | Prototipadas |
|---|---|---|---|---|
| [computer-vision](sources/computer-vision/README.md) | 8 | 1 | 0 | 0 |
| [genai](sources/genai/README.md) | 8 | 0 | 0 | 0 |
| [mlops](sources/mlops/README.md) | 1 | 0 | 0 | 0 |
| [nlp](sources/nlp/README.md) | 1 | 0 | 0 | 0 |
| [recsys](sources/recsys/README.md) | 9 | 0 | 0 | 0 |

## Em andamento

- Lendo: [VideoMAE V2 and V-JEPA (explainer)](sources/computer-vision/videomae-v2-and-v-jepa-explainer.md)
- Lab: [Estabilidade do nDCG na avaliação offline de recomendadores](labs/ndcg-stability/README.md)

## Próximos na fila (top 10)

| Fonte | Área | Prioridade | Esforço | Salva em |
|---|---|---|---|---|
| [Temporal video scene segmentation using deep-learning](sources/computer-vision/temporal-video-scene-segmentation-deep-learning.md) | computer-vision | 1 | 1h | 2024-01-11 |
| [Action Segmentation Through Self-Supervised Video Features and Positional-Encoded Embeddings](sources/computer-vision/action-segmentation-self-supervised-features.md) | computer-vision | 1 | weekend | 2024-02-26 |
| [MAPS: Netflix's Multimodal Asset Personalization at Scale](sources/recsys/maps-multimodal-asset-personalization-netflix.md) | recsys | 1 | 1h | 2026-09-01 |
| [Next Best Action: Causal Constrained Offline RL for Business Action Targeting](sources/recsys/next-best-action-causal-constrained-offline-rl.md) | recsys | 1 | weekend | 2026-09-27 |
| [Omni-Interactive Universal Embedder (OmniUE)](sources/computer-vision/omniue-omni-interactive-universal-embedder.md) | computer-vision | 1 | 1h | 2026-09-27 |
| [Your nDCG Score May Be Correct. But the Conclusion? Stability-Aware Offline Recommender Evaluation](sources/recsys/ndcg-stability-aware-offline-evaluation.md) | recsys | 1 | weekend | 2026-09-29 |
| [Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents](sources/genai/harness-engineering-coding-agents.md) | genai | 1 | weekend | 2026-10-06 |
| [StimuVAR: Spatiotemporal Stimuli-aware Video Affective Reasoning with MLLMs](sources/computer-vision/stimuvar-video-affective-reasoning.md) | computer-vision | 2 | 1h | 2024-11-27 |
| [The Lifecycle of LLM-as-a-Judge: Building, Aligning, and Monitoring at Scale](sources/genai/llm-as-a-judge-lifecycle-netflix.md) | genai | 2 | weekend | 2026-09-04 |
| [Bootstrapping Conversational Recommendation Agents at Spotify](sources/recsys/bootstrapping-conversational-recsys-agents-spotify.md) | recsys | 2 | weekend | 2026-09-27 |

## Labs concluídos

_Nenhum ainda._
<!-- END:INDEX -->

## Licença

[MIT](LICENSE). As notas são resumos e comentários próprios; os trabalhos citados pertencem aos seus autores.
