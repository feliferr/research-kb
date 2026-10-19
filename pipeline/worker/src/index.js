// Cloudflare Worker: recebe o webhook do bot do Telegram e despacha eventos para o repositório privado.
//
// Segredos (wrangler secret put): TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET, ALLOWED_USER_ID, GITHUB_DISPATCH_TOKEN
// Variáveis (wrangler.toml):      PRIVATE_REPO ("dono/repo-privado"), TIMEZONE (padrão America/Sao_Paulo)
//
// Eventos enviados (repository_dispatch):
//   capture  { id, chat_id, message_id, date, text, url, attachment }   um por link
//   decision { id, action: "publish" | "drop", chat_id, message_id }    botões de aprovação
//   weekly   {}                                                         plano semanal (/semana ou cron)
//   nudge    {}                                                         lembrete (cron)

export const CRONS = {
  "0 11 * * 1": "weekly", // segunda 08:00 em Brasília (UTC-3)
  "0 22 * * 0,4": "nudge", // quinta e domingo 19:00 em Brasília
};

const ID_RE = /^\d{8}-\d{1,12}(?:-\d{1,2})?$/;
const URL_RE = /https?:\/\/[^\s<>"')\]]+/gi;
const MAX_URLS = 5;
const MAX_TEXT = 2000;
const MAX_BODY_BYTES = 200_000;

const HELP = [
  "Mande aqui o que quiser estudar depois:",
  "• um link (paper, blog, repositório, thread): eu leio, resumo e peço sua aprovação antes de publicar;",
  "• um PDF de até 20 MB;",
  "• um tópico em texto livre (ex.: contrastive learning para vídeo egocêntrico).",
  "",
  "Comandos: /semana gera o plano da semana agora.",
  "Lembretes: segunda (plano), quinta e domingo (andamento).",
].join("\n");

export async function safeEqual(a, b) {
  const enc = new TextEncoder();
  const [ha, hb] = await Promise.all([
    crypto.subtle.digest("SHA-256", enc.encode(a)),
    crypto.subtle.digest("SHA-256", enc.encode(b)),
  ]);
  const x = new Uint8Array(ha);
  const y = new Uint8Array(hb);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

export function extractUrls(msg) {
  const text = msg.text ?? msg.caption ?? "";
  const entities = msg.entities ?? msg.caption_entities ?? [];
  const found = [];
  for (const e of entities) {
    // offsets do Telegram são em unidades UTF-16, como as strings do JavaScript
    if (e.type === "url") found.push(text.slice(e.offset, e.offset + e.length));
    else if (e.type === "text_link" && e.url) found.push(e.url);
  }
  if (!found.length) for (const m of text.matchAll(URL_RE)) found.push(m[0]);
  const urls = [];
  for (const raw of found) {
    const u = raw.trim().replace(/[.,;:!?)\]]+$/, "");
    if (/^https?:\/\/\S+$/i.test(u) && u.length <= 2048 && !urls.includes(u)) urls.push(u);
  }
  return urls.slice(0, MAX_URLS);
}

export function localDate(unixSeconds, timeZone = "America/Sao_Paulo") {
  return new Intl.DateTimeFormat("en-CA", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).format(
    new Date(unixSeconds * 1000),
  ); // AAAA-MM-DD
}

function telegram(env, doFetch) {
  const call = async (method, params) => {
    const res = await doFetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/${method}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error(`telegram ${method}: HTTP ${res.status}`);
  };
  return {
    call,
    // aviso best-effort: falha do Telegram nunca deve derrubar o processamento
    async say(chatId, text, replyTo) {
      try {
        const params = { chat_id: chatId, text };
        if (replyTo) params.reply_parameters = { message_id: replyTo, allow_sending_without_reply: true };
        await call("sendMessage", params);
      } catch (err) {
        console.warn(String(err.message));
      }
    },
  };
}

