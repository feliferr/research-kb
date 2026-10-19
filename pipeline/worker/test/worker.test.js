import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { handleRequest, handleScheduled, extractUrls, localDate, safeEqual, CRONS } from "../src/index.js";

const env = (over = {}) => ({
  TELEGRAM_WEBHOOK_SECRET: "s3cret",
  ALLOWED_USER_ID: "42",
  TELEGRAM_BOT_TOKEN: "BOT",
  GITHUB_DISPATCH_TOKEN: "GH",
  PRIVATE_REPO: "me/inbox",
  TIMEZONE: "America/Sao_Paulo",
  ...over,
});

function harness({ dispatchStatus = 204, telegramOk = true } = {}) {
  const calls = [];
  const fetch = async (url, init) => {
    calls.push({ url, body: init?.body ? JSON.parse(init.body) : null, headers: init?.headers });
    if (url.includes("api.github.com")) return new Response(dispatchStatus === 204 ? null : "boom", { status: dispatchStatus });
    return new Response("{}", { status: telegramOk ? 200 : 500 });
  };
  return {
    fetch,
    calls,
    dispatches: () => calls.filter((c) => c.url.includes("/dispatches")),
    telegram: (method) => calls.filter((c) => c.url.endsWith(`/${method}`)),
  };
}

const post = (update, headers = {}) =>
  new Request("https://w.example/telegram", {
    method: "POST",
    headers: { "x-telegram-bot-api-secret-token": "s3cret", "content-type": "application/json", ...headers },
    body: JSON.stringify(update),
  });

const message = (text, extra = {}) => ({
  update_id: 900001,
  message: { message_id: 7, date: 1792463400, chat: { id: 42, type: "private" }, from: { id: 42 }, text, ...extra },
});

test("rejeita segredo errado ou ausente e métodos/rotas inesperados", async () => {
  const h = harness();
  assert.equal((await handleRequest(post(message("oi"), { "x-telegram-bot-api-secret-token": "errado" }), env(), h)).status, 401);
  assert.equal((await handleRequest(post(message("oi"), { "x-telegram-bot-api-secret-token": "" }), env(), h)).status, 401);
  assert.equal((await handleRequest(post(message("oi")), env({ TELEGRAM_WEBHOOK_SECRET: "" }), h)).status, 401);
  assert.equal((await handleRequest(new Request("https://w.example/telegram"), env(), h)).status, 404);
  assert.equal((await handleRequest(new Request("https://w.example/outra", { method: "POST" }), env(), h)).status, 404);
  assert.equal(h.calls.length, 0);
});

test("ignora em silêncio quem não é o dono, em grupos ou sem remetente", async () => {
  const h = harness();
  const stranger = message("https://arxiv.org/abs/1", {});
  stranger.message.from = { id: 666 };
  assert.equal((await handleRequest(post(stranger), env(), h)).status, 200);
  const group = message("https://arxiv.org/abs/1");
  group.message.chat = { id: -100, type: "supergroup" };
  await handleRequest(post(group), env(), h);
  await handleRequest(post({ update_id: 1, channel_post: { text: "x" } }), env(), h);
  assert.equal(h.calls.length, 0);
});

test("link vira uma captura com id, data local e confirmação respondendo à mensagem", async () => {
  const h = harness();
  const text = "🔥 veja https://arxiv.org/abs/2410.12345. muito bom";
  const upd = message(text, { entities: [{ type: "url", offset: 8, length: 32 }] });
  assert.equal(text.slice(8, 40), "https://arxiv.org/abs/2410.12345");
  const res = await handleRequest(post(upd), env(), h);
  assert.equal(res.status, 200);
  const [d] = h.dispatches();
  assert.equal(d.body.event_type, "capture");
  assert.equal(d.headers.authorization, "Bearer GH");
  assert.deepEqual(d.body.client_payload, {
    id: "20261019-900001-1", // 2026-10-20 02:30 UTC = 19/10 23:30 em Brasília
    chat_id: 42,
    message_id: 7,
    date: "2026-10-19",
    text,
    url: "https://arxiv.org/abs/2410.12345",
    attachment: null,
  });
  assert.match(h.telegram("sendMessage")[0].body.text, /Recebi o link/);
  assert.equal(h.telegram("sendMessage")[0].body.reply_parameters.message_id, 7);
});

test("várias URLs viram capturas separadas (sem duplicar, no máximo 5)", async () => {
  const h = harness();
  const links = Array.from({ length: 8 }, (_, i) => `https://example.org/p${i}`);
  await handleRequest(post(message(`${links.join(" ")} ${links[0]}`)), env(), h);
  const ids = h.dispatches().map((d) => d.body.client_payload.id);
  assert.deepEqual(ids, [1, 2, 3, 4, 5].map((n) => `20261019-900001-${n}`));
});

test("tópico sem link e PDF anexado", async () => {
  const h = harness();
  await handleRequest(post(message("contrastive learning para vídeo egocêntrico")), env(), h);
  let p = h.dispatches()[0].body.client_payload;
  assert.deepEqual([p.id, p.url, p.attachment], ["20261019-900001", null, null]);
  assert.match(h.telegram("sendMessage")[0].body.text, /o tópico/);

  const h2 = harness();
  const doc = { file_id: "F1", file_name: "paper.pdf", file_size: 1234, mime_type: "application/pdf" };
  await handleRequest(post(message(undefined, { caption: "ler no fim de semana", document: doc })), env(), h2);
  p = h2.dispatches()[0].body.client_payload;
  assert.deepEqual(p.attachment, doc);
  assert.equal(p.text, "ler no fim de semana");
});

