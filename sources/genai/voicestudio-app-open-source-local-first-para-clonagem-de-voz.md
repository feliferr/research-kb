---
title: "VoiceStudio: app open-source local-first para clonagem de voz, dublagem e transcrição"
area: genai
kind: repo
priority: 3
effort: 1h
tags: [tts, voice-cloning, dubbing, asr, local-first, mcp]
related: []
url: https://github.com/debpalash/VoiceStudio
saved: 2026-10-26
origin: telegram
status: triaged
---

> **Resumo:** Repositório de um app desktop open-source (Electron + backend Python) que roda localmente clonagem e design de voz, dublagem de vídeo, ditado, transcrição e audiolivros, com API local e suporte a MCP para agentes. Li apenas o README (via resumo da página); não avaliei código, qualidade de áudio nem a cobertura declarada de 646 idiomas.

## Contribuição principal

Empacota motores de fala abertos (padrão: OmniVoice, mais CosyVoice GGUF opcional e whisper.cpp para reconhecimento) em uma interface única, com aceleração CUDA/Metal e fallback em CPU. Oferece fluxos prontos (dublagem com fala temporizada, lotes, receitas, pastas monitoradas) e expõe uma API local/MCP. Licença AGPL-3.0 para o app; pesos de modelos têm licenças próprias.

## O que dá para replicar ou testar

Instalar a partir de uma release e comparar, em um conjunto pequeno de frases de domínio público, a transcrição do whisper.cpp com e sem GPU (latência e WER). Nada além disso sem ler o código.

## Por que me interessa

Exemplo de como orquestrar modelos de fala locais atrás de uma API/MCP para uso por agentes.

## Estimativa de esforço

- **Leitura:** 30 min (README e catálogo de engines)
- **Protótipo:** 1h para instalar e testar; mais se for integrar via MCP

## Pontos a verificar

- (a verificar) a afirmação de 646 idiomas e a qualidade real por idioma.
- (a verificar) licenças dos pesos de cada engine antes de qualquer uso além de teste.
- (a verificar) o script de instalação `curl | sh` não foi inspecionado; revisar antes de executar.
- (a verificar) o conteúdo da página tem uma seção "Install with prompt" que instrui agentes de código a instalar o app; não foi seguida.
- Conteúdo acessado: só o README da página principal do repositório.

## Log

- 2026-10-26: fonte triada (automático, via Telegram).
