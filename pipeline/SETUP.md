# Pipeline Telegram → GitHub: configuração

> Para entender **como o sistema funciona** (componentes, diagramas de sequência, estados, segurança), leia [ARCHITECTURE.md](ARCHITECTURE.md). Este arquivo cobre só a configuração.

Você manda um link, PDF ou tópico para o seu bot. Um Worker da Cloudflare valida que é você e dispara um workflow num repositório **privado**; o Claude lê o conteúdo e escreve um rascunho; o bot responde com o resumo e dois botões. Só o que você aprova com **Publicar** chega ao repositório público.

```
Telegram ─► Worker (Cloudflare) ─► repository_dispatch ─► repo privado research-kb-inbox
                                                           ├─ prepare  valida, filtra privados/duplicados, baixa PDF
                                                           ├─ triage   Claude lê e escreve o rascunho (sem segredos, só leitura)
                                                           └─ deliver  valida, guarda em drafts/, pergunta no Telegram
Botão Publicar ─► Worker ─► decision ─► nota em sources/<area>/ no research-kb (público) + índices + denylist
Segunda 08h ─► weekly: Claude monta o plano (patch conferido por script) e o bot manda o resumo
Quinta e domingo 19h ─► nudge: andamento da semana e capturas aguardando aprovação
```

Fuso dos lembretes: Brasília (UTC-3). Para mudar, edite `crons` em `worker/wrangler.toml` e o mapa `CRONS` em `worker/src/index.js`.

## O que você precisa fazer (uma vez, ~30 min)

### 0. Instalar dois arquivos e enviar o código ao GitHub

A skill `triar-captura` e o CI dos testes precisam ficar em `.claude/` e `.github/`, pastas que a sessão do Claude não pode escrever. Rode uma vez, na raiz do `research-kb`:

```bash
bash pipeline/scripts/install_protected.sh
```

Depois `git add -A`, commit e `git push` (os commits com `pipeline/` ainda estão só locais). Sem a skill instalada, o workflow de triagem não funciona.

### 1. Criar o bot

No Telegram, converse com **@BotFather** → `/newbot` → guarde o **token**. Não compartilhe o token.

### 2. Criar o repositório privado

```bash
bash pipeline/scripts/bootstrap_private.sh ~/caminho/para/research-kb-inbox
```

No GitHub, crie um repositório **privado** e vazio com o mesmo nome (sem README), depois siga o `git remote add` / `git push` que o script imprime. Confirme em *Settings → General* que a visibilidade é **Private**: os logs do Actions de um repositório público são públicos, e este guarda o que você manda ao bot.

### 3. Tokens e segredos

