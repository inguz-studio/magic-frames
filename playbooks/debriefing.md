# Playbook: Debriefing e Memória Viva (melhoria contínua)

Dono: `lead-editorial-director`. Antagonista: `council-editorial-arbiter` (refuta candidato que não generaliza). Vale em qualquer runtime, porque só usa o `nrv` e arquivos.

A empresa aprende em três camadas, e cada uma tem um dono diferente:

| Camada | O que guarda | Quem escreve | Como chega ao funcionário |
|---|---|---|---|
| **Projeto** (`<projeto>/memory.md`) | O que este trabalho ensinou: restrição do cliente, abordagem que falhou, correção que o usuário fez | O funcionário, durante o run | Lido no início do próximo run do mesmo projeto |
| **Memória temporal da empresa** (`nrv memory add magic-frames`) | Fato ou decisão em vigor para qualquer projeto desta empresa | Só depois do "sim" do dono | Injetada em todo prompt de funcionário como "memória ativa" (vale em Claude Code, Codex, pi, Hermes…) |
| **Permanente** (`memory/permanent.md`) | Método, números e ferramentas curados | Edição deliberada do dono; viaja no pacote | Injetada em todo prompt de funcionário |

Regra do motor que este playbook respeita: **um run nunca escreve na memória da empresa**. Ele escreve no projeto e propõe. A promoção é do dono, e o "sim" dele na conversa é a promoção.

---

## 1. Quando o debriefing acontece
1. **Ao fim de cada entrega** (depois do veredito do conselho), sempre.
2. **No meio da conversa, toda vez que o usuário corrige, prefere ou rejeita algo** ("não, legenda em amarelo não", "esse look ficou forte demais", "sempre entregue também em 16:9"). A correção vira candidato na hora, não no fim.
3. **Quando o usuário pede** ("lembra disso", "guarda essa regra", "da próxima vez faça assim").

## 2. As cinco perguntas do debrief
O diretor responde, com evidência do run (arquivos, timecodes, trechos da conversa):
1. **O que o usuário pediu e o que recebeu?** Diferença entre pedido, entregue e aceito.
2. **O que o usuário corrigiu ou preferiu?** Cada correção, com a frase dele e o que mudou.
3. **O que falhou ou custou mais de uma rodada?** Onde o conselho vetou, onde a ferramenta quebrou, onde um número da memória estava errado.
4. **O que foi assumido sem perguntar?** As premissas registradas no run e se o usuário confirmou ou derrubou.
5. **O que serve para o próximo projeto, e o que foi só deste?** É aqui que nasce a lista de candidatos.

## 3. O que sai do debrief: `debrief-memo`
Arquivo `outputs/<trace>/debrief-memo.md`, curto, com três blocos:
- **Memória do projeto (já gravada):** o que foi escrito em `<projeto>/memory.md`, uma linha por lição, com o porquê.
- **Candidatos à memória da empresa:** cada um em uma frase, datado, sem dado de cliente, com o motivo de generalizar. O conselho carimba cada um com `generaliza` ou `só deste projeto`, e diz por quê.
- **Candidatos à memória permanente:** só quando um número, ferramenta ou regra de método da `permanent.md` se provou errado ou faltou. Vem com a evidência e a frase exata a mudar.

## 4. Promoção (o "sim" do dono)
O diretor apresenta os candidatos ao usuário em linguagem normal, um por linha. Para cada "sim":
```bash
nrv memory add magic-frames "<fato em uma frase, datado>" --source <trace_id>
```
Se o fato substitui um anterior (o usuário mudou de ideia), nunca apaga: `nrv memory list magic-frames` para achar o id e `nrv memory supersede <id> --by <novo id>`. Para ler o que está em vigor, `nrv memory list magic-frames`. Candidato à `permanent.md` é editado à mão pelo dono (ou por quem ele mandar), e a cópia lida pelo motor (`~/.nirvana/memory/businesses/magic-frames/`) é sincronizada no mesmo ato.

## 5. O que nunca entra na memória
- Dado de cliente, caminho de arquivo pessoal, nome de pessoa que não é pública.
- Preferência de um projeto só ("esse podcast quer azul") sem o carimbo `generaliza` do conselho.
- O que o output ou o log já registram (a memória é cache de lição, não cópia da entrega).
- Opinião do próprio funcionário sobre o próprio trabalho sem evidência.

## 6. Ciclo longo: padrões em muitos runs
Uma vez por mês, ou a cada dez entregas, o dono roda `nrv improver run --days=30` e revisa as propostas (`nrv improver list`); o que ele aceita entra pela mesma porta (`nrv memory add` ou edição da `permanent.md`). O diretor cita no `debrief-memo` quando um padrão se repetiu em três runs seguidos, para o dono não precisar descobrir sozinho.

## 7. Formato de uma lição boa
`2026-10-02 — Legenda amarela some sobre fundo claro de cozinha; para conteúdo de gastronomia usar ciano (#00F0FF). Motivo: veto do conselho no run 7f3a, confirmado pelo usuário.`
Uma frase, data, o fato, o motivo, a origem. Nada mais.
