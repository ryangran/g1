# Instruções permanentes deste repositório

**Sempre siga o Sistema Mestre do estúdio em todo pedido de vídeo, história ou conteúdo:**

@SISTEMA_MESTRE.md

## Onde as coisas estão

- `estudio/` — o estúdio de produção: análise do ambiente, catálogo de recursos, biblioteca 3D, modelos de documentos e as produções em `estudio/producoes/`.
- `estudio/RECURSOS.md` — catálogo de bibliotecas, vozes, áudios, transições e assets (o que funciona aqui e o que precisa de conta).
- `video/` — projeto HyperFrames anterior (checagem Lula/SUS).
- Skills do HyperFrames em `.claude/skills/` (`/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry`, `/media-use`). Leia `/hyperframes` antes de editar qualquer composição.

## Regras práticas do ambiente

- Renders nunca buscam rede: bibliotecas (GSAP, Three.js) ficam copiadas em `assets/lib/` de cada produção.
- Sempre rodar `npx hyperframes check` e olhar `snapshot` antes de renderizar.
- Nunca dizer que um áudio ou imagem foi produzido se só existem instruções.