test("mensagem sem conteúdo útil não despacha", async () => {
  const h = harness();
  await handleRequest(post(message(undefined, { photo: [{ file_id: "x" }] })), env(), h);
  await handleRequest(post(message("ok")), env(), h);
  assert.equal(h.dispatches().length, 0);
  assert.equal(h.telegram("sendMessage").length, 2);
});

test("comandos: /start mostra ajuda, /semana despacha, desconhecido não despacha", async () => {
  const h = harness();
  await handleRequest(post(message("/start")), env(), h);
  assert.match(h.telegram("sendMessage")[0].body.text, /Mande aqui/);
  await handleRequest(post(message("/semana@meu_bot")), env(), h);
  assert.equal(h.dispatches()[0].body.event_type, "weekly");
  await handleRequest(post(message("/apagar tudo")), env(), h);
  assert.equal(h.dispatches().length, 1);
});

test("botão Publicar/Descartar despacha a decisão, responde ao clique e remove os botões", async () => {
  const h = harness();
  const cb = (data) => ({
    update_id: 5,
    callback_query: { id: "cbq1", from: { id: 42 }, data, message: { message_id: 99, chat: { id: 42 } } },
  });
  await handleRequest(post(cb("pub:20261019-900001-1")), env(), h);
  assert.deepEqual(h.dispatches()[0].body, {
    event_type: "decision",
    client_payload: { id: "20261019-900001-1", action: "publish", chat_id: 42, message_id: 99 },
  });
  assert.equal(h.telegram("answerCallbackQuery")[0].body.callback_query_id, "cbq1");
  assert.deepEqual(h.telegram("editMessageReplyMarkup")[0].body.reply_markup, { inline_keyboard: [] });
  await handleRequest(post(cb("drop:20261019-900001")), env(), h);
  assert.equal(h.dispatches()[1].body.client_payload.action, "drop");
});

test("callbacks inválidos ou de estranhos não despacham", async () => {
  const h = harness();
  const mk = (data, id = 42) => ({ update_id: 6, callback_query: { id: "c", from: { id }, data, message: { message_id: 1, chat: { id: 42 } } } });
  for (const data of ["pub:../../x", "rm:20261019-1", "pub:20261019-1\nX", undefined]) await handleRequest(post(mk(data)), env(), h);
  await handleRequest(post(mk("pub:20261019-1", 666)), env(), h);
  assert.equal(h.dispatches().length, 0);
});

test("falha no despacho devolve 500 para o Telegram reenviar; falha no aviso não derruba", async () => {
  const bad = harness({ dispatchStatus: 422 });
  assert.equal((await handleRequest(post(message("https://example.org/a")), env(), bad)).status, 500);
  const noTg = harness({ telegramOk: false });
  assert.equal((await handleRequest(post(message("https://example.org/a")), env(), noTg)).status, 200);
  assert.equal(noTg.dispatches().length, 1);
});

test("sem ALLOWED_USER_ID só revela o ID de quem manda /start", async () => {
  const h = harness();
  await handleRequest(post(message("/start")), env({ ALLOWED_USER_ID: "" }), h);
  assert.match(h.telegram("sendMessage")[0].body.text, /Seu ID do Telegram é 42/);
  await handleRequest(post(message("https://example.org/a")), env({ ALLOWED_USER_ID: "" }), h);
  assert.equal(h.dispatches().length, 0);
});

test("cron despacha weekly/nudge e todo cron do wrangler.toml é conhecido", async () => {
  const h = harness();
  await handleScheduled({ cron: "0 11 * * 1" }, env(), h);
  await handleScheduled({ cron: "0 22 * * 0,4" }, env(), h);
  assert.deepEqual(h.dispatches().map((d) => d.body.event_type), ["weekly", "nudge"]);
  await assert.rejects(() => handleScheduled({ cron: "* * * * *" }, env(), h));
  const toml = readFileSync(new URL("../wrangler.toml", import.meta.url), "utf8");
  const line = toml.match(/^crons\s*=\s*\[(.*)\]/m)[1];
  const crons = [...line.matchAll(/"([^"]+)"/g)].map((m) => m[1]);
  assert.ok(crons.length >= 2);
  for (const c of crons) assert.ok(CRONS[c], `cron sem tratamento: ${c}`);
});

test("utilitários: offsets UTF-16, text_link, pontuação final e fuso", async () => {
  assert.deepEqual(extractUrls({ text: "veja (https://a.org/x), ok." }), ["https://a.org/x"]);
  assert.deepEqual(extractUrls({ text: "clique aqui", entities: [{ type: "text_link", offset: 0, length: 6, url: "https://b.org/y" }] }), ["https://b.org/y"]);
  assert.deepEqual(extractUrls({ text: "javascript:alert(1) ftp://x.org" }), []);
  assert.equal(localDate(1792463400, "America/Sao_Paulo"), "2026-10-19");
  assert.equal(localDate(1792463400, "UTC"), "2026-10-20");
  assert.equal(await safeEqual("abc", "abc"), true);
  assert.equal(await safeEqual("abc", "abcd"), false);
});
