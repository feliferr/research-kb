---
name: novo-lab
description: Cria um mini-projeto de prototipação em labs/ a partir de uma fonte. Use quando o usuário quiser praticar, replicar ou prototipar algo de uma fonte já catalogada. Também acionada por /novo-lab.
---

# Novo lab

Entrada: o caminho ou título de uma fonte em `sources/` (ou uma descrição, caso em que primeiro se cataloga a fonte com `nova-fonte`).

## Passos

1. **Checar WIP**: se já houver um lab `in-progress` (ver `python3 scripts/build_index.py --queue`), avise e crie o novo como `planned`.
2. **Ler a fonte** catalogada, em especial "O que dá para replicar ou testar". Se a nota estiver rasa, leia a fonte de novo antes de planejar.
3. **Criar** `labs/<slug>/README.md` a partir de `templates/lab.md`:
   - `source:` com o caminho da fonte; `started` só quando o status for `in-progress`.
   - **Objetivo em uma frase** e **critério de pronto** mensuráveis, definidos agora.
   - **Baseline** explícito. Sem baseline, não há resultado.
   - 3 a 5 tarefas de 1 a 2 horas cada.
4. **Esqueleto mínimo** ao lado do README, só o necessário para a primeira tarefa (ex.: `requirements.txt` e um `run.py` com `argparse`). Datasets e checkpoints ficam fora do git; o README diz onde baixar (fontes públicas) e como.
5. Atualize a fonte: `status: prototyped` só quando o lab chegar a `done`; por ora, registre no Log da fonte o link para o lab.
6. `python3 scripts/build_index.py` e responda: caminho, objetivo, critério de pronto e a primeira tarefa.

## Cuidados

- Nunca preencha "Resultados" com números que não foram medidos.
- Repositório público: datasets públicos apenas; nada de dados ou código de empresa.
- Para o lab virar `done`: seção "O que aprendi" preenchida e resultado reproduzível.
