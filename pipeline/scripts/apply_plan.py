#!/usr/bin/env python3
"""Aplica o patch do plano semanal gerado pelo modelo, depois de checar o que ele toca.

Uso (repositório público na raiz, com token de push):
  python3 pipeline/scripts/apply_plan.py --patch work/plan.patch

Só aceita mudanças em study/weeks/AAAA-Www.md, sources/<area>/<nota>.md e nos READMEs de índice.
Depois do patch: regenera os índices, valida e roda o denylist antes de empurrar.
Saída (GITHUB_OUTPUT): applied=true|false.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import kbpipe as kp

ROOT = kp.KB_ROOT
ALLOWED = [
    re.compile(r"^study/weeks/\d{4}-W\d{2}\.md$"),
    re.compile(r"^sources/[a-z0-9-]+/[a-z0-9][a-z0-9-]*\.md$"),
    re.compile(r"^sources/[a-z0-9-]+/README\.md$"),
    re.compile(r"^README\.md$"),
]


def patch_paths(patch: Path) -> list:
    out = subprocess.run(["git", "apply", "--numstat", "-z", str(patch)], cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"patch inválido: {out.stderr.strip()[:200]}")
    paths = []
    for rec in out.stdout.split("\0"):
        if rec.strip():
            paths.append(rec.split("\t")[-1].strip())
    return paths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--patch", required=True, type=Path)
    args = ap.parse_args()

    if not args.patch.is_file() or args.patch.stat().st_size == 0:
        print("patch vazio: nada a aplicar")
        kp.set_output("applied", "false")
        return
    paths = patch_paths(args.patch)
    bad = [p for p in paths if not any(rx.match(p) for rx in ALLOWED)]
    if bad:
        raise SystemExit("patch toca arquivos não permitidos: " + ", ".join(bad[:5]))
    if not paths:
        raise SystemExit("patch sem arquivos")

    branch = kp.current_branch(ROOT)
    kp.configure_git(ROOT)
    for attempt in range(4):
        kp.git(ROOT, "fetch", "-q", "origin", branch)
        kp.git(ROOT, "reset", "-q", "--hard", f"origin/{branch}")
        if subprocess.run(["git", "apply", "--index", str(args.patch)], cwd=ROOT, capture_output=True, text=True).returncode != 0:
            raise SystemExit("o patch não aplica sobre a versão atual do repositório")
        for cmd in (("python3", "scripts/build_index.py"), ("python3", "scripts/build_index.py", "--check"),
                    ("python3", "scripts/check_denylist.py")):
            out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if out.returncode != 0:
                kp.git(ROOT, "reset", "-q", "--hard", f"origin/{branch}")
                raise SystemExit("validação falhou: " + (out.stderr or out.stdout).strip()[:300])
        kp.git(ROOT, "add", "--", "study", "sources", "README.md")
        week = next((Path(p).stem for p in paths if p.startswith("study/weeks/")), "semana")
        kp.git(ROOT, "commit", "-q", "-m", f"Plano de estudo {week}")
        if kp.git(ROOT, "push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            kp.set_output("applied", "true")
            return
    raise SystemExit("push falhou após várias tentativas")


if __name__ == "__main__":
    main()
