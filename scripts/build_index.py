#!/usr/bin/env python3
"""Valida o frontmatter e gera os índices (README raiz e READMEs de área).

Uso:
  python3 scripts/build_index.py          # valida e regenera os índices
  python3 scripts/build_index.py --check  # valida; falha se algum índice estiver desatualizado
  python3 scripts/build_index.py --queue  # imprime WIP atual e fila priorizada (usada por /estudo-semanal)

Somente biblioteca padrão. O frontmatter aceita `chave: valor` e listas `[a, b]`.
Os blocos gerados ficam entre <!-- BEGIN:INDEX --> e <!-- END:INDEX -->.
"""
import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
LABS = ROOT / "labs"
INBOX = ROOT / "inbox"
BEGIN, END = "<!-- BEGIN:INDEX -->", "<!-- END:INDEX -->"

SOURCE_STATUSES = ["triaged", "reading", "noted", "prototyped", "archived"]
LAB_STATUSES = ["planned", "in-progress", "done", "abandoned"]
KINDS = ["paper", "doc", "repo", "thread", "video", "blog", "other"]
EFFORTS = ["1h", "weekend", "project"]
STALE_DAYS = 60
QUEUE_TOP = 10


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("frontmatter ausente")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [x.strip().strip("\"'") for x in val[1:-1].split(",") if x.strip()]
        else:
            meta[key] = val.strip("\"'")
    return meta


def parse_date(value: str):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def rel(path: Path, base: Path) -> str:
    return os.path.relpath(path, base).replace(os.sep, "/")


def load_sources(errors):
    items = []
    if not SOURCES.is_dir():
        return items
    for area_dir in sorted(p for p in SOURCES.iterdir() if p.is_dir()):
        for f in sorted(area_dir.glob("*.md")):
            if f.name == "README.md":
                continue
            where = rel(f, ROOT)
            try:
                meta = parse_frontmatter(f)
            except ValueError as e:
                errors.append(f"{where}: {e}")
                continue
            for req in ("title", "area", "kind", "status", "saved"):
                if not meta.get(req):
                    errors.append(f"{where}: campo obrigatório ausente: {req}")
            if meta.get("area") and meta["area"] != area_dir.name:
                errors.append(f"{where}: area '{meta['area']}' difere da pasta '{area_dir.name}'")
            if meta.get("status") and meta["status"] not in SOURCE_STATUSES:
                errors.append(f"{where}: status inválido '{meta['status']}'")
            if meta.get("kind") and meta["kind"] not in KINDS:
                errors.append(f"{where}: kind inválido '{meta['kind']}'")
            if meta.get("effort") and meta["effort"] not in EFFORTS:
                errors.append(f"{where}: effort inválido '{meta['effort']}'")
            if meta.get("priority") and meta["priority"] not in ("1", "2", "3"):
                errors.append(f"{where}: priority deve ser 1, 2 ou 3")
            if meta.get("saved") and parse_date(meta["saved"]) is None:
                errors.append(f"{where}: saved deve ser AAAA-MM-DD")
            items.append({"path": f, "meta": meta, "area": area_dir.name})
    return items


def load_labs(errors):
    items = []
    if not LABS.is_dir():
        return items
    for lab_dir in sorted(p for p in LABS.iterdir() if p.is_dir()):
        f = lab_dir / "README.md"
        where = rel(f, ROOT)
        if not f.exists():
            errors.append(f"{rel(lab_dir, ROOT)}: README.md ausente")
            continue
        try:
            meta = parse_frontmatter(f)
        except ValueError as e:
            errors.append(f"{where}: {e}")
            continue
        for req in ("title", "area", "status"):
            if not meta.get(req):
                errors.append(f"{where}: campo obrigatório ausente: {req}")
        if meta.get("status") and meta["status"] not in LAB_STATUSES:
            errors.append(f"{where}: status inválido '{meta['status']}'")
        if meta.get("status") == "done" and "## O que aprendi" not in f.read_text(encoding="utf-8"):
            errors.append(f"{where}: lab 'done' precisa da seção '## O que aprendi'")
        items.append({"path": f, "meta": meta, "area": meta.get("area", "")})
    return items


def last_activity(item):
    """Data da última entrada do Log (`- AAAA-MM-DD: ...`); sem Log, a data em que foi salva."""
    text = item["path"].read_text(encoding="utf-8")
    dates = [d for d in (parse_date(x) for x in re.findall(r"^- (\d{4}-\d{2}-\d{2}):", text, re.M)) if d]
    return max(dates) if dates else parse_date(item["meta"].get("saved"))


def count_inbox() -> int:
    if not INBOX.is_dir():
        return 0
    return sum(1 for f in INBOX.glob("*.md") if f.name != "README.md")


def sort_key(item):
    m = item["meta"]
    return (int(m.get("priority") or 3), m.get("saved") or "9999-12-31", m.get("title", ""))


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def link(item, base: Path) -> str:
    return f"[{esc(item['meta'].get('title', item['path'].stem))}]({rel(item['path'], base)})"


