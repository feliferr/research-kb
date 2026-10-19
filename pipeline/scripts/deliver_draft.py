#!/usr/bin/env python3
"""Passo 3: valida o rascunho produzido pelo modelo, guarda no repositório privado e pede aprovação no Telegram.

Uso:
  python3 pipeline/scripts/deliver_draft.py --private private --work work --id <id> [--triage-result success|failure|...]

Lê work/drafts/<id>.md (artefato do job de triagem) e private/captures/<id>.json.
Sucesso: grava private/drafts/<id>.md, status=pending e envia o resumo com botões Publicar/Descartar.
Falha (sem rascunho ou inválido): status=failed e aviso no Telegram.
"""
import argparse
import sys
from pathlib import Path

import kbpipe as kp


def keyboard(cid: str) -> dict:
    return {"inline_keyboard": [[
        {"text": "✅ Publicar", "callback_data": f"pub:{cid}"},
        {"text": "🗑 Descartar", "callback_data": f"drop:{cid}"},
    ]]}


def describe(meta: dict, body: str, cap: dict) -> str:
    bits = [meta.get("area", "?"), meta.get("kind", "?")]
    if meta.get("priority"):
        bits.append(f"prioridade {meta['priority']}")
    if meta.get("effort"):
        bits.append(f"esforço {meta['effort']}")
    lines = [f"🆕 {meta.get('title', '(sem título)')}", " · ".join(bits)]
    if cap.get("url"):
        lines.append(f"🔗 {cap['url']}")
    if "conteúdo não acessado" in body.lower():
        lines.append("⚠️ Não consegui ler o conteúdo: a nota tem só metadados.")
    lines += ["", kp.extract_summary(body), "", "Publicar no repositório público?"]
    return "\n".join(lines)


def fail(cap: dict, path: Path, private: Path, reason: str) -> None:
    cap["status"] = "failed"
    cap["detail"] = reason[:300]
    kp.save_json(path, cap)
    kp.commit_push(private, [path], f"capture {cap['id']}: falhou")
    kp.try_send(cap["chat_id"], f"⚠️ Não consegui triar essa captura ({reason[:200]}). Mande de novo se quiser tentar outra vez.",
                reply_to=cap["message_id"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--id", required=True)
    ap.add_argument("--triage-result", default="success")
    args = ap.parse_args()

    cid = kp.check_id(args.id)
    cap_path = args.private / "captures" / f"{cid}.json"
    cap = kp.load_json(cap_path)
    if cap.get("status") != "triaging":
        print(f"{cid}: status {cap.get('status')}; nada a entregar")
        return

    draft_file = args.work / "drafts" / f"{cid}.md"
    if args.triage_result != "success" or not draft_file.is_file():
        return fail(cap, cap_path, args.private, f"triagem terminou com '{args.triage_result}' e sem rascunho")
    try:
        text = kp.force_fields(draft_file.read_text(encoding="utf-8"), cap)
    except (ValueError, UnicodeDecodeError) as e:
        return fail(cap, cap_path, args.private, f"rascunho ilegível: {e}")
    meta, errors = kp.validate_draft(text)
    if errors:
        return fail(cap, cap_path, args.private, "rascunho inválido: " + "; ".join(errors[:3]))

    draft_out = args.private / "drafts" / f"{cid}.md"
    draft_out.parent.mkdir(parents=True, exist_ok=True)
    draft_out.write_text(text, encoding="utf-8")
    cap["status"] = "pending"
    cap["title"] = meta["title"]
    kp.save_json(cap_path, cap)
    kp.commit_push(args.private, [draft_out, cap_path], f"capture {cid}: rascunho pronto")

    _, body = kp.split_frontmatter(text)
    kp.send(cap["chat_id"], describe(meta, body, cap), reply_to=cap["message_id"], keyboard=keyboard(cid))
    print(f"{cid}: rascunho entregue ({meta['title']})")


if __name__ == "__main__":
    try:
        main()
    except kp.TelegramError as e:
        sys.exit(f"erro do Telegram: {e}")
