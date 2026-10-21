# research-kb-inbox (privado)

Área de passagem do pipeline do [research-kb](https://github.com/feliferr/research-kb). **Este repositório deve ser privado**: guarda o que foi enviado ao bot do Telegram antes de você aprovar a publicação.

- `captures/<id>.json`: cada mensagem recebida (inclui o seu comentário original) e o estado (`triaging`, `pending`, `published`, `dropped`, `failed`, `duplicate`, `rejected_private`…).
- `drafts/<id>.md`: rascunho de nota gerado pelo Claude, aguardando os botões Publicar/Descartar. Só o aprovado vai para o repositório público.
- `.github/workflows/`: `capture`, `decision` e `weekly` (no repositório público ficam em `pipeline/private-repo/workflows/`). A lógica fica em `pipeline/scripts/` do repositório público; estes arquivos só orquestram.

Configuração e operação: [`pipeline/SETUP.md`](https://github.com/feliferr/research-kb/blob/main/pipeline/SETUP.md). Como o sistema funciona, com diagramas: [`pipeline/ARCHITECTURE.md`](https://github.com/feliferr/research-kb/blob/main/pipeline/ARCHITECTURE.md).