def table(headers, rows):
    if not rows:
        return ""
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def render_root(sources, labs):
    n_by = lambda s: sum(1 for x in sources if x["meta"].get("status") == s)
    parts = [
        f"**Fontes:** {len(sources)} · **Labs:** {len(labs)}",
        "",
        "**Fontes por status:** " + " · ".join(f"{s}: {n_by(s)}" for s in SOURCE_STATUSES),
        "",
        "## Áreas",
        "",
    ]
    areas = sorted({x["area"] for x in sources} | {p.name for p in SOURCES.iterdir() if p.is_dir()} if SOURCES.is_dir() else set())
    rows = []
    for a in areas:
        in_area = [x for x in sources if x["area"] == a]
        c = lambda s: str(sum(1 for x in in_area if x["meta"].get("status") == s))
        rows.append([f"[{a}](sources/{a}/README.md)", str(len(in_area)), c("reading"), c("noted"), c("prototyped")])
    t = table(["Área", "Fontes", "Lendo", "Anotadas", "Prototipadas"], rows)
    parts += [t or "_Nenhuma área ainda._", ""]

    parts += ["## Em andamento", ""]
    doing = [f"- Lendo: {link(x, ROOT)}" for x in sources if x["meta"].get("status") == "reading"]
    doing += [f"- Lab: {link(x, ROOT)}" for x in labs if x["meta"].get("status") == "in-progress"]
    parts += (doing or ["_Nada em andamento._"]) + [""]

    parts += [f"## Próximos na fila (top {QUEUE_TOP})", ""]
    queue = sorted((x for x in sources if x["meta"].get("status") == "triaged"), key=sort_key)[:QUEUE_TOP]
    rows = [
        [link(x, ROOT), x["area"], x["meta"].get("priority", "3"), x["meta"].get("effort", "-"), x["meta"].get("saved", "")]
        for x in queue
    ]
    parts += [table(["Fonte", "Área", "Prioridade", "Esforço", "Salva em"], rows) or "_Fila vazia._", ""]

    parts += ["## Labs concluídos", ""]
    done = [f"- {link(x, ROOT)}" for x in labs if x["meta"].get("status") == "done"]
    parts += (done or ["_Nenhum ainda._"])
    return "\n".join(parts)


def render_area(area, sources):
    in_area = sorted(
        (x for x in sources if x["area"] == area),
        key=lambda x: (SOURCE_STATUSES.index(x["meta"].get("status", "archived")) if x["meta"].get("status") in SOURCE_STATUSES else 99, *sort_key(x)),
    )
    base = SOURCES / area
    rows = [
        [link(x, base), x["meta"].get("kind", ""), x["meta"].get("status", ""), x["meta"].get("priority", ""), x["meta"].get("effort", ""), x["meta"].get("saved", "")]
        for x in in_area
    ]
    return f"{len(in_area)} fontes\n\n" + (table(["Fonte", "Tipo", "Status", "Prior.", "Esforço", "Salva em"], rows) or "_Nenhuma fonte ainda._")


def replace_block(text: str, body: str, where: str) -> str:
    if BEGIN not in text or END not in text:
        raise SystemExit(f"{where}: marcadores {BEGIN} / {END} ausentes")
    head, _, rest = text.partition(BEGIN)
    _, _, tail = rest.partition(END)
    return f"{head}{BEGIN}\n{body}\n{END}{tail}"


def queue_report(sources, labs):
    today = date.today()
    lines = [f"Inbox local: {count_inbox()} itens a triar", "", "WIP atual:"]
    wip = [x for x in sources if x["meta"].get("status") == "reading"]
    wip_labs = [x for x in labs if x["meta"].get("status") == "in-progress"]
    for x in wip:
        lines.append(f"  [lendo] {rel(x['path'], ROOT)}")
    for x in wip_labs:
        lines.append(f"  [lab]   {rel(x['path'], ROOT)}")
    if not wip and not wip_labs:
        lines.append("  (nada)")
    lines += ["", "Fila (triaged), da mais para a menos prioritária (idade = dias desde a última entrada do Log):"]
    queue = sorted((x for x in sources if x["meta"].get("status") == "triaged"), key=sort_key)
    for i, x in enumerate(queue, 1):
        m = x["meta"]
        last = last_activity(x)
        age = (today - last).days if last else -1
        flag = " PARADA" if age > STALE_DAYS else ""
        lines.append(
            f"  {i:>2}. p{m.get('priority', '3')} {m.get('effort', '-'):<8} {age:>4}d{flag}  {rel(x['path'], ROOT)}"
        )
    if not queue:
        lines.append("  (fila vazia)")
    noted = [x for x in sources if x["meta"].get("status") in ("noted", "prototyped")]
    lines += ["", "Candidatas a revisão / protótipo (noted, prototyped):"]
    lines += [f"  [{x['meta']['status']}] {rel(x['path'], ROOT)}" for x in noted] or ["  (nenhuma)"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="falha se algum índice estiver desatualizado")
    ap.add_argument("--queue", action="store_true", help="imprime WIP atual e fila priorizada")
    args = ap.parse_args()

    errors = []
    sources, labs = load_sources(errors), load_labs(errors)
    if errors:
        print("Erros de validação:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)

    if args.queue:
        print(queue_report(sources, labs))
        return

    outputs = {ROOT / "README.md": render_root(sources, labs)}
    if SOURCES.is_dir():
        for area_dir in sorted(p for p in SOURCES.iterdir() if p.is_dir()):
            readme = area_dir / "README.md"
            if readme.exists():
                outputs[readme] = render_area(area_dir.name, sources)

    stale = []
    for path, body in outputs.items():
        current = path.read_text(encoding="utf-8")
        new = replace_block(current, body, rel(path, ROOT))
        if new != current:
            if args.check:
                stale.append(rel(path, ROOT))
            else:
                path.write_text(new, encoding="utf-8")
                print(f"atualizado: {rel(path, ROOT)}")
    if args.check:
        if stale:
            print("Índices desatualizados (rode python3 scripts/build_index.py):", file=sys.stderr)
            for s in stale:
                print(f"  - {s}", file=sys.stderr)
            sys.exit(1)
        print("ok: frontmatter válido e índices em dia")


if __name__ == "__main__":
    main()
