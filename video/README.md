# Espaço de edição de vídeo — HyperFrames

Projeto [HyperFrames](https://hyperframes.heygen.com): você monta o vídeo em HTML/CSS
com animações GSAP, vê ao vivo no navegador (Studio) e renderiza para MP4.

**Requisitos:** Node.js 22+ e FFmpeg.

## Comandos

```bash
cd video
npm run dev      # abre o Studio (preview ao vivo) — http://localhost:3002
npm run check    # valida a composição (lint, runtime, layout, contraste)
npm run render   # renderiza o MP4 (use: npm run render -- -o renders/final.mp4)
```

## Como editar

- `index.html` — composição principal (textos, cores em `:root`, timeline GSAP no `<script>`).
- `assets/` — coloque aqui seus vídeos, imagens e músicas.
- `compositions/` — cenas separadas, montadas com `data-composition-src`.
- `renders/` — saída dos renders (ignorada pelo git).

### Adicionar um vídeo seu

1. Copie o arquivo para `assets/` (ex.: `assets/meu-video.mp4`).
2. No `index.html`, dentro do `#root`:
   ```html
   <video id="clipe1" class="clip" src="assets/meu-video.mp4"
          data-start="6" data-duration="10" data-track-index="3"
          data-has-audio="true"></video>
   ```
3. Aumente o `data-duration` do `#root` para cobrir o vídeo inteiro (ex.: `16`).

Dica: `npx hyperframes init meu-projeto --video caminho/do/video.mp4` cria um projeto
já com o vídeo importado e legendas transcritas automaticamente.

### Regras importantes

- Todo elemento com tempo precisa de `data-start` e `data-duration`, e `class="clip"`.
- Nada aleatório: sem `Math.random()`, `Date.now()` ou chamadas de rede.
- Rode `npm run check` depois de cada alteração.

Mais detalhes para agentes de IA em `CLAUDE.md` / `AGENTS.md`.
