#!/usr/bin/env python3
"""Importa itens para inbox/ a partir de uma exportação do WhatsApp ou de uma lista de URLs.

Uso:
  python3 scripts/import_inbox.py whatsapp inbox/raw/conversa.txt --me "Seu Nome" [--since AAAA-MM-DD] [--month-first] [--keep-notes]
  python3 scripts/import_inbox.py urls arquivo.txt [--origin x] [--saved AAAA-MM-DD]
  Adicione --dry-run para ver o que seria criado sem escrever nada.

WhatsApp: "Exportar conversa" (sem mídia) gera um .txt. Os formatos de Android
("18/10/2026 23:39 - Nome: texto") e iOS ("[18/10/2026 23:39:12] Nome: texto") são aceitos.
Datas são lidas como dd/mm/aaaa (use --month-first para mm/dd).

Cada URL vira um arquivo inbox/AAAA-MM-DD-<slug>.md. Anexos (ex.: PDFs) viram itens com
`attachment:`. URLs que já existem em inbox/ ou sources/ são ignoradas.

Somente biblioteca padrão.
"""
import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
SOURCES = ROOT / "sources"

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.I)
LINE_RE = re.compile(
    r"^[‎‏]*\[?(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AaPp]\.?[Mm]\.?)?\]?\s*-?\s*(.*)$"
)
ATTACH_RES = [
    re.compile(r"<(?:anexado|attached):\s*([^>]+)>", re.I),
    re.compile(r"^(.+?)\s*\((?:arquivo anexado|file attached)\)", re.I | re.M),
]
MEDIA_OMITTED_RE = re.compile(r"<(?:m[ií]dia oculta|media omitted)>", re.I)
TRACKING_PARAMS = {"fbclid", "gclid", "igshid", "si", "s", "t"}
# Links de reunião, armazenamento e mensagens: nunca entram no inbox (o repositório é público).
PRIVATE_DOMAINS = {"zoom.us", "meet.google.com", "teams.microsoft.com", "drive.google.com", "docs.google.com",
                   "mail.google.com", "calendar.google.com", "wa.me", "whatsapp.com", "dropbox.com"}
EXTRA_SKIP = set()


def is_private(url: str) -> bool:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return any(host == d or host.endswith("." + d) for d in PRIVATE_DOMAINS | EXTRA_SKIP)


def clean_url(url: str) -> str:
    return url.rstrip(".,;:!?")


def normalize_url(url: str) -> str:
    p = urlparse(url)
    query = [(k, v) for k, v in parse_qsl(p.query) if not k.startswith("utm_") and k not in TRACKING_PARAMS]
    path = p.path.rstrip("/")
    return urlunparse((p.scheme.lower(), p.netloc.lower().removeprefix("www."), path, "", urlencode(query), ""))


def ascii_slug(text: str, limit: int = 50) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:limit].strip("-") or "item"


def slug_for(url: str) -> str:
    p = urlparse(url)
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w.\-/]+?)(?:\.pdf)?$", p.netloc + p.path, re.I)
    if m:
        return "arxiv-" + ascii_slug(m.group(1))
    host = p.netloc.lower().removeprefix("www.")
    last = [s for s in p.path.split("/") if s]
    return ascii_slug(host + "-" + (last[-1] if last else ""))


def existing_urls() -> set:
    seen = set()
    for base in (INBOX, SOURCES):
        if not base.is_dir():
            continue
        for f in base.rglob("*.md"):
            if "raw" in f.relative_to(ROOT).parts:
                continue
            content = f.read_text(encoding="utf-8")
            for m in re.finditer(r"^url:\s*(\S+)", content, re.M):
                seen.add(normalize_url(m.group(1)))
            for m in re.finditer(r"^attachment:\s*(.+)$", content, re.M):
                seen.add("att:" + m.group(1).strip())
    return seen


