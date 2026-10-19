#!/usr/bin/env python3
"""Mensagens periódicas no Telegram: resumo do plano da semana e lembrete de meio/fim de semana.

Uso:
  python3 pipeline/scripts/digest.py plan  --private private   # depois de gerar o plano (segunda)
  python3 pipeline/scripts/digest.py nudge --private private   # quinta e domingo

Precisa de TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID. Lê o arquivo da semana atual (ISO) em
study/weeks/ e as capturas pendentes de aprovação em private/captures/. Não usa modelo.
"""
import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

import kbpipe as kp

ROOT = kp.KB_ROOT
ITEM_RE = re.compile(r"^- \[( |x|X)\]\s*(.+)$")


def week_id(today: date) -> str:
    return today.strftime("%G-W%V")


def plan_items(text: str) -> list:
    """Itens do bloco '## Plano': [(feito, rótulo curto)]."""
    m = re.search(r"^## Plano\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    items = []
    for line in (m.group(1) if m else "").splitlines():
        im = ITEM_RE.match(line.strip())
        if not im:
            continue
        label = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", im.group(2))  # links → só o texto
        label = re.sub(r"[*_`]", "", label)
        label = re.split(r"\s+\(≈|\.\s", label, maxsplit=1)[0]
        items.append((im.group(1).lower() == "x", label[:110].strip()))
    return items


def pending_count(private: Path) -> int:
    n = 0
    for f in (private / "captures").glob("*.json") if (private / "captures").is_dir() else []:
        try:
            if kp.load_json(f).get("status") == "pending":
                n += 1
        except ValueError:
            pass
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["plan", "nudge"])
    ap.add_argument("--private", required=True, type=Path)
    ap.add_argument("--today", help="AAAA-MM-DD (testes)")
    args = ap.parse_args()

    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not chat_id.lstrip("-").isdigit():
        raise SystemExit("TELEGRAM_CHAT_ID ausente ou inválido")
    today = date.fromisoformat(args.today) if args.today else date.today()
    wk = week_id(today)
    wfile = ROOT / "study" / "weeks" / f"{wk}.md"
    pend = pending_count(args.private)
    pend_line = f"\n📥 {pend} captura(s) aguardando sua aprovação." if pend else ""

    if not wfile.is_file():
        kp.send(int(chat_id), f"📅 Ainda não há plano para {wk}. Mande /semana para gerar.{pend_line}")
        return
    items = plan_items(wfile.read_text(encoding="utf-8"))
    link = f"https://github.com/{kp.kb_repo()}/blob/main/study/weeks/{wk}.md"

    if args.mode == "plan":
        body = "\n".join(f"{'✅' if done else '▫️'} {label}" for done, label in items) or "(plano sem itens)"
        kp.send(int(chat_id), f"📅 Plano {wk}\n{body}\n\n{link}{pend_line}")
        return

    done = sum(1 for d, _ in items if d)
    lines = [f"📚 {wk}: {done}/{len(items)} itens feitos."]
    lines += [f"▫️ {label}" for d, label in items if not d]
    if items and done == len(items):
        lines = [f"🎉 {wk}: plano da semana concluído."]
    if today.weekday() == 6:  # domingo
        lines.append("Hoje fecha a semana: preencha a Retro (feito / aprendi / segue).")
    lines.append(link)
    kp.send(int(chat_id), "\n".join(lines) + pend_line)


if __name__ == "__main__":
    try:
        main()
    except kp.TelegramError as e:
        sys.exit(f"erro do Telegram: {e}")
