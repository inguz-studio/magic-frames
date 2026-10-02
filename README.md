# Magic Frames — Estúdio de Edição Cinematográfica, Vídeo Longo, Short-Form & Motion Intelligence

O **Magic Frames** (até 02/10/2026 chamada CineCut Studio; renomeada para entrar na família do Magic Studio, com o Merlin como voz) é uma empresa autônoma e de alto calibre criada por Vitor Piagge, especializada em elevar produções audiovisuais ao padrão de Hollywood e YouTube de alta retenção. Unimos a teoria de montagem clássica à engenharia de prompts para câmeras de IA, mineração automatizada de B-rolls reais e criação de motion overlays determinísticos em código via HyperFrames e Remotion.

---

## 1. Mission & Scope

Nossa missão é eliminar o abismo entre o vídeo genérico amador e as produções audiovisuais memoráveis. Atuamos em toda a esteira de pós-produção e direção de corte:
- **Gramática de Montagem Profissional:** Aplicação rigorosa das 17 técnicas clássicas de edição, com destaque para J-Cuts e L-Cuts fluidos, cortes na ação e transições invisíveis.
- **Direção de Câmera & Fotografia para IA:** Engenharia de prompts estruturados para ferramentas como Veo 3.1, Sora e Kling, especificando enquadramentos, ângulos de câmera, ópticas e movimentos com precisão cirúrgica.
- **Mineração & Curadoria de Assets Reais:** Integração via MCP com bancos de imagem (Pexels, Pixabay, Unsplash) e download de mídias de referência pública para criar uma teia rica de B-rolls que sustentam o ritmo a cada 2 a 3 segundos.
- **Motion Design Code-Based (HyperFrames & Remotion):** Substituição do After Effects por overlays determinísticos em código web (HTML/CSS/GSAP/React), gerando cards de dados, kinetic typography e lower thirds leves e reproduzíveis por agentes.
- **Retenção & Legendas Padrão Creator:** Pacotes de legendas estilo Alex Hormozi (1 a 3 palavras por linha, destaque karaokê, stroke preto) e respeito absoluto às Safe Zones das redes sociais.
- **Conselho Executivo de Edição:** Gating de qualidade adversarial com conselheiros virtuais inspirados em Walter Murch, Thelma Schoonmaker, Kirk Baxter, Sally Menke e Hayden Hillier-Smith.
- **Colorização:** Pipeline de cor em ordem fixa (técnica → primária → skin tone → look → entrega), LUTs com licença registrada, scopes como prova e compensação por plataforma (`memory/permanent.md` §8).
- **Smart Clipper:** Corte de vídeo longo local (podcast, aula, live, entrevista) em clipes verticais 9:16 de 40 a 150s, com transcrição por palavra (whisper-cpp), seleção de momentos, reenquadramento e render acelerado por VideoToolbox via FFmpeg (`playbooks/smart-clipper.md`).

---

## 2. Org Chart & Roles

O estúdio opera com 9 cargos. A pessoa fala sempre com um só: **Merlin**, a voz do Lead Editorial Director; os outros oito trabalham por baixo e nunca atendem o cliente diretamente.

```
                        ┌──────────────────────────────┐
                        │   Merlin · Lead Editorial    │
                        │   Director (voz única)       │
                        └──────────────┬───────────────┘
        ┌──────────────┬───────────────┼───────────────┬──────────────┬──────────────┐
        │              │               │               │              │              │
 ┌──────┴──────┐ ┌─────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐
 │ Smart Clip  │ │ Cinematog. │ │ Asset &     │ │ Motion &    │ │ Retention  │ │ Council    │   + Color Grading Colorist · Reference Scout
 │ Editor      │ │ & AI Cam.  │ │ B-Roll      │ │ HyperFrames │ │ & Subtitles│ │ Editorial  │
 │ (Clipper)   │ │ Director   │ │ Curator     │ │ Engineer    │ │ Specialist │ │ Arbiter ⚔  │
 └─────────────┘ └────────────┘ └─────────────┘ └─────────────┘ └────────────┘ └────────────┘
```

1. **Merlin, Lead Editorial Director (`lead-editorial-director`):** A voz única do estúdio. Orquestrador geral, arquiteto da narrativa, intake de projetos e dono do debrief.
2. **Cinematography & AI Camera Director (`cinematography-ai-director`):** Diretor técnico de óptica, enquadramentos e movimentos para geração por IA.
3. **Asset & B-Roll Curator (`asset-broll-curator`):** Stock footage, download dos inserts liberados, manifesto de B-roll e dono da biblioteca de assets (pastas no disco e no Google Drive, índice com licença, contact sheets).
4. **Motion & HyperFrames Engineer (`motion-hyperframes-engineer`):** Especialista em motion design via HyperFrames (HTML/GSAP/Three.js) e Remotion.
5. **Retention & Subtitles Specialist (`retention-subtitles-specialist`):** Tipografia cinética, ganchos nos primeiros 3s e respeito às safe zones.
6. **Council Editorial Arbiter (`council-editorial-arbiter`):** Antagonista responsável pelo gating da Regra dos Seis de Walter Murch e veto técnico.
7. **Smart Clip Editor (`smart-clip-editor`):** Dono do playbook Smart Clipper: transcrição por palavra, seleção de momentos, reenquadramento 9:16 e render local.
8. **Color Grading Colorist (`color-grading-colorist`):** Normalização log → Rec.709, correção primária e de tom de pele, look por LUT/CDL e emulação de filme, prova por scopes e entrega no espaço de cor da plataforma.
9. **Reference Scout (`reference-scout`):** Pesquisa notícias, Reels, TikToks e Shorts sobre o tema; entrega o reference-board com números e data e os candidatos a insert com direito de uso classificado.

