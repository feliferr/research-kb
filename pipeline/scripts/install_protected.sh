#!/usr/bin/env bash
# Copia para os lugares onde o Claude Code e o GitHub os procuram dois arquivos que ficam em pipeline/install/:
#   .claude/skills/triar-captura/SKILL.md   (skill usada pelo workflow de triagem)
#   .github/workflows/pipeline-tests.yml    (CI dos testes do pipeline neste repositório)
# Rode uma vez, na raiz do repositório: bash pipeline/scripts/install_protected.sh
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$root/.claude/skills/triar-captura" "$root/.github/workflows"
cp "$root/pipeline/install/triar-captura/SKILL.md" "$root/.claude/skills/triar-captura/SKILL.md"
cp "$root/pipeline/install/pipeline-tests.yml" "$root/.github/workflows/pipeline-tests.yml"
echo "instalado: .claude/skills/triar-captura/SKILL.md e .github/workflows/pipeline-tests.yml"
