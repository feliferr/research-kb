// Registra o webhook do bot no Telegram.
// Uso: TELEGRAM_BOT_TOKEN=... TELEGRAM_WEBHOOK_SECRET=... WORKER_URL=https://research-kb-bot.<conta>.workers.dev node scripts/set-webhook.mjs
// Opcional: --info mostra o estado atual (url, erros recentes) sem alterar nada.
const { TELEGRAM_BOT_TOKEN: token, TELEGRAM_WEBHOOK_SECRET: secret, WORKER_URL: base } = process.env;
const api = (method, body) =>
  fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body ?? {}),
  }).then((r) => r.json());

if (!token) throw new Error("defina TELEGRAM_BOT_TOKEN");
if (process.argv.includes("--info")) {
  const { result } = await api("getWebhookInfo");
  console.log({ url: result.url, pending: result.pending_update_count, last_error: result.last_error_message ?? null });
} else {
  if (!secret || !/^[A-Za-z0-9_-]{16,256}$/.test(secret)) throw new Error("TELEGRAM_WEBHOOK_SECRET deve ter 16-256 caracteres [A-Za-z0-9_-] (ex.: openssl rand -hex 32)");
  if (!base?.startsWith("https://")) throw new Error("defina WORKER_URL com https://");
  const res = await api("setWebhook", {
    url: `${base.replace(/\/$/, "")}/telegram`,
    secret_token: secret,
    allowed_updates: ["message", "callback_query"],
    drop_pending_updates: false,
  });
  console.log(res.ok ? "webhook registrado" : `falhou: ${res.description}`);
  process.exitCode = res.ok ? 0 : 1;
}
