# Como instalar e usar a Magic Frames

A Magic Frames é uma empresa do Nirvana-OS: nove cargos de edição de vídeo que trabalham juntos, com uma voz só (o Merlin). Este repositório traz a empresa inteira, biblioteca de assets incluída (ver "Biblioteca").

## O que precisa estar na máquina

Obrigatório:

- **Nirvana-OS** (`nrv`) instalado e licenciado, com **Bun** (o motor não roda em Node). Instalador: `npx @nirvana-os/cli`. A licença é por máquina; quem te enviou a empresa indica como obter a sua.
- **FFmpeg** e **ffprobe**. No Mac com Apple Silicon o render usa o encoder `h264_videotoolbox`; em outra máquina qualquer encoder H.264 serve.
- **whisper-cpp** (`whisper-cli`) com um modelo ggml para a transcrição por palavra do Smart Clipper. O playbook `playbooks/smart-clipper.md` mostra o download do modelo.
- **Node** com `npx hyperframes` para os overlays e legendas em motion design.
- **Python 3** para `scripts/check_safe_zone.py`.

Opcional, melhora o resultado:

- Pacote `genesis-circle` do catálogo Nirvana: traz os cinco mind-clones que os cargos citam (`walter-murch`, `roger-deakins-cinematographer`, `joey-korenman-motion`, `alex-hormozi`, `ali-abdaal-creator`) e os squads de vídeo preferidos (`nirvana-video-creator`, `veo-motion-studio`, `vivid-pancake-keyframe-i2v`). Sem eles a empresa roda; com eles ganha voz e ferramentas.
- Conexões com editores (DaVinci Resolve, Premiere, Final Cut via FCPXML, CapCut). São servidores MCP instalados no seu runtime; `memory/permanent.md` §13 tem a tabela e os comandos.
- `opencolorio` para conversões de cor mais finas (§8.6b da memória).

## Instalar

Direto do GitHub:

```bash
nrv install git+https://github.com/inguz-studio/magic-frames
```

Ou a partir do pacote `.tgz`, conferindo a integridade antes:

```bash
shasum -a 256 -c magic-frames-2.0.0.tgz.sha256
nrv install magic-frames-2.0.0.tgz
```

Depois confira:

```bash
nrv validate business magic-frames --strict
nrv list-businesses
```

Para atualizar quando sair uma versão nova, repita o `nrv install` com `--force` (o motor guarda uma cópia da versão anterior).

## Usar

Fale com a empresa em linguagem natural. O pedido entra pelo Merlin, que decide qual cargo atende:

```bash
nrv run magic-frames "Cortar o vídeo do podcast em 2 reels de 60s e 1 de 90s para o Instagram com legendas dinâmicas"
```

Outros pedidos que a empresa entende: colorização com LUT e tom de pele, pesquisa de reels e notícias para inserts, organização de biblioteca de B-roll, shotlist de câmera para vídeo gerado por IA, overlays em HyperFrames, parecer do conselho editorial sobre um corte bruto. A lista completa de exemplos está em `business.yaml` (`example_briefs`).

Para só preparar o pedido sem executar:

```bash
nrv dispatch magic-frames "<pedido>"
```

O resultado sai como arquivo (MP4, YAML, Markdown, `.cube`) na pasta de saída do projeto. Nenhum cargo abre um editor que você não escolheu na entrada.

## Ensinar a empresa

O que você aprende em uma entrega pode virar regra permanente:

```bash
nrv memory add magic-frames "<fato>"
```

O fato passa a entrar em todo pedido dali em diante. O protocolo completo está em `playbooks/debriefing.md`.

## Biblioteca

A pasta `library/` guarda LUTs (`40_luts/`), molduras com alfa (`50_overlays/`) e efeitos sonoros (`60_audio/`), e vem junto no repositório e no pacote. Cada subpasta tem um manifesto com origem e licença de cada arquivo. Enquanto um item estiver marcado como `pendente` no manifesto, os cargos não o usam em entrega; preencher o campo `licenca` libera o uso.
