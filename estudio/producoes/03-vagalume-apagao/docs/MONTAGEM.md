# Montagem — 03-vagalume-apagao ("Apagão")

## 1. Fluxo de geração (para manter o Lumi idêntico)

1. **Folha do personagem** (`CENAS.md` §0) num gerador de imagem (Midjourney, Ideogram, Flux, Leonardo). Escolha **uma** versão e guarde como `refs/lumi-folha.png`. Ela é a referência de tudo.
2. **Quadro inicial de cada cena:** gere a imagem com o prompt **IMG** e a folha como referência de personagem (Midjourney `--cref`, Flux/Leonardo "character reference", Runway "References").
3. **Clipe:** image-to-video com o quadro inicial + prompt **VID** (Runway Gen-4, Kling, Veo, Hailuo). Gere 2–3 variações e escolha a melhor.
4. **Encadeamento:** o **último quadro** aprovado da cena N vira o **quadro inicial** da cena N+1 nos cortes contínuos (3→4 no whip-pan, 5→6 no tilt/zoom-out, 7→8 no preto).
5. Anote **seed, ferramenta e versão** de cada clipe aprovado na tabela abaixo, para poder regerar sem perder a continuidade.
6. Salve como `assets/clips/cena-N.mp4` (N = 1…9), em vertical 1080×1920. Se o gerador entregar 720p ou 16:9, faça upscale e recorte para 9:16 antes, mantendo o rosto do Lumi no terço superior-médio.

| Cena | Arquivo | Ferramenta | Seed | Aprovado |
|---|---|---|---|---|
| 1–9 | `assets/clips/cena-N.mp4` | | | |

> Sem gerador de vídeo? A alternativa é animar no próprio estúdio, com Three.js + Estudio3D, como nos episódios 01 e 02. Isso exige modelar o Lumi proceduralmente (cabeça, olhos, pijama, abdômen emissivo) e a cidade com blocos e janelas emissivas, o que é viável.

## 2. Linha do tempo (corte final, 26,0 s)

| # | Entra | Sai | Clipe | Ajuste de montagem | Transição de saída |
|---|---|---|---|---|---|
| 1 | 0,00 | 2,20 | cena-1 | começa já com o olho abrindo (sem frames parados) | corte seco no levantar |
| 2 | 2,20 | 4,60 | cena-2 | mantenha o silêncio cômico de 0,3 s no fim | corte no recuo |
| 3 | 4,60 | 7,40 | cena-3 | queda do abajur a 50% de velocidade (speed ramp) e volta a 100% na faísca | **whip-pan** (4 quadros de borrão) |
| 4 | 7,40 | 10,20 | cena-4 | 4 microcortes de ~0,6 s, um por "pop" | corte seco no "clonk" |
| 5 | 10,20 | 13,20 | cena-5 | — | tilt-up que emenda na cena 6 |
| 6 | 13,20 | 16,60 | cena-6 | zoom-out contínuo; acelere 1,2× se a onda estiver lenta | tilt-up para o céu |
| 7 | 16,60 | 19,00 | cena-7 | termina em **preto absoluto** (RGB 0) | preto continua |
| 8 | 19,00 | 22,40 | cena-8 | o pontinho surge em 19,4 s; o push-in vai até 22,0 s | corte seco |
| 9 | 22,40 | 26,00 | cena-9 | preto em 24,0 s; piscadas em 24,8 e 25,4 s | fim |

**Cor:** interior quente/azul, exterior âmbar/azul-noite. O preto das cenas 7–9 deve ser preto puro, para a luz do Lumi ser a única coisa na tela.
**Texto na tela:** nenhum. O único texto é o "BOA NOITE" do outdoor da cena 6. Não precisa de legenda, porque não há fala.
**Zona segura (Reels/TikTok):** rosto do Lumi e ações principais entre 168 e 1330 px de altura. Nada importante embaixo à direita (botões).

## 3. Som (cue sheet)

O pico de cada efeito cai **1 quadro depois** da imagem correspondente. "Embutido" = SFX que já vem com o HyperFrames (licença Pixabay, uso comercial livre).

