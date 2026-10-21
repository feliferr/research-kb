---
title: "The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery"
area: genai
kind: paper
authors: [Robert Tjarko Lange, Luca Grillotti, Yutaro Yamada, Rujikorn Charakorn, David Ha]
year: 2026
priority: 2
effort: weekend
tags: [agents, coding-agents, orchestration, automated-research, multi-agent]
url: https://arxiv.org/pdf/2610.18933
saved: 2026-10-20
origin: telegram
status: triaged
---

> **Resumo:** O paper propõe o Agentic Scientist, um pipeline distribuído em que agentes de código e pesquisadores humanos conduzem juntos pesquisa computacional, com um meta-controlador que roda agentes em paralelo e verifica cada etapa por rubricas. Os autores argumentam, com ablações, que a camada de orquestração pesa tanto quanto o modelo base para a confiabilidade. Foi lido apenas o abstract/resumo da página do arXiv, não o PDF completo.

## Contribuição principal

- Pipeline em etapas: rascunho da tarefa, geração de ideias, planejamento, experimentos em sandbox, agregação de resultados, baselines e ablações, análise e relatório, com agentes de código executando e autoverificando cada etapa.
- Meta-controlador que coordena agentes paralelos e aplica verificação por rubricas a cada passo, buscando evitar ideias estreitas e busca míope (hill-climbing) de agentes totalmente autônomos.
- Camada de orquestração reutilizável entre domínios, com autonomia ajustável: co-cientista guiado por humanos ou investigação de ponta a ponta.
- Segundo a página, um paper feito com uma versão de desenvolvimento foi aceito no ALIFE 2026 (a verificar no texto completo).

## O que dá para replicar ou testar

Montar um mini-orquestrador: um agente de código executa um experimento pequeno em sandbox e um segundo agente o avalia por uma rubrica fixa; comparar com o agente único sem verificação em uma tarefa de ML simples e pública.

## Por que me interessa

Interesse geral em como orquestração e verificação por rubricas tornam agentes de código mais confiáveis em tarefas longas.

## Estimativa de esforço

- **Leitura:** cerca de 1h, focando em arquitetura do pipeline e ablações.
- **Protótipo:** fim de semana, versão reduzida sem GPU dedicada.

## Pontos a verificar

- (a verificar) o PDF completo não foi lido; detalhes de método, rubricas, métricas e resultados das ablações não foram confirmados.
- (a verificar) alcance real das demonstrações autônomas em problemas abertos de ML.
- (a verificar) se há código ou repositório público disponível.

## Log

- 2026-10-20: fonte triada (automático, via Telegram).
