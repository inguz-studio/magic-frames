# Animações de texto — presets da casa

Um preset por pasta. Cada preset é uma composição HyperFrames (HTML/CSS/GSAP) parametrizada: o cargo passa texto, fonte (por id de `../70_fonts/fonts-manifest.yaml`), cor, tamanho e tempos por variáveis, e renderiza com alfa (`npx hyperframes render --format webm`, ou `--format mov` para ProRes 4444) em 1080x1920 (`--resolution portrait`). Para legenda sincronizada, o preset lê o `transcript.json` do whisper (palavra a palavra).

```
<preset-id>/
├── index.html        # composição; carrega ../../70_fonts/fonts.css; root timeline em window.__timelines
├── preset.yaml       # nome, uso, variáveis (nome, tipo, padrão), formatos que combinam, zona segura
├── vars.example.json # exemplo de variáveis (`--variables-file`) e linha-modelo para `render --batch`
└── preview.png       # frame-chave gerado por `npx hyperframes snapshot`
```

Mecânica do HyperFrames: as variáveis são declaradas em `data-composition-variables` no `<html>` (id, type string|number|color|boolean|enum, label, default) e lidas com `window.__hyperframes.getVariables()`; o render recebe `--variables '{...}'`, `--variables-file vars.json` ou `--batch rows.json`, e `--strict-variables` recusa variável desconhecida. Fundo de `html`, `body` e da composição sem pintura, senão o alfa vira pixel opaco. Timeline GSAP `paused: true` registrada em `window.__timelines[<data-composition-id>]`, só `fromTo` em transform e opacity, sem `Math.random()` e sem `repeat: -1`. Preview: `npx hyperframes snapshot . --at <segundos> --zoom '#stage'`.

Regras: posição dentro da zona segura de legenda (`memory/permanent.md` §5); easing da casa (`cubic-bezier(0.16, 1, 0.3, 1)` ou spring), nunca linear; `npx hyperframes check` sem erro antes de entrar aqui; preview obrigatório para o diretor e o conselho escolherem sem renderizar. O índice é `presets-manifest.yaml`.
