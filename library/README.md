# Magic Frames Library (dentro da empresa)

O que viaja com a empresa: LUTs (`40_luts/`, 17 arquivos: 14 looks, 2 La Creme Rec.709 e a técnica DJI Avata 2), molduras com alfa (`50_overlays/frames/`, 30 PNG), efeitos sonoros (`60_audio/sfx/`, 122 arquivos em 7 categorias), fontes (`70_fonts/`, cinco famílias de licença aberta com `fonts.css`), presets de animação de texto (`80_text-animations/`, composições HyperFrames parametrizadas com preview) e formatos de vídeo curto (`90_formats/`, 20 cartões com os vídeos de exemplo, transcrição e frames). Cada pasta tem seu manifesto (`lut-library-manifest.yaml`, `overlays-manifest.yaml`, `sfx-manifest.yaml`, `fonts-manifest.yaml`, `presets-manifest.yaml`, `formats-manifest.yaml`) e os cargos referenciam cada item pelo `id`.

O que NÃO fica aqui: B-roll e referências do acervo do dono (`playbooks/asset-library.md`) e a mídia, o trabalho e as entregas de cada projeto (`playbooks/project-intake.md`). O projeto aponta para a biblioteca por id, nunca copia.

Regra única: nada entra sem origem e licença no manifesto da pasta. O que está `pendente` não é usado em entrega.