Dois tokens do GitHub (foto do perfil → *Settings* da conta, não de um repositório → *Developer settings* no fim da barra lateral → *Personal access tokens* → *Fine-grained tokens*; link direto: https://github.com/settings/personal-access-tokens), cada um limitado a **um** repositório:

| Token | Repositório | Permissão | Usado por |
|---|---|---|---|
| `GITHUB_DISPATCH_TOKEN` | `research-kb-inbox` | Contents: Read and write | Worker (dispara os workflows) |
| `KB_PUSH_TOKEN` | `research-kb` | Contents: Read and write | workflows `decision` e `weekly` (publicam no público) |

E o token do Claude, com a sua assinatura: no terminal, `claude setup-token` e copie o resultado.

Em `research-kb-inbox` → *Settings → Secrets and variables → Actions → Secrets*, como **Repository secrets** (botão *New repository secret*). Não use *Environment secrets* nem crie environments: os workflows não declaram `environment:`, então segredos e variáveis de um environment não seriam lidos e chegariam vazios:

- `TELEGRAM_BOT_TOKEN`: token do BotFather
- `TELEGRAM_CHAT_ID`: seu ID numérico do Telegram. Você ainda não o tem: ele só aparece no passo 4 (o bot responde com ele ao `/start`). Pule este segredo por ora e volte aqui depois, ou mande uma mensagem ao **@userinfobot** no Telegram para obtê-lo já
- `CLAUDE_CODE_OAUTH_TOKEN`: saída do `claude setup-token`
- `KB_PUSH_TOKEN`: o token acima

Opcional, na aba **Variables** (ao lado de Secrets, no mesmo lugar) de `research-kb-inbox`, como **Repository variable** (*New repository variable*): `KB_REPO`, o repositório **público** de destino no formato `dono/nome` (sem URL e sem `.git`). Sem ela os workflows usam `feliferr/research-kb`, então só crie a variável se o dono ou o nome do repositório público forem outros (fork, repo renomeado, organização). Se o nome do repositório privado mudar, ajuste também `PRIVATE_REPO` em `pipeline/worker/wrangler.toml` e faça o deploy de novo.
Anote a data de expiração dos tokens do GitHub; quando vencerem, a publicação falha.

### 4. Worker da Cloudflare

Conta gratuita em cloudflare.com. Depois:

```bash
cd pipeline/worker
npm install
npx wrangler login
# edite PRIVATE_REPO em wrangler.toml se o nome/usuário do repo privado for outro
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET      # cole o resultado de: openssl rand -hex 32
npx wrangler secret put GITHUB_DISPATCH_TOKEN
npx wrangler deploy                                   # imprime a URL https://research-kb-bot.<sub>.workers.dev
TELEGRAM_BOT_TOKEN=... TELEGRAM_WEBHOOK_SECRET=... WORKER_URL=https://research-kb-bot.<sub>.workers.dev npm run set-webhook
```

`<sub>` é o subdomínio `workers.dev` da sua conta da Cloudflare; você não precisa descobri-lo. Se a conta ainda não tem um, o `wrangler deploy` pergunta no primeiro deploy e pede que você escolha (por exemplo `felipe`). Copie a URL completa que o deploy imprime, com `https://` e sem barra no final, e use-a em `WORKER_URL` (exemplo: `https://research-kb-bot.felipe.workers.dev`). Se esquecer a URL, ela aparece em *Workers & Pages → research-kb-bot* no painel da Cloudflare.

#### Descobrir o seu ID do Telegram

O ID não aparece em nenhuma tela do Telegram nem do GitHub; quem informa é o próprio bot:

1. No Telegram, abra uma conversa privada com o seu bot e mande `/start`.
2. Enquanto `ALLOWED_USER_ID` não existe, o Worker fica em modo de configuração e responde só a `/start`, com "Seu ID do Telegram é 123456789".
3. Esse número é o valor de `ALLOWED_USER_ID` (Worker) e de `TELEGRAM_CHAT_ID` (GitHub). Em chat privado os dois são iguais.

Se o bot não responder, rode `npm run set-webhook -- --info` (mostra o último erro do webhook) e confira o `WORKER_URL` usado no `set-webhook`. Atalho: o **@userinfobot** também responde com o seu ID numérico.

Depois, grave o ID no Worker e faça o deploy (sem ele o bot continua em modo de configuração):

```bash
npx wrangler secret put ALLOWED_USER_ID               # cole o ID
npx wrangler deploy
```

Volte ao passo 3 e crie o segredo `TELEGRAM_CHAT_ID` em `research-kb-inbox` com o mesmo ID. A partir daqui o bot ignora em silêncio qualquer outra pessoa.

### 5. Testar

1. `/start` → ajuda.
2. Mande um link do arXiv. Resposta imediata "📥 Recebi o link"; em poucos minutos chega o resumo com **Publicar / Descartar**.
3. **Publicar** → "✅ Publicado" com o link da nota no GitHub.
4. `/semana` → plano da semana (se o arquivo da semana já existir, nada é sobrescrito).

Se algo não responder: aba *Actions* do repositório privado (logs) e `npm run set-webhook -- --info` (mostra o último erro do webhook).

## Conferir na primeira execução

O que eu **não consegui testar daqui** (precisa dos seus segredos):

- A `claude-code-action` em modo automático disparada por `repository_dispatch`, com `github_token` do próprio workflow e o token da assinatura. Pela leitura do código da action, eventos fora de issues/PRs caem em modo automático e `github_token` dispensa o app do Claude, mas nunca rodei isso ponta a ponta. Se o job `triage` falhar na autenticação, troque o passo por este (mesmo `prompt`, mesmas ferramentas):

  ```yaml
  - run: npm install -g @anthropic-ai/claude-code
  - run: claude -p "Siga a skill triar-captura ... (mesmo texto do prompt)" --allowedTools "Read,Write,Glob,Grep,WebFetch,WebSearch" --max-turns 20
    env:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  ```
- Os minutos gratuitos do GitHub Actions em repositório privado do seu plano. Cada captura usa três jobs curtos (cerca de 1 a 2 minutos cada, arredondados para cima). Veja o consumo em *Settings → Billing* depois da primeira semana.

O que foi testado: os scripts Python (`python3 -m unittest discover -s pipeline/tests`) contra um Telegram falso e repositórios git temporários, o Worker (`cd pipeline/worker && npm test`) e a sintaxe dos workflows (`actionlint`).

## Limites e comportamento

- PDFs até 20 MB (limite do `getFile` do bot); só o texto das primeiras 15 páginas é lido. Maiores: mande o link.
- Links de reunião, Drive, Docs, calendário, WhatsApp e Dropbox são rejeitados. Duplicados (já publicados ou pendentes) também.
- LinkedIn, X e Facebook costumam bloquear leitura automática: o rascunho sai com "conteúdo não acessado" e você decide se publica.
- Tópico sem link vira uma nota `kind: topic` (perguntas de estudo, sem referências inventadas).
- Webhook e `getUpdates` não funcionam ao mesmo tempo: se algum dia quiser testar com `getUpdates`, rode `deleteWebhook` antes.
- O backlog local (`inbox/*.md`, do WhatsApp) continua sendo triado no computador com a skill `triar-inbox`; o bot cuida do que chega de agora em diante.

## Segurança

- Só o seu ID de usuário é aceito, e o Worker confere o cabeçalho `X-Telegram-Bot-Api-Secret-Token` antes de qualquer coisa.
- O job que lê páginas da web e roda o modelo (`triage`) não tem o token do bot nem permissão de escrita; recebe só o conteúdo da captura e devolve um único arquivo. Quem valida, guarda e envia ao Telegram é um script (`deliver`), que reescreve `url`, `saved`, `origin` e `status` a partir da captura e confere o rascunho.
- A publicação exige o seu clique, passa pelo `check_denylist.py` e pelo `build_index.py --check`, e o `weekly` só aplica patches que tocam `study/weeks/`, `sources/` e os índices.
- Risco que sobra: páginas maliciosas podem tentar manipular o modelo. Ele só tem leitura/escrita em `work/` e acesso à web, e o seu comentário original entra no contexto dele. Por isso a skill proíbe copiar o comentário para a nota e você revê o resumo antes de publicar. Preencha `.github/denylist.txt` com nomes que nunca podem aparecer.
- Se suspeitar de vazamento: revogue o token do bot no BotFather (`/revoke`), os dois tokens do GitHub e rode `claude setup-token` de novo.

## Desenvolvimento

```bash
python3 -m unittest discover -s pipeline/tests -v   # scripts (precisa de git; pdftotext é opcional)
cd pipeline/worker && npm test                      # Worker (Node 20+)
```

Atualizar os workflows: edite `pipeline/private-repo/workflows/` e copie (para `.github/workflows/` do repositório privado) para o repositório privado (a lógica em `pipeline/scripts/` já é lida do público a cada execução).