| Tempo | Evento na tela | Som | Fonte |
|---|---|---|---|
| 0,00–2,20 | quarto, luz do abajur | zumbido grave da lâmpada + tic-tac de relógio, bem baixos | gerar (prompts abaixo) |
| 0,90 | Lumi puxa a meia | farfalhar de tecido | gerar |
| 1,80 | "hmpf" | grunhido curto do Lumi | gerar (voz) |
| 2,30 | voo até o botão | `whoosh-short` (asas) | embutido |
| 3,10 | empurra o botão | "nnnngh!" + rangido de borracha | gerar |
| 4,30 | desiste | 0,3 s de silêncio | — |
| 5,35 | chute | `whoosh-short` (outra tomada) + "hup!" | embutido + gerar |
| 6,30 | abajur bate na mesa | `impact-bass-1` | embutido |
| 6,45 | escuridão | a música entra: pizzicato sorrateiro | música |
| 6,90 | faísca | `glitch-3` (estalo elétrico) | embutido |
| 7,40 / 7,95 / 8,50 / 9,05 | 4 pops da régua | `pop` ×4 subindo de tom (+0, +2, +4, +7 semitons) | embutido |
| 9,70 | disjuntor desarma | `click` + `glitch-1` curto; a música para em seco | embutido |
| 10,40–12,80 | andares apagando | "tunc" grave por andar, acelerando; vira a batida | gerar |
| 13,20–16,40 | cidade apagando | vuuummm descendente (cidade desligando) + crescendo da música | gerar + música |
| 15,10–18,60 | rumo ao céu | `riser` com pico no clique da lua | embutido |
| 16,80–18,40 | estrelas apagando | tiques acelerando | `key-press` em sequência |
| 18,60 | a lua apaga | `click` alto e seco; a música corta | embutido |
| 18,60–19,60 | preto | **1 s de silêncio total** | — |
| 21,20 | Lumi percebe | `ping` minúsculo (bem baixo) | embutido |
| 23,40 | puxa a meia | farfalhar | gerar |
| 24,00 | preto | silêncio | — |
| 24,80 / 25,40 | piscadas | ronquinho agudo ×2 | gerar |
| 25,70 | fim | "plim" de 2 notas da música | música |

**Música (procure por clima e andamento, não por tema):** "sneaky pizzicato comedy, light strings and bassoon, 100 bpm, builds into a short orchestral crescendo, hard stop". Fontes: biblioteca da plataforma (TikTok CML, Meta Sound Collection, YouTube Audio Library), Pixabay Music, ou o catálogo HeyGen (`/media-use`, `bgm`). Use de 6,45 s a 18,60 s e o "plim" no fim.

**Prompts para os sons que precisam ser gerados** (ElevenLabs Sound Effects, Stable Audio ou similar):
- `tiny cartoon insect grumpy "hmpf", very high pitched, short, dry` (0,4 s)
- `tiny cartoon insect straining "nnnngh" effort sound, high pitched, comedic` (1 s)
- `rubber button squeak under pressure, small, comedic` (0,6 s)
- `deep single thump of a building floor power switching off, "tunc", muffled` (0,4 s, use em sequência)
- `whole city power grid shutting down, long descending electrical hum "vuuuum", cinematic` (3 s)
- `fabric sock rustle, tiny, close` (0,5 s)
- `tiny cute high-pitched snore, cartoon insect, single breath in and out` (0,6 s)
- `quiet electrical lamp hum and soft clock ticking in a dark bedroom` (2,5 s, ambiente)

**Níveis:** música −20 a −22 LUFS sob os efeitos; efeitos 3–6 dB acima da música; mix final −14 a −16 LUFS, pico ≤ −1 dBTP. O silêncio de 18,6–19,6 s é obrigatório.

## 4. Montagem no HyperFrames (pronta)

> **Atualização:** a versão animada em 3D já existe (`lumi.js` + `cena.js`, veja o `README.md`). O `index.html` agora usa o canvas 3D. Para usar clipes gerados por IA, troque o `<canvas>` por `<video>` dos arquivos `assets/clips/cena-N.mp4`, com os tempos da tabela da seção 2.


`index.html` já tem a linha do tempo completa: os 9 clipes, os SFX embutidos posicionados e a faixa de música. Hoje os clipes são **placeholders do animatic** (`tools/animatic.sh`): cartões com o número, o título e a ação de cada cena, na duração certa. Para montar o vídeo final:

1. Substitua `assets/clips/cena-N.mp4` pelos clipes gerados (mesmo nome).
2. Coloque a música em `assets/audio/musica.mp3` e os sons gerados em `assets/audio/` (veja `index.html`, comentários `GERAR:`), e remova o `data-hidden` dos `<audio>` correspondentes.
3. `npx hyperframes check` → `npx hyperframes snapshot --at 1,3.5,6,8.5,11.5,15,18,21,25` → `npx hyperframes render -o renders/apagao.mp4`.

## 5. Exportação
MP4 H.264, 1080×1920, 30 fps, 12–16 Mbps, AAC 320 kbps, −14 a −16 LUFS. Capa: quadro de 0,6 s (olho irritado + abajur gigante) ou de 21,8 s (bumbum aceso no escuro).
