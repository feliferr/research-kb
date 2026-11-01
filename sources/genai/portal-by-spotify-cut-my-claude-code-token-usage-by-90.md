---
title: Portal by Spotify cut my Claude Code token usage by 90%
area: genai
kind: blog
authors: [Dimitri Mazmanov]
year: 2026
priority: 2
effort: 1h
tags: [coding-agents, model-routing, token-cost, claude-code, hooks]
related: []
url: https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
saved: 2026-11-01
origin: telegram
status: triaged
---

> **Resumo:** O post descreve como delegar trabalho de I/O de um agente de código (ler muitos arquivos, gerar boilerplate) a um modelo mais barato, deixando o modelo de fronteira para o raciocínio. O autor reporta cerca de 90% de economia de tokens em leituras em lote num monorepo Java, com limites claros para edição e raciocínio. Conteúdo lido a partir de uma extração da página, não do texto integral.

## Contribuição principal

Roteamento de modelos como configuração: dois "modos" declarativos (um que resume vários arquivos para responder a uma pergunta, outro que gera arquivos seguindo padrões existentes) rodam num modelo barato. Um plugin aplica o roteamento em três camadas: hooks que bloqueiam leituras grandes (limite padrão de 350 linhas, configurável), scripts que encapsulam as chamadas e skills que orientam o agente. Os hooks garantem o roteamento mesmo se a skill for ignorada.

Limitações citadas pelo autor: edição não pode ser delegada (resumos sem números de linha confiáveis), raciocínio também não (o worker deixou passar um bug sutil de thread-safety), e cada delegação adiciona de 10 a 30 segundos de latência.

## O que dá para replicar ou testar

Um hook simples que bloqueia leituras de arquivos acima de N linhas e redireciona para um script que resume com um modelo barato; medir tokens do contexto principal antes e depois numa tarefa de leitura de vários arquivos em um repositório aberto.

## Por que me interessa

Controle de custo e divisão de trabalho entre modelos em agentes de código.

## Estimativa de esforço

- **Leitura:** 15 a 20 min
- **Protótipo:** algumas horas para um hook e um script de resumo

## Pontos a verificar

- (a verificar) O número de 90% vem de testes do próprio autor em quatro cenários num único monorepo; metodologia e reprodutibilidade não foram checadas.
- (a verificar) Estatísticas de mercado citadas (previsão da Gartner, gastos por desenvolvedor) não foram confirmadas na fonte original.
- (a verificar) O post foi lido via extração automática; detalhes e números podem ter perdido nuance.

## Log

- 2026-11-01: fonte triada (automático, via Telegram).
