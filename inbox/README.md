# Inbox

Itens crus, ainda não triados. Cada arquivo `AAAA-MM-DD-<slug>.md` tem `url` (ou `attachment`), `saved`, `origin` e a nota original.

- Importar uma exportação do WhatsApp: salve o `.txt` em `inbox/raw/` (ignorado pelo git) e rode
  `python3 scripts/import_inbox.py whatsapp inbox/raw/conversa.txt --me "Seu Nome"`.
- Importar uma lista de URLs (uma por linha, ou qualquer texto com links):
  `python3 scripts/import_inbox.py urls arquivo.txt --origin x`.
- Triar: peça a skill `triar-inbox`. Cada item triado vira uma nota em `sources/<area>/` e sai daqui.

Os itens de `inbox/*.md` e os arquivos de `inbox/raw/` ficam só na sua máquina (`.gitignore`): contêm anotações pessoais e links ainda não avaliados. Links de reunião e armazenamento (Zoom, Drive etc.) são ignorados na importação.
