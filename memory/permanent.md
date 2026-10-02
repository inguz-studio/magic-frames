# Magic Frames — Permanent Knowledge & Technical Manifesto

Este documento consolida a base teórica, técnica e de engenharia de software audiovisual da **Magic Frames**. Toda decisão editorial, prompt de IA e composição em código deve consultar estas diretrizes canônicas.

---

## 1. Glossário e Aplicação das 17 Técnicas Canônicas de Montagem

1. **J-Cut (Audio Lead-in):** O áudio do próximo plano começa antes que a imagem anterior termine (geralmente entre 12 e 30 frames de antecipação). Gera curiosidade, antecipação psicológica e transições suaves de diálogo.
2. **L-Cut (Visual Lead-in):** A imagem muda para a nova cena ou reação, mas o áudio da cena anterior continua soando por alguns instantes. Essencial para planos de reação e ressonância emocional.
3. **Jump Cut:** Salto temporal abrupto entre dois planos com o mesmo enquadramento e posição de câmera. Elimina dead-air, acelera processos e cria urgência rítmica.
4. **Cutting on Action:** Corte executado no ápice de um movimento (abrir porta, virar a cabeça, sentar). O olho do espectador segue o vetor de movimento, tornando o corte imperceptível.
5. **Match Cut:** Conexão conceitual, gráfica ou sonora entre dois planos completamente distintos (ex: osso girando no ar virando uma espaçonave em *2001: Uma Odisseia no Espaço*).
6. **Smash Cut:** Transição violenta e inesperada de tom, dinâmica ou volume (do silêncio absoluto para uma explosão ensurdecedora, ou de um pesadelo frenético para um despertar calmo).
7. **Cross-Cutting (Edição Paralela):** Alternância entre duas ou mais ações ocorrendo simultaneamente em locais diferentes, construindo suspense e inevitabilidade.
8. **Cutaway (Insert / B-Roll):** Saída rápida do sujeito principal para um detalhe do ambiente ou objeto mencionado, enriquecendo o contexto e escondendo edições no A-roll.
9. **Soviet / Intellectual Montage:** Justaposição de planos independentes cuja colisão na mente do espectador gera um terceiro significado metafórico (efeito Kuleshov).
10. **Invisible / Hidden Cut:** Corte disfarçado por um movimento rápido de câmera (whip pan) ou passagem de um objeto escuro em primeiro plano (foreground wipe).
11. **Whip Pan (Swish Pan):** Panorâmica ultra-rápida gerando borrão de movimento usado para saltos espaciais e energéticos.
12. **Cross Dissolve:** Fusão gradual entre dois planos, indicando passagem do tempo, sonho ou nostalgia.
13. **Split Screen:** Divisão da tela em múltiplos quadros simultâneos para comparar perspectivas ou conversas remotas.
14. **Overdub & Sound Layering:** Camadas densas de som (foley, ambiência, sub-bass, risers) que elevam a realidade percebida da imagem.
15. **Freeze Frame:** Interrupção do movimento congelando um frame para enfatizar uma revelação, humor ou introdução estilizada de personagem.
16. **Wipe:** Linha divisória geométrica que varre a tela trazendo a nova imagem.
17. **Not Cutting (Plano-Sequência / Long Take):** A escolha deliberada de NÃO cortar para preservar a tensão contínua, vulnerabilidade ou virtuosismo técnico.

---

## 2. A Regra dos Seis de Walter Murch
Ao avaliar qualquer corte na timeline, a hierarquia de prioridades é estrita:
1. **Emoção (51%):** Se o corte destrói a verdade emocional da cena, nada mais importa.
2. **História (23%):** O corte precisa avançar a narrativa ou o argumento.
3. **Ritmo (10%):** A cadência deve respirar com a fisiologia e música interna da fala.
4. **Eye Trace (7%):** O corte deve guiar o olhar do espectador suavemente para o novo ponto focal.
5. **Plano 2D (5%):** Respeito à composição e linhas de força no canvas.
6. **Espaço 3D (4%):** Relação espacial e regra dos 180°.

---

