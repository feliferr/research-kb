#!/usr/bin/env python3
"""Passo 4: aplica a decisão tomada nos botões do Telegram (publicar ou descartar).

Uso (repositório público na raiz, com token de push; privado em ./private):
  PAYLOAD='{"id","action":"publish|drop","chat_id","message_id"}' python3 pipeline/scripts/apply_decision.py --private private

Publicar: copia o rascunho para sources/<area>/<slug>.md, regenera os índices, roda o denylist
e envia o commit ao repositório público. Idempotente: decidir duas vezes não repete nada.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import kbpipe as kp

ROOT = kp.KB_ROOT


def run(*cmd) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def free_dest(area: str, slug: str) -> Path:
    dest = ROOT / "sources" / area / f"{slug}.md"
    n = 2
    while dest.exists():
        dest = ROOT / "sources" / area / f"{slug}-{n}.md"
        n += 1
    return dest


def publish_once(text: str, meta: dict) -> tuple:
    """Parte do estado limpo de origin, escreve a nota e tenta empurrar. Retorna (caminho, erro)."""
    branch = kp.current_branch(ROOT)
    kp.configure_git(ROOT)
    kp.git(ROOT, "fetch", "-q", "origin", branch)
    kp.git(ROOT, "reset", "-q", "--hard", f"origin/{branch}")
    dest = free_dest(meta["area"], kp.ii.ascii_slug(meta["title"], 60))
    dest.write_text(text, encoding="utf-8")
    for cmd in (("python3", "scripts/build_index.py"), ("python3", "scripts/build_index.py", "--check"),
                ("python3", "scripts/check_denylist.py")):
        out = run(*cmd)
        if out.returncode != 0:
            kp.git(ROOT, "reset", "-q", "--hard", f"origin/{branch}")
            kp.git(ROOT, "clean", "-fdq", "--", "sources")
            return None, (out.stderr or out.stdout).strip()[:300]
    rel = dest.relative_to(ROOT).as_posix()
    kp.git(ROOT, "add", "--", "sources", "README.md")
    kp.git(ROOT, "commit", "-q", "-m", f"Adiciona fonte: {meta['title'][:80]}")
    if kp.git(ROOT, "push", "-q", "origin", f"HEAD:{branch}", check=False).returncode != 0:
        return None, "RETRY"
    return rel, ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", required=True, type=Path)
    args = ap.parse_args()

    p = kp.payload_from_env()
    cid = kp.check_id(p.get("id"))
    action = p.get("action")
    if action not in ("publish", "drop"):
        raise SystemExit("action inválida")
    chat_id, message_id = p.get("chat_id"), p.get("message_id")
    if not isinstance(chat_id, int):
        raise SystemExit("chat_id inválido")
    message_id = message_id if isinstance(message_id, int) else None

    cap_path = args.private / "captures" / f"{cid}.json"
    if not cap_path.is_file():
        kp.edit_or_send(chat_id, message_id, "❓ Não encontrei essa captura.")
        return
    cap = kp.load_json(cap_path)
    title = cap.get("title", cid)

    if cap.get("status") != "pending":
        state = {"published": f"✅ Já publicado: {cap.get('published_path', '')}", "dropped": "🗑 Já descartado."}.get(
            cap.get("status"), f"ℹ️ Nada a fazer (status: {cap.get('status')}).")
        kp.edit_or_send(chat_id, message_id, f"{title}\n{state}")
        return

    if action == "drop":
        cap["status"] = "dropped"
        kp.save_json(cap_path, cap)
        kp.commit_push(args.private, [cap_path], f"capture {cid}: descartada")
        kp.edit_or_send(chat_id, message_id, f"🗑 Descartado: {title}")
        return

    draft = args.private / "drafts" / f"{cid}.md"
    text = draft.read_text(encoding="utf-8")
    meta, errors = kp.validate_draft(text)
    if errors:
        kp.edit_or_send(chat_id, message_id, f"⚠️ Rascunho inválido, nada publicado: {'; '.join(errors[:3])}")
        return

    rel, err = None, ""
    for _ in range(4):
        rel, err = publish_once(text, meta)
        if rel or err != "RETRY":
            break
    if not rel:
        detail = "o repositório mudou durante a publicação" if err == "RETRY" else err
        kp.edit_or_send(chat_id, message_id, f"⛔ Não publiquei '{title}': {detail}. O rascunho segue pendente; toque de novo para tentar.",
                        keyboard=kp.approval_keyboard(cid))
        sys.exit(1)

    cap["status"] = "published"
    cap["published_path"] = rel
    kp.save_json(cap_path, cap)
    kp.commit_push(args.private, [cap_path], f"capture {cid}: publicada")
    kp.edit_or_send(chat_id, message_id, f"✅ Publicado: {title}\nhttps://github.com/{kp.kb_repo()}/blob/main/{rel}")


if __name__ == "__main__":
    try:
        main()
    except kp.TelegramError as e:
        sys.exit(f"erro do Telegram: {e}")
