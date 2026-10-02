# Playbook: Biblioteca de Assets (pastas locais e Google Drive)

Dono: `asset-broll-curator`. Alimentado por: `reference-scout` (inserts liberados), `smart-clip-editor` (cortes), `color-grading-colorist` (LUTs), `motion-hyperframes-engineer` (overlays). Vale em qualquer runtime: a taxonomia é de pastas e o índice é um arquivo; o Google Drive entra quando o runtime tem o conector do Drive.

## 1. Três camadas

A casa (`library/` dentro da empresa: LUTs, molduras, SFX, fontes, presets de texto, formatos) viaja com a empresa. O projeto (uma pasta por trabalho, com a mídia do cliente, o trabalho e as entregas) está em `playbooks/project-intake.md`. Esta taxonomia é a do **acervo** do dono: o que é reutilizável entre projetos e grande demais para viajar.

```
Magic Frames Library/
├── 00_inbox/                 # chegou, ainda não classificado (fica vazio no fim do dia)
├── 10_broll/<tema>/          # tech-coding · dinheiro-financas · foco-ansiedade · luxo-lifestyle · natureza · cidade · pessoas · <novo tema>
├── 20_references/<AAAA-MM>/  # reels, shorts e notícias salvos como referência (só o que tem direito de uso registrado)
└── _index/                   # asset-library-index.yaml + contact sheets (PNG)
```
Inserts liberados e entregas não ficam no acervo: vão para `02_broll/` e `06_exports/` da pasta do projeto, que aponta para o acervo e para a casa por id no `manifest.yaml`.
Nome de arquivo: `AAAA-MM-DD_<tema>_<descricao-curta>_<orientacao>_<fonte>.<ext>` (ex.: `2026-10-02_tech-coding_dev-digitando-noite_9x16_pexels.mp4`). Orientação sempre no nome: `16x9`, `9x16`, `1x1`.

## 2. Índice: `asset-library-index.yaml`
Uma entrada por asset: `path`, `drive_id` (quando sincronizado), `tema`, `orientacao`, `duracao_s`, `resolucao`, `fonte` (URL ou "próprio"), `licenca` (pexels | pixabay | unsplash | cc-by | própria | editorial-curta | comprada:<quem>), `data_entrada`, `tags`, `usado_em` (projetos). Sem `fonte` e `licenca`, o asset não entra no índice e volta para `00_inbox`.

## 3. Visualização: contact sheets
Para cada pasta de B-roll e de referências, um PNG com miniaturas para olhar sem abrir arquivo a arquivo (verificado nesta máquina):
```bash
# um vídeo → 1 linha de 4 frames (1 frame a cada 2s)
ffmpeg -y -i "$F" -vf "fps=1/2,scale=320:-2,tile=4x1" -frames:v 1 "_index/$(basename "$F" .mp4)_sheet.png"
# uma pasta → grade com 1 frame de cada vídeo (gera um frame por arquivo e junta com tile)
for f in 10_broll/tech-coding/*.mp4; do ffmpeg -y -loglevel error -ss 1 -i "$f" -frames:v 1 -vf scale=320:-2 "_index/tmp_$(basename "$f" .mp4).png"; done
ffmpeg -y -loglevel error -pattern_type glob -i "_index/tmp_*.png" -vf "tile=5x4" "_index/tech-coding_grid.png" && rm _index/tmp_*.png
```
Metadados por `ffprobe` (duração, resolução, fps) alimentam o índice.

## 4. Google Drive (quando o runtime tem o conector)
- Espelho da mesma taxonomia a partir de uma pasta raiz `Magic Frames Library` (criada com o conector: pasta é um arquivo com tipo `application/vnd.google-apps.folder` e `parentId` da pasta-mãe).
- Busca pelo conector com `parentId`, `title contains` e `mimeType contains 'video/'`; o `drive_id` de cada arquivo entra no índice.
- Upload pelo conector para arquivos pequenos (índice, contact sheets, manifests); vídeo grande sobe pelo cliente do Drive no computador, e o curador só registra o `drive_id`.
- Sem conector no runtime: a biblioteca vive no disco e o índice marca `drive_id: null`; nada quebra.
- Compartilhar pasta com cliente só por pedido do dono, e nunca a `20_references` (contém citação editorial e material de terceiros).

## 5. Rotina
- **Entrada:** tudo cai em `00_inbox`; o curador classifica, renomeia, registra no índice e move. Inbox vazio no fim do dia.
- **Por projeto:** o que o scout liberou vai para `02_broll/` do projeto e a entrega para `06_exports/` (`playbooks/project-intake.md`); o `manifest.yaml` registra o id de cada asset do acervo usado.
- **Mensal:** contact sheets regenerados, assets sem uso em 6 meses listados para o dono decidir, licenças revisadas.