## 3. Cinematografia para Geração de Vídeo com IA
Fórmula obrigatória de prompt:
`[Camera Movement] + [Shot Size & Angle] + [Subject & Action] + [Environment & Setting] + [Lighting & Color Grade] + [Optics & Lens Properties]`

- **Lentes & Óptica:** Indicar características como `35mm anamorphic with oval bokeh`, `85mm portrait telephoto lens with shallow depth of field`, `clean 24mm wide angle view`.
- **Iluminação:** `low-key cinematic chiaroscuro`, `golden hour rim lighting`, `soft directional window daylight`, `neon noir cyberpunk palette`.
- **Movimentos:** Usar termos exatos (`slow dolly-in`, `lateral tracking shot`, `subtle crane up`, `smooth 180 orbit`).

---

## 4. HyperFrames & Motion Design Code-Based
- Pacote: `hyperframes` (npm, repositório `heygen-com/hyperframes`). Motor padrão de overlay da casa; Remotion é exceção declarada no manifest de render.
- Render: Chrome headless quadro a quadro + FFmpeg. `--format webm` (VP9 com alfa), `--format mov` (ProRes 4444 com alfa), `--format png-sequence`, `--resolution portrait` (1080x1920).
- Comandos que a esteira usa: `init` · `preview` · `beats <audio>` (batidas da trilha para cortes na batida) · `check` (lint + validação runtime + layout, roda antes do conselho) · `snapshot` (PNGs dos frames-chave para julgamento visual) · `normalize-audio` (LUFS entre clipes) · `render --batch rows.json` (um overlay por clipe a partir de variáveis).
- Stack: HTML5 / CSS3 / JavaScript / GSAP / Three.js. Easing padrão `cubic-bezier(0.16, 1, 0.3, 1)` ou spring physics para UI.
- Composição do overlay sobre o clipe: `ffmpeg -i clip.mp4 -c:v libvpx-vp9 -i overlay.webm -filter_complex "[0:v][1:v]overlay=0:0:shortest=1" ...`.

---

## 5. Legendas & Safe Zones — fonte única de valores
Esta seção é a única fonte dos números. Funcionários e playbooks referenciam; nenhum redefine.

### 5.1 Zonas de interface por plataforma (canvas 1080x1920, medidas a partir da borda)
| Plataforma | Topo | Rodapé | Direita | Esquerda | Fonte |
|---|---|---|---|---|---|
| Instagram Reels | 14% ≈ 270px | 35% ≈ 670px | ~140px (coluna de ações) | ~60px | diretriz Meta (percentuais) |
| TikTok | ~150px | ~480px (cresce com legenda longa) | ~140px | ~60px | templates 2026 |
| YouTube Shorts | ~150px | ~480px | ~140px | ~60px | templates 2026 |

**Regra única (união das três):** livre de texto e elemento essencial acima de Y=270, abaixo de Y=1250 (1920−670), à direita de X=940 e à esquerda de X=80.

### 5.2 Faixa segura de legenda
- Bloco de legenda **centralizado em Y≈1105**, ocupando **Y 1000–1230** (margem de 20px da borda da zona do Instagram). Horizontal: X 80–940.
- Em ASS, estilo `Caption`: `PlayResX: 1080`, `PlayResY: 1920`, `Alignment: 2` (inferior-centro), `MarginV: 690`, `MarginL: 80`, `MarginR: 140`. A checagem mecânica (`scripts/check_safe_zone.py`) valida esses campos e qualquer `\pos()`.
- Headline (layout A do Smart Clipper): estilo `Headline` no mesmo `.ass`, `Alignment: 8` (superior-centro), `MarginV: 300`, `MarginL: 80`, `MarginR: 140`; bloco em **Y 300–560**, dentro da zona superior livre. O FFmpeg do Homebrew não tem `drawtext`; headline é sempre via ASS.

