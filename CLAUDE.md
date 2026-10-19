# research-kb

Base de conhecimento pública e pessoal sobre IA aplicada. Idioma dos documentos: português (termos técnicos em inglês quando for o uso comum).

## Regra de ouro: este repositório é público

- Só entra material público: papers, documentação, repositórios abertos, threads públicas e comentários próprios.
- Nunca incluir informação de empregadores atuais ou anteriores: código, dados, números, arquiteturas internas, nomes de sistemas internos ou resultados de projetos de empresa. Ao relacionar uma fonte com trabalho profissional, escreva só a lição geral, sem detalhes internos.
- O conteúdo bruto exportado do WhatsApp fica em `inbox/raw/` (ignorado pelo git). Nunca commitar mensagens pessoais.
- `scripts/check_denylist.py` falha o CI se algum termo de `.github/denylist.txt` aparecer. Mantenha a lista atualizada.

## Estrutura

- `inbox/<data>-<slug>.md`: itens crus ainda não triados (url, data, origem, nota original). **Local e ignorado pelo git** (contém anotações pessoais); só as fontes triadas vão para o repositório. `inbox/raw/` também é ignorado.
- `sources/<area>/<slug>.md`: uma fonte por arquivo. Áreas: `computer-vision`, `nlp`, `recsys`, `genai`, `mlops`.
- `sources/<area>/README.md`: descrição da área + índice gerado (não editar entre `<!-- BEGIN:INDEX -->` e `<!-- END:INDEX -->`).
- `labs/<slug>/README.md`: um protótipo por pasta, com código e resultados ao lado.
- `study/plan.md`: cadência, orçamento de horas e limite de WIP.
- `study/weeks/AAAA-Www.md`: plano e retro de cada semana.
- `templates/`: modelos de fonte, lab e semana.
- `scripts/build_index.py`: regenera os índices, valida o frontmatter e calcula a fila priorizada.
- `scripts/import_inbox.py`: importa exportação do WhatsApp ou lista de URLs para `inbox/`.
- `.claude/skills/`: `nova-fonte`, `triar-inbox`, `estudo-semanal`, `novo-lab`.

## Convenções

- Frontmatter de fonte, obrigatório: `title`, `area` (igual ao nome da pasta), `kind`, `status`, `saved`. Demais: `url`, `authors`, `year`, `priority` (1 alta, 2 média, 3 baixa), `effort` (`1h`, `weekend`, `project`), `origin`, `tags`, `related`.
- Status de fonte: `triaged` → `reading` → `noted` → `prototyped` → `archived`. Fontes arquivadas não são apagadas; registre o motivo no Log.
- Status de lab: `planned`, `in-progress`, `done`, `abandoned`. Frontmatter: `title`, `area`, `status`; opcionais `source`, `tags`, `started`.
- Limite de WIP: no máximo 1 fonte em `reading` e 1 lab `in-progress`, salvo mudança em `study/plan.md`.
- Nunca fabrique referências, resultados ou números. Resumo só a partir do conteúdo realmente lido; o que for lembrado e não confirmado fica marcado `(a verificar)`. Se não conseguir acessar a fonte, diga isso na nota em vez de resumir de memória.
- Não copie trechos longos de papers ou artigos. Resuma com palavras próprias; citações curtas e atribuídas são aceitáveis.
- Nomes de arquivo: kebab-case ASCII, sem data (exceto itens de `inbox/` e `study/weeks/`).
- Após qualquer mudança em fontes ou labs, rode `python3 scripts/build_index.py`.
- Triagem de itens de `inbox/`: skill `triar-inbox`. Fonte nova avulsa: skill `nova-fonte`. Plano da semana: skill `estudo-semanal`. Protótipo: skill `novo-lab`.
