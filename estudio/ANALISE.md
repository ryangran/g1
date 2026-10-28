# Análise do HyperFrames neste ambiente — e o que foi melhorado

Data: 28/10/2026. Base: testes reais feitos no container (não suposições).

## 1. O que o HyperFrames é (e o que não é)

HyperFrames **não gera imagem nem vídeo por IA**. Ele é um motor de composição: você escreve a cena em HTML/CSS/JS (incluindo 3D com Three.js), ele avança o tempo quadro a quadro num Chrome e grava MP4. Isso tem uma consequência enorme para vídeos virais com personagens:

- **Vantagem:** continuidade perfeita. O personagem é um modelo 3D. Ele tem o mesmo rosto, cor e proporção em todo quadro, e o render é idêntico toda vez. É o oposto do maior defeito dos geradores de vídeo por IA, em que o personagem muda de cara entre cortes.
- **Limite:** a qualidade visual depende dos modelos 3D disponíveis e da direção (luz, câmera, atuação). Fotorrealismo e personagens humanos complexos exigem modelos de fora (Mixamo, VRoid, KayKit) ou um gerador de vídeo externo.

## 2. Recursos reais verificados

| Recurso | Situação |
|---|---|
| CLI HyperFrames 0.8.193 + plugin 0.8.212 + 7 skills | ✅ instalados |
| Render MP4 1080×1920 com WebGL (Three.js) | ✅ funciona (GPU por software, sem placa de vídeo) |
| Voz pt-BR local (Kokoro: pm_alex, pm_santa, pf_dora) | ✅ testadas |
| 19 efeitos sonoros embutidos (Pixabay) | ✅ |
| 448 blocos do registry (transições, legendas, câmera) | ✅ catálogo lido |
| Modelos 3D CC0 via GitHub (RobotExpressive etc.) | ✅ baixados |
| Google Fonts, npm, PyPI | ✅ acessíveis |
| HeyGen (avatar, vozes premium, catálogo de música, text-to-video) | ❌ CLI não instalado, sem conta |
| Geração de imagem/vídeo por IA (FLUX, LTX, Runway, Kling…) | ❌ sem GPU e sem contas |
| Transcrição (whisper/parakeet) | ❌ modelo vem do Hugging Face, bloqueado |
| Freesound, Pixabay, Kenney, Quaternius, CDNs | ❌ bloqueados pela rede deste ambiente (funcionam na sua máquina) |

## 3. Gargalos para vídeo 3D viral de qualidade

1. **Sem fonte de personagens.** O projeto só tinha texto animado. Não havia modelos, rig nem animações.
2. **3D quadro a quadro é difícil de escrever.** O HyperFrames exige que cada quadro seja função pura do tempo. Animação esquelética, expressões, câmera e luz precisam ser recalculadas do zero a cada quadro, e não havia ferramenta para isso.
3. **Rede restrita.** Bibliotecas por CDN quebram o render aqui. Tudo precisa estar dentro do projeto.
4. **Música.** Sem HeyGen e sem MusicGen, não há banco de música acessível. A trilha precisa ser sintetizada ou trazida por você.
5. **Fluxo manual.** Não havia estrutura de episódio, bíblia visual, plano de cenas ou checklist de QA.
6. **Render lento sem GPU.** Cerca de 1–2 s por quadro em 1080×1920 com sombras. Um vídeo de 38 s leva por volta de 20–40 min aqui. Na sua máquina, com GPU, é bem mais rápido.

## 4. Melhorias implementadas

| Melhoria | Onde | Resolve |
|---|---|---|
| **Motor Estudio3D**: personagens a partir de glTF com recoloração (vários personagens consistentes do mesmo modelo), atuação por segmentos com mistura suave entre animações, expressões faciais por chaves, ajustes finos de ossos (cabeça, tronco), câmera por planos (de → para, com tremor), texto em textura 3D (placas), PRNG com seed | `estudio/lib/estudio3d.js` | gargalos 1 e 2 |
| **Three.js empacotado** (com GLTFLoader, SkeletonUtils, RoundedBox) num script local | `estudio/lib/three-bundle.js` | gargalo 3 |
| **Biblioteca local**: RobotExpressive (CC0, 14 animações, 3 expressões), aves CC0, 5 fontes cartoon/impacto | `estudio/biblioteca/` + `tools/baixar-biblioteca.sh` | gargalos 1 e 3 |
| **Criador de episódio**: projeto vertical 1080×1920 pronto, com libs, modelos, fontes e modelos de documentos | `estudio/tools/novo-episodio.sh` | gargalo 5 |
| **Modelos de documentos** do Sistema Mestre: IDEIAS (com pontuação), BÍBLIA VISUAL, CENAS (A–M), PUBLICAÇÃO, QA | `estudio/modelos-docs/` | gargalo 5 |
| **Trilha procedural** sincronizada à grade de batidas (a dança do modelo = 8 batidas a 144 BPM) | `producoes/01-*/audio/gerar_trilha.py` | gargalo 4 (paliativo) |
| **Catálogo de recursos** com licenças e o que funciona aqui | `estudio/RECURSOS.md` | todos |
| **Sistema Mestre sempre ativo** via `CLAUDE.md` | raiz | regras do estúdio |

## 5. Próximos passos recomendados (dependem de você)

1. **Música de verdade:** baixe faixas da Pixabay Music / YouTube Audio Library na sua máquina e coloque em `assets/audio/`. Ou conecte o HeyGen (`heygen auth login --oauth`) para o catálogo de 10 mil faixas.
2. **Mais personagens:** baixe os pacotes KayKit (CC0) e Quaternius na sua máquina e coloque em `estudio/biblioteca/modelos/`. Para um protagonista próprio, crie no VRoid Studio ou anime no Mixamo.
3. **Vozes com emoção (narração/diálogo):** ElevenLabs ou Azure para suspense/drama. O Kokoro serve para rascunho e narração neutra.
4. **Render mais rápido:** rode `npm run render` na sua máquina (GPU), ou use `npx hyperframes cloud` / Lambda.