### 5.3 Estilo
- 1 a 3 palavras por tela, ALL CAPS, palavra ativa destacada em sincronia com a transcrição por palavra (whisper-cpp).
- Fontes: Montserrat Black, Anton, Bebas Neue, The Bold Font. Tamanho base 72–84px em 1080x1920.
- Cores: base `#FFFFFF`; destaque `#FFE600` (amarelo), `#39FF14` (verde) ou `#00F0FF` (ciano). Uma cor de destaque por vídeo.
- Stroke preto **4 a 6px**, sombra projetada suave.

---

## 6. Ritmo, cadência e áudio — fonte única de valores
- **Cadência de mudança visual:** algo muda na tela a cada **2 a 4 segundos** (corte de ângulo, insert, overlay, punch-in). Máximo absoluto: **4s** sem mudança.
- **Insert de B-roll:** entre **1,5 e 3s** quando parado; pode passar de 3s só se tiver movimento interno.
- **Punch-in de ênfase:** 8 a 12% (padrão 10%), cortado na sílaba tônica.
- **Hook:** primeira frase de impacto antes de 3s; sem cumprimento, sem hesitação.
- **J-cut padrão:** áudio antecipa a imagem em 12 a 30 frames (a 30fps).
- **Loudness de entrega:** −14 LUFS integrado, pico real −1 dBTP, para Instagram, TikTok e YouTube. Trilha sob voz 12 a 18 dB abaixo da voz.

---

## 7. Smart Clipper — ferramentas locais (macOS, Apple Silicon)
- FFmpeg 9.0.1 (Homebrew) com `h264_videotoolbox`, `hevc_videotoolbox`, `prores_videotoolbox`, `libvpx-vp9` (decodifica WebM com alfa). **Sem** `libass`, `freetype` e `zscale`: não há `subtitles`, `ass`, `drawtext` nem tonemapping HDR fiel. Legenda e headline são renderizadas como overlay com alfa pelo HyperFrames e compostas com `overlay`. Sempre `-pix_fmt yuv420p -movflags +faststart`; fonte 10-bit/HDR é convertida para 8-bit antes.
- Transcrição: `whisper-cli` (pacote `whisper-cpp` do Homebrew). Modelo em `~/.nirvana/models/whisper/ggml-small.bin` (ou `medium` para PT com sotaque forte). Flags para palavra a palavra: `-ojf -ml 1 -sow`.
- Áudio para transcrição: WAV 16kHz mono PCM (`-ac 1 -ar 16000 -c:a pcm_s16le`), nunca MP3.
- `-ss`/`-to` antes de `-i` funciona a partir do FFmpeg 5; em versão mais antiga, usar `-t` com duração.
- Procedimento completo: `playbooks/smart-clipper.md`.

---

## 8. Colorização — fonte única de regras, números e ferramentas
Dono: `color-grading-colorist`. Juiz: `council-editorial-arbiter` (§8.5). Pesquisa de 02/10/2026 (fontes no fim da seção); comandos verificados nesta máquina no mesmo dia.

### 8.1 Ordem canônica do pipeline (não se inverte)
1. **Normalização técnica:** cada fonte vai para o espaço de trabalho (Rec.709 por padrão). Log (S-Log3, V-Log, C-Log, Apple Log, LogC) recebe a LUT técnica do fabricante (log → Rec.709) ou conversão por `colorspace`. **LUT criativa nunca se aplica direto em log.**
2. **Correção primária:** exposição, balanço de branco, contraste, saturação globais, por fonte, até todas parecerem da mesma câmera.
3. **Secundária:** isolamento de tom de pele (e céu/fundo quando preciso), depois da LUT técnica, porque LUTs deslocam pele para laranja/magenta.
4. **Look criativo:** LUT ou receita (CDL: slope/offset/power), com intensidade parcial (referência 50–70%, nunca 100% por padrão).
5. **Entrega:** compensação de plataforma (§8.3) e metadados de cor gravados.
Fluxo com color management completo (DaVinci Wide Gamut/Intermediate ou ACES) fica no Resolve; a esteira automatizada recebe o resultado como `.cube` ou CDL.

