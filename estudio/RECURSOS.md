# Catálogo de recursos do estúdio

Levantamento feito em 28/10/2026. Cada item diz **onde está**, **licença** e **se funciona neste ambiente** (container na nuvem do Claude Code).

Legenda: ✅ testado e funcionando aqui · 🟡 funciona, mas precisa de conta/pagamento · 🔵 só na sua máquina (o acesso daqui é bloqueado) · ⚠️ restrição de licença

> Rede deste ambiente: acessa npm, PyPI, Google Fonts e arquivos do GitHub (raw). **Bloqueados:** Hugging Face, Freesound, Pixabay, Kenney, Quaternius, Poly Pizza, Openverse e os CDNs (jsDelivr/unpkg). Por isso as bibliotecas e os assets ficam **copiados dentro de cada projeto**.

---

## 1. Personagens e modelos 3D

| Recurso | O que é | Licença | Status |
|---|---|---|---|
| **RobotExpressive** (Tomás Laulhé / Quaternius, ajustes de Don McCurdy) | Robô cartoon com esqueleto, 14 animações (Idle, Walking, Running, Jump, Dance, Wave, Yes, No, ThumbsUp, Punch, Sitting, Standing, Death, WalkJump) e 3 expressões faciais por morph (Angry, Surprised, Sad) | CC0 | ✅ em `estudio/biblioteca/modelos/` |
| Parrot, Flamingo, Stork, Horse (exemplos do Three.js) | Animais low-poly com animação de voo/corrida | ver README do Three.js | ✅ Parrot e Flamingo baixados |
| Xbot (Three.js) | Manequim humano com animações de corrida/andar | exemplo do Three.js (Mixamo) ⚠️ | ✅ baixável; prefira CC0 |
| **KayKit** (Kay Lousberg) — Adventurers, Skeletons, Character Animations | Personagens estilizados com 90+ animações, glTF | CC0 | 🔵 itch.io; Skeletons também no GitHub |
| **Quaternius** — Ultimate Animated Characters, Universal Base Characters | 50+ personagens animados | licença própria, uso comercial sem atribuição, não redistribuir o pacote | 🔵 quaternius.com |
| **Kenney** — Animated Characters, Mini Characters | Personagens e cenários low-poly | CC0 | 🔵 kenney.nl |
| 100 Avatars | 167 avatares com rig, glTF | CC0 | 🔵 |
| **Mixamo** (Adobe) | Rig automático + milhares de animações para qualquer personagem | grátis com conta Adobe | 🟡 |
| VRoid Studio + `@pixiv/three-vrm` | Criar personagem anime próprio e consistente (mesmo rosto/roupa sempre) | grátis | 🔵 VRoid / ✅ lib no npm |
| Personagens procedurais (código) | Feitos de formas 3D no Three.js, 100% originais | nossos | ✅ `estudio/lib/` |

**Por que isso importa para continuidade:** um modelo 3D é o mesmo arquivo em toda cena — rosto, roupa e proporções nunca mudam. Isso resolve o maior problema de vídeo por IA (personagem que muda de cara a cada corte).

## 2. Bibliotecas de animação e 3D

| Biblioteca | Para quê | Licença | Status |
|---|---|---|---|
| **HyperFrames** 0.8.x | Composição, timeline, render MP4 determinístico | open source | ✅ |
| **Three.js** 0.170 | 3D: personagens, luz, sombras, câmera | MIT | ✅ copiada em `estudio/lib/` |
| GLTFLoader / SkeletonUtils (Three.js addons) | Carregar `.glb` e clonar personagens com esqueleto | MIT | ✅ |
| **GSAP** 3.14 (inclui SplitText, MorphSVG etc., grátis desde 2025) | Animação de texto e UI | licença GSAP (grátis) | ✅ |
| `postprocessing` / EffectComposer | Bloom, profundidade de campo, granulação | MIT | ✅ npm |
| Lottie (`@lottiefiles/dotlottie-web`) | Animações 2D do After Effects / LottieFiles | MIT (player) | ✅ player · 🔵 site LottieFiles |
| Rive, anime.js, Theatre.js | Alternativas de animação | várias | ✅ npm |

## 3. Blocos prontos do HyperFrames (registry: 448 itens)

Instalar: `npx hyperframes add <nome>` · buscar: `npx hyperframes catalog <palavra>`