---

## 3. Capabilities & Outputs

A empresa produz artefatos padronizados prontos para execução em timelines de edição ou renderização direta:

| Output | Descrição | Formato |
|---|---|---|
| `editing-master-cut` | Roteiro de edição estruturado com marcações de cortes, ritmo e transições | Markdown / XML |
| `vertical-clip-set` | Conjunto de cortes verticais 1080x1920 renderizados, com legendas queimadas | MP4 (H.264/AAC) |
| `clip-manifest` | Por corte: timestamps na origem, duração, layout, deslocamento de crop, hook e payoff | YAML / CSV |
| `color-grade-package` | Por clipe: espaço de cor de entrada, correções, look (LUT, origem, licença, intensidade), scopes antes/depois | YAML + PNG + .cube |
| `lut-library-manifest` | Biblioteca de LUTs da casa com origem, licença e uso permitido | YAML |
| `reference-board` | Notícias e short-form de referência com URL, data, métrica, uso proposto e direito de uso | Markdown |
| `asset-library-index` | Índice da biblioteca de assets: caminho, Drive id, tema, orientação, fonte, licença, uso | YAML + contact sheets PNG |
| `debrief-memo` | Lições do projeto, candidatos à memória da empresa carimbados pelo conselho, candidatos à memória permanente | Markdown |
| `camera-shotlist-directive` | Shotlist com instruções de enquadramento, ângulo, lente e movimento para IA | YAML / Markdown |
| `broll-insert-manifest` | Lista detalhada de B-rolls minerados com timestamps de entrada/saída e fonte | CSV / YAML |
| `subtitle-style-package` | Especificação de estilo de legendas, fontes, cores de destaque e posições seguras | JSON / CSS / ASS |
| `hyperframes-motion-overlay` | Código-fonte em HTML/CSS/GSAP para overlays renderizáveis via CLI | Bundle Web |
| `editorial-critique-memo` | Parecer detalhado do conselho executivo com notas por timecode e veredito | Markdown |
| `retention-hook-architecture` | Estrutura de ganchos visuais e verbais dos primeiros 3 segundos | Markdown |
| `ai-prompt-cinematography` | Conjunto de prompts otimizados para geradores de vídeo generativo | YAML / Text |

---

## 4. Routing & Playbooks

### Roteamento Automático de Briefs
A ordem das rotas importa: a primeira que casa define quem recebe o pedido.
1. Pedido composto de edição (`editar um reel/vídeo`, `edit a video`, `alta retenção`) entra pelo `lead-editorial-director`, que decompõe.
2. Corte de vídeo longo (`cortar`, `clipar`, `podcast`, `highlights`, `reels de 60s`) entra pelo `smart-clip-editor`.
3. Só então as especialidades, com padrões estreitos: `referências de reels`/`pesquisar notícias`/`tendências` → `reference-scout`; `organizar drive`/`biblioteca de assets`/`contact sheet` → `asset-broll-curator`; `colorização`/`LUT`/`color grading`/`log para Rec.709` → `color-grading-colorist`; `ângulos de câmera`/`shotlist` → `cinematography-ai-director`; `banco de imagens`/`B-roll`/`pexels` → `asset-broll-curator`; `HyperFrames`/`Remotion`/`lower third` → `motion-hyperframes-engineer`; `conselho executivo`/`Murch`/`corte bruto` → `council-editorial-arbiter`; `legendas`/`captions`/`safe zones` → `retention-subtitles-specialist`.
4. Nada casou: `lead-editorial-director`.

### Fonte única de números
Zonas seguras, faixa de legenda, cadência de B-roll, loudness, regras de cor e gramática de transição moram em `memory/permanent.md` §5–§9. Funcionários e playbooks referenciam; nenhum redefine. A checagem mecânica de zona segura é `scripts/check_safe_zone.py`.

### Biblioteca de assets e referências
`playbooks/asset-library.md`: taxonomia de pastas igual no disco e no Google Drive, índice com fonte e licença, contact sheets para visualizar. O `reference-scout` pesquisa notícias e reels (com a ferramenta vidIQ quando o runtime a tem; sem ela, busca na web) e só libera insert com direito de uso classificado.

