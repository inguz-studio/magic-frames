# Playbook: Smart Clipper & Highlight Extractor

Dono: `smart-clip-editor`. Direção e janelas: `lead-editorial-director`. Legendas: `retention-subtitles-specialist`. Aprovação: `council-editorial-arbiter`.

Transforma vídeo longo armazenado localmente (podcast, aula, live, palestra, entrevista) em cortes verticais 9:16 de alta retenção para Instagram Reels, TikTok e YouTube Shorts (40s, 60s, 90s, 120s, 150s). Todos os números (zonas seguras, faixa de legenda, cadência, loudness) vêm de `memory/permanent.md` §5–§7; este playbook só os aplica.

Convenções dos comandos: `SRC` = vídeo de origem · `W` = diretório de trabalho (`scratch/`) · `OUT` = `outputs/clips/` · `IN`/`TO` = timestamps `hh:mm:ss.mmm` do corte.

---

## Fluxo Operacional Ponta a Ponta

```
[ Vídeo Longo Local ]
        │
        ├─► 1. Diagnóstico (ffprobe) e normalização para 8-bit se preciso
        ├─► 2. Áudio WAV 16kHz mono  →  transcrição por palavra (whisper-cli, JSON)
        ├─► 3. Mapa de pausas (silencedetect)
        ├─► 4. Seleção de momentos (hook → tensão → payoff) nas janelas pedidas, bordas ajustadas ao silêncio
        ├─► 5. Reenquadramento 9:16: Layout A (fundo desfocado + headline) · B (center-crop com deslocamento) · C (split screen)
        ├─► 6. Legendas: .ass do especialista → checagem mecânica de zona segura → queima
        ├─► 7. Overlays HyperFrames (opcional) compostos por alfa
        ├─► 8. Render final (VideoToolbox) + clip-manifest
        └─► 9. Checklist do conselho
```

---

## 1. Comandos

