"""Testes do pipeline com um Telegram falso (HTTP local) e repositórios git temporários.

Rodar da raiz do repositório:  python3 -m unittest discover -s pipeline/tests -v
Somente biblioteca padrão; precisa de git e (para o teste de PDF) pdftotext.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parents[2]
TOKEN = "TEST:SECRET-TOKEN"
CHAT = 4242
MIN_PDF = (b"%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
           b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 100]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
           b"4 0 obj<</Length 44>>stream\nBT /F1 14 Tf 20 50 Td (Hello KB PDF) Tj ET\nendstream\nendobj\n"
           b"5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\ntrailer<</Root 1 0 R/Size 6>>\n%%EOF\n")

INDEX_BLOCK = "<!-- BEGIN:INDEX -->\nx\n<!-- END:INDEX -->\n"


class FakeTelegram:
    """Registra chamadas à Bot API e serve um PDF mínimo."""

    def __init__(self):
        self.calls = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                method = self.path.rsplit("/", 1)[-1]
                assert TOKEN in self.path
                outer.calls.append((method, body))
                if method == "getFile":
                    result = {"file_path": "docs/file.pdf", "file_size": len(MIN_PDF)}
                else:
                    result = {"message_id": 777}
                data = json.dumps({"ok": True, "result": result}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                assert TOKEN in self.path
                self.send_response(200)
                self.end_headers()
                self.wfile.write(MIN_PDF)

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def messages(self):
        return [b for m, b in self.calls if m == "sendMessage"]

    def edits(self):
        return [b for m, b in self.calls if m == "editMessageText"]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def sh(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout


def init_clone(tmp: Path, name: str, seed) -> tuple:
    """Cria origin (bare) + clone com um commit inicial em main."""
    origin = tmp / f"{name}.git"
    work = tmp / name
    sh("git", "init", "-q", "--bare", "-b", "main", str(origin))
    sh("git", "clone", "-q", str(origin), str(work))
    sh("git", "config", "user.name", "t", cwd=work)
    sh("git", "config", "user.email", "t@t", cwd=work)
    seed(work)
    sh("git", "add", "-A", cwd=work)
    sh("git", "commit", "-q", "-m", "seed", cwd=work)
    sh("git", "push", "-q", "origin", "HEAD:main", cwd=work)
    sh("git", "branch", "-q", "--set-upstream-to=origin/main", cwd=work)
    return origin, work


def seed_kb(kb: Path):
    shutil.copytree(REAL_ROOT / "scripts", kb / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REAL_ROOT / "pipeline" / "scripts", kb / "pipeline" / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REAL_ROOT / "templates", kb / "templates")
    for area in ("computer-vision", "genai", "mlops", "nlp", "recsys"):
        d = kb / "sources" / area
        d.mkdir(parents=True)
        (d / "README.md").write_text(f"# {area}\n\n{INDEX_BLOCK}")
    (kb / "README.md").write_text(f"# kb\n\n{INDEX_BLOCK}")
    (kb / "study" / "weeks").mkdir(parents=True)
    (kb / "study" / "weeks" / ".gitkeep").write_text("")
    (kb / ".github").mkdir()
    (kb / ".github" / "denylist.txt").write_text("# vazio\n")
    (kb / ".gitignore").write_text("private/\nwork/\n__pycache__/\n")
    (kb / "sources" / "recsys" / "existing.md").write_text(
        "---\ntitle: Existente\narea: recsys\nkind: paper\nurl: https://arxiv.org/abs/2401.00001\n"
        "status: triaged\nsaved: 2026-01-01\n---\n\n> **Resumo:** já existe.\n")


def seed_private(p: Path):
    (p / "captures").mkdir()
    (p / "captures" / ".gitkeep").write_text("")


def draft_text(**over) -> str:
    fm = {"title": "Um paper bom", "area": "genai", "kind": "paper", "url": "https://evil.example/forged",
          "status": "reading", "priority": "2", "effort": "weekend", "origin": "whatsapp", "saved": "1999-01-01"}
    fm.update(over)
    head = "\n".join(f"{k}: {v}" for k, v in fm.items() if v is not None)
    return f"---\n{head}\n---\n\n> **Resumo:** Propõe algo útil e mostra um resultado.\n\n## Contribuição principal\n\ntexto\n\n## Log\n\n- 2026-10-19: fonte triada.\n"


class PipelineCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.tg = FakeTelegram()
        self.addCleanup(self.tg.close)
        self.kb_origin, self.kb = init_clone(self.tmp, "kb", seed_kb)
        self.pr_origin, self.pr = init_clone(self.tmp, "private", seed_private)
        self.work = self.kb / "work"
        self.out = self.tmp / "gh_output.txt"

    # -- utilidades
    def run_script(self, script, *args, payload=None, extra_env=None, check=True):
        env = {**os.environ, "TELEGRAM_BOT_TOKEN": TOKEN, "TELEGRAM_API_BASE": self.tg.url, "TELEGRAM_CHAT_ID": str(CHAT),
               "KB_REPO": "me/kb", "GITHUB_OUTPUT": str(self.out), "PYTHONDONTWRITEBYTECODE": "1"}
        if payload is not None:
            env["PAYLOAD"] = json.dumps(payload)
        env.update(extra_env or {})
        proc = subprocess.run([sys.executable, f"pipeline/scripts/{script}", *args], cwd=self.kb, env=env, capture_output=True, text=True)
        if check and proc.returncode != 0:
            self.fail(f"{script} falhou:\n{proc.stdout}\n{proc.stderr}")
        self.assertNotIn(TOKEN, proc.stdout + proc.stderr)
        return proc

    def outputs(self):
        return dict(line.split("=", 1) for line in self.out.read_text().splitlines()) if self.out.exists() else {}

    def capture(self, cid="20261019-1001-1", **over):
        p = {"id": cid, "chat_id": CHAT, "message_id": 55, "date": "2026-10-19", "text": "interessante", "url": "https://arxiv.org/abs/2410.12345", "attachment": None}
        p.update(over)
        return p

    def process(self, payload, check=True):
        if self.out.exists():
            self.out.unlink()
        return self.run_script("process_capture.py", "--private", str(self.pr), "--work", str(self.work), payload=payload, check=check)

    def origin_file(self, origin, path):
        return sh("git", "--git-dir", str(origin), "show", f"main:{path}")

    def capture_status(self, cid):
        return json.loads(self.origin_file(self.pr_origin, f"captures/{cid}.json"))["status"]

    def make_pending(self, cid="20261019-1001-1", draft=None, **cap_over):
        self.process(self.capture(cid, **cap_over))
        (self.work / "drafts").mkdir(parents=True, exist_ok=True)
        (self.work / "drafts" / f"{cid}.md").write_text(draft or draft_text())
        self.run_script("deliver_draft.py", "--private", str(self.pr), "--work", str(self.work), "--id", cid)

    # -- process_capture
    def test_url_capture_is_recorded_and_queued_for_triage(self):
        self.process(self.capture())
        self.assertEqual(self.outputs(), {"triage": "true", "id": "20261019-1001-1"})
        self.assertEqual(self.capture_status("20261019-1001-1"), "triaging")
        cap = json.loads((self.work / "capture.json").read_text())
        self.assertEqual((cap["input"], cap["url"]), ("url", "https://arxiv.org/abs/2410.12345"))

    def test_redelivery_is_idempotent(self):
        self.process(self.capture())
        before = len(self.tg.calls)
        self.process(self.capture())
        self.assertEqual(self.outputs()["triage"], "false")
        self.assertEqual(len(self.tg.calls), before)

    def test_duplicate_of_published_source_is_rejected(self):
        self.process(self.capture(url="https://www.arxiv.org/abs/2401.00001?utm_source=x"))
        self.assertEqual(self.outputs()["triage"], "false")
        self.assertEqual(self.capture_status("20261019-1001-1"), "duplicate")
        self.assertIn("sources/recsys/existing.md", self.tg.messages()[-1]["text"])

    def test_duplicate_of_pending_capture_is_rejected(self):
        self.process(self.capture("20261019-1001-1"))
        self.process(self.capture("20261019-1002-1", url="https://arxiv.org/abs/2410.12345/"))
        self.assertEqual(self.capture_status("20261019-1002-1"), "duplicate")

    def test_private_domain_is_rejected(self):
        self.process(self.capture(url="https://docs.google.com/document/d/abc"))
        self.assertEqual(self.capture_status("20261019-1001-1"), "rejected_private")
        self.assertFalse((self.work / "capture.json").exists())

    def test_topic_without_link(self):
        self.process(self.capture(url=None, text="contrastive learning para vídeo egocêntrico"))
        cap = json.loads((self.work / "capture.json").read_text())
        self.assertEqual((cap["input"], self.outputs()["triage"]), ("topic", "true"))

    def test_empty_message_is_rejected(self):
        self.process(self.capture(url=None, text="  "))
        self.assertEqual(self.capture_status("20261019-1001-1"), "empty")

    def test_pdf_attachment_is_downloaded_and_text_extracted(self):
        if not shutil.which("pdftotext"):
            self.skipTest("pdftotext ausente")
        att = {"file_id": "F1", "file_name": "paper.pdf", "file_size": len(MIN_PDF), "mime_type": "application/pdf"}
        self.process(self.capture(url=None, text="", attachment=att))
        self.assertIn("Hello KB PDF", (self.work / "attachment.txt").read_text())
        self.assertEqual(json.loads((self.work / "capture.json").read_text())["attachment_text"], "attachment.txt")
        self.assertIn("getFile", [m for m, _ in self.tg.calls])

    def test_big_and_non_pdf_attachments_are_rejected(self):
        big = {"file_id": "F", "file_name": "livro.pdf", "file_size": 30 * 1024 * 1024, "mime_type": "application/pdf"}
        self.process(self.capture("20261019-2001", url=None, text="", attachment=big))
        self.assertEqual(self.capture_status("20261019-2001"), "too_big")
        doc = {"file_id": "F", "file_name": "x.docx", "file_size": 10, "mime_type": "application/zip"}
        self.process(self.capture("20261019-2002", url=None, text="", attachment=doc))
        self.assertEqual(self.capture_status("20261019-2002"), "unsupported")

    def test_invalid_payloads_fail_without_side_effects(self):
        for bad in ({"id": "../../etc/passwd"}, self.capture(date="ontem"), self.capture(url="javascript:alert(1)"), self.capture(chat_id="x")):
            proc = self.process({**self.capture(), **bad}, check=False)
            self.assertNotEqual(proc.returncode, 0, bad)
        self.assertEqual(sh("git", "--git-dir", str(self.pr_origin), "log", "--oneline").count("\n"), 1)

    # -- deliver_draft
    def test_deliver_forces_trusted_fields_and_asks_for_approval(self):
        self.make_pending()
        draft = self.origin_file(self.pr_origin, "drafts/20261019-1001-1.md")
        self.assertIn("url: https://arxiv.org/abs/2410.12345", draft)
        self.assertIn("saved: 2026-10-19", draft)
        self.assertIn("origin: telegram", draft)
        self.assertIn("status: triaged", draft)
        for forged in ("evil.example", "1999-01-01", "status: reading", "origin: whatsapp"):
            self.assertNotIn(forged, draft)
        self.assertEqual(self.capture_status("20261019-1001-1"), "pending")
        msg = self.tg.messages()[-1]
        self.assertIn("Um paper bom", msg["text"])
        self.assertIn("Propõe algo útil", msg["text"])
        buttons = [b["callback_data"] for b in msg["reply_markup"]["inline_keyboard"][0]]
        self.assertEqual(buttons, ["pub:20261019-1001-1", "drop:20261019-1001-1"])

    def test_deliver_rejects_invalid_draft_and_missing_draft(self):
        self.process(self.capture())
        (self.work / "drafts").mkdir(parents=True)
        (self.work / "drafts" / "20261019-1001-1.md").write_text(draft_text(area="astrologia"))
        self.run_script("deliver_draft.py", "--private", str(self.pr), "--work", str(self.work), "--id", "20261019-1001-1")
        self.assertEqual(self.capture_status("20261019-1001-1"), "failed")
        self.assertIn("área inválida", self.origin_file(self.pr_origin, "captures/20261019-1001-1.json"))
        self.process(self.capture("20261019-1003-1", url="https://example.org/a"))
        self.run_script("deliver_draft.py", "--private", str(self.pr), "--work", str(self.work), "--id", "20261019-1003-1", "--triage-result", "failure")
        self.assertEqual(self.capture_status("20261019-1003-1"), "failed")

    def test_topic_draft_without_url_is_accepted(self):
        self.make_pending("20261019-3001", draft_text(kind="topic", url=None), url=None, text="contrastive learning para vídeo")
        self.assertEqual(self.capture_status("20261019-3001"), "pending")
        self.assertNotIn("url:", self.origin_file(self.pr_origin, "drafts/20261019-3001.md"))

    # -- apply_decision
    def decide(self, action, cid="20261019-1001-1", check=True):
        return self.run_script("apply_decision.py", "--private", str(self.pr),
                               payload={"id": cid, "action": action, "chat_id": CHAT, "message_id": 321}, check=check)

    def test_publish_adds_note_updates_index_and_is_idempotent(self):
        self.make_pending()
        self.decide("publish")
        note = self.origin_file(self.kb_origin, "sources/genai/um-paper-bom.md")
        self.assertIn("origin: telegram", note)
        self.assertIn("um-paper-bom.md", self.origin_file(self.kb_origin, "sources/genai/README.md"))
        self.assertIn("**Fontes:** 2", self.origin_file(self.kb_origin, "README.md"))
        self.assertEqual(self.capture_status("20261019-1001-1"), "published")
        self.assertIn("https://github.com/me/kb/blob/main/sources/genai/um-paper-bom.md", self.tg.edits()[-1]["text"])
        commits = sh("git", "--git-dir", str(self.kb_origin), "rev-list", "--count", "main").strip()
        self.decide("publish")
        self.assertEqual(sh("git", "--git-dir", str(self.kb_origin), "rev-list", "--count", "main").strip(), commits)
        self.assertIn("Já publicado", self.tg.edits()[-1]["text"])

    def test_publish_survives_a_concurrent_push_to_the_public_repo(self):
        self.make_pending()
        other = self.tmp / "other"
        sh("git", "clone", "-q", str(self.kb_origin), str(other))
        sh("git", "config", "user.name", "o", cwd=other)
        sh("git", "config", "user.email", "o@o", cwd=other)
        (other / "NOTAS.md").write_text("alguém empurrou algo\n")
        sh("git", "add", "-A", cwd=other)
        sh("git", "commit", "-q", "-m", "concorrente", cwd=other)
        sh("git", "push", "-q", "origin", "HEAD:main", cwd=other)
        self.decide("publish")
        self.assertIn("alguém empurrou", self.origin_file(self.kb_origin, "NOTAS.md"))
        self.origin_file(self.kb_origin, "sources/genai/um-paper-bom.md")

    def test_publish_name_collision_gets_suffix(self):
        self.make_pending("20261019-1001-1")
        self.decide("publish", "20261019-1001-1")
        self.make_pending("20261019-1002-1", url="https://example.org/outro")
        self.decide("publish", "20261019-1002-1")
        self.origin_file(self.kb_origin, "sources/genai/um-paper-bom-2.md")

    def test_denylist_blocks_publication(self):
        (self.kb / ".github" / "denylist.txt").write_text("sistema-interno-x\n")
        sh("git", "add", "-A", cwd=self.kb)
        sh("git", "commit", "-q", "-m", "denylist", cwd=self.kb)
        sh("git", "push", "-q", "origin", "HEAD:main", cwd=self.kb)
        self.make_pending(draft=draft_text().replace("texto", "usamos o Sistema-Interno-X em produção"))
        proc = self.decide("publish", check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Não publiquei", self.tg.edits()[-1]["text"])
        self.assertEqual(self.capture_status("20261019-1001-1"), "pending")
        with self.assertRaises(subprocess.CalledProcessError):
            self.origin_file(self.kb_origin, "sources/genai/um-paper-bom.md")

    def test_drop_marks_capture_and_publishes_nothing(self):
        self.make_pending()
        self.decide("drop")
        self.assertEqual(self.capture_status("20261019-1001-1"), "dropped")
        with self.assertRaises(subprocess.CalledProcessError):
            self.origin_file(self.kb_origin, "sources/genai/um-paper-bom.md")
        self.decide("publish")  # depois de descartar, publicar não faz nada
        self.assertIn("Já descartado", self.tg.edits()[-1]["text"])

    def test_decision_payload_validation(self):
        self.make_pending()
        self.assertNotEqual(self.run_script("apply_decision.py", "--private", str(self.pr), payload={"id": "x", "action": "publish", "chat_id": CHAT}, check=False).returncode, 0)
        self.assertNotEqual(self.run_script("apply_decision.py", "--private", str(self.pr), payload={"id": "20261019-1001-1", "action": "rm -rf", "chat_id": CHAT}, check=False).returncode, 0)

    # -- apply_plan
    def make_patch(self, files: dict) -> Path:
        for path, content in files.items():
            f = self.kb / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content)
        sh("git", "add", "-A", cwd=self.kb)
        patch = sh("git", "diff", "--cached", "--binary", cwd=self.kb)
        sh("git", "reset", "-q", "--hard", cwd=self.kb)
        sh("git", "clean", "-fdq", cwd=self.kb)
        out = self.tmp / "plan.patch"
        out.write_text(patch)
        return out

    def test_plan_patch_applies_when_paths_are_allowed(self):
        patch = self.make_patch({"study/weeks/2026-W43.md": "# Semana 2026-W43\n"})
        self.run_script("apply_plan.py", "--patch", str(patch))
        self.assertEqual(self.outputs()["applied"], "true")
        self.assertIn("W43", self.origin_file(self.kb_origin, "study/weeks/2026-W43.md"))

    def test_plan_patch_with_forbidden_paths_is_refused(self):
        patch = self.make_patch({"study/weeks/2026-W43.md": "# ok\n", "scripts/build_index.py": "print('pwned')\n", ".github/workflows/x.yml": "on: push\n"})
        proc = self.run_script("apply_plan.py", "--patch", str(patch), check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("não permitidos", proc.stderr)
        with self.assertRaises(subprocess.CalledProcessError):
            self.origin_file(self.kb_origin, "study/weeks/2026-W43.md")

    def test_empty_plan_patch_is_a_noop(self):
        empty = self.tmp / "empty.patch"
        empty.write_text("")
        self.run_script("apply_plan.py", "--patch", str(empty))
        self.assertEqual(self.outputs()["applied"], "false")

    # -- digest
    WEEK = ("# Semana 2026-W43\n\n## Plano\n\n"
            "- [x] **Ler:** [VideoMAE V2](../../sources/cv/v.md) (≈ 30 min). Se sobrar tempo, ler mais.\n"
            "- [ ] **Prototipar:** [nDCG](../../sources/recsys/n.md) (≈ 2 h).\n"
            "- [ ] **Revisar:** nenhum item nesta semana.\n\n## Retro\n\n- **Feito:**\n")

    def test_digest_nudge_and_plan(self):
        (self.kb / "study" / "weeks" / "2026-W43.md").write_text(self.WEEK)
        self.make_pending()
        self.run_script("digest.py", "plan", "--private", str(self.pr), "--today", "2026-10-19")
        text = self.tg.messages()[-1]["text"]
        self.assertIn("✅ Ler: VideoMAE V2", text)
        self.assertIn("▫️ Prototipar: nDCG", text)
        self.assertIn("1 captura(s) aguardando", text)
        self.run_script("digest.py", "nudge", "--private", str(self.pr), "--today", "2026-10-22")  # quinta
        text = self.tg.messages()[-1]["text"]
        self.assertIn("1/3 itens feitos", text)
        self.assertNotIn("Retro", text)
        self.run_script("digest.py", "nudge", "--private", str(self.pr), "--today", "2026-10-25")  # domingo
        self.assertIn("Retro", self.tg.messages()[-1]["text"])

    def test_digest_without_plan_suggests_command(self):
        self.run_script("digest.py", "nudge", "--private", str(self.pr), "--today", "2026-10-22")
        self.assertIn("/semana", self.tg.messages()[-1]["text"])


class UnitCase(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(REAL_ROOT / "pipeline" / "scripts"))
        import kbpipe
        self.kp = kbpipe

    def test_extract_summary_multiline_and_missing(self):
        text = "---\n---\n\n> **Resumo:** primeira linha\n> segunda linha.\n\n## X\n"
        self.assertEqual(self.kp.extract_summary(text), "primeira linha segunda linha.")
        self.assertEqual(self.kp.extract_summary("sem resumo"), "(sem resumo)")
        self.assertTrue(self.kp.extract_summary("> **Resumo:** " + "a" * 900).endswith("…"))

    def test_id_regex(self):
        for ok in ("20261019-123", "20261019-123-2"):
            self.assertTrue(self.kp.ID_RE.fullmatch(ok))
        for bad in ("../x", "20261019", "20261019-1-123", "20261019-1\n", ""):
            self.assertFalse(self.kp.ID_RE.fullmatch(bad), bad)


if __name__ == "__main__":
    unittest.main()