### 8.2 Regras práticas
- **Tom de pele:** na skin line do vectorscope (entre vermelho e amarelo, ~11h), vale para qualquer etnia; saturação de pele em 20–50% do raio do vectorscope para parecer natural.
- **Waveform:** highlights sem clipping (abaixo de 100 IRE / 235 em 8-bit vídeo), shadows sem crush (acima de 0 IRE / 16).
- **Continuidade:** sem salto de exposição, balanço ou saturação entre cortes consecutivos; corrigir fonte a fonte antes do look.
- **Short-form:** look mais contido que em longo; o grade não pode competir com legenda e headline.
- **Fontes misturadas** (câmera, banco de imagens, IA): normalizar primeiro, look por último, mesmo grão/mesma temperatura.

### 8.3 Entrega por plataforma (o que a compressão faz e como compensar)
| Plataforma | Espaço/profundidade de entrega | Efeito observado da compressão | Compensação |
|---|---|---|---|
| Instagram Reels | Rec.709 SDR 8-bit (HDR só via HEVC 10-bit HLG, Rec.2100; PQ é rebaixado para SDR) | desatura vermelhos/laranjas, levanta shadows | +10–15% saturação, contraste um pouco acima do neutro |
| TikTok | Rec.709 SDR (HDR não é aceito de forma confiável) | esmaga pretos, desatura midtones, puxa quente | +10–15% saturação, proteger shadows (não deixar abaixo de 16) |
| YouTube / Shorts | Rec.709 SDR; aceita HDR (HLG/PQ) em 10-bit | mais fiel; HDR só com monitoração própria | sem compensação agressiva |
Sempre gravar metadados: `-color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv`. Entregar 1080x1920 H.264/HEVC, bitrate alto (8–12 Mb/s).

### 8.4 Looks e biblioteca de LUTs
**Looks com receita conhecida**
- **Teal & orange:** shadows frias (teal), highlights e pele quentes (laranja). Em short-form, sutil.
- **Bleach bypass:** desaturação 15–20% + curva S de contraste, tom frio e pálido (*Saving Private Ryan*).
- **Emulação de filme de impressão:** Kodak 2383 (contraste alto, saturação natural baixa), Kodak 2393, Fuji 3513/3510. Após a LUT: balanço de branco → offset um pouco para cima → highlights para baixo → saturação para cima.
- **Neutro limpo:** correção primária + skin tone, sem look. É o padrão quando o pedido não declara look.