def write_item(day: date, origin: str, note: str, url: str = "", attachment: str = "", dry_run=False) -> Path:
    slug = slug_for(url) if url else ascii_slug(attachment or note)
    path = INBOX / f"{day.isoformat()}-{slug}.md"
    n = 2
    while path.exists():
        path = INBOX / f"{day.isoformat()}-{slug}-{n}.md"
        n += 1
    fm = ["---"]
    if url:
        fm.append(f"url: {url}")
    if attachment:
        fm.append(f"attachment: {attachment}")
    fm += [f"saved: {day.isoformat()}", f"origin: {origin}", "---", ""]
    body = note.strip()
    text = "\n".join(fm) + (body + "\n" if body else "")
    if not dry_run:
        INBOX.mkdir(exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return path


def parse_whatsapp(text: str, me: str, month_first: bool):
    messages, current = [], None
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if m:
            a, b, y, rest = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
            day, month = (b, a) if month_first else (a, b)
            y += 2000 if y < 100 else 0
            sender, sep, body = rest.partition(": ")
            try:
                d = date(y, month, day)
            except ValueError:
                current = None
                continue
            if not sep:  # mensagem de sistema (criptografia, grupo etc.)
                current = None
                continue
            if me and sender.strip().lower() != me.strip().lower():
                current = None
                continue
            current = {"date": d, "sender": sender.strip(), "text": body.replace("‎", "")}
            messages.append(current)
        elif current is not None:
            current["text"] += "\n" + raw.replace("‎", "")
    return messages


def run_whatsapp(args) -> None:
    src = Path(args.file)
    messages = parse_whatsapp(src.read_text(encoding="utf-8"), args.me, args.month_first)
    since = date.fromisoformat(args.since) if args.since else None
    seen = existing_urls()
    created = dupes = skipped = private = 0
    for msg in messages:
        if since and msg["date"] < since:
            continue
        text = msg["text"].strip()
        urls = []
        for u in URL_RE.findall(text):
            u = clean_url(u)
            if is_private(u):
                private += 1
            elif u not in urls:
                urls.append(u)
        wrote = False
        for u in urls:
            key = normalize_url(u)
            if key in seen:
                dupes += 1
                continue
            seen.add(key)
            note = text.replace(u, "").strip() if len(urls) == 1 else text
            write_item(msg["date"], "whatsapp", note, url=u, dry_run=args.dry_run)
            created += 1
            wrote = True
        if urls:
            continue
        att = next((m.group(1).strip() for r in ATTACH_RES for m in [r.search(text)] if m), "")
        if att:
            if "att:" + att in seen:
                dupes += 1
                continue
            seen.add("att:" + att)
            write_item(msg["date"], "whatsapp", "", attachment=att, dry_run=args.dry_run)
            created += 1
        elif args.keep_notes and len(text) >= 20 and not MEDIA_OMITTED_RE.search(text):
            write_item(msg["date"], "whatsapp", text, dry_run=args.dry_run)
            created += 1
        else:
            skipped += 1
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}{len(messages)} mensagens lidas · {created} itens criados · {dupes} URLs já conhecidas · {skipped} sem URL/anexo ignoradas · {private} links de domínios privados ignorados")


def run_urls(args) -> None:
    text = Path(args.file).read_text(encoding="utf-8")
    day = date.fromisoformat(args.saved) if args.saved else date.today()
    seen = existing_urls()
    created = dupes = private = 0
    for u in dict.fromkeys(clean_url(x) for x in URL_RE.findall(text)):
        if is_private(u):
            private += 1
            continue
        key = normalize_url(u)
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        write_item(day, args.origin, "", url=u, dry_run=args.dry_run)
        created += 1
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}{created} itens criados · {dupes} URLs já conhecidas · {private} links de domínios privados ignorados")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    w = sub.add_parser("whatsapp", help="importa uma exportação de conversa do WhatsApp")
    w.add_argument("file")
    w.add_argument("--me", default="", help="nome do remetente a considerar (padrão: todos)")
    w.add_argument("--since", help="só mensagens a partir de AAAA-MM-DD")
    w.add_argument("--month-first", action="store_true", help="datas no formato mm/dd")
    w.add_argument("--keep-notes", action="store_true", help="mantém mensagens de texto sem URL como itens")
    w.add_argument("--dry-run", action="store_true")
    w.add_argument("--skip-domains", default="", help="domínios extras a ignorar, separados por vírgula")
    w.set_defaults(func=run_whatsapp)
    u = sub.add_parser("urls", help="importa URLs de um arquivo de texto")
    u.add_argument("file")
    u.add_argument("--origin", default="manual", help="whatsapp | x | manual (padrão: manual)")
    u.add_argument("--saved", help="data a registrar (padrão: hoje)")
    u.add_argument("--dry-run", action="store_true")
    u.add_argument("--skip-domains", default="", help="domínios extras a ignorar, separados por vírgula")
    u.set_defaults(func=run_urls)
    args = ap.parse_args()
    EXTRA_SKIP.update(d.strip().lower() for d in args.skip_domains.split(",") if d.strip())
    if not Path(args.file).is_file():
        sys.exit(f"arquivo não encontrado: {args.file}")
    args.func(args)


if __name__ == "__main__":
    main()
