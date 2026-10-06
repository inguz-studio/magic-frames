# Playbook: Projeto de vídeo e ingestão do Drive do cliente

Dono: `lead-editorial-director` (abre o projeto e preenche o manifesto). Executa a ingestão: `asset-broll-curator`. Consomem: `smart-clip-editor`, `color-grading-colorist`, `retention-subtitles-specialist`, `motion-hyperframes-engineer`. Vale em qualquer runtime: é pasta, manifesto e `rclone`.

## 1. Três camadas, nunca misturadas

| Camada | Onde | O que guarda | Viaja com a empresa? |
|---|---|---|---|
| **Casa** | `library/` dentro da empresa | fontes (`70_fonts`), presets de animação de texto (`80_text-animations`), formatos (`90_formats`), LUTs, molduras, SFX | sim |
| **Acervo** | `Magic Frames Library/` no disco e no Drive do dono | B-roll por tema, referências por mês, inbox (`playbooks/asset-library.md`) | não |
| **Projeto** | uma pasta por trabalho, raiz padrão `~/Movies/magic-frames/` | mídia bruta do cliente, trabalho intermediário, entregas | não |

Regra: o projeto **aponta** para a casa e para o acervo pelo `id` no manifesto; nunca copia fonte, preset, LUT ou SFX para dentro de si. O render lê da biblioteca.

## 2. Árvore do projeto

```
<cliente>_<projeto>_<AAAAMMDD>/
├── manifest.yaml          # origem de cada mídia + assets da casa usados + entregas
├── 01_raw/                # espelho da pasta do Drive do cliente; só leitura depois da ingestão
├── 02_broll/              # inserts liberados pelo scout, stock, material gerado
├── 03_work/
│   ├── transcripts/       # whisper: .json por palavra, .srt
│   ├── proxies/
│   ├── cuts/              # trechos e rascunhos de corte
│   └── project_files/     # timeline.json do CapCut, .drp, .prproj, .fcpxml, EDL (quando o cliente escolheu um editor)
├── 04_audio/              # trilha, SFX escolhidos (por id da casa), VO
├── 05_graphics/           # overlays renderizados com alfa, legendas, lower thirds
└── 06_exports/
    ├── drafts/
    └── final/             # o que volta para a pasta Exports/ no Drive do cliente
```

O que veio do cliente existe só em `01_raw`. Todo derivado nasce em `03_work`. Referência pública da convenção: `github.com/lsuxrstudio/production-template` e o padrão Project · Footage · Audio · Graphics · Exports dos estúdios de pós.

## 3. O que o cliente faz (uma vez)

1. Separa no Google Drive uma pasta com o rolo de câmera: vídeos e imagens, do jeito que saíram da câmera ou do celular. Subpastas são bem-vindas (por dia, por câmera).
2. Compartilha a pasta com o e-mail da empresa como **Leitor** (para baixar) ou **Editor** (para receber os cortes de volta). Link "qualquer pessoa com o link" não é necessário e só serve ao caminho de emergência (§6).
3. Manda o link da pasta. O id está na URL: `drive.google.com/drive/folders/<ID>`.

## 4. Descoberta pelo conector do Drive (quando o runtime tem)

Verificado em 02/10/2026 nesta máquina: o conector `mcp:google-drive` lista o conteúdo de uma pasta pelo id, inclusive pasta compartilhada com a conta (`search_files` com `parentId = '<ID>'`; `sharedWithMe = true and mimeType = 'application/vnd.google-apps.folder'` lista as pastas que chegaram por compartilhamento), e devolve id, nome, dono, data e tamanho de cada arquivo (`get_file_metadata`). É o jeito mais rápido de achar a pasta certa, conferir o que o cliente mandou e preencher `media[]` do manifesto antes de baixar. O que ele não faz é trazer vídeo em volume: `download_file_content` devolve o arquivo em base64 dentro da conversa, bom só para arquivo pequeno (um `.cube`, um `.srt`). O download fica com o `rclone` (§5). Uma pasta pode aparecer vazia no conector mesmo compartilhada (caso da pasta de SFX de terceiro em 02/10/2026): aí o dono dela precisa liberar a listagem ou o caminho é o `rclone` com o id.

## 5. Ingestão com rclone (caminho padrão)

Pré-requisito na máquina da empresa, uma vez: `brew install rclone`, depois `rclone config` criando um remote chamado `gdrive` (tipo Google Drive, escopo `drive.readonly` se for só baixar; `drive` se for devolver exports). Sem navegador na máquina: responder "No" ao auto config e colar o token gerado por `rclone authorize "drive"` em outra máquina. Doc: `rclone.org/drive`.

```bash
ID=<id da pasta do cliente>
P=~/Movies/magic-frames/<cliente>_<projeto>_<AAAAMMDD>
mkdir -p "$P"/{01_raw,02_broll,03_work/{transcripts,proxies,cuts,project_files},04_audio,05_graphics,06_exports/{drafts,final}}

# 1. Listar com id, tamanho, data e MD5 (o Drive fornece o hash de todo arquivo)
rclone lsjson gdrive: --drive-root-folder-id "$ID" -R --files-only --hash > "$P/03_work/drive-listing.json"

# 2. Baixar só mídia, com retomada, sem apagar nada em lugar nenhum (copy, nunca sync)
rclone copy gdrive: "$P/01_raw" --drive-root-folder-id "$ID" \
  --include "*.{mp4,MP4,mov,MOV,mxf,mkv,m4v,jpg,jpeg,JPG,png,heic,HEIC,wav,mp3}" \
  --drive-acknowledge-abuse --transfers 4 --progress

# 3. Conferir integridade comparando o MD5 local com o do Drive
rclone check gdrive: "$P/01_raw" --drive-root-folder-id "$ID" --one-way
```

