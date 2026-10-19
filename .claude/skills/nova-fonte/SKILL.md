---
name: nova-fonte
description: Cataloga uma fonte (paper, doc, repositório, thread, vídeo) em sources/. Use quando o usuário colar um link ou paper para guardar/estudar, ou ao triar um item de inbox/. Também acionada por /nova-fonte.
---

# Catalogar nova fonte

Entrada: um link, um PDF anexado, ou um item de `inbox/`. Pode vir com uma nota do usuário.

## Passos

1. **Duplicata**: busque a URL (e o id do arXiv, se houver) em `sources/` e `inbox/` (`grep -rl`). Se já existir, não crie outra: informe o caminho e, se fizer sentido, atualize o Log da existente.
2. **Ler de verdade**: obtenha o conteúdo (WebFetch; para arXiv, o resumo e as seções relevantes; conectores como alphaXiv se estiverem disponíveis). Se não conseguir acessar a fonte, **não resuma de memória**: crie a nota com os metadados que você tem, escreva "conteúdo não acessado" no resumo e liste o que falta em "Pontos a verificar".
3. **Classificar a área** entre as pastas de `sources/` (`computer-vision`, `nlp`, `recsys`, `genai`, `mlops`). Decida e informe, sem perguntar. Se tocar em outra área, use `tags`.
4. **Criar o arquivo** `sources/<area>/<slug>.md` a partir de `templates/source.md`:
   - `slug`: kebab-case ASCII curto (sem acentos, sem data).
   - `status: triaged`; `saved` = data original do item de inbox, ou hoje se for avulso; `origin` conforme o item.
   - `kind`, `authors`, `year` só se constarem na fonte.
   - `priority` e `effort` são **propostas** suas (1 a 3; `1h`, `weekend`, `project`); o usuário pode ajustar.
   - Resumo com palavras próprias. Não copie trechos longos.
   - "O que dá para replicar" deve ser concreto e pequeno (dataset público, baseline, uma ablação).
5. **Itens de inbox**: depois de criar a nota, remova o arquivo correspondente de `inbox/`.
6. **Regenerar índices**: `python3 scripts/build_index.py`.
7. **Responder** curto: caminho, área, prioridade/esforço propostos e, se houver, uma pergunta ou risco relevante.

## Cuidados

- Repositório público: nada de informação de empregadores. Se o usuário citar trabalho profissional, registre só a lição geral.
- Referências só se verificadas; o resto vai como `(a verificar)`.