### Biblioteca dentro da empresa
`library/` guarda o que viaja no pacote: LUTs em `40_luts/` (15 inventariadas do Drive do dono em 02/10/2026: 14 looks criativos e a LUT técnica DJI Avata 2 D-Log M → Rec.709) e efeitos sonoros em `60_audio/sfx/`. Cada pasta tem seu manifesto com origem e licença; o que está `pendente` não entra em entrega.

### Enviar a empresa para alguém (só ela)
```bash
nrv pack create ~/businesses/magic-frames --output=<pasta>
```
Gera `magic-frames-<versão>.tgz`, o `.sha256` e o `.pack.json`. Quem recebe instala com `nrv install magic-frames-<versão>.tgz` (passa pelo mesmo validador). O pacote leva só a empresa: funcionários, rotas, memória permanente, playbooks e scripts. Não leva squads, clones nem a memória aprendida (`nrv memory`), que fica com o dono. Requisitos na máquina de quem recebe: o motor de execução (`nrv`), FFmpeg com VideoToolbox (ou outro encoder H.264), whisper-cpp com um modelo ggml, Node com `npx hyperframes`, Python 3. Opcionais que melhoram: squads de vídeo do catálogo, clone `walter-murch`, conector do Google Drive e vidIQ no runtime.

### Conexões com editores (opcionais)
Instaladas e registradas no Claude Code e no Codex em 02/10/2026: DaVinci Resolve (`davinci-resolve`), Premiere Pro (`premiere-pro`), Final Cut por FCPXML (`fcpxml`) e CapCut (`capcut-smartcut`). Precisam do aplicativo instalado (Resolve Studio para scripting externo; Premiere com o painel MCP Bridge aberto; Final Cut; CapCut). São opcionais de verdade: a pessoa escolhe na entrada onde quer o resultado (esteira própria em MP4, que é o padrão, ou CapCut, Premiere, Final Cut, Resolve), a escolha vale só para aquele projeto e nenhum cargo abre editor que ela não escolheu. Quando escolhido, o colorista usa o Resolve e o editor de cortes usa CapCut, Premiere ou Final Cut. Tudo volta para a esteira como arquivo e passa pelo conselho. Tabela, comandos de reinstalação e estado em `memory/permanent.md` §13.

### Runtimes e modelos
A empresa roda em qualquer runtime com adapter no motor: Claude Code, Codex (modelo Astra, da OpenAI, por decisão do dono), Antigravity, pi (15+ provedores e modelos locais) e Hermes. Arquivos, rotas, aceitação, memória e comandos de terminal são os mesmos em todos. O `model` de cada cargo é intenção de tier (forte: diretor e conselho; padrão: os seis executores); o `model_policy` do `business.yaml` diz o que cada runtime executa. Fora do Claude Code o motor não fixa modelo: vale o do runtime ou `NIRVANA_MODEL`. Detalhe em `memory/permanent.md` §10.

### Melhoria contínua (debriefing)
Toda entrega e toda correção do usuário passam pelo `playbooks/debriefing.md`: o diretor responde cinco perguntas com evidência, grava lições na memória do projeto e lista candidatos à memória da empresa; o conselho carimba o que generaliza; o dono promove com um "sim", que vira `nrv memory add magic-frames "<fato>"` e passa a ser injetado em todo prompt de funcionário, em qualquer runtime. Nada se apaga; fato que muda é substituído. Saída: `debrief-memo`.

### Smart Clipper (corte de vídeo longo)
Esteira completa em `playbooks/smart-clipper.md`: diagnóstico → WAV 16kHz → transcrição por palavra (`whisper-cli`) → mapa de pausas → seleção por hook/tensão/payoff → layout A/B/C → `.ass` + checagem de zona segura → overlays HyperFrames → render VideoToolbox → checklist do conselho.

### Playbook de Execução Recomendado
1. **Passo 1:** O `lead-editorial-director` decompõe o brief e monta a linha mestra (A-roll assembly) com identificação dos pontos de J-cut e L-cut. Se o pedido é corte de vídeo longo, despacha o `smart-clip-editor` com janelas e quantidade.
2. **Passo 2:** O `cinematography-ai-director` cria a shotlist para cenas que necessitam de geração sintética com IA.
3. **Passo 3:** O `asset-broll-curator` mina imagens e vídeos reais para ilustrar os conceitos na cadência de `memory/permanent.md` §6.
4. **Passo 4:** O `motion-hyperframes-engineer` programa os overlays interativos com HyperFrames.
5. **Passo 5:** O `retention-subtitles-specialist` sincroniza as legendas dinâmicas garantindo as margens de safe zone.
6. **Passo 6:** O `council-editorial-arbiter` revisa o corte, testa os 6 critérios de Murch e aprova o envio ao cliente.
7. **Passo 7:** O `lead-editorial-director` faz o debrief, o conselho carimba os candidatos e o dono promove o que vale para sempre.