Depois, para cada arquivo em `01_raw`, o curador lê duração, resolução, fps e codec com `ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_name:format=duration -of json "$f"` e grava no manifesto (§7). `01_raw` passa a ser só leitura: `chmod -R a-w "$P/01_raw"`.

Limites que importam: cerca de 2 arquivos por segundo; download de até 10 TiB por dia; `--drive-acknowledge-abuse` libera arquivos que o Drive marcou no antivírus (usar só em mídia de cliente conhecido). Arquivos nativos do Google (Docs, Sheets) não são mídia e ficam de fora pelo filtro.

## 6. Caminhos de emergência

- **Pasta pequena e pública** (o cliente só sabe mandar link aberto): `brew install gdown` e `gdown --folder "https://drive.google.com/drive/folders/$ID" -O "$P/01_raw"`. Limite de 50 arquivos por pasta; acima disso, listar com `gdown <url> --json` e baixar um a um. Não faz upload.
- **Conector do Drive do runtime** (`mcp:google-drive`): descoberta e metadados (§4); não é caminho de download em volume.
- **API do Drive em Python**: só quando o `rclone` não serve. Escopo `drive.readonly`, consulta `'<ID>' in parents and trashed = false`, download com `MediaIoBaseDownload`. Doc: `developers.google.com/drive/api/guides/search-files`.

## 7. `manifest.yaml`

```yaml
project: { id: acme-lancamento-01, client: acme, created: 2026-10-02, root: ~/Movies/magic-frames/acme_lancamento-01_20261002 }
format: 06-listicle                 # id em library/90_formats/formats-manifest.yaml (ou null)
source:
  drive_folder_id: <ID>
  access: shared_with_me            # shared_with_me | public_link | own
  role: viewer                      # viewer | editor
  ingested_at: 2026-10-02T18:40:00Z
media:
  - local: 01_raw/DSC_0012.MOV
    drive_id: 1AbC...
    original_name: DSC_0012.MOV
    md5: <hash do Drive>
    duration_s: 84.2
    resolution: 3840x2160
    fps: 29.97
    codec: h264
library_assets:                     # por id; o render lê da biblioteca da casa
  fonts: [montserrat, bebasneue]
  presets: [caption-karaoke, headline-hook]
  luts: [look-01]
  sfx: [swoosh-01]
  overlays: []
deliverables:
  - file: 06_exports/final/acme-lancamento-01_clip-01.mp4
    drive_id: null                  # preenchido depois do upload
```

Sem `source` e sem `media` preenchidos, nenhum cargo começa a cortar: o conselho recusa entrega de projeto sem manifesto.

## 8. Devolver os cortes

O cliente precisa ter dado papel de **Editor**. Pegar o id da subpasta `Exports` (criar se não existir) e copiar só o final:

```bash
EXPORTS_ID=$(rclone lsjson gdrive: --drive-root-folder-id "$ID" --dirs-only | python3 -c "import json,sys;print(next(d['ID'] for d in json.load(sys.stdin) if d['Name']=='Exports'))")
rclone copy "$P/06_exports/final" gdrive: --drive-root-folder-id "$EXPORTS_ID" --progress
```

Sempre `copy`, nunca `sync`, nos dois sentidos: nada do cliente é apagado. `--dry-run` antes da primeira execução em cliente novo. O que subiu numa pasta compartilhada pertence à conta da empresa e consome a cota dela, não a do cliente. Pasta de Shared Drive (Workspace) usa `--drive-team-drive`.

## 9. Rotina

### Conectar o Drive no runtime (opcional)

No Codex, um servidor MCP local de Google Drive entra com `codex mcp add gdrive -- npx -y @piotr-agier/google-drive-mcp` (ou `dylancaponi/gdrive-mcp-server`, continuação mantida do servidor de referência), com uma credencial OAuth de app desktop criada no Google Cloud e apontada pela variável de ambiente que o servidor documenta. No Claude Code, o conector oficial do Google Drive se liga pela própria conta. Em qualquer caso o conector serve à descoberta (§4); o volume continua no `rclone`.

- **Abertura:** o diretor cria a pasta, escolhe o formato por id e abre o manifesto; o curador ingere, confere hash, preenche `media` e trava `01_raw`.
- **Produção:** Smart Clipper lê de `01_raw` e escreve em `03_work/cuts`; entrega no CapCut = rascunho gerado por `scripts/capcut_draft.py` na pasta de rascunhos do CapCut, com as mídias apontando para a pasta do projeto (`memory/permanent.md` §13); legendas e motion lêem fontes e presets da casa por id; cor registra a LUT por id.
- **Entrega:** `06_exports/final` sobe para `Exports/` do cliente; `deliverables[].drive_id` preenchido; debriefing (`playbooks/debriefing.md`).