**Repositórios no GitHub (ordenados por estrelas em 02/10/2026; só entram com licença conferida)**
| Estrelas | Repositório | O que é |
|---|---|---|
| 2.661 | `colour-science/colour` | Biblioteca Python de ciência da cor: lê/escreve `.cube`, `.3dl`, `.csp`, conversões de espaço, CDL |
| 668 | `hahnec/color-matcher` | Color matching automático entre imagens (casar B-roll com A-roll) |
| 598 | `ozwaldorf/lutgen-rs` | Gerador/aplicador de LUT a partir de paletas, em Rust, CLI |
| 525 | `jedypod/open-display-transform` | Display transforms de gamut amplo (alternativa aberta a ACES para look base) |
| 492 | `shenmintao/Raw-Alchemy` | Aplica LUT criativa de vídeo em foto com fidelidade (ponte foto↔vídeo) |
| 330 | `Greenysmac/awesome-davinci-resolve` | Lista curada de plugins, DCTLs, LUTs e recursos do Resolve |
| 323 | `colour-science/awesome-colour` | Lista curada de recursos de ciência da cor |
| 276 | `YahiaAngelo/Film-Luts` | Coleção de LUTs de emulação de filme (G'MIC) |
| 229 | `changyun233/Lumix-V-log-LUTs` | LUTs gratuitas V-Log → Rec.709 (Panasonic) |
| 163 | `imnz730/LUTs` | LUTs técnicas e informações de gerenciamento de cor |
| 121 | `Wavechaser/NamiColor` | DCTL para linearizar scans de filme no Resolve |
| 116 | `jeremieLouvaert/ComfyUI-Darkroom` | 161 emulações de filme (ComfyUI) |
| 114 | `digitaltvguy/NBCUniversal-UHD-HDR-SDR-...-LUTs` | LUTs de produção HDR↔SDR da NBCUniversal |
| 108 | `yoonsikp/pycubelut` | Aplica `.cube` em imagens, Python |
| 102 | `JanLohse/spectral_film_lut` | Gera LUT de emulação a partir de datasheet de filme |
| 90 | `seunghyuns98/VideoColorGrading` | Pesquisa ICCV 2025: grade de vídeo por geração de LUT |
| 58 | `aras-p/smol-cube` | Formato binário equivalente a `.cube` |
Observação: no GitHub, pacotes de LUT "cinematográficas" comerciais têm poucas estrelas e licença duvidosa; os repositórios de peso são de ferramentas e de LUTs técnicas. LUT criativa de qualidade vem de autores reconhecidos (ex.: Juan Melara, emulações Kodak/Fuji) com licença comprada, registrada em `lut-library-manifest`.

### 8.5 Checklist de QA de cor (o conselho aplica a cada clipe)
1. Tom de pele na skin line? Saturação de pele em 20–50%?
2. Sem salto de exposição/balanço/saturação entre cortes?
3. Highlights sem clipping e shadows sem crush no waveform?
4. Look visível sem roubar a cena? Se saturado demais, reduzir a intensidade da LUT.
5. Nenhum cast global não intencional?
6. Compensado para a plataforma (§8.3) e metadados de cor gravados?
7. Scopes consultados e anexados (PNG), não só o olho?
8. LUT com origem e licença registradas?

### 8.6 Comandos verificados (FFmpeg 9.0.1 desta máquina)
Aplicar LUT `.cube` com profundidade maior que a fonte 8-bit, e voltar para 4:2:0 na saída:
```bash
ffmpeg -y -i clip.mp4 -vf "format=gbrp16le,lut3d=file=look.cube:interp=tetrahedral,format=yuv420p" \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -c:v h264_videotoolbox -b:v 8M -c:a copy -movflags +faststart clip_graded.mp4
```
Normalização técnica log → Rec.709 quando há LUT do fabricante: mesmo comando com a LUT técnica primeiro e a criativa depois (`lut3d=tech.cube,lut3d=look.cube`). Sem LUT do fabricante, `colorspace=all=bt709:iall=bt2020` cobre só gamut/primárias, não a curva log.
Primária por filtros (quando não há LUT): `eq=brightness=0.02:contrast=1.05:saturation=1.1`, `colortemperature=temperature=5600`, `colorbalance=rs=0.03:bs=-0.03`, `curves=preset=medium_contrast`.
Scopes (frame + waveform + vectorscope num PNG):
```bash
ffmpeg -y -ss 2 -i clip_graded.mp4 -frames:v 1 -vf "scale=540:-2,split=3[a][b][c];[a]waveform=mode=column:intensity=0.2[w];[b]vectorscope=mode=color3:graticule=green:flags=name[v];[c][w]vstack[sw];[v]scale=540:-2[v2];[sw][v2]vstack" scopes.png
```
Leitura numérica e metadados:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=color_range,color_space,color_transfer,color_primaries,pix_fmt -of csv=p=0 clip.mp4
ffmpeg -i clip.mp4 -vf "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -frames:v 10 -f null -
```
Comparar looks lado a lado (HyperFrames): `npx hyperframes grade-compare --for clip.mp4 --luts a.cube,b.cube --out grade-compare.png` (o original entra como linha de base).
Grade dentro de composição HyperFrames: `npx hyperframes media-treatment --selector video --grading '<json>' --apply`; presets disponíveis: neutral, warm-daylight, clean-studio, skin-soft, food-pop, night-lift, muted-editorial, vintage-wash, mono-clean, mono-fade, soft-boost, bright-pop, deep-contrast; LUT `.cube` até 64³ com `intensity` 0–1.

### 8.6b Ferramentas complementares (levantamento de 02/10/2026; não executadas nesta máquina)
- **OpenColorIO 2.4** (`brew install opencolorio` ou `pip install opencolorio`): `ociobakelut` gera `.cube`/ICC a partir de um config (`--inputspace`, `--outputspace`, `--shaperspace`, `--format cube`); `ocioconvert` aplica transformações a imagens; `ociochecklut` valida LUT. Caminho para fluxo ACES fora do Resolve.
- **`colour-science` (Python, 2.661 estrelas):** `colour.read_LUT()` / `colour.write_LUT()` para `.cube`, `.3dl`, `.csp`, CLF; conversão entre formatos e inspeção programática de LUT. **`pylut`** (`gregcotten/pylut`): cria, modifica e converte `.cube`/`.3dl` por código.
- **`lut3d` em outros formatos:** aceita `.cube`, `.3dl`, `.dat`, `.m3d`, `.csp`; `interp` = `nearest` | `trilinear` | `tetrahedral` | `pyramid` | `prism`. `haldclut` aplica LUT em forma de imagem (dois inputs). `lut1d` para curvas tonais.
- **DaVinci Resolve** (gratuito; Studio acrescenta HDR grading room e Fusion completo): pasta de LUT no macOS `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/`; aceita `.cube`, `.3dl`, `.m3d`. **Final Cut Pro:** efeito Custom LUT (`.cube`, `.mga`), Apple Log nativo. **Premiere/Lumetri:** Input LUT (Basic Correction) para técnica, Creative para look.
- **CapCut:** presets e HSL para short-form; serve para protótipo rápido, não para entrega fina.

### 8.7 Fontes da pesquisa (02/10/2026)
FFmpeg Filters Documentation · Jeff Geerling, apply LUT with FFmpeg (jan/2026) · OpenColorIO 2.4 release notes e tool overview (set/2024) · colour-science (PyPI/GitHub) · pylut (GitHub) · Apple Support, Custom LUT no Final Cut Pro · Adobe, Premiere color workflows · Frame.io, Premiere color guide 2024 · Vidar Andersen, "On my color grading in 2025" · Miracamp, best color space in DaVinci · Daniel Grindrod, skin tone · Video Editing Tips, scopes · Passion Fuels Ambition, color grading para TikTok/Reels/Shorts · Luminxel, Rec.2100 PQ vs HLG · The Post Flow, export settings YouTube/Instagram/TikTok · Pixflow, teal & orange · Boris FX, bleach bypass no Resolve · Juan Melara, print film emulation LUTs · Blackmagic Design, treinamento oficial (Introduction to Color, Advanced Color, Color Management) · Canais: Waqas Qazi, Cullen Kelly, Darren Mostyn, Casey Faris, Team2Films.

---

## 9. Gramática de transição (qual corte, em qual situação)
Complemento da §1. O diretor decide; o conselho cobra.
| Situação | Corte padrão | Evitar |
|---|---|---|
| Diálogo e entrevista | J-cut (áudio antecipa 12–30 frames) e corte na reação | corte seco na última sílaba |
| Fala contínua com hesitação | jump cut com punch-in de 8–12% para disfarçar | dissolve (denuncia o salto) |
| Mudança de assunto dentro do mesmo vídeo | smash cut ou whip pan com som (whoosh) | cross dissolve |
| Passagem de tempo, memória, sonho | cross dissolve curto (8–15 frames) | dissolve longo em short-form |
| Entrada de B-roll ilustrando a fala | hard cut na sílaba tônica ou J-cut do som ambiente | fade |
| Dois lugares em paralelo | cross-cutting em cadência crescente | alternância aleatória |
| Objeto/forma que rima com a próxima cena | match cut | usar match cut sem rima real |
| Revelação, humor, apresentação de personagem | freeze frame ou crash zoom | repetir no mesmo vídeo |
| Tensão que precisa respirar | não cortar (long take), silêncio antes do impacto | encher o silêncio com B-roll |
Regra geral: em short-form, no máximo um efeito de transição visível (whip, dissolve, wipe) a cada 15–20s; o resto é corte seco bem colocado.

---

## 10. Runtimes e orquestração de modelos
Esta empresa é portátil: roda em qualquer runtime com adapter no motor (Claude Code, Codex, Antigravity, pi, Hermes; a lista viva está em `~/.nirvana/skills/_shared/adapters/README.md`). O que não muda entre runtimes: os arquivos da empresa, as rotas, a aceitação por cargo, a memória e os comandos de terminal (FFmpeg, whisper-cpp, HyperFrames, `nrv`).

**Como o modelo é escolhido.** O motor só fixa modelo no Claude Code; nos demais runtimes o modelo é o que o usuário configurou no próprio runtime (ou `NIRVANA_MODEL`). Por isso o `model:` de cada cargo é **intenção de tier**, traduzida pelo `model_policy` do `business.yaml`:
| Tier | Cargos | Claude Code | Codex / Antigravity / pi / Hermes |
|---|---|---|---|
| forte (julgamento, orquestração) | diretor, conselho | `opus`, effort high | Codex: **Astra** (OpenAI, decisão do dono 02/10/2026; passa por `NIRVANA_MODEL`, senão vale o model do `~/.codex/config.toml`); demais: modelo do runtime, effort high |
| padrão (execução com desenho decidido) | editor de cortes, colorista, câmera, B-roll, motion, legendas | `sonnet`, effort high | modelo do runtime |
`fable` só entra por decisão do dono (`NIRVANA_MODEL=fable`), nunca por padrão: o gate da casa reserva o tier mais caro para erro silencioso e caro, e edição de vídeo não é esse caso.

**Diferenças de runtime que mudam o trabalho.** Claude Code: subagentes em processo e notificações de conclusão. Codex: sandbox forte, subagentes via `[agents]`, sem hooks finos, sem agendamento. pi: um runtime para 15+ provedores e modelos locais (útil para rodar sem custo por token). Hermes: cron e escalação por mensagem. Em runtime sem subagente em processo, o despacho é pelo caminho `nrv dispatch --exec`.

**Astra** é modelo da OpenAI (esclarecido pelo dono em 02/10/2026), não runtime: roda pelo Codex. O `~/.codex/config.toml` desta máquina está em `gpt-5.6-sol`; para o tier forte usar Astra, o id exato do modelo entra em `NIRVANA_MODEL` ou no `model` do config do Codex.

## 11. Como esta empresa aprende (melhoria contínua)
Protocolo completo: `playbooks/debriefing.md`. Resumo: todo run escreve lições no `memory.md` do projeto; no fim da entrega e a cada correção do usuário o diretor faz o debrief (cinco perguntas), o conselho carimba o que generaliza, e o dono promove com um "sim". A promoção é `nrv memory add magic-frames "<fato>"`, que o motor injeta em todo prompt de funcionário como memória ativa, em qualquer runtime. Nada se apaga: fato que muda é substituído (`nrv memory supersede`). Padrões de muitos runs saem do `nrv improver`.


## 12. Voz única e biblioteca
- **Merlin** é a única voz: a pessoa fala sempre com o Lead Editorial Director na persona Merlin (definida no arquivo do cargo, para viajar com a empresa). Nenhum outro cargo atende o cliente.
- **Biblioteca de assets:** `playbooks/asset-library.md` (taxonomia igual no disco e no Google Drive, índice com fonte e licença, contact sheets por `ffmpeg tile`). Dono: curador de B-roll.
- **Biblioteca dentro da empresa (`library/`, viaja no pacote):** 17 LUTs em `40_luts/` (14 looks numerados sem autor, 2 'LA CREME REC 709', 1 técnica DJI Avata 2 D-Log M → Rec.709), 122 efeitos sonoros em `60_audio/sfx/` (packs 'SFX FPV [Mini Disc]' e 'Filmkid SFX Bundle'), 30 molduras PNG com alfa em `50_overlays/frames/` (@harrisonniap). Cada pasta tem manifesto com origem e licença; em 02/10/2026 tudo está `pendente` até o dono confirmar compra/termos, e o que está pendente não entra em entrega nem no pacote de venda.
- **Referências e notícias:** `reference-scout` entrega `reference-board` datado; padrão só com dois exemplos por plataforma; insert só com direito de uso classificado.

## 13. Conexões com editores (MCP) — camada opcional por runtime
Instaladas em 02/10/2026 nesta máquina e registradas no Claude Code (escopo usuário) e no Codex. A esteira da empresa roda sem elas (FFmpeg + HyperFrames); elas entram quando o runtime as oferece e o aplicativo está instalado. Em outra máquina, instalar de novo (comandos abaixo) ou seguir sem.

| Editor | Servidor (estrelas no GitHub em 02/10/2026) | Nome registrado | Precisa de | Estado nesta máquina |
|---|---|---|---|---|
| DaVinci Resolve | `samuelgursky/davinci-resolve-mcp` (3.291, MIT) | `davinci-resolve` | Resolve 18.5+ (**Studio** para scripting externo; no gratuito, ponte interna por Workspace ▸ Scripts ▸ resolve_bridge) | instalado em `~/Library/Application Support/davinci-resolve-mcp`; Resolve não instalado, API não detectada |
| Adobe Premiere Pro | `hetpatel-11/Adobe_Premiere_Pro_MCP` (641, MIT) | `premiere-pro` | Premiere 2020+ com o painel `Window ▸ Extensions ▸ MCP Bridge (CEP)` iniciado | pacote npm `adobe-premiere-pro-mcp` global; painel CEP instalado, modo debug ativado; Premiere não instalado |
| Final Cut Pro | `DareDev256/fcp-mcp-server` (113, MIT, PyPI) | `fcpxml` | Final Cut (troca por FCPXML exportado/importado; pasta `FCP_PROJECTS_DIR=~/Movies`) | roda por `uvx --python 3.12 fcp-mcp-server`; testado |
| CapCut | `mrbuslov/capcut-ai-editor` (115, MIT) | `capcut-smartcut` | CapCut instalado; edita o rascunho em disco (corta pausas, takes repetidos, legenda) | clonado em `~/.nirvana/tools/mcp/capcut-ai-editor` com venv Python 3.12; **não testado** (a execução foi bloqueada pela política da sessão) |

**Regra de uso (decisão do dono, 02/10/2026): editor é opt-in da pessoa, projeto a projeto.** O padrão da Magic Frames é a esteira própria (FFmpeg + HyperFrames, entrega em MP4). Na entrada, o Merlin pergunta onde a pessoa quer o resultado (esteira própria, CapCut, Premiere, Final Cut ou Resolve); a resposta fica na memória do projeto e vale só para ele. Nenhum cargo abre um editor que a pessoa não escolheu, e CapCut não é usado por padrão em nenhum fluxo. Preferência repetida ("sempre no Premiere") vira candidato de memória no debrief, e só vira regra com o sim do dono.

**Quem usa o quê (quando escolhido).** Colorista → `davinci-resolve` (cor dentro do Resolve, exporta `.cube`/CDL de volta para a esteira). Editor de cortes → `capcut-smartcut` (talking head rápido), `premiere-pro` e `fcpxml` (quando o cliente trabalha nesses editores e quer a timeline de volta). Motion → nenhum; HyperFrames é o motor. Regra: o resultado do editor volta para a esteira como arquivo (XML, `.cube`, MP4) e passa pelos mesmos revisores; o editor é ferramenta, não atalho para pular o conselho.

**Reinstalar em outra máquina.**
```bash
npx davinci-resolve-mcp setup --clients manual            # depois registrar o comando impresso
npm install -g adobe-premiere-pro-mcp && premiere-pro-mcp --install-cep
claude mcp add -s user fcpxml -e FCP_PROJECTS_DIR=$HOME/Movies -- uvx --python 3.12 fcp-mcp-server
git clone https://github.com/mrbuslov/capcut-ai-editor ~/.nirvana/tools/mcp/capcut-ai-editor  # venv 3.12, pip install -e ., mcp<2
```
Alternativas abertas feitas para agente, não instaladas: `jub0t/Concat` (3.977, substituto do CapCut com MCP) e `pireel/pireel` (1.251). Não instalada de propósito: `SpliceKit` (160), porque remenda o binário do Final Cut.
