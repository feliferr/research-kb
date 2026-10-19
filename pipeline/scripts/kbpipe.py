"""Funções compartilhadas pelos scripts do pipeline Telegram → GitHub (somente biblioteca padrão).

Os scripts rodam no workflow do repositório privado, com este repositório (público)
na raiz do workspace. Nada aqui grava segredos em disco nem os imprime.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

KB_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KB_ROOT / "scripts"))

import build_index as bi  # noqa: E402
import import_inbox as ii  # noqa: E402

ID_RE = re.compile(r"\d{8}-\d{1,12}(?:-\d{1,2})?")  # usar fullmatch ($ aceitaria "\n" no fim)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
MAX_TELEGRAM_TEXT = 3900
MAX_DRAFT_CHARS = 30000
MAX_ATTACHMENT_BYTES = 20 * 1024 * 1024  # limite do getFile do Telegram

# Estados de uma captura (campo `status` em captures/<id>.json)
TERMINAL = {"duplicate", "rejected_private", "too_big", "unsupported", "empty", "published", "dropped", "failed"}


# ---------------------------------------------------------------- arquivos / saídas

def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def set_output(name: str, value: str) -> None:
    line = f"{name}={value}"
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    else:
        print(f"[output] {line}")


def payload_from_env() -> dict:
    raw = os.environ.get("PAYLOAD", "")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit("PAYLOAD ausente ou inválido")
    if not isinstance(data, dict):
        raise SystemExit("PAYLOAD deve ser um objeto JSON")
    return data


def check_id(value) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise SystemExit(f"id inválido: {str(value)[:40]!r}")
    return value


# ---------------------------------------------------------------- Telegram

class TelegramError(RuntimeError):
    pass


def _base() -> str:
    return os.environ.get("TELEGRAM_API_BASE", "https://api.telegram.org").rstrip("/")


def _token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise TelegramError("TELEGRAM_BOT_TOKEN ausente")
    return token


def tg_call(method: str, params: dict) -> dict:
    req = urllib.request.Request(
        f"{_base()}/bot{_token()}/{method}",
        data=json.dumps(params).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:  # a mensagem nunca inclui a URL (que contém o token)
        body = e.read().decode("utf-8", "replace")[:300]
        raise TelegramError(f"{method}: HTTP {e.code} {body}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise TelegramError(f"{method}: {type(e).__name__}") from None
    if not data.get("ok"):
        raise TelegramError(f"{method}: {data.get('description')}")
    return data["result"]


def tg_download(file_id: str, dest: Path, max_bytes: int = MAX_ATTACHMENT_BYTES) -> int:
    info = tg_call("getFile", {"file_id": file_id})
    if (info.get("file_size") or 0) > max_bytes:
        raise TelegramError("arquivo maior que o limite")
    url = f"{_base()}/file/bot{_token()}/{info['file_path']}"
    total = 0
    try:
        with urllib.request.urlopen(url, timeout=120) as resp, open(dest, "wb") as out:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise TelegramError("arquivo maior que o limite")
                out.write(chunk)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise TelegramError(f"download: {type(e).__name__}") from None
    return total


def send(chat_id, text: str, reply_to=None, keyboard=None) -> dict:
    params = {"chat_id": chat_id, "text": text[:MAX_TELEGRAM_TEXT], "disable_web_page_preview": True}
    if reply_to:
        params["reply_parameters"] = {"message_id": reply_to, "allow_sending_without_reply": True}
    if keyboard:
        params["reply_markup"] = keyboard
    return tg_call("sendMessage", params)


def try_send(chat_id, text: str, reply_to=None, keyboard=None):
    """Envia sem derrubar o job se o Telegram falhar."""
    try:
        return send(chat_id, text, reply_to, keyboard)
    except TelegramError as e:
        print(f"aviso: não foi possível avisar no Telegram ({e})", file=sys.stderr)
        return None


def edit_or_send(chat_id, message_id, text: str) -> None:
    """Troca o texto de uma mensagem (e remove os botões); se não der, envia uma nova."""
    if message_id:
        try:
            tg_call(
                "editMessageText",
                {"chat_id": chat_id, "message_id": message_id, "text": text[:MAX_TELEGRAM_TEXT],
                 "disable_web_page_preview": True, "reply_markup": {"inline_keyboard": []}},
            )
            return
        except TelegramError as e:
            if "not modified" in str(e):
                return
            print(f"aviso: edição falhou, enviando nova mensagem ({e})", file=sys.stderr)
    try_send(chat_id, text)


# ---------------------------------------------------------------- git

def git(repo, *args, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True, capture_output=True)


def configure_git(repo) -> None:
    git(repo, "config", "user.name", "kb-pipeline[bot]")
    git(repo, "config", "user.email", "kb-pipeline@users.noreply.github.com")


def current_branch(repo) -> str:
    return git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def commit_push(repo, paths, message: str, retries: int = 5) -> bool:
    """Commit aditivo (arquivos distintos por id) com rebase em caso de corrida. False se nada mudou."""
    configure_git(repo)
    git(repo, "add", "--", *[str(p) for p in paths])
    if git(repo, "diff", "--cached", "--quiet", check=False).returncode == 0:
        return False
    git(repo, "commit", "-q", "-m", message)
    branch = current_branch(repo)
    for attempt in range(retries):
        if git(repo, "push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            return True
        git(repo, "pull", "-q", "--rebase", "origin", branch, check=False)
        time.sleep(1 + attempt)
    raise RuntimeError("push falhou após várias tentativas")


# ---------------------------------------------------------------- rascunhos (notas de fonte)

FORCED_KEYS = ("url", "saved", "origin", "status", "attachment")


def split_frontmatter(text: str):
    m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not m:
        raise ValueError("frontmatter ausente")
    return m.group(1).splitlines(), m.group(2)


def force_fields(text: str, capture: dict) -> str:
    """Sobrescreve os campos que vêm do Telegram (não confiamos no que o modelo escreveu)."""
    lines, body = split_frontmatter(text)
    kept = [ln for ln in lines if ln.partition(":")[0].strip() not in FORCED_KEYS]
    forced = []
    if capture.get("url"):
        forced.append(f"url: {capture['url']}")
    forced += [f"saved: {capture['date']}", "origin: telegram", "status: triaged"]
    return "---\n" + "\n".join(kept + forced) + "\n---\n" + body


def validate_draft(text: str, kb_root: Path = KB_ROOT):
    """Retorna (meta, erros) para o texto de uma nota de fonte."""
    errors = []
    if len(text) > MAX_DRAFT_CHARS:
        errors.append("rascunho grande demais")
    try:
        meta = bi.parse_frontmatter_text(text)
    except ValueError as e:
        return {}, [str(e)]
    for req in ("title", "area", "kind", "status", "saved"):
        if not meta.get(req):
            errors.append(f"campo obrigatório ausente: {req}")
    if meta.get("title") and len(meta["title"]) > 200:
        errors.append("título longo demais")
    areas = {p.name for p in (kb_root / "sources").iterdir() if p.is_dir()} if (kb_root / "sources").is_dir() else set()
    if meta.get("area") and meta["area"] not in areas:
        errors.append(f"área inválida '{meta['area']}' (válidas: {', '.join(sorted(areas))})")
    if meta.get("kind") and meta["kind"] not in bi.KINDS:
        errors.append(f"kind inválido '{meta['kind']}'")
    if meta.get("status") and meta["status"] != "triaged":
        errors.append("status deve ser triaged")
    if meta.get("effort") and meta["effort"] not in bi.EFFORTS:
        errors.append(f"effort inválido '{meta['effort']}'")
    if meta.get("priority") and meta["priority"] not in ("1", "2", "3"):
        errors.append("priority deve ser 1, 2 ou 3")
    if meta.get("saved") and bi.parse_date(meta["saved"]) is None:
        errors.append("saved deve ser AAAA-MM-DD")
    return meta, errors


def extract_summary(text: str, limit: int = 500) -> str:
    m = re.search(r"^>\s*\*\*Resumo:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S | re.M)
    if not m:
        return "(sem resumo)"
    summary = re.sub(r"\s*\n>?\s*", " ", m.group(1)).strip()
    return summary if len(summary) <= limit else summary[: limit - 1].rstrip() + "…"


def kb_repo() -> str:
    return os.environ.get("KB_REPO", "feliferr/research-kb")