### A. Diagnóstico
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,r_frame_rate,pix_fmt,color_transfer -of json "$SRC"
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,channels,sample_rate -of json "$SRC"
```
Se `pix_fmt` for 10-bit (`yuv420p10le`) ou `color_transfer` for `arib-std-b67`/`smpte2084` (HDR), normalize antes de tudo. O FFmpeg do Homebrew não traz `zscale`, então o tonemapping fiel não está disponível aqui; a conversão abaixo mantém o fluxo funcionando com cores um pouco lavadas. Sempre que possível, grave a origem em SDR.
```bash
ffmpeg -i "$SRC" -vf "format=yuv420p" -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:v h264_videotoolbox -b:v 12M -c:a copy "$W/src_sdr.mp4"
```

### B. Áudio para transcrição (WAV 16kHz mono, nunca MP3)
```bash
ffmpeg -y -i "$SRC" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$W/audio.wav"
```

### B2. Transcrição por palavra (whisper-cpp)
Modelo, uma vez (~470 MB, fonte oficial do projeto):
```bash
mkdir -p ~/.nirvana/models/whisper && curl -L -o ~/.nirvana/models/whisper/ggml-small.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
```
Transcrição:
```bash
whisper-cli -m ~/.nirvana/models/whisper/ggml-small.bin -l pt -f "$W/audio.wav" -ojf -ml 1 -sow -of "$W/transcript"
```
Gera `$W/transcript.json` com um segmento por palavra e `offsets.from/to` em ms. É a entrada da seleção (passo 4) e da legenda karaokê (passo 6). Para sotaque forte ou áudio ruim, troque para `ggml-medium.bin`.

### C. Mapa de pausas
```bash
ffmpeg -i "$W/audio.wav" -af silencedetect=noise=-30dB:d=0.4 -f null - 2>&1 | grep -E "silence_(start|end)" > "$W/silences.txt"
```

### D. Seleção de momentos (passo agêntico, com regras fixas)
O editor lê `transcript.json` e `silences.txt` e produz candidatos por janela. Regras:
1. Começa numa frase de impacto (afirmação contraintuitiva, número, pergunta, história). Nunca em cumprimento, hesitação ("hmm", "então...") ou meio de palavra.
2. Termina numa frase conclusiva. Nunca em conjunção ("mas", "porque", "então", "e").
3. As bordas `IN`/`TO` se movem para o `silence_start`/`silence_end` mais próximo (tolerância ±1,5s) para não cortar sílaba.
4. Duração dentro da janela pedida ±3s.
5. Cada candidato registra `hook` (primeira frase) e `payoff` (última frase) no `clip-manifest`.

### E. Reenquadramento 9:16 (canvas 1080x1920)
Flags comuns a todos os renders: `-c:v h264_videotoolbox -b:v 8M -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`.

**Layout A — fundo desfocado + vídeo centralizado + headline** (podcast/entrevista 16:9). A headline (frase-gancho do corte) não usa `drawtext` (o FFmpeg do Homebrew vem sem ele); ela entra como estilo `Headline` do mesmo `.ass` das legendas (Alignment 8, MarginV 300, §5.2) e é queimada no passo F.
```bash
ffmpeg -y -ss "$IN" -to "$TO" -i "$SRC" -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg]; \
[0:v]scale=1080:-2[fg]; \
[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p" \
-c:v h264_videotoolbox -b:v 8M -c:a aac -b:a 192k -movflags +faststart "$OUT/clip_${N}_A.mp4"
```

**Layout B — center-crop com deslocamento** (`XOFF` em px a partir do centro, positivo para a direita; defina por corte olhando um frame, nunca assuma 0).
```bash
ffmpeg -y -ss "$IN" -to "$TO" -i "$SRC" -filter_complex "\
[0:v]crop=ih*9/16:ih:(iw-ow)/2+${XOFF}:0,scale=1080:1920,format=yuv420p" \
-c:v h264_videotoolbox -b:v 8M -c:a aac -b:a 192k -movflags +faststart "$OUT/clip_${N}_B.mp4"
```

**Layout C — split screen: orador em cima, B-roll embaixo** (`BROLL` vem do `broll-insert-manifest`; faz loop até o fim do corte).
```bash
ffmpeg -y -ss "$IN" -to "$TO" -i "$SRC" -stream_loop -1 -i "$BROLL" -filter_complex "\
[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[top]; \
[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bot]; \
[top][bot]vstack=inputs=2,format=yuv420p[v]" \
-map "[v]" -map 0:a -shortest -c:v h264_videotoolbox -b:v 8M -c:a aac -b:a 192k -movflags +faststart "$OUT/clip_${N}_C.mp4"
```

### F. Legendas: contrato em ASS, checagem mecânica, render por overlay com alfa
O `retention-subtitles-specialist` gera `$W/clip_${N}.ass` a partir do `transcript.json` (PlayRes 1080x1920, estilos `Caption` e `Headline` com as margens de §5.2–§5.3). O `.ass` é o contrato de posição e estilo, e é o que a checagem valida:
```bash
python3 scripts/check_safe_zone.py "$W/clip_${N}.ass"
```
Sai 0 quando está dentro da faixa; 1 lista cada violação. Nada é renderizado antes do 0.

**Render das legendas.** O FFmpeg do Homebrew (9.0.1) vem **sem** `libass`/`freetype`, então `subtitles=`, `ass=` e `drawtext` não existem nesta máquina. O caminho padrão da casa é renderizar legenda e headline como overlay com alfa pelo `motion-hyperframes-engineer` (composição karaokê que lê o `transcript.json` e as mesmas margens do `.ass` via `--variables`), e compor com `overlay`:
```bash
npx hyperframes render --format webm --resolution portrait --variables "$(cat $W/clip_${N}.vars.json)" -o "$W/captions_${N}.webm"
ffmpeg -y -i "$OUT/clip_${N}_A.mp4" -c:v libvpx-vp9 -i "$W/captions_${N}.webm" -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p" -c:v h264_videotoolbox -b:v 8M -c:a copy -movflags +faststart "$OUT/clip_${N}_A_sub.mp4"
```
Queima direta do `.ass` só num FFmpeg com libass (`ffmpeg -filters | grep subtitles` retorna algo):
```bash
ffmpeg -y -i "$OUT/clip_${N}_A.mp4" -vf "subtitles=$W/clip_${N}.ass" -c:v h264_videotoolbox -b:v 8M -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT/clip_${N}_A_sub.mp4"
```
Em qualquer caminho, o conselho confere um frame do resultado (`ffmpeg -ss 2 -i clip.mp4 -frames:v 1 frame.png`), porque a checagem valida o contrato, não os pixels.

Punch-in de ênfase (§6) é feito no passe do layout quando pedido: `zoompan` ou `scale=1.1*iw:-2,crop=1080:1920` entre `enable='between(t,A,B)'`.

### G. Overlays HyperFrames de dados e lower thirds (opcional)
Mesmo caminho do passo F, outra composição:
```bash
npx hyperframes render --format webm --resolution portrait -o "$W/overlay_${N}.webm"
ffmpeg -y -i "$OUT/clip_${N}_A_sub.mp4" -c:v libvpx-vp9 -i "$W/overlay_${N}.webm" -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p" -c:v h264_videotoolbox -b:v 8M -c:a copy -movflags +faststart "$OUT/clip_${N}_final.mp4"
```
Para cortes na batida de uma trilha: `npx hyperframes beats "$W/music.wav"` gera `beats/music.json`; os pontos de corte do passo D se alinham às batidas mais próximas.

### H. Loudness e verificação final
```bash
ffmpeg -i "$OUT/clip_${N}_final.mp4" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=summary -f null - 2>&1 | tail -12
ffprobe -v error -show_entries format=duration:stream=width,height,pix_fmt -of csv=p=0 "$OUT/clip_${N}_final.mp4"
```
Se o integrado estiver fora de −14 ±1 LUFS, re-renderize o áudio com `-af loudnorm=I=-14:TP=-1:LRA=11`.

---

## 2. Critérios de Seleção dos Cortes por Duração

| Duração | Estrutura Psicológica | Objetivo no Instagram |
|---|---|---|
| **40s** | Hook Agressivo (3s) → 1 Afirmação Contraintuitiva → Payoff Imediato → CTA | Viralidade máxima, compartilhamentos em Stories |
| **60s** | O Padrão Ouro: Tese → Tensão/Obstáculo → Revelação da Solução | Retenção máxima no feed de Reels |
| **90s** | Narrativa Curta: História antes/depois, erro clássico e reviravolta | Autoridade e salvamento de post |
| **120s (2m)** | Masterclass Compacta: Decomposição de processo em 3 passos | Conversão de leads e engajamento qualificado |
| **150s (2m30)**| Discussão Conceitual: Debate aprofundado, reflexão filosófica/estratégica | Audiência madura e alta conexão |

---

## 3. Checklist do Conselho para o Conjunto de Cortes

1. **Os primeiros 3 segundos seguram o scroll?** Frase de impacto, sem hesitação, cumprimento ou risinho.
2. **O raciocínio termina fechado?** Última frase conclusiva, não conjunção.
3. **Zona segura provada?** `check_safe_zone.py` saiu 0 para cada `.ass`; conferido também num frame (`ffmpeg -ss 5 -i clip.mp4 -frames:v 1 frame.png`).
4. **Cadência (§6) cumprida?** Nenhum trecho passa do máximo sem mudança visual; punch-ins na sílaba tônica.
5. **Enquadramento certo?** Em layout B, o orador está inteiro no quadro em pelo menos três frames amostrados (início, meio, fim).
6. **Loudness (§6) dentro do alvo?**
7. **clip-manifest completo?** `timestamp_in/out`, duração, layout, `XOFF`, `hook`, `payoff`, caminho do `.ass` e do MP4.
