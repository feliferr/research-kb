#!/usr/bin/env python3
"""Falha se algum termo de .github/denylist.txt aparecer em arquivos de texto do repositório.

Uso: python3 scripts/check_denylist.py
Termos (um por linha, sem diferenciar maiúsculas); linhas com # são comentários.
Somente biblioteca padrão. Ignora .git, inbox/raw e o próprio arquivo de termos.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DENYLIST = ROOT / ".github" / "denylist.txt"
SKIP_DIRS = {".git", "raw", "__pycache__", ".venv"}
TEXT_SUFFIXES = {".md", ".py", ".txt", ".yml", ".yaml", ".json", ".toml", ".ipynb", ".cfg", ".sh", ".csv"}


def main():
    if not DENYLIST.exists():
        print("sem denylist: nada a checar")
        return
    terms = [
        line.strip().lower()
        for line in DENYLIST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not terms:
        print("ok: denylist vazia (preencha .github/denylist.txt)")
        return
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == DENYLIST:
            continue
        if SKIP_DIRS & set(path.relative_to(ROOT).parts) or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8").lower()
        except (UnicodeDecodeError, OSError):
            continue
        for term in terms:
            if term in text:
                hits.append(f"{path.relative_to(ROOT)}: contém '{term}'")
    if hits:
        print("Termos proibidos encontrados:", file=sys.stderr)
        for h in hits:
            print(f"  - {h}", file=sys.stderr)
        sys.exit(1)
    print(f"ok: nenhum dos {len(terms)} termos proibidos encontrado")


if __name__ == "__main__":
    main()
