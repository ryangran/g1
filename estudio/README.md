# Estúdio de vídeos virais — HyperFrames

Estúdio para produzir histórias curtas de animação 3D, verticais (9:16), seguindo o [Sistema Mestre](../SISTEMA_MESTRE.md).

## Estrutura

```
estudio/
├── ANALISE.md            o que o ambiente tem de verdade, gargalos e melhorias
├── RECURSOS.md           catálogo: modelos 3D, vozes BR, música, SFX, transições, fontes, licenças
├── lib/
│   ├── estudio3d.js      motor: personagens, atuação, expressões, câmera por planos, placas
│   ├── three-bundle.js   Three.js 0.170 + GLTFLoader + SkeletonUtils (local, sem CDN)
│   └── gsap.min.js
├── biblioteca/           modelos CC0 (RobotExpressive…) e fontes
├── modelos-docs/         IDEIAS, BIBLIA, CENAS, PUBLICACAO, QA
├── tools/
│   ├── baixar-biblioteca.sh   rebaixa/gera lib e biblioteca
│   └── novo-episodio.sh       cria um episódio pronto para produzir
└── producoes/
    └── 01-proibido-dancar/    demo completa (render, docs, áudio)
```

## Fluxo de produção

1. `./estudio/tools/novo-episodio.sh 02-nome` cria o projeto vertical com libs, modelos, fontes e documentos.
2. Preencha `docs/IDEIAS.md`: 3–5 ideias pontuadas, escolha uma.
3. `docs/BIBLIA.md`: personagens (cores por material, escala, animações), cenário, luz, câmera, continuidade.
4. `docs/CENAS.md`: cada plano com os campos A–M (inclui prompt para ferramentas externas).
5. Escreva `cena.js` usando o Estudio3D. Veja a demo como referência:
   - `E.criarPersonagem(gltf, { cores, escala })` para cada personagem;
   - `p.atuar([...segmentos])`, `p.mover(pos, rot)`, `p.rostoChaves(...)`, `p.ajustes = (t,p) => p.girar("Head", ...)`;
   - `E.diretorDeCamera(camera, PLANOS, DUR)` para a lista de planos.
6. Áudio: trilha em `audio/`, SFX em `<audio>` no `index.html` (pico 1 quadro depois da imagem).
7. `npx hyperframes check` → `npx hyperframes snapshot --at ...` (olhar os quadros!) → corrigir → `npm run render`.
8. `docs/QA.md` e `docs/PUBLICACAO.md`.

## Comandos úteis

```bash
cd estudio/producoes/01-proibido-dancar
npm run dev        # Studio (prévia ao vivo) — na sua máquina
npm run check
npx hyperframes snapshot --at 0.5,10,20,30
npm run render     # gera renders/final.mp4
```
