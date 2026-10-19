#!/usr/bin/env python3
"""Passo 1 do pipeline: valida uma captura vinda do Telegram e prepara a triagem.

Uso (no workflow, com o repositório público na raiz e o privado em ./private):
  PAYLOAD='<json>' python3 pipeline/scripts/process_capture.py --private private --work work

Payload (um item por despacho; o Worker separa várias URLs):
  {"id", "chat_id", "message_id", "date", "text", "url" | null, "attachment": {file_id, file_name, file_size, mime_type} | null}

Saídas (GITHUB_OUTPUT): triage=true|false, id=<id>.
Grava captures/<id>.json no repositório privado e, se a captura for triável, work/capture.json
(+ work/attachment.txt para PDFs) para o job que roda o modelo.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import kbpipe as kp

MAX_TEXT = 2000
MAX_ATTACHMENT_TEXT = 60000
REJECTIONS = {
    "duplicate": "♻️ Já tenho isso: {detail}",
    "rejected_private": "🔒 Link privado (reunião, drive, calendário…): não vou triar nem publicar.",
    "too_big": "📦 Arquivo grande demais para o bot (limite de 20 MB). Mande o link, ou triamos depois no computador.",
    "unsupported": "📎 Só consigo ler PDFs por aqui. Mande o link do material.",
    "empty": "🤔 Não encontrei link, PDF nem tópico nessa mensagem.",
    "failed": "⚠️ Não consegui processar: {detail}",
}


def clean(payload: dict) -> dict:
    cid = kp.check_id(payload.get("id"))
    date = payload.get("date")
    if not isinstance(date, str) or not kp.DATE_RE.fullmatch(date):
        raise SystemExit("date inválida")
    chat_id, message_id = payload.get("chat_id"), payload.get("message_id")
    if not isinstance(chat_id, int) or not isinstance(message_id, int):
        raise SystemExit("chat_id/message_id devem ser inteiros")
    text = payload.get("text") or ""
    if not isinstance(text, str):
        raise SystemExit("text inválido")
    url = payload.get("url") or ""
    if url:
        url = ii_clean(url)
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.netloc or len(url) > 2048:
            raise SystemExit("url inválida")
    att = payload.get("attachment") or None
    if att is not None:
        if not isinstance(att, dict) or not isinstance(att.get("file_id"), str):
            raise SystemExit("attachment inválido")
        att = {
            "file_id": att["file_id"],
            "file_name": re.sub(r"[^\w.\- ]", "_", str(att.get("file_name") or "arquivo"))[:120],
            "file_size": int(att.get("file_size") or 0),
            "mime_type": str(att.get("mime_type") or "")[:80],
        }
    return {"id": cid, "chat_id": chat_id, "message_id": message_id, "date": date,
            "text": text[:MAX_TEXT].strip(), "url": url, "attachment": att, "origin": "telegram"}


def ii_clean(url: str) -> str:
    return kp.ii.clean_url(str(url).strip())


def known_elsewhere(url: str, private: Path):
    """Procura a URL em sources/ (público) e nas capturas já recebidas (privado)."""
    key = kp.ii.normalize_url(url)
    for f in sorted((kp.KB_ROOT / "sources").rglob("*.md")):
        for m in re.finditer(r"^url:\s*(\S+)", f.read_text(encoding="utf-8"), re.M):
            if kp.ii.normalize_url(m.group(1)) == key:
                return f"já está em {f.relative_to(kp.KB_ROOT).as_posix()}"
    for f in sorted((private / "captures").glob("*.json")):
        try:
            other = kp.load_json(f)
        except ValueError:
            continue
        if other.get("url") and kp.ii.normalize_url(other["url"]) == key and other.get("status") in ("triaging", "pending", "published"):
            return f"já capturado ({other.get('status')}) em {f.name}"
    return ""


def extract_pdf_text(raw: Path) -> str:
    out = subprocess.run(["pdftotext", "-l", "15", "-layout", str(raw), "-"], capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError("pdftotext falhou")
    return out.stdout[:MAX_ATTACHMENT_TEXT]


def reject(cap: dict, status: str, detail: str, private: Path) -> None:
    cap["status"] = status
    if detail:
        cap["detail"] = detail
    kp.save_json(private / "captures" / f"{cap['id']}.json", cap)
    kp.commit_push(private, [private / "captures" / f"{cap['id']}.json"], f"capture {cap['id']}: {status}")
    kp.try_send(cap["chat_id"], REJECTIONS[status].format(detail=detail), reply_to=cap["message_id"])
    kp.set_output("triage", "false")
    kp.set_output("id", cap["id"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    args = ap.parse_args()

    cap = clean(kp.payload_from_env())
    path = args.private / "captures" / f"{cap['id']}.json"
    if path.exists():  # reentrega do Telegram ou do dispatch
        print(f"{cap['id']}: já processada; nada a fazer")
        kp.set_output("triage", "false")
        kp.set_output("id", cap["id"])
        return

    if cap["url"]:
        cap["input"] = "url"
        if kp.ii.is_private(cap["url"]):
            return reject(cap, "rejected_private", "", args.private)
        dup = known_elsewhere(cap["url"], args.private)
        if dup:
            return reject(cap, "duplicate", dup, args.private)
    elif cap["attachment"]:
        cap["input"] = "attachment"
        att = cap["attachment"]
        if att["file_size"] > kp.MAX_ATTACHMENT_BYTES:
            return reject(cap, "too_big", "", args.private)
        if not (att["mime_type"] == "application/pdf" or att["file_name"].lower().endswith(".pdf")):
            return reject(cap, "unsupported", "", args.private)
    elif len(cap["text"]) >= 3:
        cap["input"] = "topic"
    else:
        return reject(cap, "empty", "", args.private)

    args.work.mkdir(parents=True, exist_ok=True)
    if cap["input"] == "attachment":
        tmp = Path(tempfile.mkdtemp())
        try:
            raw = tmp / "arquivo.pdf"
            try:
                kp.tg_download(cap["attachment"]["file_id"], raw)
                (args.work / "attachment.txt").write_text(extract_pdf_text(raw), encoding="utf-8")
            except (kp.TelegramError, RuntimeError, subprocess.TimeoutExpired) as e:
                print(f"falha ao obter o PDF: {e}", file=sys.stderr)
                return reject(cap, "failed", "não consegui baixar/ler o PDF", args.private)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    cap["status"] = "triaging"
    kp.save_json(path, cap)
    kp.commit_push(args.private, [path], f"capture {cap['id']}: recebida")
    kp.save_json(args.work / "capture.json", {k: v for k, v in cap.items() if k != "attachment"} | (
        {"attachment_name": cap["attachment"]["file_name"], "attachment_text": "attachment.txt"} if cap["attachment"] else {}))
    kp.set_output("triage", "true")
    kp.set_output("id", cap["id"])


if __name__ == "__main__":
    main()
