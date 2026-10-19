#!/usr/bin/env bash
# Cria a pasta do repositório privado (workflows + pastas de dados) a partir de pipeline/private-repo/.
# Uso: bash pipeline/scripts/bootstrap_private.sh /caminho/para/research-kb-inbox
set -euo pipefail
dest="${1:?uso: bootstrap_private.sh <pasta-de-destino>}"
src="$(cd "$(dirname "${BASH_SOURCE[0]}")/../private-repo" && pwd)"
if [ -e "$dest" ] && [ -n "$(ls -A "$dest" 2>/dev/null)" ]; then
  echo "erro: $dest já existe e não está vazia" >&2
  exit 1
fi
mkdir -p "$dest/.github"
cp -R "$src"/. "$dest"/
mv "$dest/workflows" "$dest/.github/workflows"   # no template ficam fora de .github para não rodarem neste repositório
mkdir -p "$dest/captures" "$dest/drafts"
touch "$dest/captures/.gitkeep" "$dest/drafts/.gitkeep"
git -C "$dest" init -q -b main
git -C "$dest" add -A
git -C "$dest" commit -q -m "Estrutura inicial do pipeline (workflows e pastas de dados)"
cat <<MSG
Pronto: $dest

Próximos passos:
  1. Crie no GitHub um repositório PRIVADO vazio (ex.: research-kb-inbox), sem README nem .gitignore.
  2. cd "$dest" && git remote add origin git@github.com:<seu-usuario>/research-kb-inbox.git && git push -u origin main
  3. Siga pipeline/SETUP.md (segredos, Worker e webhook).
MSG