- **Transições (52):** `whip-pan`, `cinematic-zoom`, `light-leak`, `flash-through-white`, `glitch`, `sdf-iris`, `swirl-vortex`, `ridged-burn`, `domain-warp-dissolve`, `chromatic-radial-split`, `beat-freeze-cut`; componentes `iris-reveal`, `match-cut`, `cut-the-curve`, `curtain-reveal`, `halftone-dissolve`, `grid-pixelate-wipe`, `fade-through`; vitrines `transitions-3d/blur/cover/dissolve/light/mechanical/push/radial/scale`.
- **Legendas estilo TikTok (16):** `caption-highlight` (fundo vermelho na palavra ativa), `caption-pill-karaoke`, `caption-kinetic-slam`, `caption-emoji-pop`, `caption-gradient-fill`, `caption-neon-glow`, `caption-particle-burst`, `caption-glitch-rgb`, `caption-matrix-decode`, `caption-texture`, `caption-parallax-layers`.
- **Câmera e efeitos:** `camera-shake` (9 perfis), `camera-dolly-zoom` (efeito Vertigo), `rack-focus`, `push-in`, `pull-back-reveal`, `confetti`, `snow`, `starfield`.
- **Títulos:** `glass-shard-title`, `wireframe-portal-title`, `extruded-logo`, `hw-write-title` (escrita à mão), `yt-prism-title`.
- **Social (9:16):** `tiktok-follow`, `instagram-follow`, `message-thread-reveal` (conversa de celular), `notification-cascade`, `notes-reveal`.
- **Desenho à mão:** `hw-arrow`, `hw-callout-circle`, `hw-underline`, `hw-text-cloud` (balão de fala), `hw-boil`.

## 4. Vozes brasileiras (narração e personagens)

| Voz | Motor | Licença | Status |
|---|---|---|---|
| **pm_alex** (masculina, grave) | Kokoro-82M, local | Apache 2.0 (uso comercial ok) | ✅ testada |
| **pm_santa** (masculina, mais madura) | Kokoro-82M | Apache 2.0 | ✅ testada |
| **pf_dora** (feminina) | Kokoro-82M | Apache 2.0 | ✅ testada |
| Piper `pt_BR` (faber, cadu, jeff…) | Piper, local, muito rápido | varia por voz ⚠️ | 🔵 vozes no Hugging Face |
| F5-TTS pt-BR (clonagem de voz) | local, GPU recomendada | pesos CC-BY-NC ⚠️ não comercial | 🔵 |
| XTTS-v2 (clonagem, emoção) | local | Coqui CPML ⚠️ não comercial | 🔵 |
| **ElevenLabs** (Multilingual v2 / v3) | nuvem — melhor emoção para suspense/drama | pago, uso comercial nos planos pagos | 🟡 |
| Azure Neural pt-BR (Francisca, Antonio, Thalita…) | nuvem, barato | pago | 🟡 |
| Google Cloud Neural2/WaveNet pt-BR | nuvem | pago | 🟡 |
| HeyGen voices + clonagem | integrado ao HyperFrames (`/media-use`) | pago/créditos | 🟡 `heygen auth login --oauth` |

Comando local: `npx hyperframes tts "texto" -v pm_alex -l pt-br -s 0.9 -o voz.wav` (precisa `pip install kokoro-onnx soundfile`).

## 5. Música

| Fonte | Licença | Observação | Status |
|---|---|---|---|
| Biblioteca Comercial do TikTok (CML) | grátis no TikTok | só cobre o TikTok | 🔵 no app |
| Meta Sound Collection | grátis no Instagram/Facebook | só Meta | 🔵 |
| YouTube Audio Library | grátis | ótima para Shorts; algumas pedem atribuição | 🔵 |
| Pixabay Music | Pixabay Content License (comercial, sem atribuição) | boa para todas as redes | 🔵 |
| Incompetech (Kevin MacLeod) | CC BY (atribuição obrigatória) | clássicos de suspense/comédia | 🔵 |
| Free Music Archive | varia por faixa ⚠️ | confira cada faixa | 🔵 |
| HeyGen catalog (10k+ faixas) | créditos HeyGen | integrado ao `/media-use` | 🟡 |
| MusicGen local | MIT (código) / CC-BY-NC (pesos) ⚠️ | precisa baixar do Hugging Face | 🔵 |
| Trilha sintetizada em código (`estudio/tools/`) | nossa | funciona aqui, qualidade limitada | ✅ |

