---
name: estudo-semanal
description: Monta o plano de estudo da semana (um item para ler, um para prototipar, um para revisar) e fecha a retro da semana anterior. Use no ritual semanal ou quando o usuário pedir o plano/cronograma de estudo. Também acionada por /estudo-semanal.
---

# Plano de estudo semanal

## Passos

1. **Contexto**: leia `study/plan.md` (orçamento de horas, limite de WIP, regras) e o plano da semana anterior, se existir, em `study/weeks/`.
2. **Fechar a retro anterior**: pergunte ao usuário (uma única vez, de forma curta) o que foi feito. Com a resposta, preencha a retro e atualize status: leitura concluída → `noted`; lab concluído → `done` e a fonte → `prototyped`; abandonado → `archived`/`abandoned` com motivo no Log. Se o usuário não responder, deixe a retro em branco e siga.
3. **Fila**: rode `python3 scripts/build_index.py --queue`. Ela traz o WIP atual e as fontes `triaged` ordenadas por prioridade e antiguidade, com marcação de paradas há mais de 60 dias.
4. **Escolher os 3 itens**, respeitando o WIP:
   - **Ler:** a melhor fonte `triaged` cuja leitura caiba no orçamento (considere `effort`). Se já houver uma em `reading`, ela continua e nada novo entra.
   - **Prototipar:** um lab `in-progress` existente; senão, a fonte `noted` mais promissora (proponha a skill `novo-lab`); senão, "nenhum nesta semana".
   - **Revisar:** uma fonte `noted` ou `prototyped` de revisão rápida (≈ 20 min).
5. **Criar** `study/weeks/AAAA-Www.md` (semana ISO; `python3 -c "import datetime;print(datetime.date.today().strftime('%G-W%V'))"`) a partir de `templates/week.md`. Ajuste os tempos ao orçamento de `study/plan.md`. Mude a fonte escolhida para `reading` e registre no Log dela.
6. **Itens parados**: liste as fontes marcadas como paradas (> 60 dias) na seção própria, como **sugestão** de agir ou arquivar. Nunca arquive sem confirmação.
7. `python3 scripts/build_index.py` e responda com o plano em poucas linhas.

## Cuidados

- Máximo de 3 itens. Se o usuário pedir mais, lembre o limite de WIP e o orçamento antes de ceder.
- Se a fila estiver vazia, diga isso e sugira rodar `triar-inbox`.