export async function dispatch(env, doFetch, eventType, payload) {
  const res = await doFetch(`https://api.github.com/repos/${env.PRIVATE_REPO}/dispatches`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.GITHUB_DISPATCH_TOKEN}`,
      accept: "application/vnd.github+json",
      "x-github-api-version": "2022-11-28",
      "user-agent": "research-kb-bot",
      "content-type": "application/json",
    },
    body: JSON.stringify({ event_type: eventType, client_payload: payload }),
  });
  if (res.status !== 204) {
    const detail = (await res.text().catch(() => "")).slice(0, 200);
    throw new Error(`dispatch ${eventType}: HTTP ${res.status} ${detail}`);
  }
}

async function onMessage(update, env, doFetch, tg) {
  const msg = update.message;
  const chatId = msg.chat.id;
  const text = msg.text ?? msg.caption ?? "";

  if (/^\/(start|help|ajuda)(@\w+)?(\s|$)/i.test(text)) return tg.say(chatId, HELP);
  if (/^\/semana(@\w+)?(\s|$)/i.test(text)) {
    await dispatch(env, doFetch, "weekly", {});
    return tg.say(chatId, "📅 Gerando o plano da semana… aviso quando estiver pronto.");
  }
  if (text.startsWith("/")) return tg.say(chatId, "Comando desconhecido.\n\n" + HELP);

  const tz = env.TIMEZONE || "America/Sao_Paulo";
  const date = localDate(msg.date, tz);
  const base = `${date.replaceAll("-", "")}-${update.update_id}`;
  const common = { chat_id: chatId, message_id: msg.message_id, date, text: text.slice(0, MAX_TEXT) };
  const urls = extractUrls(msg);
  const items = [];
  if (urls.length) {
    urls.forEach((url, i) => items.push({ ...common, id: `${base}-${i + 1}`, url, attachment: null }));
  } else if (msg.document) {
    const d = msg.document;
    const attachment = { file_id: d.file_id, file_name: d.file_name ?? "arquivo", file_size: d.file_size ?? 0, mime_type: d.mime_type ?? "" };
    items.push({ ...common, id: base, url: null, attachment });
  } else if (text.trim().length >= 3) {
    items.push({ ...common, id: base, url: null, attachment: null });
  } else {
    return tg.say(chatId, "Só entendo links, PDFs e tópicos em texto.", msg.message_id);
  }

  for (const item of items) await dispatch(env, doFetch, "capture", item);
  const what = items[0].url ? (items.length > 1 ? `${items.length} links` : "link") : items[0].attachment ? "PDF" : "tópico";
  return tg.say(chatId, `📥 Recebi ${what === "tópico" ? "o tópico" : `o ${what}`}. Triando… aviso quando o resumo estiver pronto.`, msg.message_id);
}

async function onCallback(update, env, doFetch, tg) {
  const cq = update.callback_query;
  const m = /^(pub|drop):(.+)$/.exec(cq.data ?? "");
  if (!m || !ID_RE.test(m[2]) || !cq.message) {
    return tg.call("answerCallbackQuery", { callback_query_id: cq.id, text: "Botão inválido." }).catch(() => {});
  }
  const publish = m[1] === "pub";
  await dispatch(env, doFetch, "decision", {
    id: m[2],
    action: publish ? "publish" : "drop",
    chat_id: cq.message.chat.id,
    message_id: cq.message.message_id,
  });
  await tg.call("answerCallbackQuery", { callback_query_id: cq.id, text: publish ? "Publicando…" : "Descartando…" }).catch(() => {});
  await tg
    .call("editMessageReplyMarkup", { chat_id: cq.message.chat.id, message_id: cq.message.message_id, reply_markup: { inline_keyboard: [] } })
    .catch(() => {});
}

export async function handleRequest(request, env, deps = {}) {
  const doFetch = deps.fetch ?? fetch;
  const url = new URL(request.url);
  if (request.method !== "POST" || url.pathname !== "/telegram") return new Response("not found", { status: 404 });

  const secret = request.headers.get("x-telegram-bot-api-secret-token") ?? "";
  if (!env.TELEGRAM_WEBHOOK_SECRET || !(await safeEqual(secret, env.TELEGRAM_WEBHOOK_SECRET))) {
    return new Response("forbidden", { status: 401 });
  }
  if (Number(request.headers.get("content-length") ?? 0) > MAX_BODY_BYTES) return new Response("too large", { status: 413 });

  let update;
  try {
    update = await request.json();
  } catch {
    return new Response("bad request", { status: 400 });
  }

  const tg = telegram(env, doFetch);
  const from = update.message?.from ?? update.callback_query?.from;
  const allowed = String(env.ALLOWED_USER_ID ?? "").trim();

  if (!allowed) {
    // modo de configuração: só revela o ID de quem escreve /start, e não faz mais nada
    if (from && update.message?.chat?.type === "private" && /^\/start/.test(update.message.text ?? "")) {
      await tg.say(update.message.chat.id, `Seu ID do Telegram é ${from.id}. Guarde-o como ALLOWED_USER_ID (wrangler secret put) e rode o deploy de novo.`);
    }
    return new Response("ok");
  }
  if (!from || String(from.id) !== allowed) return new Response("ok"); // silêncio para estranhos

  try {
    if (update.callback_query) await onCallback(update, env, doFetch, tg);
    else if (update.message && update.message.chat?.type === "private") await onMessage(update, env, doFetch, tg);
  } catch (err) {
    console.error(String(err.message));
    return new Response("dispatch failed", { status: 500 }); // o Telegram reenvia; a captura é idempotente por id
  }
  return new Response("ok");
}

export async function handleScheduled(event, env, deps = {}) {
  const type = CRONS[event.cron];
  if (!type) throw new Error(`cron desconhecido: ${event.cron}`);
  await dispatch(env, deps.fetch ?? fetch, type, {});
}

export default {
  fetch: (request, env) => handleRequest(request, env),
  scheduled: (event, env, ctx) => ctx.waitUntil(handleScheduled(event, env)),
};