## 6. Efeitos sonoros

| Fonte | Licença | Status |
|---|---|---|
| **19 SFX embutidos no HyperFrames** (whoosh ×3, impact-bass ×2, riser, pop, sparkle, glitch ×3, click, chime…) | Pixabay (comercial, sem atribuição) | ✅ `.claude/skills/media-use/audio/assets/sfx/` |
| Freesound | CC0 / CC BY (varia) | 🔵 |
| Pixabay Sound Effects | Pixabay | 🔵 |
| ZapSplat | grátis com atribuição / pago sem | 🔵 |
| Sonniss GDC Bundle (anual, dezenas de GB) | royalty-free comercial | 🔵 |
| BBC Sound Effects | ⚠️ só uso pessoal/educacional | 🔵 |

## 7. Fontes (texto na tela)

Embutidas no HyperFrames: Inter, Montserrat, Outfit, Nunito, Oswald, League Gothic, Archivo Black, Poppins, Roboto, Lato, Playfair Display, EB Garamond, Space Mono…
Google Fonts (✅ baixa daqui, licença OFL/Apache): **Bangers** e **Luckiest Guy** (cartoon), **Bebas Neue** (impacto), **Creepster** (terror), **Caveat** (manuscrita).

## 8. Textos e histórias

- **Folclore brasileiro** (Saci, Curupira, Boitatá, Iara, Mula sem cabeça, Boto): domínio público como tradição — crie versões e personagens próprios.
- **Domínio público no Brasil** (autor morto há 70+ anos): Machado de Assis, Monteiro Lobato (desde 2019), Lima Barreto, Aluísio Azevedo, Esopo, Irmãos Grimm, Perrault. Ilustrações de edições modernas **não** são livres.
- Fontes: Domínio Público (dominiopublico.gov.br), Projeto Gutenberg, Biblioteca Brasiliana.

## 9. Geração de imagem e vídeo por IA

| Ferramenta | Uso | Status |
|---|---|---|
| HeyGen (avatar, text-to-video, dublagem, lipsync) | integrado ao HyperFrames | 🟡 conta |
| FLUX local (mflux), LTX-Video local | imagem/vídeo grátis, GPU/Mac | 🔵 sem GPU aqui |
| Runway, Kling, Veo, Sora, Pika, Hailuo | clipes de vídeo com personagem | 🟡 conta (use os assets 3D como imagem de referência para manter continuidade) |
| Midjourney, Ideogram, Leonardo | arte conceitual e capas | 🟡 |

## Fontes da pesquisa

- [Kokoro-82M (vozes completas)](https://replicate.com/codingayam/kokoro-82m-complete/readme) · [Guia de TTS self-hosted 2026](https://offlinetts.com/blog/self-hosted-tts-guide-2026/) · [Comparativo TTS open source](https://www.codesota.com/guides/tts-models) · [F5-TTS pt-BR](https://huggingface.co/firstpixel/F5-TTS-pt-br) · [Piper/Coqui/XTTS](https://www.promptquorum.com/pt/power-local-llm/local-tts-voice-cloning-piper-coqui-xtts)
- [Melhores APIs de TTS 2026](https://blogs.novita.ai/pt/best-text-to-speech-api-2026/) · [Locução IA em pt-BR](https://fluxnote.io/guides/ai-voice-over-portuguese-brazil) · [Ranking de vozes em português](https://json2video.com/ai-voices/ranking/portuguese/)
- [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers) · [KayKit Character Animations](https://kaylousberg.itch.io/kaykit-character-animations) · [Quaternius Universal Base Characters](https://quaternius.com/packs/universalbasecharacters.html) · [Guia de personagens 3D gratuitos com rig](https://app.cinevva.com/pt-BR/guides/free-rigged-3d-character-models)
- [Biblioteca de Música Comercial do TikTok](https://ads.tiktok.com/business/pt-BR/blog/audio-library-royalty-free-music) · [Música para Reels 2026](https://www.foximusic.com/blog/pt/?p=585) · [15 bancos de som grátis](https://www.crehana.com/br/blog/brasil/15-bancos-de-som-gratis-para-baixar-musicas-e-efeitos/)
- Licença do RobotExpressive: README em `mrdoob/three.js/examples/models/gltf/RobotExpressive/`. Licença dos SFX: `CREDITS.md` do `/media-use`.
