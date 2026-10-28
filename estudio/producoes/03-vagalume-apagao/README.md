# Apagão — episódio 03 (26 s, vertical)

Lumi, um vagalume de pijama, só quer apagar o abajur para dormir e apaga a cidade inteira. Só sobra uma luz: o bumbum dele.

**Versão animada (feita aqui, 3D procedural):**
- `lumi.js`: o personagem (olhos com pálpebras, pupilas, boca, bochechas, antenas, touca, pijama, asas e abdômen que brilha) e as expressões.
- `cena.js`: os cenários (quarto em cm, apartamento, prédio, cidade com 2.116 prédios e ruas em shader, céu com 420 estrelas e lua), a atuação e as 12 câmeras.
- `audio/gerar_audio.py`: música (pizzicato 100 BPM + crescendo de cordas) e foley sintetizados, com vozes do Kokoro aceleradas (`build/voz/`, gere com `npx hyperframes tts`).
- `index.html`: composição HyperFrames (canvas 3D + música + foley + 25 SFX embutidos).

```bash
python3 audio/gerar_audio.py
npx hyperframes check && npx hyperframes render -o renders/apagao.mp4
```

**Versão com gerador de vídeo por IA** (Runway, Kling, Veo…): prompts em `docs/CENAS.md` e montagem em `docs/MONTAGEM.md`. `tools/animatic.sh` gera os cartões provisórios.
