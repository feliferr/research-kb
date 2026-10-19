---
name: triar-inbox
description: Tria em lote os itens de inbox/, transformando cada um em uma nota de fonte. Use quando o usuário pedir para triar, processar o acúmulo ou limpar o inbox. Também acionada por /triar-inbox.
---

# Triar inbox

Entrada opcional: limite de itens (ex.: "os 10 mais antigos"). Sem limite, processe até 15 por execução e avise quantos restam.

## Passos

1. Liste `inbox/*.md` (ignore `README.md` e `inbox/raw/`), do mais antigo para o mais novo.
2. Para cada item, aplique a skill `nova-fonte` sem pedir confirmação. Itens cujo conteúdo não pôde ser acessado entram com "conteúdo não acessado" em vez de resumo inventado.
3. Antes de triar, descarte do repositório (mova para `inbox/raw/descartados/`) o que for pessoal ou não técnico: documentos financeiros, de identidade, saúde, trabalho de empregadores, convites de reunião, vagas, religião etc. O repositório é público; na dúvida, não triar e perguntar.
3b. Links de LinkedIn, X e Facebook costumam exigir login: tente uma vez; se não abrir, deixe o item no inbox e conte no relatório.
4. Itens sem URL e sem anexo (notas soltas) viram fonte só se tiverem substância; caso contrário, deixe em `inbox/` e liste no relatório.
5. Ao final, rode `python3 scripts/build_index.py`.
6. Responda com um relatório curto:
   - quantos foram triados, quantos ficaram (e por quê);
   - o top 3 da fila (`python3 scripts/build_index.py --queue`);
   - itens candidatos a arquivar de imediato (baixa prioridade, sem conexão com os temas atuais), **como sugestão**; não arquive sem o usuário confirmar.

## Cuidados

- Triagem em lote não é licença para resumir sem ler: a regra de não inventar vale para cada item.
- Seja consistente nas tags: reutilize as existentes (`grep -rh '^tags:' sources/`).
